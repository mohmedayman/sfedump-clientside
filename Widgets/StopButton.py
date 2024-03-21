from PyQt5.QtWidgets import QPushButton

class StopButton(QPushButton):
    def __init__(self, parent=None, title:str = "Stop"):
        super().__init__(parent)
        self.setText(title)
        self.setStyleSheet(
            "QPushButton {"
            "   background-color: #FF6E6E;"      # Red background color
            "   color: white;"                    # White text color
            "   border: none;"
            "   border-radius: 5px;"              # No border
            "   padding: 8px 16px;"               # Padding for better appearance
            "}"
            "QPushButton:hover {"
            "   background-color: #FF4D4D;"       # Lighter red on hover
            "}"
            "QPushButton:pressed {"
            "   background-color: #CC3333;"       # Darker red when pressed
            "}"
        )

