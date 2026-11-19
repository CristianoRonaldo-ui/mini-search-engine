from tokenizer import tokenize


def test_lowercases_and_removes_punctuation():
    assert tokenize("Hello, World!") == ["hello", "world"]


def test_removes_stop_words():
    assert tokenize("The cat is on the mat") == ["cat", "mat"]


def test_empty_string_returns_empty_list():
    assert tokenize("") == []


def test_apostrophe_splits_word():
    # Known limitation: "It's" becomes "it" + "s", and "it" is a stop word.
    assert tokenize("It's fast") == ["s", "fast"]