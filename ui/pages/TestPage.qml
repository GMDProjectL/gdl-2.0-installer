import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
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