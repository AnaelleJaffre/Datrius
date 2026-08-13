"""Generates text according to patterns in long-term memory."""

import random
from brain.memory.long_term_memory import LongTermMemory

ltm = LongTermMemory()

PUNCTUATION = {
    "middle": [",", ";", ":", " -", " —"],
    "end": [".", "!", "?"],
}

def choose_next_word(word: str) -> str:
    """Chooses the next word among the strongest associations in long-term memory."""
    top = ltm.get_top_associations(word, "words", 5)
    return random.choice(top)[0] if top else "..."


def target_length(input_length: int) -> int:
    proportion = random.uniform(0.5, 1.5)  # Randomly choose a proportion between 50% and 150%
    return int(input_length * proportion)


def assemble_sentence(words: list) -> str:
    """Assembles a list of words into a sentence, adding punctuation."""
    if not words:
        return "..."

    sentence = []
    for i, word in enumerate(words):
        sentence.append(word)
        # Randomly decide to add punctuation after the word
        if i < len(words) - 1:  # Don't add punctuation after the last word
            if random.random() < 0.2:  # 20% chance to add punctuation
                sentence.append(random.choice(PUNCTUATION["middle"]))
    
    # Add end punctuation
    sentence.append(random.choice(PUNCTUATION["end"]))
    
    return " ".join(sentence).replace(" ,", ",").replace(" .", ".").replace(" !", "!").replace(" ?", "?")


# To improve
def make_memory_sentence(memory: list, input_length: int) -> str:
    """
    Creates a sentence: starts with a random word from memory, then
    chains each next word via its strongest known association.
    """
    if not memory:
        return "..."

    length = target_length(input_length)
    sentence = [random.choice(memory)]

    for _ in range(length - 1):
        next_word = choose_next_word(sentence[-1])
        if next_word == "...":  # no known association -> fall back instead of stalling
            next_word = random.choice(memory)
        sentence.append(next_word)

    return assemble_sentence(sentence)