from PySide6.QtCore import QObject, Slot, Signal, Property
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette

class AdaptiveImageProvider(QObject):
    themeChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self._theme = self.detect_system_theme()
        app = QApplication.instance()
        if app:
            app.paletteChanged.connect(self.on_palette_changed)

    def detect_system_theme(self) -> str:
        palette = QApplication.palette()
        color = palette.color(QPalette.Window)
        lightness = (color.red() + color.green() + color.blue()) / 3
        if lightness < 128:
            return "dark"
        else:
            return "light"

    def on_palette_changed(self, palette):
        new_theme = self.detect_system_theme()
        if new_theme != self._theme:
            self._theme = new_theme
            self.themeChanged.emit(self._theme)

    @Property(str, notify=themeChanged)
    def theme(self):
        return self._theme

    @Slot(str, result=str)
    def adaptiveImagePath(self, name: str) -> str:
        return f"../../images/{name}-{self._theme}.png"
