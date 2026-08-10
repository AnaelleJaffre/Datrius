"""Keeps instances into the long-term memory with a key-value structure.
The more the key is called, the more its count increases.
"""

import json
from pathlib import Path

MEMORY_FILE = Path(__file__).parent / "long_term_memory.json"

def _load_memory() -> dict:
    """Loads long-term memory from the JSON file.
    Creates an empty dict if the file doesn't exist."""
    if not MEMORY_FILE.exists():
        _save_memory({})
        return {}
    
    try:
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print(f"Error reading {MEMORY_FILE}. Resetting.")
        _save_memory({})
        return {}

def _save_memory(data: dict) -> None:
    """Saves data to the JSON file."""
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

class LongTermMemory:
    def __init__(self):
        self._memory = _load_memory()

    def _persist(self) -> None:
        """Internal helper to save current state."""
        _save_memory(self._memory)

    def store(self, key: str, associations: dict) -> None:
        """Stores or reinforces associations for a key.
        
        Args:
            key (str): The main word/concept (e.g., "sun").
            associations (dict): A dictionary of associated words and their strengths (e.g., {"warm": 3, "big": 2}).
        
        Logic:
        - If key exists, it merges the new associations with existing ones.
        - If an association already exists, its strength is added to the new strength (reinforcement).
        - If the key is new, it creates the entry.
        """
        if key not in self._memory:
            self._memory[key] = {}
        
        current_associations = self._memory[key]
        for assoc_word, strength in associations.items():
            if assoc_word in current_associations:
                # Reinforcement: add the new strength to the existing one
                current_associations[assoc_word] += strength
            else:
                # New association
                current_associations[assoc_word] = strength
        
        self._persist()

    def retrieve(self, key: str) -> dict:
        """Retrieves all associations for a specific key.
        Returns an empty dict if the key doesn't exist."""
        return self._memory.get(key, {})

    def get_top_associations(self, key: str, limit: int = 5) -> list:
        """Returns the strongest associations for a key, sorted by strength (descending).
        
        Returns:
            list: List of tuples [(word, strength), ...]
        """
        associations = self.retrieve(key)
        if not associations:
            return []
        
        # Sort by strength (value) descending
        sorted_associations = sorted(associations.items(), key=lambda x: x[1], reverse=True)
        return sorted_associations[:limit]

    def delete(self, key: str) -> None:
        """Removes a key and all its associations."""
        if key in self._memory:
            del self._memory[key]
            self._persist()

    def get_all_keys(self) -> list:
        """Returns a list of all stored keys."""
        return list(self._memory.keys())
    
    def clear(self) -> None:
        """Clears all long-term memory."""
        self._memory = {}
        self._persist()