from typing import TypeVar, Type

T = TypeVar('T')

class Singleton:
    """
    Base class for implementing the Singleton pattern. 
    I just don't wanna copy over ts lol
    """
    _instance = None

    def __new__(cls: Type[T]) -> T:
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls: Type[T]) -> T:
        if cls._instance is None:
            cls()
        return cls._instance
