import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
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

    property bool nextButtonEnabled: (
        driveBackend.partitionMethod == 0 
        ? driveBackend.drive !== -1
        : driveBackend.bootPartition !== -1 && driveBackend.rootPartition !== -1 
    )

    Component.onCompleted: {
        driveComboBox.forceActiveFocus()
    }

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
                            "It's important to use your space wisely.", 
                            translatorBackend.language
                        )
                    }

                    ColumnLayout {
                        Layout.fillWidth: true

                        Label { text: translatorBackend.translate("Select the drive:", translatorBackend.language) }

                        RowLayout {
                            Layout.fillWidth: true

                            ComboBox {
                                id: driveComboBox
                                Layout.alignment: Qt.AlignLeft
                                model: driveBackend.drives
                                currentIndex: driveBackend.drive
                                Layout.fillWidth: true
                                
                                onActivated: {
                                    driveBackend.drive = currentIndex
                                }
                            }

                            Button {
                                Layout.leftMargin: 10
                                visible: driveComboBox.currentIndex > -1 && driveBackend.partitionMethod == 1
                                text: translatorBackend.translate("Repartition the drive", translatorBackend.language) 
                                onClicked: {
                                    driveBackend.openPartitionManager()
                                }
                            }
                        }

                        ColumnLayout {
                            visible: driveBackend.drive !== -1

                            Label { 
                                Layout.topMargin: 10
                                text: translatorBackend.translate("Partition method:", translatorBackend.language) 
                            }
                            
                            ComboBox {
                                id: partitionMethodComboBox
                                Layout.alignment: Qt.AlignLeft
                                model: [
                                    translatorBackend.translate("Automatic", translatorBackend.language),
                                    translatorBackend.translate("Manual", translatorBackend.language)
                                ]
                                currentIndex: driveBackend.partitionMethod
                                Layout.fillWidth: true
                                
                                onActivated: {
                                    driveBackend.partitionMethod = currentIndex
                                }
                            }
                        }

                        ColumnLayout {
                            Layout.fillWidth: true
                            visible: driveBackend.partitionMethod == 1

                            Label { 
                                Layout.topMargin: 10
                                text: translatorBackend.translate("Select boot partition:", translatorBackend.language) 
                            }

                            ComboBox {
                                id: bootPartitionComboBox
                                Layout.alignment: Qt.AlignLeft
                                model: driveBackend.partitions
                                currentIndex: driveBackend.bootPartition
                                Layout.fillWidth: true
                                
                                onActivated: {
                                    driveBackend.bootPartition = currentIndex
                                }
                            }
                            
                            Label { 
                                Layout.topMargin: 10
                                text: translatorBackend.translate("Select root partition:", translatorBackend.language) 
                            }

                            ComboBox {
                                id: rootPartitionComboBox
                                Layout.alignment: Qt.AlignLeft
                                model: driveBackend.partitions
                                currentIndex: driveBackend.rootPartition
                                Layout.fillWidth: true
                                
                                onActivated: {
                                    driveBackend.rootPartition = currentIndex
                                }
                            }
                        }

                        RowLayout {
                            Layout.topMargin: 20
                            visible: driveBackend.partitionMethod == 0 && driveBackend.drive !== -1

                            Kirigami.Icon {
                                Layout.maximumHeight: 16
                                source: "emblem-warning"
                            }
                            Label {
                                verticalAlignment: Text.AlignVCenter
                                color: Kirigami.Theme.neutralTextColor
                                text: translatorBackend.translate(
                                    "<b>Warning:</b> everything on this drive will be erased!", 
                                    translatorBackend.language
                                ) 
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