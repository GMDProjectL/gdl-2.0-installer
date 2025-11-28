from installation.pacman import Pacman
from .tweakbase import TweakBase

class SystemUtils(TweakBase):
    def install_paru(self):
        return Pacman.get_instance().install_packages(self._root, ['paru'])[0] == 0
