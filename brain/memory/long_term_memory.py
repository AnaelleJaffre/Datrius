"""Keeps instances into the long-term memory with a key-value structure.
The more the key is called, the more its count increases.
"""

import json
from pathlib import Path

MEMORY_FILE = Path(__file__).parent / "storage/long_term_memory.json"

def _load_memory() -> dict:
    """Loads long-term memory from the JSON file.
    Creates an empty dict if the file doesn't exist."""
    if not MEMORY_FILE.exists():
        _save_memory({"words": {}, "punctuation": {}})
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

    def store(self,  key: str, associations: dict, category: str = "words") -> None:
        """Stores or reinforces associations for a key.
        
        Args:
            category (str): The category under which to store the key (e.g., "words", "punctuation").
            key (str): The main word/concept (e.g., "sun").
            associations (dict): A dictionary of associated words and their strengths (e.g., {"warm": 3, "big": 2}).
        
        Logic:
        - If key exists, it merges the new associations with existing ones.
        - If an association already exists, its strength is added to the new strength (reinforcement).
        - If the key is new, it creates the entry.
        """
        if category not in self._memory:
            self._memory[category] = {}
        
        if key not in self._memory[category]:
            self._memory[category][key] = {}
        
        current_associations = self._memory[category][key]
        for assoc_word, strength in associations.items():
            if assoc_word in current_associations:
                # Reinforcement: add the new strength to the existing one
                current_associations[assoc_word] += strength
            else:
                # New association
                current_associations[assoc_word] = strength
        
        self._persist()

    def retrieve(self, key: str, category: str = "words") -> dict:
        """Retrieves all associations for a specific key.
        Returns an empty dict if the key doesn't exist."""
        return self._memory.get(category, {}).get(key, {})

    def get_top_associations(self, key: str, category: str = "words", limit: int = 5) -> list:
        """Returns the strongest associations for a key, sorted by strength (descending).
        
        Returns:
            list: List of tuples [(word, strength), ...]
        """
        associations = self.retrieve(key, category)
        if not associations:
            return []
        
        # Sort by strength (value) descending
        sorted_associations = sorted(associations.items(), key=lambda x: x[1], reverse=True)
        return sorted_associations[:limit]

    def delete(self, key: str, category: str = "words") -> None:
        """Removes a key and all its associations."""
        if category in self._memory and key in self._memory[category]:
            del self._memory[category][key]
            self._persist()

    def get_all_keys(self, category: str = "words") -> list:
        """Returns a list of all stored keys."""
        return list(self._memory.get(category, {}).keys())

    def clear(self) -> None:
        """Clears all long-term memory."""
        self._memory = {}
        self._persist()