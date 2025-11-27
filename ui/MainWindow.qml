pragma ComponentBehavior: Bound
import QtQuick
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami

import "pages" as Pages

Kirigami.ApplicationWindow {
    id: root

    minimumWidth: 900
    minimumHeight: 600

    height: minimumHeight
    width: minimumWidth

    title: translatorBackend.translate("Project GDL Installer", translatorBackend.language)

    Component {
        id: aboutPage
        About {}
    }

    property bool exitConfirmationDialogActive: false

    Component {
        id: exitConfirmationDialogComponent
        ExitConfirmation {
            onRefuseClosing: {
                root.exitConfirmationDialogActive = false
            }
        }
    }

    Component {
        id: installConfirmationDialogComponent
        InstallConfirmation {
            onYes: {
                root.pageStack.clear()
                root.pageStack.push(installationProcessPageComponent)
            }
        }
    }

    onClosing: {
        if (root.exitConfirmationDialogActive) {
            return
        }
        var exitDialog = exitConfirmationDialogComponent.createObject(root)
        exitDialog.open()
        root.exitConfirmationDialogActive = true
        close.accepted = false
    }

    pageStack.defaultColumnWidth: width
    pageStack.globalToolBar.showNavigationButtons: Kirigami.ApplicationHeaderStyle.NoNavigationButtons

    globalDrawer: Kirigami.GlobalDrawer {
        isMenu: true
        actions: [
            Kirigami.Action {
                id: aboutAction
                icon.name: "help-about-symbolic"
                text: translatorBackend.translate("About", translatorBackend.language)
                onTriggered: {
                    root.pageStack.layers.push(aboutPage)
                }
            },
            Kirigami.Action {
                id: exitAction
                icon.name: "application-exit-symbolic"
                text: translatorBackend.translate("Exit", translatorBackend.language)
                onTriggered: Qt.quit()
            }
        ]
    }

    Component {
        id: mainPageComponent
        Pages.MainPage {
            onNextPressed: {
                root.pageStack.push(userProfilePageComponent)
            }
        }
    }

    Component {
        id: userProfilePageComponent
        Pages.UserProfilePage {
            onBackPressed: {
                root.pageStack.goBack()
            }
            onNextPressed: {
                root.pageStack.push(destinationPageComponent)
            }
        }
    }

    Component {
        id: destinationPageComponent
        Pages.DestinationPage {
            onBackPressed: {
                root.pageStack.goBack()
            }
            onNextPressed: {
                root.pageStack.push(additionalTweaksPageComponent)
            }
        }
    }

    Component {
        id: additionalTweaksPageComponent
        Pages.AdditionalTweaksPage {
            onBackPressed: {
                root.pageStack.goBack()
            }
            onDonePressed: {
                var installDialog = installConfirmationDialogComponent.createObject(root)
                installDialog.open()
            }
        }
    }

    Component {
        id: installationProcessPageComponent
        Pages.InstallationProcessPage {}
    }

    pageStack.initialPage: mainPageComponent
}
