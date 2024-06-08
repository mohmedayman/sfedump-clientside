from PyQt5.QtWidgets import QCheckBox

class CheckBox(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setText("Send")
        self.setStyleSheet(
            """QCheckBox {
    color: #333333;
    font-size: 14px;
    font-weight: bold;
    padding: 5px;
}
"""
        )

