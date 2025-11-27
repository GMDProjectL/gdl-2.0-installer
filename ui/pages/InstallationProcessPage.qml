import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami
import "../components" as Components

Kirigami.Page {
    id: installationProcessPage
    title: translatorBackend.translate(
        "Installing...",
        translatorBackend.language
    )

    Rectangle {
        id: contentArea
        anchors.fill: parent
        color: Kirigami.Theme.backgroundColor
        Layout.fillWidth: true
        Layout.fillHeight: true

        ColumnLayout {
            anchors.fill: parent
            spacing: 20
            Layout.fillWidth: true
            Layout.fillHeight: true

            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                ScrollBar.vertical.policy: ScrollBar.AlwaysOn

                TextArea {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    padding: 10
                    readOnly: true
                    
                    font.family: "Adwaita Mono"
                    text: installationProcessBackend.installationLogs
                }
            }

            ColumnLayout {
                Layout.rightMargin: 20
                Layout.fillWidth: true
                spacing: 10

                ProgressBar {
                    Layout.fillWidth: true
                    value: installationProcessBackend.progress
                }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 30

                    Label { 
                        text: translatorBackend.translate("Copying base system", translatorBackend.language)
                        Layout.fillWidth: true
                        opacity: installationProcessBackend.stage >= 1 ? 1 : 0.5
                    }

                    Label { 
                        text: translatorBackend.translate("Setting up", translatorBackend.language)
                        Layout.fillWidth: true
                        opacity: installationProcessBackend.stage >= 2 ? 1 : 0.5
                    }

                    Label { 
                        text: translatorBackend.translate("Installing additional features", translatorBackend.language)
                        Layout.fillWidth: true
                        opacity: installationProcessBackend.stage >= 3 ? 1 : 0.5
                    }
                }
            }
        }
    }
}