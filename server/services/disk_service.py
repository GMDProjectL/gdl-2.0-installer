import subprocess
from utils.singleton import Singleton
from installation.process_utils import ProcessUtils
from storage.logs import Logs

class DiskService:
    def __init__(self, process_utils: ProcessUtils):
        self.process_utils = process_utils

    def format_ext4(self, blk_name: str):
        run_result = self.process_utils.run_command(['mkfs.ext4', f'/dev/{blk_name}'])

        if run_result[0] != 0:
            return False

        return True
