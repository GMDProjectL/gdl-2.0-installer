from typing import List
from dataclasses import dataclass
from storage.settings import Settings

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
    
    @classmethod
    def add_log(cls, log_text: str):
        user_pass = Settings.get_instance().password
        log_text = log_text.replace(user_pass, '*' * len(user_pass))

        Logs.get_instance().new_lines.append(log_text)