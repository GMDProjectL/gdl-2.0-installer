from dataclasses import dataclass

@dataclass
class Settings():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            # user profile
            self.username = ""
            self.password = ""
            self.hostname = ""
            self.autoLoginEnabled = False

            # destination
            self.drive = ""
            self.partition_method = ""
            self.boot_partition = ""
            self.root_partition = ""

            # additional_tweaks
            self.install_steam = False
            self.install_firefox = False
            self.install_qbittorrent = False
            self.install_paru = False
            self.install_obs = False
            self.install_kdenlive = False
            self.install_gsr = False
            self.install_nvidia_drivers = False
            self.force_nvidia_pstate = False
            self.use_nobara_kernel = False
            self.install_libreoffice = False
            self.install_onlyoffice = False
            self.install_vscode = False
            self.install_devtools = False
            self.install_plasma_sdk = False
            self.install_qt_creator = False
            self._initialized = True

    @classmethod
    def get_instance(cls) -> 'Settings':
        if cls._instance is None:
            cls()
        
        return cls._instance