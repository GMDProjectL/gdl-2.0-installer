from installation.pacman import Pacman
from traceback import format_exc
from typing import Optional
from storage.settings import Settings

class TweakBase:
    def __init__(self, settings: Settings, root: str):
        self._settings = settings
        self._root = root