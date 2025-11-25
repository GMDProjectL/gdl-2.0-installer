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

    property bool nextButtonEnabled: (
        driveProvider.partitionMethod == 0 
        ? driveProvider.drive !== -1
        : driveProvider.bootPartition !== -1 && driveProvider.rootPartition !== -1 
    )

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
                            "Which partitions will be used to install the system?", 
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
                                model: driveProvider.drives
                                currentIndex: driveProvider.drive
                                Layout.fillWidth: true
                                
                                onActivated: {
                                    driveProvider.drive = currentIndex
                                }
                            }

                            Button {
                                Layout.leftMargin: 10
                                visible: driveComboBox.currentIndex > -1 && driveProvider.partitionMethod == 1
                                text: translatorBackend.translate("Repartition the drive", translatorBackend.language) 
                                onClicked: {
                                    driveProvider.openPartitionManager()
                                }
                            }
                        }

                        ColumnLayout {
                            visible: driveProvider.drive !== -1

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
                                currentIndex: driveProvider.partitionMethod
                                Layout.fillWidth: true
                                
                                onActivated: {
                                    driveProvider.partitionMethod = currentIndex
                                }
                            }
                        }

                        ColumnLayout {
                            Layout.fillWidth: true
                            visible: driveProvider.partitionMethod == 1

                            Label { 
                                Layout.topMargin: 10
                                text: translatorBackend.translate("Select boot partition:", translatorBackend.language) 
                            }

                            ComboBox {
                                id: bootPartitionComboBox
                                Layout.alignment: Qt.AlignLeft
                                model: driveProvider.partitions
                                currentIndex: driveProvider.bootPartition
                                Layout.fillWidth: true
                                
                                onActivated: {
                                    driveProvider.bootPartition = currentIndex
                                }
                            }
                            
                            Label { 
                                Layout.topMargin: 10
                                text: translatorBackend.translate("Select root partition:", translatorBackend.language) 
                            }

                            ComboBox {
                                id: rootPartitionComboBox
                                Layout.alignment: Qt.AlignLeft
                                model: driveProvider.partitions
                                currentIndex: driveProvider.rootPartition
                                Layout.fillWidth: true
                                
                                onActivated: {
                                    driveProvider.rootPartition = currentIndex
                                }
                            }
                        }

                        RowLayout {
                            Layout.topMargin: 20
                            visible: driveProvider.partitionMethod == 0 && driveProvider.drive !== -1

                            Kirigami.Icon {
                                Layout.maximumHeight: 16
                                source: "emblem-warning"
                            }
                            Label {
                                verticalAlignment: Text.AlignVCenter
                                color: Kirigami.Theme.neutralTextColor
                                text: translatorBackend.translate("<b>Warning:</b> everything on this drive will be erased!", translatorBackend.language) 
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