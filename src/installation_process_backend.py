import os
import time
import requests
from PySide6.QtCore import QObject, Property, Signal, Slot, QThread

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
            
            time.sleep(2)

class InstallationProcessBackend(QObject):
    logsChanged = Signal()
    progressChanged = Signal()
    stageChanged = Signal()
    error = Signal(str)
    success = Signal()

    def __init__(self, local_server_url, installer_state, parent=None):
        super().__init__(parent)
        self._installer_state = installer_state
        self._installation_logs = "Installation logs go here..."
        self._progress = 0
        self._stage = 0

        self.server_event_thread = ServerEventThread(local_server_url)
        self.server_event_thread.logsChanged.connect(self.on_new_log)
        self.server_event_thread.progressChanged.connect(self.on_new_progress)
        self.server_event_thread.stageChanged.connect(self.on_new_stage)
        self.server_event_thread.error.connect(self.error)
        self.server_event_thread.success.connect(self.success)

    @Slot()
    def reboot(self):
        os.system('reboot')
    
    @Slot()
    def sendSettings(self):
        installer = self._installer_state
        user_profile = installer.user_profile_backend
        drive = installer.drive_backend
        tweaks = installer.additional_tweaks_backend

        if drive._partition_method_index == 0:
            self.error.emit('Automatic partitioning is not supported yet. Sorry.')
            return

        settings = {
            'username': user_profile._username,
            'password': user_profile._password,
            'hostname': user_profile._hostname,
            'auto_login_enabled': user_profile._autoLoginEnabled,
            'drive': drive._drives[drive._drive]['name'],
            'partition_method': 'automatic' if drive._partition_method_index == 0 else 'manual',
            'boot_partition': drive._partitions[drive._boot_partition_index]['name'],
            'root_partition': drive._partitions[drive._root_partition_index]['name'],
            'install_steam': tweaks._installSteam,
            'install_firefox': tweaks._installFirefox,
            'install_qbittorrent': tweaks._installQBitTorrent,
            'install_paru': tweaks._installParu,
            'install_obs': tweaks._installObs,
            'install_kdenlive': tweaks._installKdenlive,
            'install_gsr': tweaks._installGpuRecorder,
            'install_nvidia_drivers': tweaks._installNvidia,
            'force_nvidia_pstate': tweaks._forceNvidiaPerf,
            'use_nobara_kernel': tweaks._useNobaraKernel,
            'install_libreoffice': tweaks._installLibreOffice,
            'install_onlyoffice': tweaks._installOnlyOffice,
            'install_vscode': tweaks._installVscode,
            'install_devtools': tweaks._installDevTools,
            'install_plasma_sdk': tweaks._installPlasmaSdk,
            'install_qt_creator': tweaks._installQtCreator
        }

        r = requests.post(installer.local_server_url + '/apply_settings', json=settings)
        if r.json().get('error'):
            self.error.emit(r.json().get('message'))
            return
        
        self.server_event_thread.start()

    # logs
    @Property(str, notify=logsChanged)
    def installationLogs(self):
        return self._installation_logs
    
    @Slot(str)
    def on_new_log(self, logs):
        self._installation_logs += '\n' + logs
        self.logsChanged.emit()
    

    # progress bar
    @Property(float, notify=progressChanged)
    def progress(self):
        return self._progress
    
    @Slot(float)
    def on_new_progress(self, prog):
        if self._progress < prog:
            self._progress = prog
            self.progressChanged.emit()
    

    # stage highligts
    @Property(int, notify=stageChanged)
    def stage(self):
        return self._stage
    
    @Slot(int)
    def on_new_stage(self, stage):
        if self._stage != stage:
            self._stage = stage
            self.stageChanged.emit()