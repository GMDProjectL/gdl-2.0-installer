import time
import urllib.request
from PySide6.QtCore import Signal, QThread

class ConnectivityCheckerThread(QThread):
    statusUpdated = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.running = True

    def run(self):
        while self.running:
            is_available = self.check_connectivity()
            self.statusUpdated.emit(is_available)
            time.sleep(5)

    def check_connectivity(self):
        urls = ['https://archlinux.org', 'https://github.com']
        for url in urls:
            try:
                urllib.request.urlopen(url, timeout=5)
                return True
            except:
                continue
        return False

    def stop(self):
        self.running = False
        self.wait()