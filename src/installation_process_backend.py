from PySide6.QtCore import QObject, Property, Signal, Slot

class InstallationProcessBackend(QObject):
    logsChanged = Signal()
    progressChanged = Signal()
    stageChanged = Signal()
    error = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._installation_logs = "Installation logs go here..."
        self._progress = 0.25
        self._stage = 1

    @Slot()
    def giveTestError(self):
        self.error.emit("Test error")
    
    # logs
    @Property(str, notify=logsChanged)
    def installationLogs(self):
        return self._installation_logs
    
    @Slot(str)
    def on_new_log(self, logs):
        self._installation_logs + '\n' + logs
        self.logsChanged.emit()
    

    # progress bar
    @Property(float, notify=progressChanged)
    def progress(self):
        return self._progress
    
    @Slot(float)
    def on_new_progress(self, prog):
        if self._progress < prog:
            self._progress = prog
            self.logsChanged.emit()
    

    # stage highligts
    @Property(float, notify=stageChanged)
    def stage(self):
        return self._stage
    
    @Slot(float)
    def on_new_stage(self, stage):
        if self._stage < stage:
            self._stage = stage
            self.logsChanged.emit()