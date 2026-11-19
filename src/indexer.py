"""Build an inverted index that maps each word to the documents containing it"""

from pathlib import Path
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


def load_documents(folder: str) -> dict[str, str]:
    """Read every .txt file in folder into {file_name: file_text}."""
    folder_path = Path(folder)
    if not folder_path.is_dir():
        raise FileNotFoundError(f"Folder not found: {folder}")

    documents: dict[str, str] = {}
    for file_path in sorted(folder_path.glob("*.txt")):
        documents[file_path.name] = file_path.read_text(encoding="utf-8")
    return documents
