"""Central router: dispatches normalized sensor input to the relevant brain function."""

from brain.language import extrapolate_text

def process(raw_input: str) -> str:
    """Processes raw input and returns the fitting output from the brain.

    Args:
        raw_input (str): The raw input text.
    
    Returns:
        str: The processed output from the brain.
    """
    output = extrapolate_text(raw_input)

    return output