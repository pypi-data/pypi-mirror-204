from datetime import datetime
from uuid import uuid4
from abc import ABCMeta



class IdDescriptor:
    _ids = set()

    def __get__(self, instance, owner):
        return instance.__dict__['_id']

    def __set__(self, instance, value):
        if value in self._ids:
            raise ValueError(f"Id '{value}' is already in use.")
        self._ids.add(value)
        instance.__dict__['_id'] = value

    def __delete__(self, instance):
        self._ids.remove(instance.__dict__['_id'])
        del instance.__dict__['_id']
        
    def generate_id(self) -> str:
        return str(uuid4())


class TimestampMeta(type):
    def __new__(cls, name, bases, dct):
        dct['timestamp'] = datetime.utcnow()
        return super().__new__(cls, name, bases, dct)
    
    

class CombinedMeta(TimestampMeta, ABCMeta):
    __slots__ = ()
   
    
    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct)   
    
    def __init__(self, name, bases, dct):
        super().__init__(name, bases, dct)
        self._id = IdDescriptor().generate_id()
        
    def __str__(self):
        return f"{self.__class__.__name__}({self._id})"
    
    def __repr__(self): 
        return f"{self.__class__.__name__}({self._id})"
    
    
class Component(metaclass=CombinedMeta):
        
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value
        
    def accept(self, visitor):
        visitor.visit_component(self)
        
    def __str__(self):
        return f"{self.__class__.__name__}({self._id})"
    
    def __repr__(self): 
        return f"{self.__class__.__name__}({self._id})"
    
    def __eq__(self, other):
        return self._id == other._id
    
    def __hash__(self):
        return hash(self._id)
    
    