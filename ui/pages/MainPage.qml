import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import org.kde.kirigami as Kirigami
import "../components" as Components

Kirigami.Page {
    id: mainPage
    title: translatorBackend.translate("Welcome to Project GDL Installer!", translatorBackend.language)

    Rectangle {
        id: contentArea
        anchors.fill: parent
        color: Kirigami.Theme.backgroundColor

        ColumnLayout {
            anchors.fill: parent
            spacing: Kirigami.Units.gridUnit * 2

            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.alignment: Qt.AlignCenter

                width: Kirigami.Units.gridUnit * 20
                height: Kirigami.Units.gridUnit * 20
                color: Kirigami.Theme.highlightColor
                radius: Kirigami.Units.gridUnit / 2

                Text {
                    anchors.centerIn: parent
                    text: "Image Placeholder"
                    color: Kirigami.Theme.highlightColor.text
                    font.pixelSize: Kirigami.Units.fontSizes.large
                }
            }

            RowLayout {
                Layout.fillWidth: true
                Layout.preferredHeight: Kirigami.Units.gridUnit * 4

                ComboBox {
                    id: languageComboBox
                    Layout.alignment: Qt.AlignLeft
                    model: ["English (en)", "Русский (ru)"]
                    currentIndex: 0
                    
                    onActivated: {
                        if (currentIndex === 0) {
                            translatorBackend.language = "en"
                        }
                        else if (currentIndex === 1) {
                            translatorBackend.language = "ru"
                        }
                    }
                }

                Item { Layout.fillWidth: true }

                Button {
                    text: translatorBackend.translate("Exit", translatorBackend.language)
                    leftPadding: 20
                    rightPadding: 20
                    
                    onClicked: {
                        Qt.quit()
                    }
                }

                Button {
                    text: translatorBackend.translate("Next", translatorBackend.language)
                    icon.name: "arrow-right"
                    leftPadding: 20
                    
                    onClicked: {
                        console.log("Next clicked")
                    }
                }
            }
        }
    }
}