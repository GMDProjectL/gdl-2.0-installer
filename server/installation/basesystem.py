import os
import subprocess
from installation.process_utils import ProcessUtils
from storage.logs import Logs

class Basesystem(ProcessUtils):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Basesystem, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
    
    @classmethod
    def get_instance(cls) -> 'Basesystem':
        if cls._instance is None:
            cls()
        
        return cls._instance
    
    def rsync(self, excludes: list[str], source: str, destination: str, dry_run = False):
        command = ['rsync', '-aAXv']

        for exclude in excludes:
            command.append(f'--exclude={exclude}')

        command.extend([source, destination])

        if dry_run:
            command.append('--dry-run')

        run_result = self.run_command(command)

        if run_result[0] != 0:
            return False

        return True
    
    def copy_system_to_root(self, from_dir: str, root: str):
        return self.rsync(
            [
                "/dev/*", "/proc/*", "/sys/*",
                "/tmp/*", "/run/*","/mnt/*", 
                "/media/*","/lost+found","/etc/fstab",
                "/home/*","/boot/*", "/var/lib/libvirt/*", 
                "/var/cache/*", "/var/lib/systemd/coredump/*"], 
            from_dir, root + '/'
        )

    def remove_autologin(self, root: str):
        path = root + '/etc/sddm.conf.d/autologin.conf'
        if os.path.exists(path):
            os.remove(path)