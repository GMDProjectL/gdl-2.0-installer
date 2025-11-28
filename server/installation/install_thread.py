from installation.basesystem import Basesystem
from storage.settings import Settings
from storage.logs import Logs
from storage.stage import Stage
from storage.result import Result
from storage.progress import Progress
from installation.mounts import Mounts
from installation.disks import Disks
from installation.configuration import Configuration
from installation.process_utils import ProcessUtils
from installation.pacman import Pacman
from installation.tweaks.tweaks import Tweaks
import os
import threading

class InstallThread():
    def __init__(self, settings: Settings):
        super().__init__()
        self.settings = settings
        self.basesystem = Basesystem()

    def run(self):
        mounts = Mounts.get_instance()
        mountpoints = mounts.get_mounts(self.settings.drive)
        system_source = os.getenv("CUSTOM_SYSTEM_SOURCE", "/run/archiso/airootfs")
        boot_source = os.getenv("CUSTOM_SYSTEM_SOURCE", "/run/archiso/bootmnt/arch/boot/x86_64")

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
        
        configuration = Configuration().get_instance()
        configuration.set_settings(boot_source, root_mountpoint)

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
        
        if not self.basesystem.copy_system_to_root(system_source, root_mountpoint):
            Result.get_instance().error = True
            Result.get_instance().message = 'Failed to copy base system.'
            return
        
        Stage.get_instance().stage = 1
        
        self.basesystem.remove_autologin(root_mountpoint)

        if not configuration.copy_boot_files():
            Result.get_instance().error = True
            Result.get_instance().message = 'Failed to copy boot files.'
            return
        
        Progress.get_instance().progress = 0.33

        if not configuration.remove_archiso_mkinitcpio_conf():
            Result.get_instance().error = True
            Result.get_instance().message = 'Failed to remove archiso mkinitcpio conf.'
            return
        
        Progress.get_instance().progress = 0.35

        if not configuration.copy_linux_mkinitcpio_preset():
            Result.get_instance().error = True
            Result.get_instance().message = 'Failed to copy mkinitcpio linux preset.'
            return
        
        Progress.get_instance().progress = 0.4

        if not configuration.genfstab():
            Result.get_instance().error = True
            Result.get_instance().message = 'Failed to generate fstab.'
            return
        
        Progress.get_instance().progress = 0.42

        if not configuration.fix_vconsole():
            Result.get_instance().error = True
            Result.get_instance().message = 'Failed to fix vconsole.'
            return
        
        Progress.get_instance().progress = 0.45

        if not configuration.mkinitcpio():
            Result.get_instance().error = True
            Result.get_instance().message = 'Failed to generate ramdisk.'
            return
        
        Progress.get_instance().progress = 0.47

        if not configuration.install_grub():
            Result.get_instance().error = True
            Result.get_instance().message = 'Failed to install GRUB.'
            return
        
        Progress.get_instance().progress = 0.5

        if not configuration.generate_grub_config():
            Result.get_instance().error = True
            Result.get_instance().message = 'Failed to generate GRUB config.'
            return
        
        Progress.get_instance().progress = 0.52

        if not configuration.set_root_password(Settings.get_instance().password):
            Result.get_instance().error = True
            Result.get_instance().message = 'Failed to set root password.'
            return
        
        Progress.get_instance().progress = 0.55

        if not configuration.create_user(Settings.get_instance().username, Settings.get_instance().password):
            Result.get_instance().error = True
            Result.get_instance().message = 'Failed to set create user.'
            return
        
        Progress.get_instance().progress = 0.57

        if Settings.get_instance().auto_login_enabled:
            if not configuration.setup_autologin(Settings.get_instance().username):
                Result.get_instance().error = True
                Result.get_instance().message = 'Failed to setup autologin.'
                return

        if not configuration.set_hostname(Settings.get_instance().hostname):
            Result.get_instance().error = True
            Result.get_instance().message = 'Failed to set hostname.'
            return
        
        if not configuration.create_sudoers_file(Settings.get_instance().username):
            Result.get_instance().error = True
            Result.get_instance().message = 'Failed to create sudoers file.'
            return
        
        Progress.get_instance().progress = 0.6
        Stage.get_instance().stage = 2

        Logs.add_log('Updating Pacman database...')

        pacman = Pacman.get_instance()
        pacman.init_keys(root_mountpoint)

        Progress.get_instance().progress = 6.1

        pacman.update_all_packages(root_mountpoint)

        Progress.get_instance().progress = 6.3

        tweaks = Tweaks.get_instance()

        tweaks.apply_settings(Settings.get_instance(), root_mountpoint)
        tweaks.begin_features_installation()

        Logs.add_log('Done.')

        Progress.get_instance().progress = 1
        Stage.get_instance().stage = 3

        Result.get_instance().success = True
    
    def start(self):
        threading.Thread(target=self.run).start()