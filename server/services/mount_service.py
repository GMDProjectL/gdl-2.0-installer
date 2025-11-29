import os
import subprocess
import json
from typing import List, Dict, Any, Optional
from utils.singleton import Singleton
from storage.logs import Logs
from installation.process_utils import ProcessUtils

class MountService:
    def __init__(self, process_utils: ProcessUtils):
        self.process_utils = process_utils

    def get_mounts(self, drive: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get mount information for a specific drive using lsblk.
        Returns a list of mount points or False on error.
        """
        try:
            # why am I even using CLI tools in the first place...
            result = self.process_utils.run_command([
                'lsblk', '-J', '-o', 'NAME,MOUNTPOINT,SIZE,TYPE'
            ])

            if result[0] != 0:
                Logs.add_log(f"Failed to get mount information: {result[2]}")
                return False

            lsblk_output = json.loads(result[1])

            mountpoints = []
            for device in lsblk_output.get('blockdevices', []):
                if device.get('name', '').startswith(drive.replace('/dev/', '')):
                    mountpoints.extend(self._extract_mountpoints(device))

            Logs.add_log(f"Retrieved mount information for drive {drive}")
            return mountpoints

        except (json.JSONDecodeError, KeyError, Exception) as e:
            Logs.add_log(f"Error getting mount information: {e}")
            return False

    def _extract_mountpoints(self, device: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recursively extract mount points from lsblk device structure."""
        mountpoints = []

        # any mountpoints?
        if device.get('mountpoint') and device['mountpoint'].strip():
            mountpoints.append({
                'name': f"/dev/{device['name']}",
                'mountpoint': device['mountpoint'],
                'size': device.get('size', ''),
                'type': device.get('type', '')
            })

        for child in device.get('children', []):
            mountpoints.extend(self._extract_mountpoints(child))

        return mountpoints

    def mount(self, device: str, mountpoint: str) -> bool:
        """
        Mount a device to a mount point.
        """
        try:
            result = self.process_utils.run_command(['mount', '-m', '/dev/' + device, mountpoint])

            if result[0] == 0:
                Logs.add_log(f"Successfully mounted {device} to {mountpoint}")
                return True
            else:
                Logs.add_log(f"Failed to mount {device} to {mountpoint}: {result[2]}")
                return False

        except Exception as e:
            Logs.add_log(f"Error mounting {device}: {e}")
            return False

    def unmount(self, device: str) -> bool:
        """
        Unmount a device.
        """
        try:
            result = self.process_utils.run_command(['umount', '-Al', '/dev/' + device])

            if result[0] == 0:
                Logs.add_log(f"Successfully unmounted {device}")
                return True
            else:
                Logs.add_log(f"Failed to unmount {device}: {result[2]}")
                return False

        except Exception as e:
            Logs.add_log(f"Error unmounting {device}: {e}")
            return False

    def is_mounted(self, device: str) -> bool:
        """
        Check if a device is currently mounted.
        """
        try:
            with open('/proc/mounts', 'r') as f:
                mounts = f.read()

            return device in mounts
        except Exception as e:
            Logs.add_log(f"Error checking mount status for {device}: {e}")
            return False
