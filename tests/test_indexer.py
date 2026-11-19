import pytest

from indexer import build_index, load_documents


def test_build_index_counts_terms_per_document():
    docs = {"d1": "cat cat dog", "d2": "dog"}
    index = build_index(docs)
    assert index["cat"] == {"d1": 2}
    assert index["dog"] == {"d1": 1, "d2": 1}


def test_load_documents_reads_only_txt_files(tmp_path):
    (tmp_path / "a.txt").write_text("hello world", encoding="utf-8")
    (tmp_path / "b.txt").write_text("goodbye", encoding="utf-8")
    (tmp_path / "notes.md").write_text("ignore me", encoding="utf-8")

    documents = load_documents(str(tmp_path))

    assert documents == {"a.txt": "hello world", "b.txt": "goodbye"}


def test_load_documents_missing_folder_raises_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_documents(str(tmp_path / "does_not_exist"))