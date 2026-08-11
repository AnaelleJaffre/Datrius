"""Normalization utilities for words."""

PUNCTUATION_CHARS = set(",;:-—.!?")

# Adapt : we use string.punctuation to strip punctuation from words,
# But after the brain should define itself what is punctuation thanks to LTM.
def strip_punctuation(word: str) -> str:
    return "".join(char for char in word if char not in PUNCTUATION_CHARS)


def extract_punctuation(word: str) -> str:
    """Extracts punctuation from a word."""
    return "".join(char for char in word if char in PUNCTUATION_CHARS)


def normalize_word(word: str) -> str:
    """
    Normalizes a word by stripping punctuation and converting it to lowercase.
    """
    return strip_punctuation(word).lower()