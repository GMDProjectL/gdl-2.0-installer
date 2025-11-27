import os
import subprocess
from installation.process_utils import ProcessUtils
from storage.logs import Logs

class Disks(ProcessUtils):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Disks, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
    
    @classmethod
    def get_instance(cls) -> 'Disks':
        if cls._instance is None:
            cls()
        
        return cls._instance
    
    def format_ext4(self, blk_name: str):
        run_result = self.run_command(['mkfs.ext4', f'/dev/{blk_name}'])

        if run_result[0] != 0:
            return False

        return True