import sys
import requests
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QPlainTextEdit, QFileDialog, QMessageBox, QDialog, QWidget, QInputDialog
)
from PyQt5.QtGui import QTextCursor
from urllib.parse import urlsplit, urlunsplit
from Widgets.InputBox import *
from Widgets.ResponseBox import *
from Widgets.SendButton import *
from Widgets.FunctionalButton import *

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
        # self.modify_button = QPushButton("Modify Request")
        # self.modify_button.clicked.connect(self.modify_request)
        # button_layout.addWidget(self.modify_button)
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
        raw_request = self.request_text.toPlainText()
        method = self.get_method(raw_request)
        try:
            if method == "GET":
                url = self.extract_url(raw_request)
                response = requests.get(url)
            elif method == "POST":
                url = self.extract_url(raw_request)
                data = self.extract_data(raw_request)
                response = requests.post(url, data=data)
            else:
                QMessageBox.information(self, "Send Request", "Unsupported HTTP method.")
                return

            self.display_response(response)
        except requests.exceptions.RequestException as e:
            self.response_text.clear()
            self.response_text.insertPlainText(f"Error: {e}")

    def display_response(self, response):
        self.response_text.clear()
        self.response_text.insertPlainText(f"HTTP/{response.raw.version} {response.status_code} {response.reason}\n")
        self.response_text.insertPlainText(f"{response.headers}\n\n")
        self.response_text.insertPlainText(response.text)

#     def modify_request(self):
#         self.request_text.setReadOnly(False)
#         self.request_text.setFocus()

    def copy_as_url(self):
        raw_request = self.request_text.toPlainText()
        url = self.extract_url(raw_request)
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
            new_method = "GET" if current_method == "POST" else "POST"
            first_line_parts[0] = new_method
            lines[0] = " ".join(first_line_parts)
        return "\n".join(lines)

    def get_method(self, raw_request):
        lines = raw_request.split("\n")
        first_line_parts = lines[0].split()
        return first_line_parts[0] if first_line_parts else "GET"

    def extract_url(self, raw_request):
        lines = raw_request.split("\n")
        first_line_parts = lines[0].split()
        if len(first_line_parts) >= 2:
            method, path = first_line_parts[0], first_line_parts[1]
            host = None
            for line in lines[1:]:
                if line.lower().startswith("host:"):
                    host = line.split(":", 1)[1].strip()
                    break
            if host:
                scheme = "https" if "https://" in path else "http"
                url = urlunsplit((scheme, host, path, "", ""))
                return url
        return None

    def extract_data(self, raw_request):
        lines = raw_request.split("\n")
        data_line = None
        for line in lines[1:]:
            if line.lower().startswith("content-type: application/x-www-form-urlencoded"):
                data_line = line
                break
        if data_line:
            return data_line.split(":", 1)[1].strip()
        return None

    def parse_raw_headers(self, raw_request):
        headers = {}
        lines = raw_request.split("\n")
        for line in lines[1:]:
            if not line.strip():
                break  # Stop when an empty line is encountered
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()
        return headers
    
    def convert_to_python_request(self, raw_request):
        lines = raw_request.split('\n')
        method, url, *_ = lines[0].split()
        headers = {}
        data = None

        # Parse headers and data
        for line in lines[1:]:
                if not line.strip():
                        break
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()
        if method == 'POST':
                data = lines[-1]

        # Format into Python code snippet
        python_code = f"import requests\n\n"
        python_code += f"url = '{url}'\n"
        python_code += f"headers = {headers}\n"
        if data:
                python_code += f"data = '{data}'\n"
        else:
                python_code += f"data = None\n"
        python_code += f"response = requests.{method.lower()}(url, headers=headers, data=data)\n"
        python_code += f"print(response.text)"

        return python_code


    def search_response(self):
        text_to_find, ok = QInputDialog.getText(self, "Search", "Enter text to find in the response:")
        if ok:
                text_to_find = str(text_to_find)
                if text_to_find:
                        cursor = self.response_text.textCursor()
                        found = False
                        while cursor.hasSelection():
                                cursor.movePosition(QTextCursor.NextWord, QTextCursor.KeepAnchor)
                                if text_to_find in cursor.selectedText():
                                        found = True
                                        self.response_text.setTextCursor(cursor)
                                        self.response_text.ensureCursorVisible()
                                        QMessageBox.information(self, "Search", f"Text found: {text_to_find}")
                                        break
                        if not found:
                                QMessageBox.information(self, "Search", f"Text not found: {text_to_find}")




