from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox
from PyQt5.QtCore import Qt, QObject

from Widgets.SearchButton import *
from Widgets.ClearButton import *
from Widgets.ResponseBox import *
from Widgets.TargetInput import *
from Service.Sniffer import SnifferService

def setup_sniffer_tab(self: QObject,sniffer_tab):
        
        input_layout = QVBoxLayout()
        gateway_input = TargetInput()
        gateway_input.setPlaceholderText("Filter Conditions")
        input_layout.addWidget(gateway_input)

        target_input = TargetInput()
        target_input.setPlaceholderText("Interface")
        target_input.setText("eth0")
        input_layout.addWidget(target_input)

        self.res_box = ResponseBox()
        
        button_layout = QHBoxLayout()
        search_button = SearchButton(title="Start")
        stop_button = SearchButton(title="Stop")
        clear_button = ClearButton()
        
        service = SnifferService(self, button=search_button, output=self.res_box)

        search_button.clicked.connect(lambda _: service.start(target_input.text(),gateway_input.text()))
        stop_button.clicked.connect(service.kill)
        clear_button.clicked.connect(self.res_box.clear_text)
        
        button_layout.addWidget(search_button)
        button_layout.addWidget(stop_button)
        button_layout.addWidget(clear_button)

        layout = QVBoxLayout()
        layout.addLayout(input_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.res_box)

        # Add the layout to the sniffer tab
        sniffer_tab.setLayout(layout)
