import os
import shutil
from storage.logs import Logs
from installation.process_utils import ProcessUtils

class ConfigService:
    def __init__(self, process_utils: ProcessUtils):
        self.process_utils = process_utils
        self._boot_files_location = ""
        self._root = ""

    def set_settings(self, boot_files_location: str, root: str):
        self._boot_files_location = boot_files_location
        self._root = root

    def copy_boot_files(self) -> bool:
        try:
            boot_dir = os.path.join(self._root, 'boot')
            if not os.path.exists(boot_dir):
                os.makedirs(boot_dir)

            for item in os.listdir(self._boot_files_location):
                s = os.path.join(self._boot_files_location, item)
                d = os.path.join(boot_dir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)

            Logs.add_log("Boot files copied successfully.")
            return True
        except Exception as e:
            Logs.add_log(f"Failed to copy boot files: {e}")
            return False

    def remove_archiso_mkinitcpio_conf(self) -> bool:
        try:
            path = os.path.join(self._root, 'etc', 'mkinitcpio.conf.d', 'archiso.conf')
            if os.path.exists(path):
                os.remove(path)
                Logs.add_log("Removed archiso mkinitcpio.conf")
            return True
        except Exception as e:
            Logs.add_log(f"Failed to remove archiso mkinitcpio.conf: {e}")
            return False

    def copy_linux_mkinitcpio_preset(self) -> bool:
        try:
            src = f'./resources/linux.preset'
            dst = os.path.join(self._root, 'etc', 'mkinitcpio.d', 'linux.preset')
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            Logs.add_log("Copied linux mkinitcpio preset")
            return True
        except Exception as e:
            Logs.add_log(f"Failed to copy linux mkinitcpio preset: {e}")
            return False

    def genfstab(self) -> bool:
        try:
            result = self.process_utils.run_command(['genfstab', '-U', self._root])
            if result[0] == 0:
                fstab_content = result[1]
                fstab_path = os.path.join(self._root, 'etc', 'fstab')
                with open(fstab_path, 'w') as f:
                    f.write(fstab_content)
                Logs.add_log("Generated fstab")
                return True
            else:
                Logs.add_log(f"Failed to generate fstab: {result[2]}")
                return False
        except Exception as e:
            Logs.add_log(f"Failed to generate fstab: {e}")
            return False

    def fix_vconsole(self) -> bool:
        try:
            vconsole_path = os.path.join(self._root, 'etc', 'vconsole.conf')
            with open(vconsole_path, 'w') as f:
                f.write('KEYMAP=us\n')
            Logs.add_log("Fixed vconsole.conf")
            
            return True
        except Exception as e:
            Logs.add_log(f"Failed to fix vconsole: {e}")
            return False

    def mkinitcpio(self) -> bool:
        try:
            result = self.process_utils.run_command_in_chroot(['mkinitcpio', '-P'], self._root)
            if result[0] == 0:
                Logs.add_log("Generated ramdisk")
                return True
            else:
                Logs.add_log(f"Failed to generate ramdisk: {result[2]}")
                return False
        except Exception as e:
            Logs.add_log(f"Failed to generate ramdisk: {e}")
            return False

    def install_grub(self) -> bool:
        try:
            result = self.process_utils.run_command_in_chroot(
                ['grub-install', '--target=x86_64-efi', '--efi-directory=/boot/efi', '--bootloader-id=GRUB'], 
                self._root
            )
            if result[0] == 0:
                Logs.add_log("Installed GRUB")
                return True
            else:
                Logs.add_log(f"Failed to install GRUB: {result[2]}")
                return False
        except Exception as e:
            Logs.add_log(f"Failed to install GRUB: {e}")
            return False

    def generate_grub_config(self) -> bool:
        try:
            result = self.process_utils.run_command_in_chroot(['grub-mkconfig', '-o', '/boot/grub/grub.cfg'], self._root)
            if result[0] == 0:
                Logs.add_log("Generated GRUB config")
                return True
            else:
                Logs.add_log(f"Failed to generate GRUB config: {result[2]}")
                return False
        except Exception as e:
            Logs.add_log(f"Failed to generate GRUB config: {e}")
            return False
    
    def change_user_password(self, username: str, password: str):
        result = self.process_utils.run_command_in_chroot([
            'sh', '-c', f'echo -e "{password}\n{password}" | passwd {username}'
        ], self._root)

        return result[0] == 0

    def set_root_password(self, password: str) -> bool:
        return self.change_user_password('root', password)

    def create_user(self, username: str, password: str) -> bool:
        result = self.process_utils.run_command_in_chroot(['useradd', '-m', '-G', 'wheel', '-s', '/usr/bin/fish', username], self._root)
        if result[0] != 0:
            Logs.add_log(f"Failed to create user: {result[2]}")
            return False
        
        if not self.change_user_password(username, password):
            Logs.add_log(f"Failed to change password.")
            return False
        
        return True

    def setup_autologin(self, username: str) -> bool:
        try:
            sddm_dir = os.path.join(self._root, 'etc', 'sddm.conf.d')
            os.makedirs(sddm_dir, exist_ok=True)

            autologin_path = os.path.join(sddm_dir, 'autologin.conf')
            with open(autologin_path, 'w') as f:
                f.write(f'[Autologin]\nUser={username}\nSession=plasma\n')

            Logs.add_log(f"Setup autologin for user {username}")
            return True
        except Exception as e:
            Logs.add_log(f"Failed to setup autologin: {e}")
            return False

    def set_hostname(self, hostname: str) -> bool:
        try:
            hostname_path = os.path.join(self._root, 'etc', 'hostname')
            with open(hostname_path, 'w') as f:
                f.write(hostname)

            hosts_path = os.path.join(self._root, 'etc', 'hosts')
            with open(hosts_path, 'a') as f:
                f.write(f'\n127.0.0.1\tlocalhost\n::1\t\tlocalhost\n127.0.1.1\t{hostname}.localdomain\t{hostname}\n')

            Logs.add_log(f"Set hostname to {hostname}")
            return True
        except Exception as e:
            Logs.add_log(f"Failed to set hostname: {e}")
            return False

    def create_sudoers_file(self, username: str) -> bool:
        try:
            sudoers_path = os.path.join(self._root, 'etc', 'sudoers.d', username)
            os.makedirs(os.path.dirname(sudoers_path), exist_ok=True)

            with open(sudoers_path, 'w') as f:
                f.write(f'{username} ALL=(ALL) ALL\n')

            # set proper permissions
            os.chmod(sudoers_path, 0o440)

            Logs.add_log(f"Created sudoers file for {username}")
            return True
        except Exception as e:
            Logs.add_log(f"Failed to create sudoers file: {e}")
            return False
