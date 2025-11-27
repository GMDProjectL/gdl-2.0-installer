from PySide6.QtCore import QObject, Property, Signal, Slot, QThread

class InstallationProcessBackend(QObject):
    logsChanged = Signal()
    progressChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._installation_logs = "Installation logs go here..."
        self._progress = 0.1
    
    @Property(str, notify=logsChanged)
    def installationLogs(self):
        return self._installation_logs
    
    @Slot(str)
    def on_new_log(self, logs):
        self._installation_logs + '\n' + logs
        self.logsChanged.emit()
    
    @Property(float, notify=progressChanged)
    def progress(self):
        return self._progress
    
    @Slot(float)
    def on_new_progress(self, prog):
        if self._progress < prog:
            self._progress = prog
            self.logsChanged.emit()