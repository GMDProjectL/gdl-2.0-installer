from installation.basesystem import BaseSystem
from storage.settings import Settings
from storage.logs import Logs
import time
import threading

class InstallThread():
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self.basesystem = BaseSystem()

    def run(self):
        Logs.add_log('Test log #1')
        time.sleep(5)
        Logs.add_log('Test log #2')
        time.sleep(5)
        Logs.add_log('Test log #3')
    
    def start(self):
        threading.Thread(target=self.run).start()