from typing import List
from dataclasses import dataclass

@dataclass
class Logs():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logs, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.new_lines: List[str] = []
            self._initialized = True
    
    @classmethod
    def get_instance(cls) -> 'Logs':
        if cls._instance is None:
            cls()
        
        return cls._instance