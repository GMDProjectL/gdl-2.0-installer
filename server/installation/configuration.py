import os
import shutil
import subprocess
from traceback import format_exc
from typing import Iterator, Dict, Any, List, Optional
from storage.logs import Logs
from storage.progress import Progress
from installation.process_utils import ProcessUtils

class Configuration:
    _instance: Optional['Configuration'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Configuration, cls).__new__(cls)
            cls._instance._initialized = False 

        return cls._instance

    def __init__(self, boot_files_location: str, root: str):
        if not hasattr(self, '_initialized') or not self._initialized:
            self._boot_files_location = boot_files_location
            self._root = root

            self._initialized = True

    @classmethod
    def get_instance(cls) -> 'Configuration':
        if cls._instance is None:
            cls()
        
        return cls._instance
    
    def copy_boot_files(self):
        result = ProcessUtils.get_instance().run_command([
            'cp', '-r', self._boot_files_location + '.', self._root + '/boot/'
        ])

        return result[0] == 0
    
    def remove_archiso_mkinitcpio_conf(self):
        try:
            os.remove(self._root + '/etc/mkinitcpio.conf.d/archiso.conf')

            return True
        except:
            Logs.add_log(format_exc())

        return False
    
    def copy_linux_mkinitcpio_preset(self):
        target = f'{self._root}/etc/mkinitcpio.d/linux.preset'

        try:
            os.remove(target)
            shutil.copy('./resources/linux.preset', target)

            return True
        
        except:
            Logs.add_log(format_exc())

        return False
    
    def genfstab(self):
        try:
            result = ProcessUtils.get_instance().run_command([
                'genfstab', '-U', '/mnt'
            ])

            fstab_result = result[1]

            with open(f'{self._root}/etc/fstab', 'w') as f:
                f.write(fstab_result)
            
            return True
        
        except:
            Logs.add_log(format_exc())

        return False
    
    def fix_vconsole(self):
        result = ProcessUtils.get_instance().run_command([
            'touch', f'{self._root}/etc/vconsole.conf'
        ])

        return result[0] == 0
    
    def mkinitcpio(self):
        result = ProcessUtils.get_instance().run_command_in_chroot(['mkinitcpio', '-P'], self._root)

        return result[0] == 0
    
    def install_grub(self):
        result = ProcessUtils.get_instance().run_command_in_chroot(['grub-install', '--efi-directory=/boot/efi'], self._root)

        return result[0] == 0
    
    def generate_grub_config(self):
        result = ProcessUtils.get_instance().run_command_in_chroot(['grub-mkconfig', '-o', '/boot/grub/grub.cfg'], self._root)

        return result[0] == 0