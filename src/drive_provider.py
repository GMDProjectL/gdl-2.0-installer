import subprocess
from PySide6.QtCore import QObject, Property, Signal
from typing import List
import io

class DriveProvider(QObject):
    drivesChanged = Signal()
    driveChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._drives = self.get_drives()
        self._drive = 0
    
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
            type_val = line[type_start:size_start].split()[0].strip()
            
            model_part = line[model_start:type_start].strip()
            size_part = line[:size_start+4].split()[-1].strip()
            
            if type_val not in ('part', 'loop') and name:
                data.append({
                    'name': name,
                    'model': model_part,
                    'size': size_part
                })

        return data

    @Property("QVariantList", notify=drivesChanged)
    def drives(self):
        return [f'{drive["model"]} ({drive["size"]}) - {drive["name"]}' for drive in self._drives]


    @Property(int, notify=driveChanged)
    def drive(self):
        return self._drive

    @drive.setter
    def drive(self, value):
        if self._drive != value:
            self._drive = value
            self.driveChanged.emit()

    def refresh_drives(self):
        self._drives = self.get_drives()
        self.drivesChanged.emit()
