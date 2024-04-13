from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,QTextEdit,QComboBox
from PyQt5.QtCore import Qt, QObject
from Service.HostDiscovery import service_scanner
from Widgets.SearchButton import *
from Widgets.ClearButton import *
from Widgets.ResponseBox import *
from Widgets.TargetInput import *
from Options.host_discovery import ServiceScannerEnum

def setup_service_scanner_tab(self: QObject, service_scanner_tab):
    button_layout = QHBoxLayout()
    search_button = SearchButton()
    clear_button = ClearButton()
    button_layout.addWidget(search_button)
    button_layout.addWidget(clear_button)
    self.res_box = ResponseBox()
    clear_button.clicked.connect(self.res_box.clear_text)

    api = service_scanner.ServiceScannerService(self, button=search_button, output=self.res_box)
    layout = QVBoxLayout()
    # dial = Dialog("get", "/enums/dns/service_scanner")

    # Add input box and dropdown list
    input_layout = QVBoxLayout()
    target_label = QLabel("Target:")
    target_input = TargetInput()
    target_input.setPlaceholderText("domain_name")
    input_layout.addWidget(target_label)
    input_layout.addWidget(target_input)
    type_list_label = QLabel("Method:")
    type_list=QComboBox()
    type_list.setFixedHeight(30)
    options=[e.value for e in ServiceScannerEnum]
    #type_list.currentIndexChanged.connect()
    type_list.addItems(options)
    input_layout.addWidget(type_list_label)
    input_layout.addWidget(type_list)
    response_label = QLabel("Response:")
    

    search_button.clicked.connect(lambda _: api.service_scanner(
        target_input.text(),type_list.currentText()))
    #print(type_list.currentText())
    #input_layout.addWidget(button, alignment=Qt.AlignTop)
    layout.addLayout(input_layout)
    layout.addWidget(response_label)
    layout.addWidget(self.res_box)
    layout.addLayout(button_layout)
    service_scanner_tab.setLayout(layout)
    # options_dropdown.setFixedWidth(int((input_layout.sizeHint().width())*0.8))
