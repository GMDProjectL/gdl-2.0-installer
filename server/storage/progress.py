from dataclasses import dataclass

@dataclass
class Progress():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Progress, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.progress = 0
            self._initialized = True
    
    @classmethod
    def get_instance(cls) -> 'Progress':
        if cls._instance is None:
            cls()
        
        return cls._instance