import math

import pytest

from indexer import build_index
from ranker import compute_idf, search

DOCS = {
    "d1": "The cat sat on the mat. The cat is happy.",
    "d2": "The dog chased the cat.",
    "d3": "Dogs love bones.",
}


def test_idf_of_unseen_term_is_zero():
    index = build_index(DOCS)
    assert compute_idf("pizza", index, 3) == 0.0


def test_idf_matches_formula():
    index = build_index(DOCS)
    assert compute_idf("cat", index, 3) == pytest.approx(math.log(3 / 2))


def test_rare_term_outranks_repeated_common_term():
    index = build_index(DOCS)
    results = search("cat bones", index, 3)
    ranked_ids = [doc_id for doc_id, _ in results]
    assert ranked_ids == ["d3", "d1", "d2"]


def test_search_with_no_matches_returns_empty_list():
    index = build_index(DOCS)
    assert search("pizza", index, 3) == []