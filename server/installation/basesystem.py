import os
import re
import subprocess
from installation.process_utils import ProcessUtils
from storage.logs import Logs
from storage.progress import Progress
from storage.result import Result

class Basesystem(ProcessUtils):
    _instance = None
    _total_size_regex = re.compile(r"Total size is ([0-9,]+) bytes") 

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Basesystem, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.total_bytes_to_copy = 0
            self.accumulated_bytes = 0
    
    @classmethod
    def get_instance(cls) -> 'Basesystem':
        if cls._instance is None:
            cls()
        
        return cls._instance
    
    def rsync_dry_run_total_size(self, source: str, destination: str, options: list[str] = None) -> int:
        if options is None:
            options = ['-avn']
        
        command = ['rsync'] + options + [source, destination]

        try:
            Logs.add_log(f"Starting rsync dry-run for size estimation: {' '.join(command)}")
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )
            
            output = result.stdout + result.stderr
            
            match = self._total_size_regex.search(output)
            
            if match:
                total_size_str = match.group(1).replace(',', '')
                total_size_bytes = int(total_size_str)
                Logs.add_log(f"rsync dry-run successful. Total size: {total_size_bytes} bytes.")
                return total_size_bytes
            else:
                Logs.add_log("Error: rsync dry-run did not report 'Total size' in expected format.")
                return 0
                
        except subprocess.CalledProcessError as e:
            Logs.add_log(f"rsync dry-run error: {e.stderr.strip()}")
            print(f"rsync dry-run error: {e.stderr.strip()}")
            return 0
        except Exception as e:
            Logs.add_log(f"Unexpected error during rsync dry-run: {e}")
            print(f"Unexpected error during rsync dry-run: {e}")
            return 0


    def rsync_with_progress(self, source: str, destination: str, options: list[str] = None):
        if options is None:
            # --info=progress2 сообщает байты в первом поле
            options = ['-ah', '--info=progress2']

        command = ['rsync'] + options + [source, destination]

        last_bytes_transferred = 0

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1
            )

            for line in process.stdout:
                stripped_line = line.strip()

                if '%' in stripped_line and '(' in stripped_line and ')' in stripped_line:
                    try:
                        parts = stripped_line.split()

                        if len(parts) >= 6:
                            bytes_transferred_raw = parts[0] 
                            
                            percent_match = re.search(r'(\d+)\%', parts[1])
                            percent = int(percent_match.group(1)) if percent_match else 0
                            
                            speed = parts[2]
                            eta = parts[3]
                            
                            xfr_to_chk_raw = " ".join(parts[4:])
                            inner_content = xfr_to_chk_raw.strip('()')
                            inner_parts = [p.strip() for p in inner_content.split(',', 1)]
                            
                            try:
                                size_match = re.match(r"([\d\.]+)([KkMmGgTt]?)$", bytes_transferred_raw)
                                if size_match:
                                    value = float(size_match.group(1))
                                    unit = size_match.group(2).upper()
                                    
                                    unit_multipliers = {'': 1, 'K': 1024, 'M': 1048576, 'G': 1073741824, 'T': 1099511627776}
                                    current_bytes = int(value * unit_multipliers.get(unit, 1))
                                else:
                                    current_bytes = last_bytes_transferred
                            except (ValueError, IndexError):
                                current_bytes = last_bytes_transferred
                            
                            self.accumulated_bytes = max(self.accumulated_bytes, current_bytes)
                            last_bytes_transferred = self.accumulated_bytes

                            if len(inner_parts) == 2:
                                xfr = inner_parts[0]
                                to_chk = inner_parts[1]

                                yield {
                                    'type': 'progress',
                                    'bytes_transferred': bytes_transferred_raw,
                                    'current_bytes_total': self.accumulated_bytes,
                                    'percent': percent,
                                    'speed': speed,
                                    'eta': eta,
                                    'xfr': xfr,
                                    'to_chk': to_chk
                                }
                            else:
                                yield {'type': 'message', 'content': stripped_line}
                        else:
                            yield {'type': 'message', 'content': stripped_line}
                    except (ValueError, IndexError):
                        yield {'type': 'message', 'content': stripped_line}
                else:
                    yield {'type': 'message', 'content': stripped_line}

            process.wait()

            if process.returncode != 0:
                stderr_output = process.stderr.read()
                yield {'type': 'error', 'message': f"rsync exited with error code {process.returncode}: {stderr_output.strip()}"}
            else:
                if self.total_bytes_to_copy > 0:
                     self.accumulated_bytes = self.total_bytes_to_copy
                
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
        
        flags_for_exceptions = list(map(lambda x: '--exclude='+x, exceptions))
        rsync_options = ['-a', '--info=progress2'] + flags_for_exceptions
        final_progress_number = 0.3
        
        # 1. ФАЗА ОЦЕНКИ (DRY-RUN)
        print("Starting rsync dry-run for size estimation...")
        self.total_bytes_to_copy = self.rsync_dry_run_total_size(
            from_dir + '/',
            root + '/', 
            options=['-avn'] + flags_for_exceptions
        )
        
        if self.total_bytes_to_copy == 0:
            print("WARNING: Could not determine total size. Progress will be based on unstable file count.")
        
        self.accumulated_bytes = 0 
        
        print("Starting rsync data transfer...")
        
        for update in self.rsync_with_progress(from_dir + '/', root + '/', rsync_options):
            if update['type'] == 'progress':
                
                if self.total_bytes_to_copy > 0:
                    progress_ratio = update['current_bytes_total'] / self.total_bytes_to_copy
                else:
                    progress_ratio = update['percent'] / 100.0
                
                current_progress_update = progress_ratio * final_progress_number
                
                current_total_progress = Progress.get_instance().progress
                
                Progress.get_instance().progress = max(current_total_progress, current_progress_update)
                
                print(f"Progress: {progress_ratio*100:.2f}% ({update['current_bytes_total']}/{self.total_bytes_to_copy} B) | Speed: {update['speed']} | ETA: {update['eta']}")

            elif update['type'] == 'message':
                print(f"rsync message: {update['content']}")

            elif update['type'] == 'error':
                Logs.add_log(f"Error: {update['message']}")
                print(f"Error: {update['message']}")
                return False

            elif update['type'] == 'completed':
                Progress.get_instance().progress = current_total_progress + final_progress_number 
                print(update['message'])

        print("rsync done")
        return True

    def remove_autologin(self, root: str):
        path = root + '/etc/sddm.conf.d/autologin.conf'
        if os.path.exists(path):
            os.remove(path)