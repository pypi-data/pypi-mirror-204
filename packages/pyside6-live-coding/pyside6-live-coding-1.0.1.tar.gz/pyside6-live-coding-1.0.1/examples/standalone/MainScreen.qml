import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window
import example.module

Item {
  id: root

  Calculator {
    id: calc
    in1: Number(in1Input.text)
    in2: Number(in2Input.text)
  }

  Rectangle {
    anchors.fill: parent
    anchors.margins: 10
    color: "green"

    Row {
      anchors.centerIn: parent
      spacing: 10

      TextInput {
        id: in1Input
        text: "50"
      }

      Text {
        text: "+"
      }

      TextInput {
        id: in2Input
        text: "4"
      }

      Text {
        text: "="
      }

      Text {
        text: calc.out
      }
    }
  }
}
