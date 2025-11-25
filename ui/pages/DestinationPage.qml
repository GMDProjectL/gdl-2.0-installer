import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import org.kde.kirigami as Kirigami
import "../components" as Components

Kirigami.Page {
    id: userProfilePage
    title: translatorBackend.translate(
        "Where do you want to install the system?", 
        translatorBackend.language
    )
    signal backPressed()
    signal nextPressed()

    property bool nextButtonEnabled: false

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
                    spacing: Kirigami.Units.gridUnit * 2
                    
                    Kirigami.Heading {
                        level: 3
                        text: translatorBackend.translate(
                            "Select the appropriate drive and/or partitions", 
                            translatorBackend.language
                        )
                    }

                    ColumnLayout {
                        Layout.fillWidth: true

                        ComboBox {
                            id: driveComboBox
                            Layout.alignment: Qt.AlignLeft
                            model: driveProvider.drives
                            currentIndex: 0
                            Layout.fillWidth: true
                            
                            onActivated: {
                                driveProvider.drive = currentIndex
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
                        userProfilePage.backPressed()
                    }
                }

                Button {
                    text: translatorBackend.translate("Next", translatorBackend.language)
                    icon.name: "arrow-right"
                    icon.width: 10
                    leftPadding: 20
                    rightPadding: 20
                    enabled: userProfilePage.nextButtonEnabled
                    
                    onClicked: {
                        userProfilePage.nextPressed()
                    }
                }
            }
        }
    }
}