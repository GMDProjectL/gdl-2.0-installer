import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import org.kde.kirigami as Kirigami
import "../components" as Components

Kirigami.Page {
    id: userProfilePage
    title: translatorBackend.translate(
        "Tell us more about yourself", 
        translatorBackend.language
    )
    signal backPressed()
    signal nextPressed()

    property bool passwordsMatch: passwordField.text === repeatPasswordField.text

    property bool allFieldsFilled: usernameField.text.length > 0 &&
                                  passwordField.text.length > 0 &&
                                  repeatPasswordField.text.length > 0 &&
                                  hostnameField.text.length > 0
    
    property bool nextButtonEnabled: allFieldsFilled && passwordsMatch

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
                            "This way, you'll be able to log into your computer right after installation.", 
                            translatorBackend.language
                        )
                    }

                    ColumnLayout {
                        Layout.fillWidth: true

                        Label {
                            text: translatorBackend.translate(
                                "Your username:", 
                                translatorBackend.language
                            )
                        }
                        TextField { 
                            id: usernameField
                            leftPadding: 10
                            Layout.fillWidth: true
                            text: userProfileBackend.username
                            onTextChanged: userProfileBackend.username = text
                        }

                        Label {
                            Layout.topMargin: 10
                            text: translatorBackend.translate(
                                "Create a password:", 
                                translatorBackend.language
                            )
                        }
                        TextField { 
                            id: passwordField
                            leftPadding: 10 
                            Layout.fillWidth: true
                            echoMode: TextInput.Password
                            text: userProfileBackend.password
                            onTextChanged: userProfileBackend.password = text
                        }

                        Label {
                            Layout.topMargin: 10
                            text: translatorBackend.translate(
                                "Repeat the password:", 
                                translatorBackend.language
                            )
                        }
                        TextField { 
                            id: repeatPasswordField
                            leftPadding: 10 
                            Layout.fillWidth: true
                            echoMode: TextInput.Password
                            text: userProfileBackend.repeatPassword
                            onTextChanged: userProfileBackend.repeatPassword = text
                        }

                        Label {
                            Layout.topMargin: 10
                            text: translatorBackend.translate(
                                "Think of the name for your computer:", 
                                translatorBackend.language
                            )
                        }

                        TextField { 
                            id: hostnameField
                            leftPadding: 10 
                            Layout.fillWidth: true
                            text: userProfileBackend.hostname
                            onTextChanged: userProfileBackend.hostname = text
                        }

                        Switch {
                            Layout.topMargin: 20
                            leftPadding: 0
                            checked: userProfileBackend.automaticLogin
                            onCheckedChanged: userProfileBackend.automaticLogin = checked
                            
                            text: translatorBackend.translate(
                                "Automatic login, only ask password when doing administrative stuff", 
                                translatorBackend.language
                            )
                        }

                        Label {
                            Layout.topMargin: 20
                            color: Kirigami.Theme.negativeTextColor
                            visible: userProfilePage.allFieldsFilled && !userProfilePage.passwordsMatch
                            text: translatorBackend.translate("Passwords do not match.", translatorBackend.language)
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