"""Central router: dispatches normalized sensor input to the relevant brain function."""

from brain.language import make_memory_sentence
from brain.memory.long_term_memory import LongTermMemory
from brain.memory.short_term_memory import ShortTermMemory 
from brain.language.normalize_word import normalize_word, extract_punctuation

ltm = LongTermMemory()

def process(raw_input: str) -> str:
    """Processes raw input and returns the fitting output from the brain.

    Args:
        raw_input (str): The raw input text.
    
    Returns:
        str: The processed output from the brain.
    """
    # Is this supposed to be here? Or memory can be used outside, in language scripts?
    words_to_use = []
    words_from_memory = ltm.get_all_keys()

    words = [normalize_word(w) for w in raw_input.split()]

    for i in range(len(words) - 1):
        ltm.store(words[i], {words[i + 1]: 1}, "words")

    # If there are words of the sentence that are into memory, they are leveraged.
    for word in words:
        if word in words_from_memory:
            words_to_use.append(word)

    # Then it can be used to generate random text
    output = make_memory_sentence(words_to_use, len(words))

    return output