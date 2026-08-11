"""Generates abstract poetic text from raw input, based on dominant vowels."""

import random

VOWELS = "aeiou"
WORDS_BY_VOWEL = {
    "a": ["teach", "alienate", "cascade", "a", "amplify", "astral", "and", "arcane", "awaken"],
    "e": ["echo", "elevate", "enlighten", "end", "essence", "eternal", "ethereal", "embrace"],
    "i": ["ignite", "illuminate", "inspire", "infinite", "intagible", "it", "I"],
    "o": ["observe", "of", "oscillate", "for", "overcome", "omnipresent", "orchestrate", "open"],
    "u": ["unite", "uplift", "unveil", "universe", "understand", "unfold", "unique", "ubiquitous"],
}
PUNCTUATION = {
    "middle": [",", ";", ":", " -", " —"],
    "end": [".", "!", "?"],
}

def dominant_vowel(word: str) -> str | None:
    """Determines the dominant vowel in the given word.

    Args:
        word (str): The input word.

    Returns:
        str | None: The dominant vowel or None if no vowels are found.
    """
    vowel_count = {vowel: 0 for vowel in VOWELS}
    
    for char in word.lower():
        if char in VOWELS:
            vowel_count[char] += 1

    if max(vowel_count.values()) == 0:
        return None

    return max(vowel_count, key=vowel_count.get)


# Not used
def extrapolate_text(raw_text: str) -> str: 
    """Generates abstract poetic text based on the dominant vowels in the raw input.

    Args:
        raw_text (str): The raw input text.

    Returns:
        str: The generated abstract poetic text.
    """
    words = raw_text.split()
    dominant_vowels = [dominant_vowel(word) for word in words if dominant_vowel(word) is not None]
    final_sentence = []

    for vowel in dominant_vowels:
        final_sentence.append(random.choice(WORDS_BY_VOWEL[vowel]))
        if random.random() < 0.2 and (final_sentence[-1] not in PUNCTUATION["middle"]):
            final_sentence[-1] += random.choice(PUNCTUATION["middle"])

    if not final_sentence:
            return "..."
    
    final_sentence = [word.capitalize() if i == 0 else word for i, word in enumerate(final_sentence)]

    if final_sentence[-1] in PUNCTUATION["middle"]:
        final_sentence[-1] = final_sentence[-1].pop()
        
    final_sentence[-1] += random.choice(PUNCTUATION["end"])
   
    return " ".join(final_sentence)


# To improve
def make_memory_sentence(memory: list) -> str :
    """
    Creates a sentence with words that [the user said and the brain has in memory].
    """

    final_sentence = []
    proportion = random.randint(2,10)

    if not memory:
        return "..."
    
    for counter in range(1, proportion):
        final_sentence.append(random.choice(memory))

    # Capital at the begining and end punctuation
    final_sentence = [word.capitalize() if i == 0 else word for i, word in enumerate(final_sentence)]
    final_sentence[-1] += random.choice(PUNCTUATION["end"])

    return " ".join(final_sentence)