import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami

Kirigami.Dialog {
    id: exitConfirmationDialog
    title: translatorBackend.translate("Exit Installer", translatorBackend.language)
    standardButtons: Kirigami.Dialog.NoButton
    padding: 20

    footer: RowLayout {
        Layout.fillWidth: true
        spacing: 10

        Item {
            Layout.fillWidth: true
        }

        Button {
            text: translatorBackend.translate("Exit", translatorBackend.language)
            icon.name: "application-exit-symbolic"
            leftPadding: 10
            rightPadding: 10
            Layout.bottomMargin: 10

            onClicked: {
                exitConfirmationDialog.accepted()
                exitConfirmationDialog.close()
            }
        }

        Button {
            text: translatorBackend.translate("Cancel", translatorBackend.language)
            icon.name: "dialog-cancel"

            leftPadding: 10
            rightPadding: 10
            Layout.rightMargin: 10
            Layout.bottomMargin: 10

            onClicked: {
                exitConfirmationDialog.refuseClosing()
                exitConfirmationDialog.close()
            }
        }
    }

    signal refuseClosing()

    Label {
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