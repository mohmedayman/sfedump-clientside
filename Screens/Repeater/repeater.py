import sys
import requests
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QPlainTextEdit, QFileDialog, QMessageBox, QDialog, QWidget, QInputDialog
)
from PyQt5.QtGui import QTextCursor, QTextCharFormat
import webbrowser
from bs4 import BeautifulSoup
from urllib.parse import urlsplit, urlunsplit
from Widgets.InputBox import *
from Widgets.ResponseBox import *
from Widgets.SendButton import *
from Widgets.FunctionalButton import *
from PyQt5.QtCore import QRunnable, QThread, QMetaObject, Q_ARG, Qt, QProcess
from PyQt5.QtCore import pyqtSlot, QThreadPool, QObject
from Screens.http_request_parser import HTTPRequestParser

class RepeaterTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Request section
        request_layout = QVBoxLayout()
        self.request_label = QLabel("Enter HTTP Request:")
        request_layout.addWidget(self.request_label)
        self.request_text = InputBox()
        self.request_text.setPlaceholderText("HTTP Request")
        request_layout.addWidget(self.request_text)
        layout.addLayout(request_layout)

        # Buttons related to request
        button_layout = QHBoxLayout()
        self.send_button = SendButton("Send Request")
        self.send_button.clicked.connect(self.send_request)
        button_layout.addWidget(self.send_button)
        layout.addLayout(button_layout)

        # Response section
        self.response_label = QLabel("Response:")
        layout.addWidget(self.response_label)
        self.response_text = ResponseBox()
        layout.addWidget(self.response_text)

        # Buttons related to response
        response_button_layout = QHBoxLayout()
        self.copy_as_url_button = FunctionalButton("Copy as URL")
        self.copy_as_url_button.clicked.connect(self.copy_as_url)
        response_button_layout.addWidget(self.copy_as_url_button)
        self.copy_as_python_button = FunctionalButton("Copy as Python Request")
        self.copy_as_python_button.clicked.connect(self.copy_as_python_request)
        response_button_layout.addWidget(self.copy_as_python_button)
        layout.addLayout(response_button_layout)

        # Other buttons
        other_buttons_layout = QHBoxLayout()
        self.toggle_method_button = FunctionalButton("Toggle Method")
        self.toggle_method_button.clicked.connect(self.toggle_method)
        other_buttons_layout.addWidget(self.toggle_method_button)
        self.pretty_print_button = FunctionalButton("Pretty Print")
        self.pretty_print_button.clicked.connect(self.pretty_print_response)
        other_buttons_layout.addWidget(self.pretty_print_button)
        self.render_response_button = FunctionalButton("Render Response")
        self.render_response_button.clicked.connect(self.render_response)
        other_buttons_layout.addWidget(self.render_response_button)
        self.search_button = FunctionalButton("Search response")
        self.search_button.clicked.connect(self.search_response)
        other_buttons_layout.addWidget(self.search_button)
        layout.addLayout(other_buttons_layout)

        self.setLayout(layout)

    def send_request(self):
        raw_request = self.request_text.toPlainText().strip()
        parser = HTTPRequestParser()

        url = parser.extract_url(raw_request)
        method = self.get_method(raw_request).upper()
        data = parser.extract_data(raw_request)
        parameters = parser.extract_parameters(raw_request)
        headers = parser.parse_raw_headers(raw_request)

        if not url:
            QMessageBox.information(self, "Send Request", "Invalid URL in the request.")
            return


        try:
            if method == "GET":
                response = requests.get
                runnable = Runnable(self, response, url, headers=headers, params=parameters)
                QThreadPool.globalInstance().start(runnable)
            elif method == "POST":
                url = parser.extract_url(raw_request)
                data = parser.extract_data(raw_request)

                response = requests.post
                runnable = Runnable(self, response, url, headers=headers, data=data, params=parameters)
                QThreadPool.globalInstance().start(runnable)
            else:
                QMessageBox.information(self, "Send Request", "Unsupported HTTP method.")
                return
        except requests.exceptions.RequestException as e:
            self.response_text.clear()
            self.response_text.insertPlainText(f"Error: {e}")

    @pyqtSlot(requests.Response)
    def display_response(self, response):
        self.response_text.clear()
        self.response_text.insertPlainText(
            f"HTTP/{response.raw.version} {response.status_code} {response.reason}\n")
        
        # Display headers as key-value pairs
        for key, value in response.headers.items():
            self.response_text.insertPlainText(f"\"{key}\": {value}\n")
        
        self.response_text.insertPlainText("\n")
        self.response_text.insertPlainText(response.text)

    def copy_as_url(self):
        raw_request = self.request_text.toPlainText()
        parser = HTTPRequestParser()
        url = parser.extract_url(raw_request)
        if url:
            QApplication.clipboard().setText(url)
            QMessageBox.information(self, "Copy as URL", f"URL copied to clipboard:\n{url}")

    def toggle_method(self):
        raw_request = self.request_text.toPlainText()
        toggled_request = self.toggle_http_method(raw_request)
        self.request_text.setPlainText(toggled_request)

    def copy_as_python_request(self):
        raw_request = self.request_text.toPlainText()
        python_request = self.convert_to_python_request(raw_request)
        QApplication.clipboard().setText(python_request)
        QMessageBox.information(self, "Copy as Python Request", "Python request script copied to clipboard.")

    def render_response(self):
        response_text = self.response_text.toPlainText()
        with open("response.html", "w") as f:
            f.write(response_text)
        webbrowser.open("response.html")
        # No webbrowser.open() used

    def pretty_print_response(self):
        response_text = self.response_text.toPlainText()
        try:
            pretty_response = json.dumps(json.loads(response_text), indent=4)
            self.response_text.clear()
            self.response_text.insertPlainText(pretty_response)
        except json.JSONDecodeError:
            QMessageBox.information(self, "Pretty Print", "Response is not in JSON format.")

    def toggle_http_method(self, raw_request):
        lines = raw_request.split("\n")
        first_line_parts = lines[0].split()
        if len(first_line_parts) >= 3:
            current_method = first_line_parts[0]
            new_method = "GET" if current_method.upper() == "POST" else "POST"
            first_line_parts[0] = new_method
            lines[0] = " ".join(first_line_parts)
        return "\n".join(lines)

    def get_method(self, raw_request):
        lines = raw_request.split("\n")
        first_line_parts = lines[0].split()
        return first_line_parts[0] if first_line_parts else "GET"

    def convert_to_python_request(self, raw_request):
        parser = HTTPRequestParser()
        url = parser.extract_url(raw_request)
        method = self.get_method(raw_request).upper()
        headers = parser.parse_raw_headers(raw_request)
        data = parser.extract_data(raw_request)

        python_code = f"import requests\n\n"
        python_code += f"url = '{url}'\n"
        python_code += f"headers = {json.dumps(headers, indent=4)}\n"
        if data:
            python_code += f"data = {json.dumps(data)}\n"
        else:
            python_code += f"data = None\n"
        python_code += f"response = requests.{method.lower()}(url, headers=headers, data=data)\n"
        python_code += f"print(response.text)"

        return python_code
    
    def search_response(self):
        self.response_text.search_response(self)


class Runnable(QRunnable):
    def __init__(self, main, callable,  *args, **kwargs):
        QRunnable.__init__(self)
        self.main = main
        self.args = args
        self.kwargs = kwargs
        self.callable = callable

    def run(self):

        r = self.callable(*self.args, **self.kwargs)

        QThread.msleep(1000)
        QMetaObject.invokeMethod(self.main, "display_response",
                                 Qt.QueuedConnection,
                                 Q_ARG(requests.Response, r))
