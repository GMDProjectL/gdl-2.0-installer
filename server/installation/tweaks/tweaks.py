import os
import shutil
import subprocess
from traceback import format_exc
from typing import Iterator, Dict, Any, List, Optional
from storage.logs import Logs
from storage.progress import Progress
from storage.settings import Settings
from installation.process_utils import ProcessUtils
from .games import Games
from .internet import Internet
from .sysutils import SystemUtils
from .multimedia import Multimedia

class Tweaks:
    _instance: Optional['Tweaks'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Tweaks, cls).__new__(cls)
            cls._instance._initialized = False 

        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized') or not self._initialized:
            self._initialized = True

    @classmethod
    def get_instance(cls) -> 'Tweaks':
        if cls._instance is None:
            cls()
        
        return cls._instance
    
    def apply_settings(self, settings: Settings, root: str):
        self._settings = settings
        self._root = root
    
    def begin_features_installation(self):
        games = Games(self._settings, self._root)
        internet = Internet(self._settings, self._root)
        sysutils = SystemUtils(self._settings, self._root)
        multimedia = Multimedia(self._settings, self._root)

        if self._settings.install_steam:
            games.install_steam()

        Progress.get_instance().progress = 0.65
        
        if self._settings.install_firefox:
            internet.install_firefox()

        Progress.get_instance().progress = 0.68
        
        if self._settings.install_qbittorrent:
            internet.install_qbittorrent()

        Progress.get_instance().progress = 0.7

        if self._settings.install_paru:
            sysutils.install_paru()

        Progress.get_instance().progress = 0.75
        
        if self._settings.install_obs:
            multimedia.install_obs()

        Progress.get_instance().progress = 0.78
        
        if self._settings.install_kdenlive:
            multimedia.install_kdenlive()

        Progress.get_instance().progress = 0.8
        
        if self._settings.install_gsr:
            multimedia.install_gsr()

        Progress.get_instance().progress = 0.81