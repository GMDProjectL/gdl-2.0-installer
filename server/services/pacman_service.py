import os
import subprocess
from installation.process_utils import ProcessUtils
from storage.logs import Logs

class PacmanService:
    def __init__(self, process_utils: ProcessUtils):
        self.process_utils = process_utils

    def init_keys(self, root: str):
        return self.process_utils.run_command_in_chroot(['pacman-key', '--init'], root)

    def update_all_packages(self, root: str):
        return self.process_utils.run_command_in_chroot(['pacman', '-Syu', '--noconfirm'], root)

    def install_packages(self, root: str, packages: list[str]):
        return self.process_utils.run_command_in_chroot(['pacman', '-S', '--noconfirm'] + packages, root)

    def remove_packages(self, root: str, packages: list[str]):
        return self.process_utils.run_command_in_chroot(['pacman', '-R', '--noconfirm'] + packages, root)

    def build_and_install_aur_packages(self, root: str, packages: list[str]):
        return self.process_utils.run_command_in_chroot(['yay', '-S', '--noconfirm'] + packages, root)
