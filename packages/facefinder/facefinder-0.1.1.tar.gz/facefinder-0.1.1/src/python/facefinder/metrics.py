# -*- coding: utf-8 -*-

# Standard Imports
from __future__ import annotations
from pathlib import Path
from collections import defaultdict
import contextlib
import pickle
import os
import io

# Third Party Imports
from deepface import DeepFace
from deepface.commons.functions import extract_faces as _extract_faces
from tqdm import tqdm
import numpy as np
import cv2

# Local Imports
from facefinder import rust
from . import metadata
from .interact import InteractiveSession

# Typing imports
from typing import Callable, Any


def extract_faces(image_path: Path, model: str) -> None:
    with contextlib.redirect_stdout(io.StringIO()):
        return _extract_faces(
            img=str(image_path),
            target_size=metadata.MODEL_TARGET_SIZES[model],
            detector_backend="mtcnn",
            grayscale=False,
            enforce_detection=False,
            align=True,
        )


def get_extracted_faces(image_path: Path, model: str) -> None:
    extracted_path = metadata.PATHS.EXTRACTED_FACES_DIR.joinpath(
        f"{image_path.name[:-4]}.pkl"
    )

    if not os.path.exists(extracted_path):
        img_objs = extract_faces(image_path, model)
        with open(extracted_path, "wb+") as f:
            pickle.dump(img_objs, f)
        return img_objs

    else:
        with open(extracted_path, "rb") as f:
            return pickle.load(f)


def create_representation(
    image_path: Path,
    model: str,
    skip_face: bool = False,
) -> list[list[float]]:
    img_objs = get_extracted_faces(image_path, model)

    representations = []
    for img_content, _, confidence in img_objs:
        if skip_face or confidence:
            embedding_obj = DeepFace.represent(
                img_path=img_content,
                model_name=model,
                enforce_detection=False,
                detector_backend="skip",
                align=True,
                normalization="base",
            )
            representations.append(embedding_obj[0]["embedding"])

    return representations


def get_representation(
    image_path: Path,
    model: str,
    skip_face: bool = False,
) -> list[list[float]]:
    repr_name = f"{model}_{os.path.splitext(image_path.name)[0]}.repr"
    repr_path = metadata.PATHS.REPRESENTATIONS_DIR.joinpath(repr_name).resolve()

    if not os.path.exists(repr_path):
        img_representation = create_representation(image_path, model, skip_face)
        with open(repr_path, "wb+") as f:
            pickle.dump(img_representation, f)
        return img_representation

    else:
        with open(repr_path, "rb") as f:
            return pickle.load(f)


def get_representations(
    images: Path,
    model: str,
    skip_face: bool = False,
    silent: bool = False,
) -> tuple[list[Path], list[list[float]]]:
    valid = (".png", ".jpg", ".jpeg")
    images = [
        images.joinpath(image) for image in os.listdir(images) if image.endswith(valid)
    ]
    paths = []
    representations = []

    with tqdm(
        total=len(images),
        disable=silent,
        desc=f"Gathering face representations for {model}",
    ) as pbar:
        for image_path in images:
            reprs = get_representation(image_path, model, skip_face)

            for rep in reprs:
                paths.append(image_path)
                representations.append(rep)

            pbar.update(1)

    return paths, representations


# n_embedding_images x 512 @ n_input_images x 512 -> n_input_images x n_embedding_images
def cosine_dist(
    source_reprs: list[list[float]],
    target_reprs: list[list[float]],
) -> list[list[float]]:
    target_reprs = np.array(target_reprs)
    source_reprs = np.array(source_reprs)

    # Dims 1 must match (length of representation vector)
    assert source_reprs.shape[1] == target_reprs.shape[1]

    a = np.matmul(target_reprs, source_reprs.T)
    b = np.sqrt(np.sum(target_reprs**2, axis=1))
    c = np.sqrt(np.sum(source_reprs**2, axis=1))
    return np.ones(a.shape) - (a / np.matmul(b[:, None], c[None, :]))


def filter_duplicates(paths: list[Path], distances: list[float]) -> list[int]:
    """Returns a numpy index that will filter out the duplicates with non-max scores"""
    visited = defaultdict(list)
    for i, path in enumerate(paths):
        visited[path].append(i)
    duplicates = {k: v for k, v in visited.items() if len(v) > 1}
    visited = {k: v[0] for k, v in visited.items()}
    for path, idx in duplicates.items():
        scores = distances[np.array(idx)]
        visited[path] = idx[np.argmin(scores)]
    non_duplicate_idx = np.array(list(visited.values()))
    return non_duplicate_idx


def get_filtered(
    target_repr: list[float],
    input_reprs: list[list[float]],
    input_paths: list[Path],
) -> tuple[list[Path], list[list[float]], list[float]]:
    # Finding metrics for distance from target image (BASE_FACE)
    target_distances = cosine_dist(target_repr, input_reprs)

    # Filtering embedding duplicates by distance to target
    non_duplicate_idx = filter_duplicates(input_paths, target_distances)
    input_paths = np.array(input_paths)[non_duplicate_idx]
    input_reprs = np.array(input_reprs)[non_duplicate_idx]
    target_distances = np.array(target_distances)[non_duplicate_idx]

    return input_paths, input_reprs, target_distances


def calculate_image_scores(
    embedding_target_distances: list[float],
    input_embedding_distances: list[list[float]],
    weight_relevance: int = 1,
) -> list[float]:
    weights = np.power(embedding_target_distances.T, weight_relevance)
    weighted_distances = np.power(
        input_embedding_distances * weights, 1 / (weight_relevance + 1)
    )
    input_scores = np.mean(weighted_distances, axis=1)
    return input_scores


def get_embedding_metrics(
    model: str,
    target_path: Path = metadata.PATHS.TARGET_IMAGE,
    embedding_dir: Path = metadata.PATHS.EMBEDDING_IMAGES,
) -> dict[str, Any]:
    # Initial (non-filtered) target/embedding representations
    target_representation = get_representation(target_path, model, skip_face=True)
    paths, representations = get_representations(embedding_dir, model, skip_face=True)

    # Filtering representations/paths by distance to target repr
    paths, representations, embedding_target_distances = get_filtered(
        target_representation, representations, paths
    )

    mean_target_distance = float(np.mean(embedding_target_distances))

    # Finding overall similarity between faces in the embedding train set
    embedding_embedding_distances = np.mean(
        cosine_dist(representations, representations), axis=1
    )
    mean_embedding_distance = float(np.mean(embedding_embedding_distances))

    return {
        "target_path": target_path,
        "target_representation": target_representation,
        "representations": representations,
        "paths": paths,
        "embedding_target_distances": embedding_target_distances,
        "mean_target_distance": mean_target_distance,
        "embedding_embedding_distances": embedding_embedding_distances,
        "mean_embedding_distance": mean_embedding_distance,
    }


def get_input_metrics(
    model: str,
    target_repr: list[float],
    embedding_reprs: list[list[float]],
    embedding_target_distances: list[float],
    input_dir: Path = metadata.PATHS.UNPROCESSED_IMAGES,
    weight_relevance: int = 1,
) -> dict[str, Any]:
    # Initial (non-filtered) input representations
    paths, representations = get_representations(input_dir, model)
    x = 0

    # Filtering processed images by distance to target
    paths, representations, input_target_distances = get_filtered(
        target_repr, representations, paths
    )

    # Distances between inputs and embeddings
    input_embedding_distances = cosine_dist(embedding_reprs, representations)

    # Weighting the input distances by the embedding image scores (relative to the target)
    scores = calculate_image_scores(
        embedding_target_distances, input_target_distances, weight_relevance
    )

    # Gathering sorted indices for interactive functions
    match_indices = list(
        zip(
            *np.unravel_index(
                np.argsort(input_embedding_distances, axis=None),
                input_embedding_distances.shape,
            )
        )
    )
    cum_indices = np.argsort(scores, axis=None).tolist()
    target_indices = np.argsort(input_target_distances, axis=None).tolist()

    return {
        "paths": paths,
        "representations": representations,
        "input_target_distances": input_target_distances,
        "input_embedding_distances": input_embedding_distances,
        "input_scores": scores,
        "match_indices": match_indices,
        "cum_indices": cum_indices,
        "target_indices": target_indices,
    }


def get_metrics(
    model: str,
    target_path: str | Path = metadata.PATHS.TARGET_IMAGE,
    embedding_dir: str | Path = metadata.PATHS.EMBEDDING_IMAGES,
    input_dir: str | Path = metadata.PATHS.UNPROCESSED_IMAGES,
    weight_relevance: int = 1,
) -> dict[str, Any]:
    embedding_metrics = get_embedding_metrics(model, target_path, embedding_dir)
    input_metrics = get_input_metrics(
        model,
        embedding_metrics["target_representation"],
        embedding_metrics["representations"],
        embedding_metrics["embedding_target_distances"],
        input_dir,
        weight_relevance,
    )
    return {
        "paths": {
            "target": embedding_metrics["target_path"],
            "embedding": embedding_metrics["paths"],
            "input": input_metrics["paths"],
        },
        "representations": {
            "target": embedding_metrics["target_representation"],
            "embedding": embedding_metrics["representations"],
            "input": input_metrics["representations"],
        },
        "distances": {
            "embedding_target": embedding_metrics["embedding_target_distances"],
            "embedding_embedding": embedding_metrics["embedding_embedding_distances"],
            "input_target": input_metrics["input_target_distances"],
            "input_embedding": input_metrics["input_embedding_distances"],
        },
        "indices": {
            "match": input_metrics["match_indices"],
            "cumulative": input_metrics["cum_indices"],
            "target": input_metrics["target_indices"],
        },
        "metrics": {
            "embedding_accuracy": embedding_metrics["mean_target_distance"],
            "embedding_coherence": embedding_metrics["mean_embedding_distance"],
            "scores": input_metrics["input_scores"],
        },
        "metadata": {"model": model, "weight_relevance": weight_relevance},
    }


def create_scaler(n: float) -> Callable:
    def sigmoid(x: np.ndarray) -> np.ndarray:
        return 1 / (1 + np.exp(-10 * (x - n)))

    def f(x: np.ndarray) -> np.ndarray:
        return sigmoid(x) - sigmoid(0)

    def g(x: np.ndarray) -> np.ndarray:
        return f(x) / f(100)

    return g


def distance_mean(distances: dict[str, np.ndarray]) -> float:
    total_distance = 0
    total_size = 0
    for distance in distances.values():
        total_distance += np.sum(distance)
        total_size += distance.size

    return total_distance / total_size


def merge_metrics(metrics: list[dict[str, Any]]) -> dict[str, Any]:
    paths = metrics[0]["paths"]
    representations = {m["metadata"]["model"]: m["representations"] for m in metrics}
    metadata = {
        "model": [m["metadata"]["model"] for m in metrics],
        "weight_relevance": [m["metadata"]["weight_relevance"] for m in metrics],
    }
    means = [distance_mean(m["distances"]) for m in metrics]
    grand_mean = np.mean(np.array(means))
    distances = {
        "embedding_target": [],
        "embedding_embedding": [],
        "input_target": [],
        "input_embedding": [],
    }
    for m, mean in zip(metrics, means):
        scaler = create_scaler(mean)
        for k, v in m["distances"].items():
            if len(v.shape) == 1:
                v = v[:, None]
            distances[k].append(scaler(v)[:, :, None])
    distances = {
        k: np.mean(np.concatenate(v, axis=2), axis=2) * grand_mean
        for k, v in distances.items()
    }

    scores = calculate_image_scores(
        distances["embedding_target"],
        distances["input_embedding"],
        np.mean(metadata["weight_relevance"]),
    )
    embedding_accuracy = np.mean(distances["embedding_target"])
    embedding_coherence = np.mean(distances["embedding_embedding"])
    metrics = {
        "embedding_accuracy": embedding_accuracy,
        "embedding_coherence": embedding_coherence,
        "scores": scores,
    }

    match_indices = list(
        zip(
            *np.unravel_index(
                np.argsort(distances["input_embedding"], axis=None),
                distances["input_embedding"].shape,
            )
        )
    )
    cumulative_indices = np.argsort(scores).tolist()
    target_indices = np.argsort(distances["input_target"].flatten()).tolist()

    indices = {
        "match": match_indices,
        "cumulative": cumulative_indices,
        "target": target_indices,
    }

    return {
        "paths": paths,
        "representations": representations,
        "distances": distances,
        "indices": indices,
        "metrics": metrics,
        "metadata": metadata,
    }


def get_multimodel_metrics(
    models: list[str],
    target_path: str | Path = metadata.PATHS.TARGET_IMAGE,
    embedding_dir: str | Path = metadata.PATHS.EMBEDDING_IMAGES,
    input_dir: str | Path = metadata.PATHS.UNPROCESSED_IMAGES,
    weight_relevance: int = 1,
) -> dict[str, Any]:
    all_metrics = [
        get_metrics(model, target_path, embedding_dir, input_dir, weight_relevance)
        for model in models
    ]
    return merge_metrics(all_metrics)


def save_processed_embedding_images(
    metrics: dict[str, Any], output_dir: Path = metadata.PATHS.EMBEDDING_SCORES_DIR
) -> None:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    n_images = len(metrics["paths"]["embedding"])
    for path, accuracy, coherence in tqdm(
        zip(
            metrics["paths"]["embedding"],
            metrics["distances"]["embedding_target"],
            metrics["distances"]["embedding_embedding"],
        ),
        desc=f"Saving {n_images} embedding images",
        total=n_images,
    ):
        image_id = path.name.split("-")[0]
        image_name = f"{accuracy.item():.04f}_{coherence.item():.04f}_{image_id}.png"
        image_path = str(output_dir.joinpath(image_name))
        cv2.imwrite(image_path, cv2.imread(str(path)))


def save_processed_input_images(
    metrics: dict[str, Any], output_dir: Path = metadata.PATHS.PROCESSED_IMAGES
) -> None:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    n_images = len(metrics["paths"]["input"])
    for path, score, accuracy, coherence in tqdm(
        zip(
            metrics["paths"]["input"],
            metrics["metrics"]["scores"],
            metrics["distances"]["input_target"],
            np.mean(metrics["distances"]["input_embedding"], axis=1),
        ),
        desc=f"Saving {n_images}, Processed Images",
        total=n_images,
    ):
        image_id = path.name.split("-")[0]
        image_name = (
            f"{score:.04f}_{accuracy.item():.04f}_{coherence:.04f}_{image_id}.png"
        )
        image_path = str(output_dir.joinpath(image_name))
        cv2.imwrite(image_path, cv2.imread(str(path)))


def main(interactive: bool = False) -> None:
    # Processing Images
    metrics = get_multimodel_metrics(["Facenet512"])  # "SFace", "ArcFace"])

    # Saving scored images
    save_processed_embedding_images(metrics)
    save_processed_input_images(metrics)

    if interactive:
        InteractiveSession(metrics).session()


if __name__ == "__main__":
    metadata.create_dirs()
    main(interactive=True)
