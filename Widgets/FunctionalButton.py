from PyQt5.QtWidgets import QPushButton

class FunctionalButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setText("Send")
        self.setStyleSheet(
            """QPushButton {
                        background-color: #4CAF50; /* Green */
                        border: none;
                        color: white;
                        padding: 8px 16px;
                        text-align: center;
                        border-radius: 5px;
                }

                QPushButton:hover {
                    background-color: #45a049; /* Darker Green */
                }

                QPushButton:pressed {
                    background-color: #0d8050; /* Darker Green */
                }
                """
        )

