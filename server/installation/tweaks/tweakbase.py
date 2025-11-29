from storage.settings import Settings
from services.pacman_service import PacmanService

class TweakBase:
    def __init__(self, settings: Settings, root: str, pacman_service: PacmanService):
        self._settings = settings
        self._root = root
        self._pacman_service = pacman_service
