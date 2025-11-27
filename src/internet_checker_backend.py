from PySide6.QtCore import QObject, Property, Signal, Slot
from src.connectivity_checker_thread import ConnectivityCheckerThread

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
