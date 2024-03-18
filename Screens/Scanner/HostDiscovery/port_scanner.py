from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,QTextEdit,QComboBox
from PyQt5.QtCore import Qt, QObject
from Service.HostDiscovery import port_scanner
from Widgets.SearchButton import *
from Widgets.ClearButton import *
from Widgets.ResponseBox import *
from Widgets.TargetInput import *
from Widgets.SendButton import *

def setup_port_scanner_tab(self: QObject, port_scanner_tab):
    def onPortListTypeChanged(index):
        if index == 0:  # Top selected
            self.ports_number_label.show()
            self.ports_values_textbox.setPlaceholderText("ports_number")
            self.ports_values_label.hide()
        elif index == 1:  # Values selected
            self.ports_number_label.hide()
            self.ports_values_label.show()
            # self.ports_values_textbox.show()
            self.ports_values_textbox.setPlaceholderText("ports_values")
    
    def clearInputs():
        self.res_box.clear_text()
        self.ports_values_textbox.clear()
        self.target_input.clear()


    
    button_layout = QHBoxLayout()
    search_button = SendButton()
    clear_button = ClearButton()
    button_layout.addWidget(search_button)
    button_layout.addWidget(clear_button)
    self.res_box = ResponseBox()
    clear_button.clicked.connect(clearInputs)
    #clear_button.clicked.connect(self.)

    api = port_scanner.portScannerService(self, button=search_button, output=self.res_box)
    layout = QVBoxLayout()
    # dial = Dialog("get", "/enums/dns/port_scanner")

    # Add input box and dropdown list
    input_layout = QVBoxLayout()
    target_label = QLabel("Target")
    self.target_input = TargetInput()
    self.target_input.setPlaceholderText("ip_address")
    input_layout.addWidget(target_label)
    input_layout.addWidget(self.target_input)
    type_list_label = QLabel("Scanner type:")
    type_list=QComboBox()
    type_list.setFixedHeight(30)
    options=["connect","SYN","UDP","ACK","FIN","XMAS"]
    #type_list.currentIndexChanged.connect()
    type_list.addItems(options)
    type_list_label2 = QLabel("Port list type:")
    type_list2=QComboBox()
    type_list2.setFixedHeight(30)
    type_list2.currentIndexChanged.connect(onPortListTypeChanged)
    options2=["top","values"]
    self.ports_number_label = QLabel("Ports Number:")
    # self.ports_values_textbox=TargetInput()
    self.ports_values_label = QLabel("Ports Values (Enter values separated by comma e.g 1,2,3):")
    self.ports_values_textbox=TargetInput()
    #type_list.currentIndexChanged.connect()
    type_list2.addItems(options2)
    input_layout.addWidget(type_list_label)
    input_layout.addWidget(type_list)
    input_layout.addWidget(type_list_label2)
    input_layout.addWidget(type_list2)
    input_layout.addWidget(self.ports_number_label)
    input_layout.addWidget(self.ports_values_label)
    input_layout.addWidget(self.ports_values_textbox)
    search_button.clicked.connect(lambda _: api.portScanner(
        self.target_input.text(),type_list.currentText(),type_list2.currentText(),self.ports_values_textbox.text().split(',')))
    #print(type_list.currentText())
    #input_layout.addWidget(button, alignment=Qt.AlignTop)
    response_label = QLabel("Response:")
    layout.addLayout(input_layout)
    layout.addWidget(response_label)
    layout.addWidget(self.res_box)
    layout.addLayout(button_layout)
    port_scanner_tab.setLayout(layout)
    # options_dropdown.setFixedWidth(int((input_layout.sizeHint().width())*0.8))
