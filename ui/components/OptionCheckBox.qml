import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import org.kde.kirigami as Kirigami

CheckBox {
    property alias labelText: check.text
    property alias checkedState: check.checked
    
    id: check
    
    topPadding: Kirigami.Units.gridUnit / 2
    bottomPadding: Kirigami.Units.gridUnit / 2
    
    Layout.fillWidth: true
}