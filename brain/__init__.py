"""Central router: dispatches normalized sensor input to the relevant brain function."""

from brain.language import extrapolate_text, make_memory_sentence
from brain.memory.long_term_memory import LongTermMemory
from brain.memory.short_term_memory import ShortTermMemory 

ltm = LongTermMemory()

def process(raw_input: str) -> str:
    """Processes raw input and returns the fitting output from the brain.

    Args:
        raw_input (str): The raw input text.
    
    Returns:
        str: The processed output from the brain.
    """
    # Is this supposed to be here? Or memory can be used outside, in language scripts?
    sentence = []
    words_to_use = []
    words_from_memory = ltm.get_all_keys()

    for word in raw_input.split():

        # The word is stored / being reinforced with the 2 previous words.
        last_word_id = len(sentence) - 1
        if len(sentence) != 0:
            ltm.store(word, {sentence[last_word_id]:1, sentence[last_word_id - 1]:0.5})

        sentence.append(word.lower())

    # If there are words of the sentence that are into memory, they are leveraged.
    for word in sentence:
        if word in words_from_memory:
            words_to_use.append(word)

    # Then it can be used to generate random text
    output = make_memory_sentence(words_to_use)

    return output