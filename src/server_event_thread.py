import time
import requests
from PySide6.QtCore import Signal, QThread

class ServerEventThread(QThread):
    logsChanged = Signal(str)
    progressChanged = Signal(float)
    stageChanged = Signal(int)
    error = Signal(str)
    success = Signal()

    def __init__(self, local_server_url: str):
        super().__init__()
        self._local_server_url = local_server_url
        self._loop_active = True
    
    def stop_checking_loop(self):
        self._loop_active = False
    
    def run(self):
        while self._loop_active:
            logs_request = requests.get(self._local_server_url + '/logs')
            for log_string in logs_request.json():
                self.logsChanged.emit(log_string)

            stage_request = requests.get(self._local_server_url + '/stage')
            self.stageChanged.emit(stage_request.json()['stage'])

            progress_request = requests.get(self._local_server_url + '/progress')
            self.progressChanged.emit(progress_request.json()['progress'])

            result_request = requests.get(self._local_server_url + '/result')

            if result_request.json()['error']:
                self.error.emit(result_request.json()['message'])
                self.stop_checking_loop()

            if result_request.json()['success']:
                self.success.emit()
                self.stop_checking_loop()
            
            time.sleep(0.7)