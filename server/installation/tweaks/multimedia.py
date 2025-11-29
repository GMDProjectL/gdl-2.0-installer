from .tweakbase import TweakBase

class Multimedia(TweakBase):
    def install_gsr(self):
        return self._pacman_service.install_packages(self._root, ['gpu-screen-recorder-ui'])[0] == 0

    def install_obs(self):
        return self._pacman_service.install_packages(self._root, ['obs-studio'])[0] == 0

    def install_kdenlive(self):
        return self._pacman_service.install_packages(self._root, ['kdenlive'])[0] == 0
