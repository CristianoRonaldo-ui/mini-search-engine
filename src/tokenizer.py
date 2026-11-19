"""Turn raw text into a list of normalized words (tokens)"""

STOP_WORDS = {
    "a",
    "an",
    "the",
    "is",
    "are",
    "was",
    "and",
    "or",
    "of",
    "to",
    "in",
    "on",
    "for",
    "it",
    "this",
    "that",
}


def tokenize(text: str) -> list[str]:
    """Lowercase text, replace punctuation with spaces, split into words,
    and drop common stop words"""
    cleaned_chars = []
    for char in text.lower():
        if char.isalnum():
            cleaned_chars.append(char)
        else:
            cleaned_chars.append(" ")
    cleaned_text = "".join(cleaned_chars)

    words = cleaned_text.split()
    return [word for word in words if word not in STOP_WORDS]
