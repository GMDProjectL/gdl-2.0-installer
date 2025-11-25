pragma ComponentBehavior: Bound
import QtQuick
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami

import "pages" as Pages

Kirigami.ApplicationWindow {
    id: root

    width: 900
    height: 600

    title: translatorBackend.translate("Project GDL Installer", translatorBackend.language)

    Component {
        id: aboutPage
        About {}
    }

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
                console.log("Next from MainPage")
                var newPage = testPageComponent.createObject(root.pageStack)
                root.pageStack.replace(newPage)
            }
        }
    }

    Component {
        id: testPageComponent
        Pages.TestPage {
            onBackPressed: {
                console.log("Back from TestPage")
                var newPage = mainPageComponent.createObject(root.pageStack)
                root.pageStack.replace(newPage)
            }
        }
    }

    pageStack.initialPage: mainPageComponent
}
