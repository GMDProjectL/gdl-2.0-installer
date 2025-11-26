from PySide6.QtCore import QObject, Property, Signal

class AdditionalTweaksBackend(QObject):
    installSteamChanged = Signal()
    installFirefoxChanged = Signal()
    installParuChanged = Signal()
    installObsChanged = Signal()
    installKdenliveChanged = Signal()
    installGpuRecorderChanged = Signal()
    installNvidiaChanged = Signal()
    forceNvidiaPerfChanged = Signal()
    useNobaraKernelChanged = Signal()
    installVscodeChanged = Signal()
    installLibreOfficeChanged = Signal()
    installOnlyOfficeChanged = Signal()
    installDevToolsChanged = Signal()
    installPlasmaSdkChanged = Signal()
    installQtCreatorChanged = Signal()
    installQBitTorrentChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._installSteam = False
        self._installFirefox = False
        self._installParu = False
        self._installObs = False
        self._installKdenlive = False
        self._installGpuRecorder = False
        self._installNvidia = False
        self._forceNvidiaPerf = False
        self._useNobaraKernel = False
        self._installVscode = False
        self._installLibreOffice = False
        self._installOnlyOffice = False
        self._installDevTools = False
        self._installPlasmaSdk = False
        self._installQtCreator = False
        self._installQBitTorrent = False

    # steam
    @Property(bool, notify=installSteamChanged)
    def installSteam(self):
        return self._installSteam

    @installSteam.setter
    def installSteam(self, value):
        if self._installSteam != value:
            self._installSteam = value
            self.installSteamChanged.emit()

    # firefox
    @Property(bool, notify=installFirefoxChanged)
    def installFirefox(self):
        return self._installFirefox

    @installFirefox.setter
    def installFirefox(self, value):
        if self._installFirefox != value:
            self._installFirefox = value
            self.installFirefoxChanged.emit()

    # paru
    @Property(bool, notify=installParuChanged)
    def installParu(self):
        return self._installParu

    @installParu.setter
    def installParu(self, value):
        if self._installParu != value:
            self._installParu = value
            self.installParuChanged.emit()
            
    # obs
    @Property(bool, notify=installObsChanged)
    def installObs(self):
        return self._installObs

    @installObs.setter
    def installObs(self, value):
        if self._installObs != value:
            self._installObs = value
            self.installObsChanged.emit()
            
    # kdenlive
    @Property(bool, notify=installKdenliveChanged)
    def installKdenlive(self):
        return self._installKdenlive

    @installKdenlive.setter
    def installKdenlive(self, value):
        if self._installKdenlive != value:
            self._installKdenlive = value
            self.installKdenliveChanged.emit()

    # gsr
    @Property(bool, notify=installGpuRecorderChanged)
    def installGpuRecorder(self):
        return self._installGpuRecorder

    @installGpuRecorder.setter
    def installGpuRecorder(self, value):
        if self._installGpuRecorder != value:
            self._installGpuRecorder = value
            self.installGpuRecorderChanged.emit()

    # nvidia
    @Property(bool, notify=installNvidiaChanged)
    def installNvidia(self):
        return self._installNvidia

    @installNvidia.setter
    def installNvidia(self, value):
        if self._installNvidia != value:
            self._installNvidia = value
            self.installNvidiaChanged.emit()
            
    # nvidia pm
    @Property(bool, notify=forceNvidiaPerfChanged)
    def forceNvidiaPerf(self):
        return self._forceNvidiaPerf

    @forceNvidiaPerf.setter
    def forceNvidiaPerf(self, value):
        if self._forceNvidiaPerf != value:
            self._forceNvidiaPerf = value
            self.forceNvidiaPerfChanged.emit()

    # nobara
    @Property(bool, notify=useNobaraKernelChanged)
    def useNobaraKernel(self):
        return self._useNobaraKernel

    @useNobaraKernel.setter
    def useNobaraKernel(self, value):
        if self._useNobaraKernel != value:
            self._useNobaraKernel = value
            self.useNobaraKernelChanged.emit()

    # vscode
    @Property(bool, notify=installVscodeChanged)
    def installVscode(self):
        return self._installVscode

    @installVscode.setter
    def installVscode(self, value):
        if self._installVscode != value:
            self._installVscode = value
            self.installVscodeChanged.emit()
            
    # libreoffice
    @Property(bool, notify=installLibreOfficeChanged)
    def installLibreOffice(self):
        return self._installLibreOffice

    @installLibreOffice.setter
    def installLibreOffice(self, value):
        if self._installLibreOffice != value:
            self._installLibreOffice = value
            self.installLibreOfficeChanged.emit()

    # onlyoffice
    @Property(bool, notify=installOnlyOfficeChanged)
    def installOnlyOffice(self):
        return self._installOnlyOffice

    @installOnlyOffice.setter
    def installOnlyOffice(self, value):
        if self._installOnlyOffice != value:
            self._installOnlyOffice = value
            self.installOnlyOfficeChanged.emit()
            
    # devtools
    @Property(bool, notify=installDevToolsChanged)
    def installDevTools(self):
        return self._installDevTools

    @installDevTools.setter
    def installDevTools(self, value):
        if self._installDevTools != value:
            self._installDevTools = value
            self.installDevToolsChanged.emit()

    # plasma-sdk
    @Property(bool, notify=installPlasmaSdkChanged)
    def installPlasmaSdk(self):
        return self._installPlasmaSdk

    @installPlasmaSdk.setter
    def installPlasmaSdk(self, value):
        if self._installPlasmaSdk != value:
            self._installPlasmaSdk = value
            self.installPlasmaSdkChanged.emit()
            
    # qc
    @Property(bool, notify=installQtCreatorChanged)
    def installQtCreator(self):
        return self._installQtCreator

    @installQtCreator.setter
    def installQtCreator(self, value):
        if self._installQtCreator != value:
            self._installQtCreator = value
            self.installQtCreatorChanged.emit()

    # qbt
    @Property(bool, notify=installQBitTorrentChanged)
    def installQBitTorrent(self):
        return self._installQBitTorrent

    @installQBitTorrent.setter
    def installQBitTorrent(self, value):
        if self._installQBitTorrent != value:
            self._installQBitTorrent = value
            self.installQBitTorrentChanged.emit()