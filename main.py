#!/usr/bin/python3
import os
import sys
import signal

from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlApplicationEngine
import sys
import os

from src.global_installer_state import GlobalInstallerState

def main():
    app = QGuiApplication(sys.argv)
    app.setWindowIcon(QIcon('images/run-build-install.svg'))

    engine = QQmlApplicationEngine()

    # including QML dirs, just in case
    engine.addImportPath('ui/components')
    engine.addImportPath('ui/pages')
    engine.addImportPath('ui')

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # setting qqc style
    if not os.environ.get("QT_QUICK_CONTROLS_STYLE"):
        os.environ["QT_QUICK_CONTROLS_STYLE"] = "org.kde.desktop"

    global_installer_state = GlobalInstallerState()

    engine.rootContext().setContextProperty("translatorBackend", global_installer_state.translator_backend_wrapper)
    engine.rootContext().setContextProperty("adaptiveImageProvider", global_installer_state.adaptive_image_provider)
    engine.rootContext().setContextProperty("userProfileBackend", global_installer_state.user_profile_backend)
    engine.rootContext().setContextProperty("additionalTweaksBackend", global_installer_state.additional_tweaks_backend)
    engine.rootContext().setContextProperty("driveBackend", global_installer_state.drive_backend)
    engine.rootContext().setContextProperty("internetCheckerBackend", global_installer_state.internet_checker_backend)
    engine.rootContext().setContextProperty("installationProcessBackend", global_installer_state.installation_process_backend)

    engine.load(QUrl('ui/MainWindow.qml'))

    app.exec()

if __name__ == "__main__":
    main()
