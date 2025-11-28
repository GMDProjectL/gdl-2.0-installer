import os
import re
import subprocess
from installation.process_utils import ProcessUtils
from storage.logs import Logs
from storage.progress import Progress
from storage.result import Result

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
    
    def rsync_with_progress(self, source: str, destination: str, options: list[str] = None):
        if options is None:
            options = ['-ah', '--info=progress2']

        command = ['rsync'] + options + [source, destination]

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1
            )
            progress_pattern = re.compile(
                r'^\s*(?P<bytes_transferred>[\d,\.]+)\s+(?P<percent>\d+)%\s+'
                r'(?P<speed>[\d\.]+ ?[KMGT]?B/s)\s+(?P<eta>\d+:\d+:\d+|\d+:\d{2})\s+'
                r'\((?P<xfr>xfr#\d+),\s*(?P<to_chk>to-chk=\d+/\d+)\)$'
            )

            for line in process.stdout:
                match = progress_pattern.match(line.strip())
                if match:
                    yield {
                        'type': 'progress',
                        'bytes_transferred': match.group('bytes_transferred'),
                        'percent': int(match.group('percent')),
                        'speed': match.group('speed'),
                        'eta': match.group('eta'),
                        'xfr': match.group('xfr'),
                        'to_chk': match.group('to_chk')
                    }
                else:
                    yield {'type': 'message', 'content': line.strip()}

            process.wait()

            if process.returncode != 0:
                stderr_output = process.stderr.read()
                yield {'type': 'error', 'message': f"rsync exited with error code {process.returncode}: {stderr_output.strip()}"}
            else:
                yield {'type': 'completed', 'message': "rsync operation completed successfully."}
        except Exception as e:
            yield {'type': 'error', 'message': f"An unexpected error occurred: {e}"}

    def copy_system_to_root(self, from_dir: str, root: str):
        exceptions = [
            "/dev/*", "/proc/*", "/sys/*",
            "/tmp/*", "/run/*","/mnt/*", 
            "/media/*","/lost+found","/etc/fstab",
            "/home/*","/boot/*", "/var/lib/libvirt/*", 
            "/var/cache/*", "/var/lib/systemd/coredump/*"]
        
        flags_for_exceptions = map(lambda x: '--exclude='+x, exceptions)

        final_progress_number = 0.3
        
        for update in self.rsync_with_progress(from_dir, root + '/', ['-ah', '--info=progress2'] + flags_for_exceptions):
            if update['type'] == 'progress':
                Progress.get_instance().progress = (update['percent'] / 100) * final_progress_number
                print(f"Progress: {update['percent']}% | Speed: {update['speed']} | ETA: {update['eta']}")

            elif update['type'] == 'message':
                print(f"rsync message: {update['content']}")

            elif update['type'] == 'error':
                Logs.add_log(f"Error: {update['message']}")
                print(f"Error: {update['message']}")
                return False

            elif update['type'] == 'completed':
                print(update['message'])

        return True

    def remove_autologin(self, root: str):
        path = root + '/etc/sddm.conf.d/autologin.conf'
        if os.path.exists(path):
            os.remove(path)