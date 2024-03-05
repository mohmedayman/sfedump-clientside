from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,QTextEdit
from PyQt5.QtCore import Qt, QObject
from Service import DNS
from Widgets.SearchButton import *
from Widgets.ClearButton import *
from Widgets.ResponseBox import *
from Widgets.TargetInput import *

def setup_records_tab(self: QObject, records_tab):
    button_layout = QHBoxLayout()
    search_button =SearchButton()
    clear_button = ClearButton()
    button_layout.addWidget(search_button)
    button_layout.addWidget(clear_button)
    self.res_box = ResponseBox()
    clear_button.clicked.connect(self.res_box.clear_text)

    api = DNS.DNSRecordsService(self, button=search_button, output=self.res_box)
    layout = QVBoxLayout()
    # dial = Dialog("get", "/enums/dns/lookup")

    # Add input box and dropdown list
    input_layout = QVBoxLayout()
    target_label = QLabel("Target:")
    target_input = TargetInput()
    target_input.setPlaceholderText("domain_name")
    input_layout.addWidget(target_label)
    input_layout.addWidget(target_input)

    response_label = QLabel("Response:")
    

    search_button.clicked.connect(lambda _: api.records(
        target_input.text()))
    #input_layout.addWidget(button, alignment=Qt.AlignTop)
    layout.addLayout(input_layout)
    layout.addWidget(response_label)
    layout.addWidget(self.res_box)
    layout.addLayout(button_layout)
    records_tab.setLayout(layout)
    # options_dropdown.setFixedWidth(int((input_layout.sizeHint().width())*0.8))

