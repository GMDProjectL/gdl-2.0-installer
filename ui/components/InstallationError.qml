import QtQuick
import QtQuick.Controls
import org.kde.kirigami as Kirigami
import QtQuick.Layouts

Kirigami.Dialog {
    id: errorDialog

    property alias errorText: errorTextLabel.text

    title: translatorBackend.translate("Error", translatorBackend.language)
    padding: Kirigami.Units.gridUnit * 2

    Label {
        id: errorTextLabel
        wrapMode: Label.WordWrap
        Layout.topMargin: Kirigami.Units.gridUnit
        Layout.bottomMargin: Kirigami.Units.gridUnit
    }

    footer: RowLayout {
        Layout.fillWidth: true
        spacing: 10

        Item {
            Layout.fillWidth: true
        }

        Button {
            text: translatorBackend.translate("OK", translatorBackend.language)
            icon.name: "dialog-ok"
            leftPadding: 10
            rightPadding: 10
            Layout.bottomMargin: 10
            Layout.rightMargin: 10

            onClicked: {
                errorDialog.close()
            }
        }
    }
}