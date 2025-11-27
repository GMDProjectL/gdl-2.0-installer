import QtQuick
import QtQuick.Controls
import org.kde.kirigami as Kirigami
import QtQuick.Layouts

Kirigami.Dialog {
    id: installationSucceededDialog

    title: translatorBackend.translate("Project GDL is now installed", translatorBackend.language)
    padding: Kirigami.Units.gridUnit * 2

    Label {
        id: errorTextLabel
        wrapMode: Label.WordWrap
        Layout.topMargin: Kirigami.Units.gridUnit
        Layout.bottomMargin: Kirigami.Units.gridUnit
        text: translatorBackend.translate(
            "Do you want to reboot?", 
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
            text: translatorBackend.translate("Yes, reboot!", translatorBackend.language)
            icon.name: "system-reboot-symbolic"
            leftPadding: 10
            rightPadding: 10
            Layout.bottomMargin: 10

            onClicked: {
                installationSucceededDialog.accepted()
                installationSucceededDialog.close()
            }
        }

        Button {
            text: translatorBackend.translate("No, I will look around", translatorBackend.language)
            icon.name: "dialog-close"

            leftPadding: 10
            rightPadding: 10
            Layout.rightMargin: 10
            Layout.bottomMargin: 10

            onClicked: {
                installationSucceededDialog.close()
            }
        }
    }
}