import weakref
from typing import Optional, List, Type
import numpy as np
from hti_index.component import Composite, Component
import hashlib


class NodeComposite(Composite):
    
    lookup_table = weakref.WeakValueDictionary()  # Use a weak value dictionary to store nodes by their hashes

    def __init__(self, key: Optional[Type] = None, value: Optional[Type] = None):
        self.children = np.array([], dtype=object)
        self.children_hashes = np.array([], dtype=object)
        self.key = key
        self.value = value
        self.id = self._hash_node(self)
        self.left = None
        self.right = None

    def add_child(self, child: Component):
        if child == self:
            raise ValueError("Cannot add the node as its own child.")
        if child in self.children:
            raise ValueError(f"Child with id '{child.id}' is already added.")
        self.children = np.append(self.children, child)
        child_hash = self._hash_node(child)
        self.children_hashes = np.append(self.children_hashes, child_hash)
        self.lookup_table[child_hash] = child
        print(f"Added child with id '{child}' to node with id '{self}'.")
        
    def remove_child(self, child: Component):
        if child not in self.children:
            raise ValueError(f"Child with id '{child.id}' not found.")
        child_idx = np.where(self.children == child)[0][0]
        child_hash = self.children_hashes[child_idx]
        self.children = np.delete(self.children, child_idx)
        self.children_hashes = np.delete(self.children_hashes, child_idx)
        del self.lookup_table[child_hash]
        

    def _hash_node(self, node: Component) -> str:
        return hashlib.sha256(str(node).encode()).hexdigest()

    def get_child_by_hash(self, node_hash: str) -> Optional[Component]:
        return self.lookup_table.get(node_hash)

    def get_parent_by_hash(self, node_hash: str) -> Optional[Component]:
        for node in self.lookup_table.values():
            if isinstance(node, NodeComposite) and node_hash in node.children_hashes:
                return node
        return None

    def get_node_by_hash(self, content_hash: str) -> Optional[Component]:
        return self.lookup_table.get(content_hash)

    def get_child_by_index(self, index: int) -> Component:
        return self.children[index]
    
    def clear_children(self):
        self.children = np.array([], dtype=object)
        self.children_hashes = np.array([], dtype=object)
        self.lookup_table.clear()

    def get_children(self) -> List[Component]:
        return {
            "children": self.children,
            "children_hashes": self.children_hashes
        }

    