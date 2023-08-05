from abc import abstractmethod
from typing import List, Optional, Any
from .utils import CombinedMeta


class NodeComponent(metaclass=CombinedMeta):
        
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    @abstractmethod
    def accept(self, visitor):
        pass

    def __str__(self):
        return f"{self.__class__.__name__}({self._id})"
    
    def __repr__(self): 
        return f"{self.__class__.__name__}({self._id})"
    
    def __eq__(self, other):
        return self._id == other._id
    
    def __hash__(self):
        return hash(self._id)

    
class Component(NodeComponent):
    def __init__(self):
        self.parent = None
        self.children = []
        
    def accept(self, visitor):
        visitor.visit_component(self)


    
    @abstractmethod
    def get_ancestors(self) -> List['NodeComponent']:
        pass

    @abstractmethod
    def get_descendants(self) -> List['NodeComponent']:
        pass

    def set_parent(self, parent: 'NodeComponent'):
        self.parent = parent

    def get_parent(self) -> Optional['NodeComponent']:
        return self.parent

    def add_child(self, child: 'NodeComponent'):
        self.children.append(child)

    def get_children(self) -> List['NodeComponent']:
        return self.children.copy()
    
    def remove_child(self, child: 'NodeComponent'):
        self.children.remove(child)
        
    @abstractmethod
    def max_children(self) -> int:
        pass
    
    
    
    
class Composite(Component):
    
    def __init__(self, key: str, value: str):
        super().__init__()
        self.key = key
        self.value = value
        
    def accept(self, visitor):
        visitor.visit_composite(self)
        
    def get_ancestors(self) -> List['NodeComponent']:
        ancestors = []
        parent = self.parent
        while parent is not None:
            ancestors.append(parent)
            parent = parent.parent
        return ancestors
    
    def get_descendants(self) -> List['NodeComponent']:
        descendants = []
        for child in self.children:
            descendants.append(child)
            if isinstance(child, Composite):
                descendants.extend(child.get_descendants())
        return descendants
    
    def __str__(self):
        return f"{self.__class__.__name__}({self._id})"
    

    def get_child_by_key(self, key: str) -> Component:
        for child in self.children:
            if child.key == key:
                return child
        raise ValueError(f"Child with key '{key}' not found.")
    
    def get_child_by_value(self, value: Any) -> Component:
        for child in self.children:
            if child.value == value:
                return child
        raise ValueError(f"Child with value '{value}' not found.")
        

    def is_last_child(self, child: Component) -> bool:
        return child == self.children[-1]

    def is_first_child(self, child: Component) -> bool:
        return child == self.children[0]
    
    def max_children(self) -> int:
        return 2