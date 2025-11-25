#!/usr/bin/python3
import os
import sys
import signal

from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlApplicationEngine
import sys
import os

from src.image_provider import AdaptiveImageProvider
from src.translator_backend_wrapper import TranslatorBackendWrapper

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
    image_provider = AdaptiveImageProvider()

    engine.rootContext().setContextProperty("translatorBackend", translator_backend)
    engine.rootContext().setContextProperty("imageProvider", image_provider)

    engine.load(QUrl('ui/MainWindow.qml'))

    app.exec()

if __name__ == "__main__":
    main()
