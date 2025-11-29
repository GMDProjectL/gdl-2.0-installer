from typing import List
from dataclasses import dataclass
from utils.singleton import Singleton
from storage.settings import Settings

@dataclass
class Logs(Singleton):
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.new_lines: List[str] = []
            self._initialized = True

    @classmethod
    def add_log(cls, log_text: str):
        user_pass = Settings.get_instance().password
        log_text = log_text.replace(user_pass, '*' * len(user_pass))

        cls.get_instance().new_lines.append(log_text)
