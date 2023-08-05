from typing import Any, Dict, List, Optional, Tuple
from hti_index.composite import NodeComposite
import hashlib
import numpy as np


class HTIIndex:
    def __init__(self, size: int):
        self.size = size
        self.lookup_table: Dict[str, NodeComposite] = {}
        self.hash_table = np.empty((size,), dtype=object)
        self.num_items = 0

    def __len__(self):
        return self.num_items

    def insert(self, key: str, value: Any):
        node = NodeComposite(key=key, value=value)
        self.lookup_table[key] = node
        hash_value = self._hash_key(key)
        if self.hash_table[hash_value] is None:
            self.hash_table[hash_value] = []
        self.hash_table[hash_value].append(node)
        self.num_items += 1
        self._resize_if_needed()

    def delete(self, key: str):
        if key not in self.lookup_table:
            raise ValueError(f"Key '{key}' not found in index.")
        node = self.lookup_table.pop(key)
        hash_value = self._hash_key(key)
        for i, item in enumerate(self.hash_table[hash_value]):
            if item.key == key:
                self.hash_table[hash_value].pop(i)
                break
        self.num_items -= 1
        self._resize_if_needed()

    def search(self, key: str) -> Optional[Any]:
        if key not in self.lookup_table:
            return None
        return self.lookup_table[key].value

    def update(self, key: str, value: Any):
        if key not in self.lookup_table:
            raise ValueError(f"Key '{key}' not found in index.")
        self.lookup_table[key].value = value
        hash_value = self._hash_key(key)
        for item in self.hash_table[hash_value]:
            if item.key == key:
                item.value = value
                break

    def get_bucket(self, key: str) -> List[NodeComposite]:
        hash_value = self._hash_key(key)
        return self.hash_table[hash_value]

    def _hash_key(self, key: str) -> int:
        # Use SHA256 hash function for improved security and collision resistance
        return int.from_bytes(hashlib.sha256(key.encode()).digest(), byteorder='big') % self.size

    def clear(self):
        self.lookup_table.clear()
        self.hash_table = np.empty((self.size,), dtype=object)
        self.num_items = 0

    def keys(self) -> List[str]:
        return list(self.lookup_table.keys())

    def values(self) -> List[Any]:
        return [node.value for node in self.lookup_table.values()]

    def _resize_if_needed(self):
        # Double the size of the index if the number of items exceeds half the size
        if self.num_items > self.size // 2:
            self.size *= 2
            new_hash_table = np.empty((self.size,), dtype=object)
            for node in self.lookup_table.values():
                hash_value = self._hash_key(node.key)
                if new_hash_table[hash_value] is None:
                    new_hash_table[hash_value] = []
                new_hash_table[hash_value].append(node)
            self.hash_table = new_hash_table


    def _get_range(self, node: NodeComposite, start: str, end: str) -> List[Tuple[str, Any]]:
        if node is None:
            return []
        results = []
        if start <= node.key <= end:
            results.append((node.key, node.value))
        if start < node.key:
            results.extend(self._get_range(node.left, start, end))
            
        if end > node.key:
            results.extend(self._get_range(node.right, start, end))
        return results

    def range_search(self, start: str, end: str) -> List[Tuple[str, Any]]:
        results = []
        for bucket in self.hash_table:
            if bucket is not None:
                for node in bucket:
                    results.extend(self._get_range(node, start, end))
        return results
    
    
    
    
