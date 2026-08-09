"""Public interface for speaking, independent of the underlying destination."""

from actuators.speak.destinations.console import write as _write_console

def write(text: str) -> None:
    _write_console(text)