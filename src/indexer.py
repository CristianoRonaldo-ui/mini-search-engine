"""Build an inverted index that maps each word to the documents containing it."""

from tokenizer import tokenize


def build_index(documents: dict[str, str]) -> dict[str, dict[str, int]]:
    """Map each token to {doc_id: number of times the token appears in that doc}."""
    index: dict[str, dict[str, int]] = {}
    for doc_id, text in documents.items():
        for token in tokenize(text):
            if token not in index:
                index[token] = {}
            index[token][doc_id] = index[token].get(doc_id, 0) + 1
    return index