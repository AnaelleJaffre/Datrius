"""Keeps a short-term memory of the last 7 items.
1 item = 1 input, for now a sentence."""

import json
from collections import deque
from pathlib import Path

# Configuration
MEMORY_FILE = Path(__file__).parent / "short_term_memory.json"
MAX_LENGTH = 7

def _load_memory() -> list:
    """Loads short-term memory from the JSON file.
    Creates the file if it doesn't exist."""
    if not MEMORY_FILE.exists():
        _save_memory([])
        return []
    
    try:
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print(f"Error reading {MEMORY_FILE}. Resetting.")
        _save_memory([])
        return []

def _save_memory(data: list) -> None:
    """Saves data to the JSON file."""
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

class ShortTermMemory:
    def __init__(self):
        self._memory = _load_memory()

    def _persist(self) -> None:
        """Internal helper to save current state."""
        _save_memory(self._memory)

    def add(self, item: str) -> None:
        """Adds an item to the beginning of the memory (FIFO).
        Removes the oldest item if the max length is exceeded."""
        self._memory.insert(0, item)
        if len(self._memory) > MAX_LENGTH:
            self._memory.pop()
        self._persist()

    def get_all(self) -> list:
        """Returns a copy of the memory (order: most recent to oldest)."""
        return self._memory.copy()

    def get_recent(self, count: int = 3) -> list:
        """Retrieves the N most recent elements."""
        return self._memory[:count]
    
    def clear(self) -> None:
        """Clears the memory."""
        self._memory = []
        self._persist()