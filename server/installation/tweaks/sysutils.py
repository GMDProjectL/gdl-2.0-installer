from .tweakbase import TweakBase

class SystemUtils(TweakBase):
    def install_paru(self):
        return self._pacman_service.install_packages(self._root, ['paru'])[0] == 0
