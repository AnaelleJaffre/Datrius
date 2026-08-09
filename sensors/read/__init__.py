"""Public interface for text input, independent of the underlying source."""

from sensors.read.sources.console import read as console_read

def read(source: str = "console") -> str:
    """Reads raw text from the specified source.

    Args:
        source (str): The source to read from. Defaults to "console".

    Returns:
        str: The raw text read from the source.
    """
    if source == "console":
        return console_read()
    else:
        raise ValueError(f"Unknown source: {source}")