import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami
import "../components" as Components

Kirigami.Page {
    id: mainPage
    title: translatorBackend.translate(
        "Welcome to Project GDL Installer!", 
        translatorBackend.language
    )
    signal nextPressed()

    Rectangle {
        id: contentArea
        anchors.fill: parent
        color: Kirigami.Theme.backgroundColor

        ColumnLayout {
            anchors.fill: parent

            Kirigami.Heading {
                level: 3
                text: translatorBackend.translate(
                    "You're about to install an easy-to-use Linux distribution.", 
                    translatorBackend.language
                )
            }

            Label {
                text: translatorBackend.translate(
                    "Please connect to the internet, we can't connect to github.com and archlinux.org.", 
                    translatorBackend.language
                )
                color: Kirigami.Theme.neutralTextColor
                visible: !internetCheckerBackend.isInternetAvailable
            }

            Item {
                Layout.fillHeight: true
            }

            Rectangle {
                Layout.alignment: Qt.AlignCenter

                width: Kirigami.Units.gridUnit * 15
                height: Kirigami.Units.gridUnit * 15
                color: "transparent"
                radius: Kirigami.Units.gridUnit / 2

                Image {
                    width: parent.width
                    height: parent.height

                    anchors.centerIn: parent
                    source: (
                        adaptiveImageProvider 
                        ? adaptiveImageProvider.adaptiveImagePath('main_page') + "?" + adaptiveImageProvider.theme 
                        : ""
                    )
                    fillMode: Image.PreserveAspectFit
                }
            }

            Item {
                Layout.fillHeight: true
            }

            RowLayout {
                Layout.fillWidth: true
                Layout.preferredHeight: Kirigami.Units.gridUnit * 2

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
                    leftPadding: 15
                    rightPadding: 23
                    icon.width: 25
                    icon.height: 15
                    icon.name: "application-exit-symbolic"
                    
                    onClicked: {
                        Qt.quit()
                    }
                }

                Button {
                    text: translatorBackend.translate("Next", translatorBackend.language)
                    icon.name: "arrow-right"
                    icon.width: 10
                    leftPadding: 30
                    rightPadding: 35
                    
                    onClicked: {
                        mainPage.nextPressed()
                    }
                }
            }
        }
    }
}