# utils/vector_utils.py
import math

def is_valid_vector(vector: list[float] | None) -> bool:
    if vector is None:
        return False

    if not isinstance(vector, list):
        return False

    if len(vector) == 0:
        return False

    return True

def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    if len(vec1) != len(vec2):
        raise ValueError("Vector dimension mismatch")

    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))

    if norm1 == 0.0 or norm2 == 0.0:
        raise ValueError("Zero vector is not allowed")

    return dot_product / (norm1 * norm2)