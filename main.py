#!/usr/bin/python3
import os
import sys
import signal

from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, QCoreApplication, Signal, Property
import sys
import os

from src.translator_backend import TranslatorBackend


class TranslatorBackendWrapper(QObject):
    languageChanged = Signal()

    def __init__(self):
        super().__init__()
        self._translator = TranslatorBackend()
        self._current_language = "en"

    @Property(str, notify=languageChanged)
    def language(self):
        return self._current_language

    @language.setter
    def language(self, code):
        if self._current_language == code:
            return
        
        self._current_language = code
        self._translator.change_language(code)
        
        print(f"Language switched to: {code}")
        self.languageChanged.emit()

    @Slot(str, str, result=str)
    def translate(self, text, trigger=""): 
        print(f"Translating '{text}' for language '{self._current_language}'")
        return self._translator.translate(text)


def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    engine.addImportPath('ui/components')
    engine.addImportPath('ui/pages')
    engine.addImportPath('ui')

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    if not os.environ.get("QT_QUICK_CONTROLS_STYLE"):
        os.environ["QT_QUICK_CONTROLS_STYLE"] = "org.kde.desktop"

    translator_backend = TranslatorBackendWrapper()
    engine.rootContext().setContextProperty("translatorBackend", translator_backend)

    engine.load(QUrl('ui/MainWindow.qml'))

    app.exec()

if __name__ == "__main__":
    main()
