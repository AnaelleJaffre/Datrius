"""Central router: dispatches normalized sensor input to the relevant brain function."""

from brain.language import make_memory_sentence
from brain.memory.long_term_memory import LongTermMemory
from brain.language.normalize_word import normalize_word, extract_punctuation

ltm = LongTermMemory()


def process(raw_input: str) -> str:
    """Processes raw input and returns the fitting output from the brain.

    Args:
        raw_input (str): The raw input text.

    Returns:
        str: The processed output from the brain.
    """
    raw_tokens = raw_input.split()
    words = [normalize_word(token) for token in raw_tokens]
    words_from_memory = ltm.get_all_keys("words")

    # Learn word -> punctuation associations, from what the user actually wrote.
    for token, word in zip(raw_tokens, words):
        punctuation = extract_punctuation(token)
        if punctuation:
            ltm.store(word, {punctuation: 1}, "punctuation")

    # Learn word -> next word associations.
    for i in range(len(words) - 1):
        ltm.store(words[i], {words[i + 1]: 1}, "words")

    # If there are words of the sentence that are already in memory, they are leveraged.
    words_to_use = [word for word in words if word in words_from_memory]

    return make_memory_sentence(words_to_use, len(words))