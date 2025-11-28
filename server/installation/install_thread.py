from installation.basesystem import Basesystem
from storage.settings import Settings
from storage.logs import Logs
from storage.result import Result
from installation.mounts import Mounts
from installation.disks import Disks
from installation.process_utils import ProcessUtils
import time
import threading

class InstallThread():
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self.basesystem = Basesystem()

    def run(self):
        mounts = Mounts.get_instance()
        mountpoints = mounts.get_mounts(self.settings.drive)

        if mountpoints == False:
            Result.get_instance().error = True
            Result.get_instance().message = 'Failed to get mountpoints.'
            return
        
        root_mountpoint = '/mnt'
        boot_mountpoint = '/mnt/boot/efi'

        for point in mountpoints:
            if point['name'] == self.settings.boot_partition and point["mountpoint"].strip() != '':
                mounts.unmount(self.settings.boot_partition)

        for point in mountpoints:
            if point['name'] == self.settings.root_partition and point["mountpoint"].strip() != '':
                mounts.unmount(self.settings.root_partition)
        

        if not Disks.get_instance().format_ext4(self.settings.root_partition):
            Result.get_instance().error = True
            Result.get_instance().message = 'Failed to format root partition.'
            return
    
        if not mounts.mount(self.settings.root_partition, root_mountpoint):
            Result.get_instance().error = True
            Result.get_instance().message = 'Failed to mount root.'
            return
        
        if not mounts.mount(self.settings.boot_partition, boot_mountpoint):
            Result.get_instance().error = True
            Result.get_instance().message = 'Failed to mount boot partition.'
            return
        
        if not self.basesystem.copy_system_to_root('/', root_mountpoint):
            Result.get_instance().error = True
            Result.get_instance().message = 'Failed to copy base system.'
            return
        
        self.basesystem.remove_autologin(root_mountpoint)

        

    
    def start(self):
        threading.Thread(target=self.run).start()