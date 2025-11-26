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

            RowLayout { 
                Layout.fillWidth: true
                Layout.maximumWidth: 1000 
                Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                Layout.fillHeight: true

                ColumnLayout {
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    Kirigami.Heading {
                        level: 3
                        text: translatorBackend.translate(
                            "Anything else?",
                            translatorBackend.language
                        )
                    }

                    ScrollView {
                        Layout.topMargin: Kirigami.Units.gridUnit
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        ScrollBar.vertical.policy: ScrollBar.AlwaysOn

                        ColumnLayout {
                            Layout.fillHeight: true
                            Layout.fillWidth: true
                            spacing: 0

                            // games
                            Kirigami.ListSectionHeader {
                                text: translatorBackend.translate("Games", translatorBackend.language)
                                Layout.fillWidth: true
                            }

                            Components.OptionCheckBox {
                                labelText: translatorBackend.translate("Install Steam", translatorBackend.language)
                                checkedState: additionalTweaksBackend.installSteam
                                onCheckedStateChanged: additionalTweaksBackend.installSteam = checkedState
                            }

                            // internet
                            Kirigami.ListSectionHeader {
                                text: translatorBackend.translate("Internet", translatorBackend.language)
                                Layout.fillWidth: true
                                Layout.topMargin: 10
                            }

                            Components.OptionCheckBox {
                                labelText: translatorBackend.translate("Install Firefox instead of Chromium", translatorBackend.language)
                                checkedState: additionalTweaksBackend.installFirefox
                                onCheckedStateChanged: additionalTweaksBackend.installFirefox = checkedState
                            }
                            
                            Components.OptionCheckBox {
                                labelText: translatorBackend.translate("Install qBittorrent", translatorBackend.language)
                                checkedState: additionalTweaksBackend.installQBitTorrent
                                onCheckedStateChanged: additionalTweaksBackend.installQBitTorrent = checkedState
                            }

                            // sysutils
                            Kirigami.ListSectionHeader {
                                text: translatorBackend.translate("System utilities", translatorBackend.language)
                                Layout.fillWidth: true
                                Layout.topMargin: 10
                            }

                            Components.OptionCheckBox {
                                labelText: translatorBackend.translate("Install <code>paru</code> AUR helper [CLI]", translatorBackend.language)
                                checkedState: additionalTweaksBackend.installParu
                                onCheckedStateChanged: additionalTweaksBackend.installParu = checkedState
                            }

                            // multimedia
                            Kirigami.ListSectionHeader {
                                text: translatorBackend.translate("Multimedia/Streaming", translatorBackend.language)
                                Layout.fillWidth: true
                                Layout.topMargin: 10
                            }
                            
                            Components.OptionCheckBox {
                                labelText: translatorBackend.translate("Install OBS Studio", translatorBackend.language)
                                checkedState: additionalTweaksBackend.installObs
                                onCheckedStateChanged: additionalTweaksBackend.installObs = checkedState
                            }

                            
                            Components.OptionCheckBox {
                                labelText: translatorBackend.translate("Install Kdenlive", translatorBackend.language)
                                checkedState: additionalTweaksBackend.installKdenlive
                                onCheckedStateChanged: additionalTweaksBackend.installKdenlive = checkedState
                            }

                            Components.OptionCheckBox {
                                labelText: translatorBackend.translate("Install GPU Screen Recorder (Shadowplay ripoff)", translatorBackend.language)
                                checkedState: additionalTweaksBackend.installGpuRecorder
                                onCheckedStateChanged: additionalTweaksBackend.installGpuRecorder = checkedState
                            }

                            // kernelspace
                            Kirigami.ListSectionHeader {
                                text: translatorBackend.translate("Drivers/Kernel", translatorBackend.language)
                                Layout.fillWidth: true
                                Layout.topMargin: 10
                            }

                            Components.OptionCheckBox {
                                labelText: translatorBackend.translate("Install NVIDIA drivers", translatorBackend.language)
                                checkedState: additionalTweaksBackend.installNvidia
                                onCheckedStateChanged: additionalTweaksBackend.installNvidia = checkedState
                            }

                            Components.OptionCheckBox {
                                labelText: translatorBackend.translate("Force NVIDIA maximum performance mode", translatorBackend.language)
                                checkedState: additionalTweaksBackend.forceNvidiaPerf
                                onCheckedStateChanged: additionalTweaksBackend.forceNvidiaPerf = checkedState
                            }

                            Components.OptionCheckBox {
                                labelText: translatorBackend.translate("Use Nobara Kernel", translatorBackend.language)
                                checkedState: additionalTweaksBackend.useNobaraKernel
                                onCheckedStateChanged: additionalTweaksBackend.useNobaraKernel = checkedState
                            }

                            // office
                            Kirigami.ListSectionHeader {
                                text: translatorBackend.translate("Office", translatorBackend.language)
                                Layout.fillWidth: true
                                Layout.topMargin: 10
                            }

                            Components.OptionCheckBox {
                                labelText: translatorBackend.translate("Install LibreOffice", translatorBackend.language)
                                checkedState: additionalTweaksBackend.installLibreOffice
                                onCheckedStateChanged: additionalTweaksBackend.installLibreOffice = checkedState
                            }

                            Components.OptionCheckBox {
                                labelText: translatorBackend.translate("Install OnlyOffice", translatorBackend.language)
                                checkedState: additionalTweaksBackend.installOnlyOffice
                                onCheckedStateChanged: additionalTweaksBackend.installOnlyOffice = checkedState
                            }

                            // development
                            Kirigami.ListSectionHeader {
                                text: translatorBackend.translate("Development", translatorBackend.language)
                                Layout.fillWidth: true
                                Layout.topMargin: 10
                            }

                            Components.OptionCheckBox {
                                labelText: translatorBackend.translate("Install Visual Studio Code", translatorBackend.language)
                                checkedState: additionalTweaksBackend.installVscode
                                onCheckedStateChanged: additionalTweaksBackend.installVscode = checkedState
                            }
                            
                            Components.OptionCheckBox {
                                labelText: translatorBackend.translate("Install CMake, LLVM, Clang and Ninja", translatorBackend.language)
                                checkedState: additionalTweaksBackend.installDevTools
                                onCheckedStateChanged: additionalTweaksBackend.installDevTools = checkedState
                            }

                            Components.OptionCheckBox {
                                labelText: translatorBackend.translate("Install Plasma SDK", translatorBackend.language)
                                checkedState: additionalTweaksBackend.installPlasmaSdk
                                onCheckedStateChanged: additionalTweaksBackend.installPlasmaSdk = checkedState
                            }

                            Components.OptionCheckBox {
                                labelText: translatorBackend.translate("Install Qt Creator", translatorBackend.language)
                                checkedState: additionalTweaksBackend.installQtCreator
                                onCheckedStateChanged: additionalTweaksBackend.installQtCreator = checkedState
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
                    text: translatorBackend.translate("Done", translatorBackend.language)
                    icon.name: "checkmark-symbolic"
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