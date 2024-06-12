import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QWidget, QTabWidget, QFileDialog,
    QMessageBox, QTableWidget, QTableWidgetItem, QInputDialog, QHeaderView
)
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QBrush
from Widgets.InputBox import InputBox
from Widgets.ResponseBox import ResponseBox
from Widgets.SendButton import SendButton
from Widgets.FunctionalButton import FunctionalButton
from Widgets.StopButton import StopButton
from Screens.http_request_parser import HTTPRequestParser
import itertools

class SniperTab(QWidget):
    def __init__(self):
        super().__init__()
        self.sniper_running = False
        self.setup_sniper_tab()

    def setup_sniper_tab(self):
        layout = QVBoxLayout()

        self.raw_request_label = QLabel("Enter HTTP Request:")
        layout.addWidget(self.raw_request_label)

        self.raw_request_text = InputBox()
        self.raw_request_text.setPlaceholderText("Enter HTTP request here with $value$ placeholder...")
        layout.addWidget(self.raw_request_text)

        self.payload_label = QLabel("Payloads (comma separated):")
        layout.addWidget(self.payload_label)

        self.payload_text = InputBox()
        self.payload_text.setPlaceholderText("payloads")
        layout.addWidget(self.payload_text)

        hbox1 = QHBoxLayout()
        self.load_payload_button = FunctionalButton()
        self.load_payload_button.setText("Load payload")
        self.load_payload_button.clicked.connect(self.load_payload)
        hbox1.addWidget(self.load_payload_button)
        self.generate_payload_button = FunctionalButton()
        self.generate_payload_button.setText("Generate Payload")
        self.generate_payload_button.clicked.connect(self.generate_payload1)
        hbox1.addWidget(self.generate_payload_button)
        layout.addLayout(hbox1)

        self.sniper_button = SendButton()
        self.sniper_button.setText("Run sniper attack")
        self.sniper_button.clicked.connect(self.run_sniper_attack)
        layout.addWidget(self.sniper_button)

        self.stop_button = StopButton("Stop sniper attack")
        self.stop_button.setText("Stop sniper attack")
        self.stop_button.clicked.connect(self.stop_sniper_attack)
        self.stop_button.setVisible(False)
        

        # Response section
        self.response_label = QLabel("Response:")
        self.response_label.setVisible(False)
        layout.addWidget(self.response_label)

        self.response_table = QTableWidget()
        self.response_table.setColumnCount(7)  # Add "Comment" column
        self.response_table.setHorizontalHeaderLabels(
            ["Request", "Payload", "Status code", "Response received", "Error", "Length", "Comment"]
        )
        self.response_table.itemSelectionChanged.connect(self.display_response_body)
        self.response_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.response_table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: rgb(245, 245, 245);border: 1px solid rgb(245, 245, 245); }")
        self.response_table.setAlternatingRowColors(True)
        self.response_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.response_table.setVisible(False)
        
        layout.addWidget(self.response_table)

        self.response_body_label = QLabel("Response Body:")
        self.response_body_label.setVisible(False)
        layout.addWidget(self.response_body_label)
        self.response_body_text = ResponseBox()
        self.response_body_text.setVisible(False)
        layout.addWidget(self.response_body_text)

        self.response_bodies = []  # List to store response bodies

        self.search_button = FunctionalButton("Search response")
        self.search_button.clicked.connect(self.search_response)
        self.search_button.setVisible(False)
        layout.addWidget(self.search_button)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

    def run_sniper_attack(self):
        self.response_table.setRowCount(0)
        self.sniper_running = True
        self.sniper_button.setVisible(False)
        self.stop_button.setVisible(True)

        self.raw_request_label.setVisible(False)
        self.raw_request_text.setVisible(False)
        self.payload_label.setVisible(False)
        self.payload_text.setVisible(False)
        self.load_payload_button.setVisible(False)
        self.generate_payload_button.setVisible(False)
        
        self.response_label.setVisible(True)
        self.response_table.setVisible(True)
        self.response_body_label.setVisible(True)
        self.response_body_text.setVisible(True)
        self.search_button.setVisible(True)

        raw_request = self.raw_request_text.toPlainText()

        if not raw_request:
            QMessageBox.warning(self, "Error", "Please enter a valid HTTP request.")
            self.stop_sniper_attack()
            return

        if not hasattr(self, 'payload_values') or not self.payload_values:
            QMessageBox.warning(self, "Error", "Please load or enter payloads.")
            self.stop_sniper_attack()
            return

        self.response_table.setRowCount(0)  # Clear previous results
        self.response_bodies = []  # Clear previous response bodies

        for index, value in enumerate(self.payload_values):
            value = value.strip()
            modified_request = raw_request.replace("$value$", value)

            parser = HTTPRequestParser()
            url = parser.extract_url(modified_request)
            data = parser.extract_data(modified_request)
            parameters = parser.extract_parameters(modified_request)
            headers = parser.parse_raw_headers(modified_request)

            if not url:
                self.add_response_to_table(index, value, "404", "Invalid URL", "-", "-", "-", "-")
                continue

            if data:
                method = "POST"
            else:
                method = "GET"

            try:
                if method == "POST":
                    response = requests.post(url, headers=headers, data=data, params=parameters)
                else:
                    response = requests.get(url, headers=headers, params=parameters)

                self.add_response_to_table(index, value, response.status_code, "-", response.elapsed.microseconds / 1000, len(response.content), "-", "-")
                self.response_bodies.append(response.text)

            except Exception as e:
                self.add_response_to_table(index, value, "Error", str(e), "-", "-", "-", "-")
                self.response_bodies.append("Error: " + str(e))

    def stop_sniper_attack(self):
        self.sniper_running = False
        self.sniper_button.setVisible(True)
        self.stop_button.setVisible(False)

        self.raw_request_label.setVisible(True)
        self.raw_request_text.setVisible(True)
        self.payload_label.setVisible(True)
        self.payload_text.setVisible(True)
        self.load_payload_button.setVisible(True)
        self.generate_payload_button.setVisible(True)
        
        self.response_label.setVisible(False)
        self.response_table.setVisible(False)
        self.response_body_label.setVisible(False)
        self.response_body_text.setVisible(False)
        self.search_button.setVisible(False)

    def load_payload(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Payload", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                self.payload_values = file.readlines()
            self.payload_text.setPlainText(",".join([value.strip() for value in self.payload_values]))

    def generate_payload1(self):
        min_length, max_length, char_set = self.get_payload_parameters()
        if min_length and max_length and char_set:
            self.payload_values = self.generate_passwords(min_length, max_length, char_set)
            self.payload_text.setPlainText(",".join(self.payload_values))

    def get_payload_parameters(self):
        min_length, ok = QInputDialog.getInt(self, "Input", "Enter the minimum length of the password:")
        if not ok:
            return None, None, None
        max_length, ok = QInputDialog.getInt(self, "Input", "Enter the maximum length of the password:")
        if not ok:
            return None, None, None
        char_set, ok = QInputDialog.getText(self, "Input", "Enter the character set (e.g., abcdefghijklmnopqrstuvwxyz0123456789):")
        if not ok:
            return None, None, None
        return min_length, max_length, char_set

    def generate_passwords(self, min_length, max_length, char_set):
        passwords = []
        for length in range(min_length, max_length + 1):
            for combination in itertools.product(char_set, repeat=length):
                passwords.append(''.join(combination))
        return passwords

    def add_response_to_table(self, request, payload, status_code, error, response_received, length, timeout, comment):
        row_position = self.response_table.rowCount()
        self.response_table.insertRow(row_position)
        self.response_table.setItem(row_position, 0, QTableWidgetItem(str(request)))
        self.response_table.setItem(row_position, 1, QTableWidgetItem(payload))
        self.response_table.setItem(row_position, 2, QTableWidgetItem(str(status_code)))
        self.response_table.setItem(row_position, 3, QTableWidgetItem(str(response_received)))
        self.response_table.setItem(row_position, 4, QTableWidgetItem(error))
        self.response_table.setItem(row_position, 5, QTableWidgetItem(str(length)))
        self.response_table.setItem(row_position, 6, QTableWidgetItem(comment))  # Add comment to table

    def display_response_body(self):
        selected_items = self.response_table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            response_body = self.response_bodies[row]
            self.response_body_text.setPlainText(response_body)

    def search_response(self):
        search_word, ok = QInputDialog.getText(self, "Search Response", "Enter the word to search for:")
        if not ok or not search_word:
            return

        for row in range(self.response_table.rowCount()):
            response_body = self.response_bodies[row]
            if search_word in response_body:
                self.response_table.setItem(row, 6, QTableWidgetItem("Found"))
            else:
                self.response_table.setItem(row, 6, QTableWidgetItem("Not Found"))

