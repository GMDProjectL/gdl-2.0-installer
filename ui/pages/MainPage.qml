import QtQuick 2.15
import QtQuick.Controls 2.15
import org.kde.kirigami as Kirigami
import "../components" as Components

Kirigami.Page {
    id: mainPage
    title: translatorBackend.translate("Welcome to Project GDL Installer!", translatorBackend.language)

    Column {
        spacing: 16

        Components.TestLabel {}

        Button {
            text: "Switch Language (RU/EN)"
            onClicked: {
                if (translatorBackend.language === "ru") {
                    translatorBackend.language = "en"
                } else {
                    translatorBackend.language = "ru"
                }
            }
        }
    }
}
