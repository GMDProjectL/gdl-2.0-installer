import time
import urllib.request
from PySide6.QtCore import QObject, Property, Signal, Slot, QThread

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

class InternetCheckerBackend(QObject):
    internetStatusChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_internet_available = False
        self.thread = ConnectivityCheckerThread()
        self.thread.statusUpdated.connect(self.on_status_updated)
        self.thread.start()
    
    @Property(bool, notify=internetStatusChanged)
    def isInternetAvailable(self):
        return self._is_internet_available

    @Slot(bool)
    def on_status_updated(self, is_available):
        if self._is_internet_available != is_available:
            self._is_internet_available = is_available
            self.internetStatusChanged.emit()
