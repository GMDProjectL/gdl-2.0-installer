import select
import subprocess
import time
from storage.logs import Logs
from storage.result import Result 
import os
import fcntl

class ProcessUtils:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ProcessUtils, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
    
    @classmethod
    def get_instance(cls) -> 'ProcessUtils':
        if cls._instance is None:
            cls()
        
        return cls._instance
    
    def _set_non_blocking(self, stream):
        fd = stream.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
    
    def run_command_in_chroot(self, command: list, root: str) -> tuple[int, str, str]:
        '''
        Runs command with accurate stdout/stderr buffering in chroot.

        Returns a tuple(code, stdout, stderr), where stdout and stderr
        contain the full output as decoded strings.
        '''
        return self.run_command(['arch-chroot', root] + command)

    def run_command(self, command: list, cwd: str = None) -> tuple[int, str, str]:
        '''
        Runs command with accurate stdout/stderr buffering.

        Returns a tuple(code, stdout, stderr), where stdout and stderr
        contain the full output as decoded strings.
        '''

        Logs.add_log(f'Running command: {" ".join(command)}')
        
        res_instance = Result.get_instance()
        
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=cwd
            )
        except FileNotFoundError:
            error_message = f'Command not found: {command[0]}'
            Logs.add_log(error_message)

            res_instance.error = True
            res_instance.message = error_message

            return (-1, "", "Command not found")

        self._set_non_blocking(process.stdout)
        self._set_non_blocking(process.stderr)

        stdout_buffer = b''
        stderr_buffer = b''
        
        full_stdout = b''
        full_stderr = b''
        
        pipes = {
            process.stdout.fileno(): ('STDOUT', stdout_buffer),
            process.stderr.fileno(): ('STDERR', stderr_buffer)
        }
        
        last_log_time = time.time()

        while process.poll() is None or pipes:
            if pipes:
                rlist, _, _ = select.select(pipes.keys(), [], [], 0.1) 
            else:
                rlist = []

            current_time = time.time()
            if rlist or current_time - last_log_time >= 0.1: # throttling
                for fd in rlist:
                    stream_name, current_buffer_ref = pipes[fd]
                    pipe = process.stdout if stream_name == 'STDOUT' else process.stderr
                    
                    try:
                        chunk = pipe.read(1024)
                    except BlockingIOError:
                        chunk = b''
                    
                    if chunk:
                        current_buffer = current_buffer_ref + chunk
                        
                        if stream_name == 'STDOUT':
                            stdout_buffer = current_buffer
                            pipes[fd] = (stream_name, stdout_buffer)
                            full_stdout += chunk
                        else:
                            stderr_buffer = current_buffer
                            pipes[fd] = (stream_name, stderr_buffer)
                            full_stderr += chunk

                    if not chunk and process.poll() is not None:
                        del pipes[fd]
                        break
                
                if current_time - last_log_time >= 0.1:
                    if process.stdout.fileno() in pipes:
                        stream_name, current_buffer = pipes[process.stdout.fileno()]
                        lines = current_buffer.split(b'\n')
                        stdout_buffer = lines.pop()
                        pipes[process.stdout.fileno()] = (stream_name, stdout_buffer)
                        
                        for line_bytes in lines:
                            line = line_bytes.decode('utf-8', errors='replace').strip()
                            if line:
                                Logs.add_log(line)
                    
                    if process.stderr.fileno() in pipes:
                        stream_name, current_buffer = pipes[process.stderr.fileno()]
                        lines = current_buffer.split(b'\n')
                        stderr_buffer = lines.pop() # Оставляем неполную строку в буфере
                        pipes[process.stderr.fileno()] = (stream_name, stderr_buffer)
                        
                        for line_bytes in lines:
                            line = line_bytes.decode('utf-8', errors='replace').strip()
                            if line:
                                Logs.add_log('stderr: ' + line)

                    last_log_time = current_time

            if process.poll() is not None and not pipes:
                break
                
        def flush_buffer(buffer, stream_name):
            if buffer.strip():
                try:
                    line = buffer.decode('utf-8', errors='replace').strip()
                    if line:
                        if stream_name == 'STDOUT':
                            Logs.add_log(f'{line}')
                        else:
                            Logs.add_log('stderr: ' + line)
                except UnicodeDecodeError:
                    pass
        
        flush_buffer(stdout_buffer, 'STDOUT')
        flush_buffer(stderr_buffer, 'STDERR')

        return_code = process.wait()
        
        if return_code == 0:
            Logs.add_log(f'Command finished successfully. Return code: {return_code}')
        else:
            Logs.add_log(f'Command failed. Return code: {return_code}')
        
        final_stdout = full_stdout.decode('utf-8', errors='replace')
        final_stderr = full_stderr.decode('utf-8', errors='replace')
        
        return (return_code, final_stdout, final_stderr)