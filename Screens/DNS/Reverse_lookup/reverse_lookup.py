from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,QTextEdit
from PyQt5.QtCore import Qt, QObject
from Service import DNS

def setup_reverse_lookup_tab(self: QObject, reverse_lookup_tab):
    button_layout = QHBoxLayout()
    search_button = QPushButton(text="Search")
    clear_button = QPushButton(text="Clear")
    button_layout.addWidget(search_button)
    button_layout.addWidget(clear_button)
    self.res_box = QTextEdit()
    self.res_box.setReadOnly(True)
    clear_button.clicked.connect(lambda: self.res_box.clear())

    search_button.setStyleSheet(
            "QPushButton {"
            "   background-color: #6EB5FF;"  # Light blue background color
            "   color: white;"                 # White text color
            "   border: none;"                 # No border
            "   padding: 8px 16px;"            # Padding for better appearance
            "}"
            "QPushButton:hover {"
            "   background-color: #4D94FF;"   # Lighter blue on hover
            "}"
            "QPushButton:pressed {"
            "   background-color: #3366CC;"    # Darker blue when pressed
            "}"
        )
    clear_button.setStyleSheet(
        "QPushButton {"
            "   background-color: lightgray;"  
            "   border: none;"  
            "   padding: 8px 16px;" 
            "}"
            "QPushButton:hover {"
            "   background-color: gray;"   # Lighter blue on hover
            "}"
    )
    self.res_box.setStyleSheet(
            "QTextEdit {"
            "   background-color: #f0f0f0;"  # Black background color
            "   color: #1a1a5c;"              # White text color
            "   border: none;"              # No border
            "   padding: 8px;"              # Padding for better appearance
            "}"
        )

    api = DNS.DNSService(reverse_lookup_tab, button=search_button, output=self.res_box)
    layout = QVBoxLayout()
    # dial = Dialog("get", "/enums/dns/lookup")

    # Add input box and dropdown list
    input_layout = QVBoxLayout()
    target_label = QLabel("Target:")
    target_input = QLineEdit()
    target_input.setPlaceholderText("ip_address")
    target_input.setStyleSheet(
            "QLineEdit { border: 1px solid lightgray; }"
            "QLineEdit:focus { border: 1px solid black; }"
        )
    target_input.setFixedHeight(40)
    input_layout.addWidget(target_label)
    input_layout.addWidget(target_input)

    response_label = QLabel("Response:")
    

    search_button.clicked.connect(lambda _: api.reverse_lookup(
        target_input.text()))
    #input_layout.addWidget(button, alignment=Qt.AlignTop)
    layout.addLayout(input_layout)
    layout.addWidget(response_label)
    layout.addWidget(self.res_box)
    layout.addLayout(button_layout)
    reverse_lookup_tab.setLayout(layout)
    # options_dropdown.setFixedWidth(int((input_layout.sizeHint().width())*0.8))

