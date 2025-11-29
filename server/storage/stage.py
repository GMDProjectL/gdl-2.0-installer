from dataclasses import dataclass
from utils.singleton import Singleton

@dataclass
class Stage(Singleton):
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.stage = 0
            self._initialized = True
