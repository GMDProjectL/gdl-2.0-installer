from src.user_profile_backend import UserProfileBackend
from src.drive_backend import DriveBackend
from src.translator_backend import TranslatorBackend
from src.translator_backend_wrapper import TranslatorBackendWrapper
from src.adaptive_image_provider import AdaptiveImageProvider

class GlobalInstallerState():
    _instance = None

    user_profile_backend: UserProfileBackend
    drive_backend: DriveBackend
    translator_backend: TranslatorBackend
    translator_backend_wrapper: TranslatorBackendWrapper
    adaptive_image_provider: AdaptiveImageProvider

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalInstallerState, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.user_profile_backend = UserProfileBackend()
            self.drive_backend = DriveBackend()
            self.translator_backend = TranslatorBackend()
            self.translator_backend_wrapper = TranslatorBackendWrapper()
            self.adaptive_image_provider = AdaptiveImageProvider()
            self._initialized = True
        
    @classmethod
    def get_instance(cls) -> 'GlobalInstallerState':
        if cls._instance is None:
            cls()
        
        return cls._instance