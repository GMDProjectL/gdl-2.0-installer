import os
import subprocess
from installation.process_utils import ProcessUtils
from storage.logs import Logs

class Mounts(ProcessUtils):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Mounts, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
    
    @classmethod
    def get_instance(cls) -> 'Mounts':
        if cls._instance is None:
            cls()
        
        return cls._instance
    
    def mount(self, blk_name: str, target: str): 
        run_result = self.run_command(['mount', '-m', f'/dev/{blk_name}', target])

        if run_result[0] != 0:
            return False
        
        return True
    
    def unmount(self, blk_name: str): 
        run_result = self.run_command(['umount', '-Alf', f'/dev/{blk_name}'])

        if run_result[0] != 0:
            return False
        
        return True
    
    def get_mounts(self, disk_name: str):            
        run_result = self.run_command(['lsblk', '-l', '-n', '-a', '-o', 'NAME,SIZE,MOUNTPOINT', f'/dev/{disk_name}'])

        if run_result[0] != 0:
            return False

        output = str(run_result[1])
        data = []
        
        for line in output.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                name = parts[0].replace('/dev/', '').strip()
                size = parts[1].strip()
                mountpoint = parts[2].strip() if len(parts) > 2 else ''
                
                if name.startswith(disk_name) and name != disk_name:
                    data.append({
                        'name': name,
                        'size': size,
                        'mountpoint': mountpoint
                    })
        return data