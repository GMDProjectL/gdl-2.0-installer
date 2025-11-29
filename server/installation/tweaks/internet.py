from installation.pacman import Pacman
from .tweakbase import TweakBase

class Internet(TweakBase):
    def install_firefox(self):
        pacman = Pacman.get_instance()

        if not pacman.remove_packages(self._root, ['chromium']):
            return False

        return pacman.install_packages(self._root, ['firefox'])[0] == 0
    
    def install_qbittorrent(self):
        return Pacman.get_instance().install_packages(self._root, ['qbittorrent'])[0] == 0