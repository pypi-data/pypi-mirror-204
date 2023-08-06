import numpy as np
from typing import Tuple, Any, Set
from hti_index.indexer import HTIIndex



class FlowFreqIndex(HTIIndex):
    def __init__(self, size: int = 100):
        super().__init__(size=size)
        self.node_frequency = {}
        self.transition_frequency = {}
        self.num_items = 0
        self.num_nodes = 0
        self.num_transitions = 0
        self.prev_key = None

    def _update_node_frequency(self, key: str):
        if key in self.node_frequency:
            self.node_frequency[key] += 1
        else:
            self.node_frequency[key] = 1
            
    def _update_transition_frequency(self, prev_key: str, key: str):
        if (prev_key, key) in self.transition_frequency:
            self.transition_frequency[(prev_key, key)] += 1
        else:
            self.transition_frequency[(prev_key, key)] = 1
            
    def insert(self, key: str, value: Any):
        super().insert(key, value)
        self._update_node_frequency(key)
        self.num_items += 1
        self.num_nodes += 1
        if self.num_items > 1:
            self._update_transition_frequency(self.prev_key, key)
            self.num_transitions += 1
        self.prev_key = key

    def update(self, key: str, value: Any):
        super().update(key, value)
        self._update_node_frequency(key)
        self.num_items += 1
        if self.num_items > 1:
            self._update_transition_frequency(self.prev_key, key)
            self.num_transitions += 1
        self.prev_key = key
        
    def clear(self):
        super().clear()
        self.node_frequency = {}
        self.transition_frequency = {}
        self.num_items = 0
        self.num_nodes = 0
        self.num_transitions = 0
        
    def get_node_key(self) -> Set[str]:
        return set(self.node_frequency.keys())
    
    def get_transition_keys(self) -> Set[Tuple[str, str]]:
        return set(self.transition_frequency.keys())

    def get_node_id(self, key: str) -> int:
        return self.lookup_table[key].id

    def save(self, path: str):
        np.savez(path, 
                 num_items=self.num_items,
                 num_nodes=self.num_nodes,
                 num_transitions=self.num_transitions,
                 hash_table=self.hash_table,
                 lookup_table=self.lookup_table,
                 node_frequency=self.node_frequency,
                 transition_frequency=self.transition_frequency
                 )
        
    def load(self, path: str):
        data = np.load(path, allow_pickle=True)
        self.num_items = data['num_items']
        self.num_nodes = data['num_nodes']
        self.num_transitions = data['num_transitions']
        self.hash_table = data['hash_table'].item()
        self.lookup_table = data['lookup_table'].item()
        self.node_frequency = data['node_frequency'].item()
        self.transition_frequency = data['transition_frequency'].item()
        return self
    
    
    def get_node_frequency(self, key: str) -> int:
        return self.node_frequency[key]
    
    



                

if __name__ == '__main__':
    bplus_tree = FlowFreqIndex(100)
    bplus_tree.insert('a', 1)
    bplus_tree.insert('b', 2)
    bplus_tree.insert('c', 3)
    bplus_tree.insert('d', 4)
    bplus_tree.insert('e', 5)
    bplus_tree.insert('f', 6)
    bplus_tree.insert('g', 7)
    bplus_tree.insert('h', 8)
    bplus_tree.insert('i', 9)
    bplus_tree.insert('j', 10)
    bplus_tree.insert('k', 11)
    bplus_tree.insert('l', 12)
    bplus_tree.insert('m', 13)
    bplus_tree.insert('n', 14)
    bplus_tree.insert('o', 15)
    bplus_tree.insert('p', 16)
    bplus_tree.insert('q', 17)
    bplus_tree.insert('r', 18)
    bplus_tree.insert('s', 19)
    bplus_tree.insert('t', 20)
    bplus_tree.insert('u', 21)
    bplus_tree.insert('v', 22)
    bplus_tree.insert('w', 23)
    bplus_tree.insert('x', 24)
    bplus_tree.insert('y', 25)
    bplus_tree.insert('z', 26)
    print(bplus_tree.range_search('a', 'z'))