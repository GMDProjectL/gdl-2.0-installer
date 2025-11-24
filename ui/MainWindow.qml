import QtQuick
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami

import "pages" as Pages

Kirigami.ApplicationWindow {
    id: root

    minimumWidth: 900
    minimumHeight: 600

    width: minimumWidth
    height: minimumHeight

    title: translatorBackend.translate("Project GDL Installer", translatorBackend.language)

    pageStack.initialPage: Pages.MainPage {}
}
