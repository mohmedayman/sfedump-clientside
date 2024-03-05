from PyQt5.QtWidgets import QPushButton

class ClearButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Clear")
        self.setStyleSheet(
            """QPushButton {
                background-color: #cccccc;     /* Darker gray background */
                border: none;                  /* No border */
                border-radius: 5px;            /* Rounded corners */
                padding: 8px 16px;             /* Padding for better appearance */
            }

            QPushButton:hover {
                background-color: #b3b3b3;    /* Slightly lighter gray background on hover */
            }

            QPushButton:pressed {
                background-color: #999999;     /* Even darker gray when pressed */
            }
            """
        )

