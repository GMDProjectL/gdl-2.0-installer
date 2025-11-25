import QtQuick
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami

Kirigami.Dialog {
    id: exitConfirmationDialog
    title: translatorBackend.translate("Exit Installer", translatorBackend.language)
    standardButtons: Kirigami.Dialog.NoButton
    padding: 20

    customFooterActions: [
        Kirigami.Action {
            text: translatorBackend.translate("Exit", translatorBackend.language)
            onTriggered: {
                exitConfirmationDialog.accepted()
                exitConfirmationDialog.close()
            }
        },
        Kirigami.Action {
            text: translatorBackend.translate("Cancel", translatorBackend.language)
            onTriggered: {
                exitConfirmationDialog.refuseClosing()
                exitConfirmationDialog.close()
            }
        }
    ]

    signal refuseClosing()

    Controls.Label {
        text: translatorBackend.translate(
            "Are you sure you want to exit the installer? Your changes will not be saved.",
            translatorBackend.language
        )
    }

    onAccepted: {
        Qt.quit()
    }

    onRejected: {
        exitConfirmationDialog.refuseClosing()
    }
}