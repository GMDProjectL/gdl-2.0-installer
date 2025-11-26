import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import org.kde.kirigami as Kirigami
import "../components" as Components

Kirigami.Page {
    id: testPage
    title: translatorBackend.translate(
        "Welcome to Project GDL Installer!", 
        translatorBackend.language
    )
    signal backPressed()
    signal nextPressed()

    Components.TestLabel {}

    Button {
        text: "Back"
        onClicked: {
            testPage.backPressed()
        }
    }
}