from installation.pacman import Pacman
from .tweakbase import TweakBase

class Games(TweakBase):
    def install_steam(self):
        return Pacman.get_instance().install_packages(
            self._root, 
            ['steam', 'lib32-vulkan-intel', 'lib32-vulkan-radeon', 'lib32-vulkan-mesa-layers']
        )[0] == 0