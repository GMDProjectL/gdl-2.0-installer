from typing import List
from dataclasses import dataclass
from utils.singleton import Singleton

@dataclass
class Result(Singleton):
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.error = False
            self.success = False
            self.message = ""
            self._initialized = True
