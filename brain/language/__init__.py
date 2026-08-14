"""Generates text according to patterns in long-term memory."""

import random
from brain.memory.long_term_memory import LongTermMemory

ltm = LongTermMemory()

PUNCTUATION = {
    "middle": [",", ";", ":", " -", " —"],
    "end": [".", "!", "?"],
}
STOP_CHARS = set(PUNCTUATION["end"]) | {"..."}
FALLBACK_MIDDLE_CHANCE = 0.2  # used only when memory has no punctuation data for this word
REINFORCEMENT_SMOOTHING = 3  # higher = more repeated associations needed before punctuation feels "certain"


def choose_next_word(word: str) -> str:
    """Chooses the next word among the strongest associations in long-term memory."""
    top = ltm.get_top_associations(word, "words", 5)
    if not top:
        return "..."
    words, weights = zip(*top)
    return random.choices(words, weights=weights, k=1)[0]


def choose_punctuation_for_word(word: str) -> str | None:
    """Decides whether to attach punctuation after `word`, based on how often
    memory has seen punctuation follow it. The more reinforced the association,
    the higher the probability -- but it never becomes fully certain.

    Returns:
        str | None: A punctuation mark, or None if no punctuation is added.
    """
    top = ltm.get_top_associations(word, "punctuation", 5)

    if not top:
        return None

    total_weight = sum(weight for _, weight in top)
    probability = total_weight / (total_weight + REINFORCEMENT_SMOOTHING)

    if random.random() >= probability:
       return None

    punctuations, weights = zip(*top)
    return random.choices(punctuations, weights=weights, k=1)[0]


def target_length(input_length: int) -> int:
    proportion = random.uniform(0.5, 1.5)  # Randomly choose a proportion between 50% and 150%
    return max(1, int(input_length * proportion))


def assemble_sentence(words: list) -> str:
    """Assembles a list of words into a sentence, adding random punctuation.
    Used by extrapolate_text, which has no memory-based punctuation to draw from."""
    if not words:
        return "..."

    sentence = []
    for i, word in enumerate(words):
        sentence.append(word)
        if i < len(words) - 1 and random.random() < FALLBACK_MIDDLE_CHANCE:
            sentence.append(random.choice(PUNCTUATION["middle"]))

    sentence.append(random.choice(PUNCTUATION["end"]))

    return " ".join(sentence).replace(" ,", ",").replace(" .", ".").replace(" !", "!").replace(" ?", "?")


def finalize_sentence(words: list) -> str:
    """Capitalizes the first word and guarantees an end punctuation if none
    occurred naturally during generation."""
    words = list(words)
    words[0] = words[0].capitalize()
    if words[-1][-1] not in STOP_CHARS:
        words[-1] += random.choice(PUNCTUATION["end"])
    return " ".join(words)


def make_memory_sentence(memory: list, input_length: int) -> str:
    """
    Creates a sentence: starts with a random word from memory that has been said by the user.
    Then, chains each next word from its strongest known association.
    Punctuation is attached based on memory.
    The sentence stops early if the generated punctuation marks the end of a sentence.
    """
    if not memory:
        return "..."

    max_length = target_length(input_length)
    sentence = [random.choice(memory)] # Sentence starts with a random word from memory

    # Creation of the whole sentence
    for step in range(max_length - 1):
        current = sentence[-1]  # always punctuation-free at this point

        punctuation = choose_punctuation_for_word(current)
        if punctuation:
            sentence[-1] += punctuation # Integrated into the word ("word," instead of "word ,")
            if punctuation in STOP_CHARS:
                break  # the sentence ended naturally

        next_word = choose_next_word(current)
        sentence.append(next_word)
        
        if next_word == "...":  # no known association -> return
            return finalize_sentence(sentence)

    return finalize_sentence(sentence)