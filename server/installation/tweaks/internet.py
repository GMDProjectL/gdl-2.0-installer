from .tweakbase import TweakBase

class Internet(TweakBase):
    def install_firefox(self):
        if not self._pacman_service.remove_packages(self._root, ['chromium']):
            return False

        return self._pacman_service.install_packages(self._root, ['firefox'])[0] == 0

    def install_qbittorrent(self):
        return self._pacman_service.install_packages(self._root, ['qbittorrent'])[0] == 0
