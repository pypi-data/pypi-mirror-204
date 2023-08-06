from typing import List, Callable, Any

import numpy as np
from nltk import tokenize
from scipy.signal import argrelextrema


def _activate_text_similarities(similarities, paragraph_size: int) -> np.ndarray:
    xs = np.linspace(-10, 10, paragraph_size)
    ys = 1 / (1 + np.exp(0.5 * xs))
    activation_weights = ys.reshape(1, -1)

    diagonals = np.zeros_like(similarities)
    for k in range(similarities.shape[0]):
        diag = np.diag(similarities, k)
        diagonals[k:k + diag.shape[0], k] = diag.reshape(-1)

    activated_similarities = diagonals * activation_weights

    return np.sum(activated_similarities, axis=1)


def cosine_similarity(embeddings: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(embeddings, axis=1)
    normalized_embeddings = embeddings / norm.reshape(-1, 1)

    return np.dot(normalized_embeddings, normalized_embeddings.T)


def to_paragraphs(content: str, embed_fn: Callable[[str], Any]) -> List[List[str]]:
    # Tokenize the content into individual sentences.
    sentences = tokenize.sent_tokenize(content)

    # If no sentences are found, return an empty list.
    if len(sentences) == 0:
        return []

    # Calculate the sentence embeddings for all the sentences.
    embeddings = embed_fn(sentences)

    # Calculate the pairwise cosine similarities between all the sentence embeddings.
    similarities = cosine_similarity(embeddings)

    # Activate the similarities to create paragraph boundaries.
    paragraph_boundaries = _activate_text_similarities(similarities, len(sentences))

    # Identify the split points where paragraphs end and new ones begin.
    split_points = argrelextrema(paragraph_boundaries, np.less, order=2)[0]

    last_split_point = 0

    for split_point in split_points:
        yield " ".join(sentences[last_split_point:split_point])
        last_split_point = split_point

    if last_split_point < len(sentences):
        yield " ".join(sentences[last_split_point:])
