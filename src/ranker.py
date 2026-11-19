"""Score documents against a query using TF-IDF."""

import math


def compute_idf(term: str, index: dict[str, dict[str, int]], total_docs: int) -> float:
    """Return log(total_docs / document_frequency), or 0.0 if the term is unseen."""
    if term not in index:
        return 0.0
    document_frequency = len(index[term])
    return math.log(total_docs / document_frequency) 