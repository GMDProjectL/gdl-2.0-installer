from src.user_profile_backend import UserProfileBackend
from src.drive_backend import DriveBackend
from src.translator_backend import TranslatorBackend
from src.translator_backend_wrapper import TranslatorBackendWrapper
from src.adaptive_image_provider import AdaptiveImageProvider
from src.additional_tweaks_backend import AdditionalTweaksBackend
from src.internet_checker_backend import InternetCheckerBackend
from src.installation_process_backend import InstallationProcessBackend

class GlobalInstallerState():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalInstallerState, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.local_server_url = 'http://127.0.0.1:5000'
            self.user_profile_backend = UserProfileBackend()
            self.drive_backend = DriveBackend()
            self.translator_backend = TranslatorBackend()
            self.translator_backend_wrapper = TranslatorBackendWrapper()
            self.adaptive_image_provider = AdaptiveImageProvider()
            self.additional_tweaks_backend = AdditionalTweaksBackend()
            self.internet_checker_backend = InternetCheckerBackend()
            self.installation_process_backend = InstallationProcessBackend(self.local_server_url, self)
            self._initialized = True
        
    @classmethod
    def get_instance(cls) -> 'GlobalInstallerState':
        if cls._instance is None:
            cls()
        
        return cls._instance