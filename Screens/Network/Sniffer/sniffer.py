from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox
from PyQt5.QtCore import Qt, QObject

from Widgets.SearchButton import *
from Widgets.ClearButton import *
from Widgets.ResponseBox import *
from Widgets.TargetInput import *
from Widgets.StopButton import *
from Service.Sniffer import SnifferService
from typing import Optional

def setup_sniffer_tab(self: QObject, sniffer_tab):
        def toggle_buttons(force_stop:Optional[bool] = None):
            
            search_button.setVisible(not search_button.isVisible())
            stop_button.setVisible(not stop_button.isVisible())

            if force_stop is not None:    
                    search_button.setVisible(not force_stop)
                    stop_button.setVisible(force_stop)
        
        input_layout = QVBoxLayout()
        gateway_label = QLabel("Filter Conditions:")
        gateway_input = TargetInput()
        gateway_input.setPlaceholderText("Filter Conditions")
        input_layout.addWidget(gateway_label)
        input_layout.addWidget(gateway_input)
        target_label = QLabel("Target:")
        target_input = TargetInput()
        target_input.setPlaceholderText("Interface")
        target_input.setText("eth0")
        input_layout.addWidget(target_label)
        input_layout.addWidget(target_input)

        self.res_box = ResponseBox()
        response_label = QLabel("Response:")
        button_layout = QHBoxLayout()
        search_button = SearchButton(title="Start")
        stop_button = StopButton(title="Stop")
        clear_button = ClearButton()
        
        service = SnifferService(self, button=search_button, output=self.res_box, toggle_fun = toggle_buttons)


        search_button.clicked.connect(lambda _: service.start(target_input.text(), gateway_input.text()))
        stop_button.clicked.connect(lambda: service.kill())
        clear_button.clicked.connect(self.res_box.clear_text)
        
        button_layout.addWidget(search_button)
        button_layout.addWidget(stop_button)
        button_layout.addWidget(clear_button)

        layout = QVBoxLayout()
        layout.addLayout(input_layout)
        layout.addWidget(response_label)
        layout.addWidget(self.res_box)
        layout.addLayout(button_layout)

        # Hide the stop button initially
        stop_button.hide()

        # Add the layout to the sniffer tab
        sniffer_tab.setLayout(layout)
