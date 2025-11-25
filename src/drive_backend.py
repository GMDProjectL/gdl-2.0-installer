import io
import os
import subprocess
from typing import List
from PySide6.QtCore import QObject, Property, Signal, Slot

class DriveBackend(QObject):
    drivesChanged = Signal()
    driveChanged = Signal()
    partitionsChanged = Signal()
    bootPartitionChanged = Signal()
    rootPartitionChanged = Signal()
    rootPartitionsChanged = Signal()
    partitionMethodChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._drives = self.get_drives()
        self._drive = -1
        self._partitions = []
        self._boot_partition_index = -1
        self._root_partition_index = -1
        self._partition_method_index = 0
        
        self.driveChanged.connect(self._update_partitions_on_drive_change)
    

    @Slot()
    def openPartitionManager(self):
        os.system(f'partitionmanager --device /dev/{self._drives[self.drive]["name"]}')
        self._update_partitions_on_drive_change()


    def get_drives(self) -> List[dict]:
        result = subprocess.run(
            ['lsblk', '-o', 'NAME,MODEL,TYPE,SIZE'],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        output = result.stdout
        data = []
        f = io.StringIO(output)

        headers_line = f.readline()
        if not headers_line:
            return []
        
        name_start = headers_line.index("NAME")
        model_start = headers_line.index("MODEL")
        type_start = headers_line.index("TYPE")
        size_start = headers_line.index("SIZE")

        for line in f:
            line = line.rstrip()
            
            name = line[name_start:model_start].strip()

            type_val_part = line[type_start:size_start].strip()
            type_val = type_val_part.split()[0].strip() if type_val_part else ''
            
            model_part = line[model_start:type_start].strip()
            size_part = line[:size_start+4].split()[-1].strip()

            
            if type_val not in ('part', 'loop') and name and not name.startswith('loop'):
                data.append({
                    'name': name,
                    'model': model_part,
                    'size': size_part
                })

        return data
    
    @Property("QVariantList", notify=drivesChanged)
    def drives(self):
        return [f'{drive["model"]} ({drive["size"]}) - {drive["name"]}' for drive in self._drives]


    @Property(int, notify=partitionMethodChanged)
    def partitionMethod(self):
        return self._partition_method_index

    @partitionMethod.setter
    def partitionMethod(self, value):
        if self._partition_method_index != value:
            self._partition_method_index = value
            self.partitionMethodChanged.emit()


    @Property(int, notify=driveChanged)
    def drive(self):
        return self._drive

    @drive.setter
    def drive(self, value):
        if self._drive != value:
            self._drive = value
            self.driveChanged.emit()


    @Slot()
    def refresh_drives(self):
        self._drives = self.get_drives()
        self.drivesChanged.emit()


    def get_partitions(self, disk_name: str) -> List[dict]:
        if not disk_name:
            return []
            
        try:
            result = subprocess.run(
                ['lsblk', '-l', '-n', '-a', '-o', 'NAME,SIZE,MOUNTPOINT', f'/dev/{disk_name}'],
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8'
            )
        except subprocess.CalledProcessError:
            print(f"Error getting partitions for {disk_name}")
            return []

        output = result.stdout
        data = []
        
        for line in output.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                name = parts[0].replace('/dev/', '').strip()
                size = parts[1].strip()
                mountpoint = parts[2].strip() if len(parts) > 2 else ''
                
                if name.startswith(disk_name) and name != disk_name:
                    data.append({
                        'name': name,
                        'size': size,
                        'mountpoint': mountpoint
                    })
        return data


    @Slot()
    def _update_partitions_on_drive_change(self):
        self._partitions = []
        self._boot_partition_index = -1
        self._root_partition_index = -1
        
        if 0 <= self._drive < len(self._drives):
            selected_drive_name = self._drives[self._drive]['name']
            self._partitions = self.get_partitions(selected_drive_name)
            
            for i, p in enumerate(self._partitions):
                if p.get('mountpoint') == '/boot/efi' or p.get('mountpoint') == '/boot':
                    self._boot_partition_index = i
                elif p.get('mountpoint') == '/':
                    self._root_partition_index = i


        self.partitionsChanged.emit()
        self.bootPartitionChanged.emit()
        self.rootPartitionChanged.emit()
        self.rootPartitionsChanged.emit()


    @Property("QVariantList", notify=partitionsChanged)
    def partitions(self):
        return [f'{p["name"]} ({p["size"]}) [ {p["mountpoint"]} ]' for p in self._partitions]

    @Property("QVariantList", notify=rootPartitionsChanged)
    def rootPartitions(self):
        return [f'{p["name"]} ({p["size"]}) [ {p["mountpoint"]} ]' for p in self._partitions]

    @Property(int, notify=bootPartitionChanged)
    def bootPartition(self):
        return self._boot_partition_index


    @bootPartition.setter
    def bootPartition(self, value: int):
        if self._boot_partition_index != value and -1 <= value < len(self._partitions):
            self._boot_partition_index = value
            self.bootPartitionChanged.emit()


    @Property(int, notify=rootPartitionChanged)
    def rootPartition(self):
        return self._root_partition_index

    @rootPartition.setter
    def rootPartition(self, value: int):
        if self._root_partition_index != value and -1 <= value < len(self._partitions):
            self._root_partition_index = value
            self.rootPartitionChanged.emit()


    @Slot(int, result=str)
    def getPartitionName(self, index: int) -> str:
        if 0 <= index < len(self._partitions):
            return self._partitions[index]['name']
        return ""