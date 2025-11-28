import os
import subprocess
from installation.process_utils import ProcessUtils
from storage.logs import Logs

class Pacman(ProcessUtils):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Pacman, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
    
    @classmethod
    def get_instance(cls) -> 'Pacman':
        if cls._instance is None:
            cls()
            
        return cls._instance
    
    def init_keys(self, root: str):
        return self.run_command_in_chroot(['pacman-key', '--init'], root)
    
    def update_all_packages(self, root: str):
        return self.run_command_in_chroot(['pacman', '-Syu'], root)
    
    def install_packages(self, root: str, packages: list[str]):
        return self.run_command_in_chroot(['pacman', '-S'] + packages, root)
    
    def remove_packages(self, root: str, packages: list[str]):
        return self.run_command_in_chroot(['pacman', '-R'] + packages, root)
    
    def build_and_install_aur_packages(self, root: str, packages: list[str]):
        return self.run_command_in_chroot(['yay', '-S'] + packages, root)