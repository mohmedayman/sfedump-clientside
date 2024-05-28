import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QWidget, QTabWidget,QFileDialog
import requests
from PyQt5.QtCore import Qt, QObject
from Widgets.InputBox import *
from Widgets.ResponseBox import *
from Widgets.SendButton import *
from Widgets.FunctionalButton import *
from Widgets.TargetInput import *
from urllib.parse import urlunsplit, urlparse, parse_qs
from Screens.http_request_parser import HTTPRequestParser

class SniperTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_sniper_tab()

    def setup_sniper_tab(self):
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

        self.load_payload_button = FunctionalButton()
        self.load_payload_button.setText("Load playload")
        self.load_payload_button.clicked.connect(self.load_payload)
        layout.addWidget(self.load_payload_button)

        self.sniper_button = SendButton()
        self.sniper_button.setText("Run sniper attack")
        self.sniper_button.clicked.connect(self.run_sniper_attack)
        layout.addWidget(self.sniper_button)

        # Response section
        self.response_label = QLabel("Response:")
        layout.addWidget(self.response_label)
        self.response_text = ResponseBox()
        layout.addWidget(self.response_text)

        self.search_button = FunctionalButton("Search response")
        self.search_button.clicked.connect(self.search_response)
        layout.addWidget(self.search_button)

        

        self.setLayout(layout)

    def load_payload(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Payload", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                self.payload_values = file.readlines()
            self.payload_text.setPlainText(",".join([value.strip() for value in self.payload_values]))

    def run_sniper_attack(self):
        raw_request = self.raw_request_text.toPlainText()
        # payload_values = self.payload_text.toPlainText().split(',')
        # search_string = self.search_string_input.text()

        if not raw_request:
            QMessageBox.warning(self, "Error", "Please enter a valid HTTP request.")
            return

        if not self.payload_values:
            QMessageBox.warning(self, "Error", "Please load or enter payloads.")
            return

        for value in self.payload_values:
            value = value.strip()
            modified_request = raw_request.replace("$value$", value)

            parser = HTTPRequestParser()
            url = parser.extract_url(modified_request)
            data = parser.extract_data(modified_request)
            parameters = parser.extract_parameters(modified_request)
            headers = parser.parse_raw_headers(modified_request)

            if not url:
                self.response_text.append("Error: Invalid URL.")
                continue

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