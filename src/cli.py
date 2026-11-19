"""Command-line interface for the mini search engine."""

import argparse

from indexer import build_index, load_documents
from ranker import search


def main() -> None:
    parser = argparse.ArgumentParser(description="Search local text files with TF-IDF ranking.")
    parser.add_argument("query", help="words to search for")
    parser.add_argument("--data", default="data", help="folder of .txt files (default: data)")
    parser.add_argument("--top", type=int, default=5, help="max number of results (default: 5)")
    args = parser.parse_args()

    try:
        documents = load_documents(args.data)
    except FileNotFoundError as error:
        print(f"Error: {error}")
        return

    if not documents:
        print(f"No .txt files found in '{args.data}'.")
        return

    index = build_index(documents)
    results = search(args.query, index, len(documents))

    if not results:
        print(f"No results for '{args.query}'.")
        return

    print(f"Top results for '{args.query}':")
    for rank, (doc_id, score) in enumerate(results[: args.top], start=1):
        print(f"{rank}. {doc_id}  (score: {score:.3f})")


if __name__ == "__main__":
    main()