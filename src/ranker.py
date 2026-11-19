"""Score documents against a query using TF-IDF."""

import math
from tokenizer import tokenize


def compute_idf(term: str, index: dict[str, dict[str, int]], total_docs: int) -> float:
    """Return log(total_docs / document_frequency), or 0.0 if the term is unseen."""
    if term not in index:
        return 0.0
    document_frequency = len(index[term])
    return math.log(total_docs / document_frequency)


def search(
    query: str, index: dict[str, dict[str, int]], total_docs: int
) -> list[tuple[str, float]]:
    """Return (doc_id, score) pairs sorted from most to least relevant."""
    scores: dict[str, float] = {}
    for term in tokenize(query):
        idf = compute_idf(term, index, total_docs)
        for doc_id, term_count in index.get(term, {}).items():
            scores[doc_id] = scores.get(doc_id, 0.0) + term_count * idf
    return sorted(scores.items(), key=lambda pair: pair[1], reverse=True)
