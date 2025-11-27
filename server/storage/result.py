from typing import List
from dataclasses import dataclass

@dataclass
class Result():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Result, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.error = False
            self.success = False
            self._initialized = True
    
    @classmethod
    def get_instance(cls) -> 'Result':
        if cls._instance is None:
            cls()
        
        return cls._instance