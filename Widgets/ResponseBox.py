from PyQt5.QtWidgets import QTextEdit

class ResponseBox(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setStyleSheet(
            "QTextEdit {"
            "   background-color: #f0f0f0;"  # Black background color
            "   color: #1a1a5c;"              # White text color
            "   border: none;"              # No border
            "   padding: 8px;"              # Padding for better appearance
            "}"
        )
    def clear_text(self):
        #print("here")
        self.clear()