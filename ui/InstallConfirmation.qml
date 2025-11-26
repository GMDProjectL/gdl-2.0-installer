import QtQuick
import QtQuick.Controls
import org.kde.kirigami as Kirigami
import QtQuick.Layouts

Kirigami.Dialog {
    id: installConfirmationDialog

    title: translatorBackend.translate("Final decision", translatorBackend.language)
    padding: Kirigami.Units.gridUnit * 2

    signal yes()
    signal no()

    Label {
        text: translatorBackend.translate(
            "Are you sure you want to install the system?",
            translatorBackend.language
        )
    }

    footer: RowLayout {
        Layout.fillWidth: true
        spacing: 10

        Item {
            Layout.fillWidth: true
        }

        Button {
            text: translatorBackend.translate("Yes, install!", translatorBackend.language)
            icon.name: "checkmark-symbolic"
            leftPadding: 10
            rightPadding: 10
            Layout.bottomMargin: 10

            onClicked: {
                installConfirmationDialog.accepted()
                installConfirmationDialog.close()
            }
        }

        Button {
            text: translatorBackend.translate("No, not yet", translatorBackend.language)
            icon.name: "dialog-cancel"

            leftPadding: 10
            rightPadding: 10
            Layout.rightMargin: 10
            Layout.bottomMargin: 10

            onClicked: {
                installConfirmationDialog.reject()
                installConfirmationDialog.close()
            }
        }
    }
    onAccepted: {
        installConfirmationDialog.yes()
    }

    onRejected: {
        installConfirmationDialog.no()
    }
}