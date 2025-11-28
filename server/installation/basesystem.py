import os
import re
import subprocess
from typing import Iterator, Dict, Any, List, Optional
from storage.logs import Logs
from storage.progress import Progress

class Basesystem:
    _instance: Optional['Basesystem'] = None
    
    _TOTAL_SIZE_REGEX = re.compile(r"total size is\s+([0-9,]+)") 

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Basesystem, cls).__new__(cls)
            cls._instance._initialized = False 

        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized') or not self._initialized:
            self._initialized = True
            self.total_bytes_to_copy: int = 0
            self.accumulated_bytes: int = 0

    @classmethod
    def get_instance(cls) -> 'Basesystem':
        if cls._instance is None:
            cls()
        
        return cls._instance
    
    # --- rsync Utilities ---

    def _parse_size_string(self, size_str: str) -> int:
        """Helper to convert size string ('1,234,567') to int."""
        try:
            return int(size_str.replace(',', '').strip())
        except ValueError:
            return 0

    def rsync_dry_run_total_size(self, source: str, destination: str, options: List[str] = None) -> int:
        options = options or ['-avn']
        command = ['rsync'] + options + [source, destination]

        try:
            Logs.add_log(f"Starting rsync dry-run for size estimation: {' '.join(command)}")
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8',
                timeout=30
            )
            
            output = result.stdout + result.stderr
            match = self._TOTAL_SIZE_REGEX.search(output)
            
            if match:
                total_size_bytes = self._parse_size_string(match.group(1))
                Logs.add_log(f"rsync dry-run successful. Total size: {total_size_bytes} bytes.")
                return total_size_bytes
            
            Logs.add_log("Warning: rsync dry-run did not report 'Total size' in expected format.")
            return 0
                
        except subprocess.CalledProcessError as e:
            error_msg = f"rsync dry-run error ({e.returncode}): {e.stderr.strip()}"
            Logs.add_log(error_msg)
            print(error_msg)
            return 0
        except (TimeoutError, Exception) as e:
            error_msg = f"Unexpected error during rsync dry-run: {type(e).__name__}: {e}"
            Logs.add_log(error_msg)
            print(error_msg)
            return 0

    def rsync_with_progress(self, source: str, destination: str, options: List[str] = None) -> Iterator[Dict[str, Any]]:
        options = options or ['-a', '--info=progress2']
        command = ['rsync'] + options + [source, destination]
        
        self.accumulated_bytes = 0 

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                bufsize=1, 
                encoding='utf-8' 
            )
            
            Logs.add_log(f"Starting rsync data transfer: {' '.join(command)}")

            for line in process.stdout:
                stripped_line = line.strip()

                if '%' in stripped_line:
                    try:
                        parts = stripped_line.split()

                        if len(parts) < 4:
                            yield {'type': 'message', 'content': stripped_line}
                            continue
                        
                        bytes_transferred_raw = parts[0]
                        percent_str = parts[1].replace('%', '')
                        speed = parts[2]
                        eta = parts[3]

                        current_bytes = self._parse_size_string(bytes_transferred_raw)
                        percent = int(percent_str)

                        self.accumulated_bytes = max(self.accumulated_bytes, current_bytes)
                        
                        # Parsing optional xfr/to-chk info
                        xfr, to_chk = "", ""
                        if len(parts) > 4:
                            raw_info = " ".join(parts[4:]).strip('()')
                            info_segments = [s.strip() for s in raw_info.split(',')]
                            
                            if len(info_segments) > 0:
                                xfr = info_segments[0]
                            if len(info_segments) > 1:
                                to_chk = info_segments[1]

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

                    except (ValueError, IndexError):
                        # Catch unexpected progress line format
                        yield {'type': 'message', 'content': stripped_line}
                else:
                    if stripped_line:
                        yield {'type': 'message', 'content': stripped_line}

            process.wait()

            if process.returncode != 0:
                stderr_output = process.stderr.read()
                error_message = f"rsync exited with error code {process.returncode}: {stderr_output.strip()}"
                Logs.add_log(f"Error: {error_message}")
                yield {'type': 'error', 'message': error_message}
            else:
                if self.total_bytes_to_copy > 0:
                     self.accumulated_bytes = self.total_bytes_to_copy
                
                Logs.add_log("rsync operation completed successfully.")
                yield {'type': 'completed', 'message': "rsync operation completed successfully."}
        
        except Exception as e:
            error_message = f"An unexpected error occurred during rsync: {type(e).__name__}: {e}"
            Logs.add_log(f"Error: {error_message}")
            yield {'type': 'error', 'message': error_message}
        
        finally:
            if 'process' in locals():
                if process.stdout:
                    process.stdout.close()
                if process.stderr:
                    process.stderr.close()
                

    def copy_system_to_root(self, from_dir: str, root: str) -> bool:
        
        EXCEPTIONS = [
            "/dev/*", "/proc/*", "/sys/*",
            "/tmp/*", "/run/*","/mnt/*", 
            "/media/*","/lost+found","/etc/fstab",
            "/home/*","/boot/*", "/var/lib/libvirt/*", 
            "/var/cache/*", "/var/lib/systemd/coredump/*"]
        
        flags_for_exceptions = [f'--exclude={x}' for x in EXCEPTIONS]
        rsync_options = ['-a', '--info=progress2'] + flags_for_exceptions
        final_progress_number = 0.3
        
        source_path = from_dir.rstrip('/') + '/'
        dest_path = root.rstrip('/') + '/'
        
        print("Starting rsync dry-run for size estimation...")
        self.total_bytes_to_copy = self.rsync_dry_run_total_size(
            source_path,
            dest_path, 
            options=['-avn'] + flags_for_exceptions
        )
        
        if self.total_bytes_to_copy == 0:
            print("WARNING: Could not determine total size. Progress will be based on percent.")
        
        self.accumulated_bytes = 0 
        print("Starting rsync data transfer...")
        
        for update in self.rsync_with_progress(source_path, dest_path, rsync_options):
            
            update_type = update['type']

            if update_type == 'progress':
                
                if self.total_bytes_to_copy > 0:
                    progress_ratio = update['current_bytes_total'] / self.total_bytes_to_copy
                else:
                    progress_ratio = update['percent'] / 100.0
                
                progress_ratio = min(progress_ratio, 1.0) 

                current_progress_update = progress_ratio * final_progress_number
                
                Progress.get_instance().progress = current_progress_update 
                
                print(
                    f"Progress: {progress_ratio*100:.2f}% "
                    f"({update['current_bytes_total']:,}/{self.total_bytes_to_copy:,} B) | "
                    f"Speed: {update['speed']} | ETA: {update['eta']}"
                )
                continue

            if update_type == 'error':
                Logs.add_log(f"Error: {update['message']}")
                print(f"Error: {update['message']}")
                return False

            if update_type == 'message' and update['content'].strip():
                print(f"rsync message: {update['content']}")
            
            elif update_type == 'completed':
                print(update['message'])
                # Set final progress for this operation
                Progress.get_instance().progress = final_progress_number
                
        Logs.add_log("Done copying base system!")
        
        return True

    def remove_autologin(self, root: str) -> bool:
        path = os.path.join(root, 'etc', 'sddm.conf.d', 'autologin.conf')
        if not os.path.exists(path):
            Logs.add_log(f"Autologin file not found (ok): {path}")
            return True 
        
        try:
            os.remove(path)
            Logs.add_log(f"Removed autologin file: {path}")
            print(f"Removed autologin file: {path}")
            return True
        except OSError as e:
            Logs.add_log(f"Failed to remove autologin file {path}: {e}")
            print(f"Failed to remove autologin file {path}: {e}")
            return False