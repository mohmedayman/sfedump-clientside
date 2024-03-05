from PyQt5.QtWidgets import QLineEdit

class TargetInput(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
                "QLineEdit { border: 1px solid lightgray; }"
                "QLineEdit:focus { border: 1px solid black; }"
            )
        self.setFixedHeight(40)