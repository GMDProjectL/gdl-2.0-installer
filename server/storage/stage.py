from dataclasses import dataclass

@dataclass
class Stage():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Stage, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.stage = 0
            self._initialized = True
    
    @classmethod
    def get_instance(cls) -> 'Stage':
        if cls._instance is None:
            cls()
        
        return cls._instance