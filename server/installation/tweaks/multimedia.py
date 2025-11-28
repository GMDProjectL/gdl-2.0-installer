from installation.pacman import Pacman
from .tweakbase import TweakBase

class Multimedia(TweakBase):
    def install_gsr(self):
        return Pacman.get_instance().install_packages(self._root, ['gpu-screen-recorder-ui'])[0] == 0
    
    def install_obs(self):
        return Pacman.get_instance().install_packages(self._root, ['obs-studio'])[0] == 0

    def install_kdenlive(self):
        return Pacman.get_instance().install_packages(self._root, ['kdenlive'])[0] == 0
