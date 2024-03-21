from PyQt5.QtWidgets import QPushButton

class SearchButton(QPushButton):
    def __init__(self, parent=None, title:str = "Search"):
        super().__init__(parent)
        self.setText(title)
        self.setStyleSheet(
            "QPushButton {"
            "   background-color: #6EB5FF;"  # Light blue background color
            "   color: white;"                 # White text color
            "   border: none;"   
            "border-radius: 5px;"              # No border
            "   padding: 8px 16px;"            # Padding for better appearance
            "}"
            "QPushButton:hover {"
            "   background-color: #4D94FF;"   # Lighter blue on hover
            "}"
            "QPushButton:pressed {"
            "   background-color: #3366CC;"    # Darker blue when pressed
            "}"
        )

