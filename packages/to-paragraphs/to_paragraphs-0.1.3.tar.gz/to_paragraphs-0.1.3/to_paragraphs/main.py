from typing import List, Callable, Any

import numpy as np
from nltk import tokenize
from scipy.signal import argrelextrema


def _activate_text_similarities(similarities, paragraph_size: int) -> np.ndarray:
    x = np.linspace(-10, 10, paragraph_size)
    ys = 1 / (1 + np.exp(0.5 * x))

    diagonals = np.array([
        np.pad(
            np.diag(similarities, k),
            (0, similarities.shape[0] - np.diag(similarities, k).size)
        ) for k in range(similarities.shape[0])
    ])

    activation_weights = np.pad(ys, (0, similarities.shape[0] - paragraph_size))

    activated_similarities = diagonals * activation_weights.reshape(-1, 1)

    activated_similarities = np.sum(activated_similarities, axis=0)

    return activated_similarities


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

    # Group the sentences into paragraphs.
    paragraphs = [[]]
    current_paragraph_index = 0

    for sentence_index, sentence in enumerate(sentences):
        # Add the current sentence to the current paragraph.
        paragraphs[current_paragraph_index].append(sentence)

        # Check if the current sentence is a split point.
        if sentence_index in split_points:
            # If it is, start a new paragraph.
            current_paragraph_index += 1
            paragraphs.append([])

    # Return the resulting list of paragraphs.
    return paragraphs
