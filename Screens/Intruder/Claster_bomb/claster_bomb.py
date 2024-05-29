import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QWidget, QTabWidget
import requests
from PyQt5.QtCore import Qt, QObject
from Widgets.InputBox import *
from Widgets.ResponseBox import *
from Widgets.SendButton import *
from Widgets.FunctionalButton import *
from Widgets.TargetInput import *
from urllib.parse import urlunsplit, urlparse, parse_qs
from Screens.http_request_parser import HTTPRequestParser

class ClasterBombTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ClasterBomb_tab()

    def setup_ClasterBomb_tab(self):
        layout = QVBoxLayout()

        self.raw_request_label = QLabel("Enter HTTP Request:")
        layout.addWidget(self.raw_request_label)

        self.raw_request_text = InputBox()
        self.raw_request_text.setPlaceholderText("HTTP Request")
        layout.addWidget(self.raw_request_text)

        self.payload_label = QLabel("Payloads (comma separated):")
        layout.addWidget(self.payload_label)

        self.payload_text = InputBox()
        self.payload_text.setPlaceholderText("payloads")
        layout.addWidget(self.payload_text)

        self.ClasterBomb_button = SendButton()
        self.ClasterBomb_button.setText("Run ClasterBomb attack")
        self.ClasterBomb_button.clicked.connect(self.run_ClasterBomb_attack)
        layout.addWidget(self.ClasterBomb_button)

        # Response section
        self.response_label = QLabel("Response:")
        layout.addWidget(self.response_label)
        self.response_text = ResponseBox()
        layout.addWidget(self.response_text)

        self.search_button = FunctionalButton("Search response")
        self.search_button.clicked.connect(self.search_response)
        layout.addWidget(self.search_button)

        

        self.setLayout(layout)

    def run_ClasterBomb_attack(self):
        raw_request = self.raw_request_text.toPlainText()
        payload_values = self.payload_text.toPlainText().split(',')
        # search_string = self.search_string_input.text()

        for value in payload_values:
            value = value.strip()
            modified_request = raw_request.replace("$value$", value, 1)

            parser = HTTPRequestParser()
            url = parser.extract_url(modified_request)
            data = parser.extract_data(modified_request)
            parameters = parser.extract_parameters(modified_request)
            headers = parser.parse_raw_headers(modified_request)

            self.response_text.append(f"URL: {url}")
            self.response_text.append(f"Data: {data}")
            self.response_text.append(f"Parameters: {parameters}")
            self.response_text.append(f"Headers: {headers}")

            if data:
                method = "POST"
            else:
                method = "GET"

            try:
                if method == "POST":
                    response = requests.post(url, headers=headers, data=data, params=parameters)
                else:
                    response = requests.get(url, headers=headers, params=parameters)

                self.response_text.append(f"Response Status Code: {response.status_code}")
                self.response_text.append(f"Response Content Length: {len(response.content)}")
                self.response_text.append(f"Response Body: {response.text}")

            except Exception as e:
                self.response_text.append(f"Error: {str(e)}")

    def search_response(self):
        self.response_text.search_response(self)