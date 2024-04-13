from PyQt5.QtWidgets import QTextEdit

class InputBox(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
                "QTextEdit { border: 1px solid lightgray; }"
                "QTextEdit:focus { border: 1px solid black; }"
            )
        # self.setFixedHeight(100)