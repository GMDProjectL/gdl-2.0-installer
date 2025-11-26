import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import org.kde.kirigami as Kirigami
import "../components" as Components

Kirigami.Page {
    id: additionalTweaksPage
    title: translatorBackend.translate(
        "Additional tweaks", 
        translatorBackend.language
    )
    signal backPressed()
    signal nextPressed()

    Rectangle {
        id: contentArea
        anchors.fill: parent
        color: Kirigami.Theme.backgroundColor

        ColumnLayout {
            anchors.fill: parent
            spacing: Kirigami.Units.gridUnit * 2
            Layout.fillWidth: true
            
            RowLayout { // just in case if you want to place something side by side in future
                Layout.fillWidth: true
                Layout.maximumWidth: 1000 
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                Layout.fillHeight: true

                ColumnLayout {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    spacing: Kirigami.Units.gridUnit
                    
                    Kirigami.Heading {
                        level: 3
                        text: translatorBackend.translate(
                            "Anything else?", 
                            translatorBackend.language
                        )
                    }

                    Kirigami.ScrollablePage {
                        Layout.fillHeight: true
                        Layout.fillWidth: true

                        ColumnLayout {
                            Layout.fillHeight: true
                            Layout.fillWidth: true
                            
                            spacing: Kirigami.Units.gridUnit

                            Switch {
                                text: translatorBackend.translate("Install Steam", translatorBackend.language)
                            }

                            Switch {
                                text: translatorBackend.translate("Install Firefox instead of Chromium", translatorBackend.language)
                            }

                            Switch {
                                text: translatorBackend.translate("Install <code>paru</code> AUR helper [CLI]", translatorBackend.language)
                            }

                            Switch {
                                text: translatorBackend.translate("Install OBS Studio", translatorBackend.language)
                            }

                            Switch {
                                text: translatorBackend.translate("Install GPU Screen Recorder (Shadowplay ripoff)", translatorBackend.language)
                            }

                            Switch {
                                text: translatorBackend.translate("Install NVIDIA drivers", translatorBackend.language)
                            }
                        }
                    }
                    
                }
            }
            
            Item {
                Layout.fillHeight: true
            }

            RowLayout {
                Layout.fillWidth: true
                Layout.preferredHeight: Kirigami.Units.gridUnit * 2
                
                Item { Layout.fillWidth: true } 

                Button {
                    text: translatorBackend.translate("Back", translatorBackend.language)
                    icon.name: "arrow-left"
                    icon.width: 10
                    leftPadding: 20
                    rightPadding: 20
                    
                    onClicked: {
                        additionalTweaksPage.backPressed()
                    }
                }

                Button {
                    text: translatorBackend.translate("Next", translatorBackend.language)
                    icon.name: "arrow-right"
                    icon.width: 10
                    leftPadding: 20
                    rightPadding: 20
                    
                    onClicked: {
                        additionalTweaksPage.nextPressed()
                    }
                }
            }
        }
    }
}