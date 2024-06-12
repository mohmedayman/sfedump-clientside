import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem, QInputDialog, QHeaderView, QHBoxLayout, QLabel, QFileDialog, QLineEdit, QPushButton, QTextEdit, QWidget, QTabWidget, QMessageBox
import requests
from PyQt5.QtCore import Qt
from Widgets.InputBox import *
from Widgets.ResponseBox import *
from Widgets.SendButton import *
from Widgets.FunctionalButton import *
from Widgets.TargetInput import *
from Widgets.StopButton import StopButton
import itertools
from urllib.parse import urlunsplit, urlparse, parse_qs
from Screens.http_request_parser import HTTPRequestParser

class ClasterBombTab(QWidget):
    def __init__(self):
        super().__init__()
        self.sniper_running = False
        self.setup_ClasterBomb_tab()

    def setup_ClasterBomb_tab(self):
        layout = QVBoxLayout()

        self.raw_request_label = QLabel("Enter HTTP Request:")
        layout.addWidget(self.raw_request_label)

        self.raw_request_text = InputBox()
        self.raw_request_text.setPlaceholderText("Enter HTTP request here with $value1$ and $value2$ placeholders...")
        layout.addWidget(self.raw_request_text)

        self.payload1_label = QLabel("Payload1 (comma separated):")
        layout.addWidget(self.payload1_label)

        self.payload1_text = InputBox()
        self.payload1_text.setPlaceholderText("payload1")
        layout.addWidget(self.payload1_text)

        hbox1 = QHBoxLayout()
        self.load_payload1_button = FunctionalButton()
        self.load_payload1_button.setText("Load payload1")
        self.load_payload1_button.clicked.connect(self.load_payload1)
        hbox1.addWidget(self.load_payload1_button)
        self.generate_payload1_button = FunctionalButton()
        self.generate_payload1_button.setText("Generate Payload1")
        self.generate_payload1_button.clicked.connect(self.generate_payload1)
        hbox1.addWidget(self.generate_payload1_button)
        layout.addLayout(hbox1)

        self.payload2_label = QLabel("Payload2 (comma separated):")
        layout.addWidget(self.payload2_label)

        self.payload2_text = InputBox()
        self.payload2_text.setPlaceholderText("payload2")
        layout.addWidget(self.payload2_text)

        hbox2 = QHBoxLayout()
        self.load_payload2_button = FunctionalButton()
        self.load_payload2_button.setText("Load payload2")
        self.load_payload2_button.clicked.connect(self.load_payload2)
        hbox2.addWidget(self.load_payload2_button)
        self.generate_payload2_button = FunctionalButton()
        self.generate_payload2_button.setText("Generate Payload2")
        self.generate_payload2_button.clicked.connect(self.generate_payload2)
        hbox2.addWidget(self.generate_payload2_button)
        layout.addLayout(hbox2)

        self.ClasterBomb_button = SendButton()
        self.ClasterBomb_button.setText("Run ClasterBomb Attack")
        self.ClasterBomb_button.clicked.connect(self.toggle_clasterbomb_attack)
        layout.addWidget(self.ClasterBomb_button)

        # Response section (initially hidden)
        self.response_label = QLabel("Response:")
        self.response_label.setVisible(False)
        layout.addWidget(self.response_label)

        self.response_table = QTableWidget()
        self.response_table.setColumnCount(8)  # Add "Comment" column
        self.response_table.setHorizontalHeaderLabels(
            ["Request", "Payload1", "Payload2", "Status code", "Response received", "Error", "Length", "Comment"]
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

        self.stop_button = StopButton()
        self.stop_button.setText("Stop ClasterBomb Attack")
        self.stop_button.clicked.connect(self.stop_clasterbomb_attack)
        self.stop_button.setVisible(False)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

    def load_payload1(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Payload1", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                self.payload1_values = file.readlines()
            self.payload1_text.setPlainText(",".join([value.strip() for value in self.payload1_values]))

    def load_payload2(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Payload2", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                self.payload2_values = file.readlines()
            self.payload2_text.setPlainText(",".join([value.strip() for value in self.payload2_values]))

    def generate_payload1(self):
        min_length, max_length, char_set = self.get_payload_parameters()
        if min_length and max_length and char_set:
            self.payload1_values = self.generate_passwords(min_length, max_length, char_set)
            self.payload1_text.setPlainText(",".join(self.payload1_values))

    def generate_payload2(self):
        min_length, max_length, char_set = self.get_payload_parameters()
        if min_length and max_length and char_set:
            self.payload2_values = self.generate_passwords(min_length, max_length, char_set)
            self.payload2_text.setPlainText(",".join(self.payload2_values))

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

    def toggle_clasterbomb_attack(self):
        if self.sniper_running:
            self.stop_clasterbomb_attack()
        else:
            self.run_clasterbomb_attack()

    def run_clasterbomb_attack(self):
        raw_request = self.raw_request_text.toPlainText()
        self.response_table.setRowCount(0)
        if not raw_request:
            QMessageBox.warning(self, "Error", "Please enter a valid HTTP request.")
            return

        if not hasattr(self, 'payload1_values') or not hasattr(self, 'payload2_values'):
            QMessageBox.warning(self, "Error", "Please load or generate both payload 1 and payload 2 files.")
            return

        # Hide input fields and show response fields
        self.raw_request_label.setVisible(False)
        self.raw_request_text.setVisible(False)
        self.payload1_label.setVisible(False)
        self.payload1_text.setVisible(False)
        self.load_payload1_button.setVisible(False)
        self.generate_payload1_button.setVisible(False)
        self.payload2_label.setVisible(False)
        self.payload2_text.setVisible(False)
        self.load_payload2_button.setVisible(False)
        self.generate_payload2_button.setVisible(False)
        self.ClasterBomb_button.setVisible(False)

        self.response_label.setVisible(True)
        self.response_table.setVisible(True)
        self.response_body_label.setVisible(True)
        self.response_body_text.setVisible(True)
        self.stop_button.setVisible(True)
        self.search_button.setVisible(True)

        # self.ClasterBomb_button.setText("Stop ClasterBomb Attack")
        self.sniper_running = True

        parser = HTTPRequestParser()
        index = 0
        for value1 in self.payload1_values:
            value1 = value1.strip()
            updated1_request = raw_request.replace("$value1$", value1)

            for value2 in self.payload2_values:
                value2 = value2.strip()
                updated2_request = updated1_request.replace("$value2$", value2)

                url = parser.extract_url(updated2_request)
                data = parser.extract_data(updated2_request)
                parameters = parser.extract_parameters(updated2_request)
                headers = parser.parse_raw_headers(updated2_request)

                if not url:
                    self.add_response_to_table(index, value1, value2, "-", "Invalid URL", "-", "-", "-", "-")
                    continue

                method = "POST" if data else "GET"

                try:
                    if method == "POST":
                        response = requests.post(url, headers=headers, data=data, params=parameters)
                    else:
                        response = requests.get(url, headers=headers, params=parameters)

                    self.add_response_to_table(index, value1, value2, response.status_code, "-", response.elapsed.microseconds / 1000, len(response.content), "-", "-")
                    self.response_bodies.append(response.text)

                except Exception as e:
                    self.add_response_to_table(index, value1, value2, "Error", str(e), "-", "-", "-", "-")
                    self.response_bodies.append("Error: " + str(e))

                index += 1

    def stop_clasterbomb_attack(self):
        # Show input fields and hide response fields
        self.raw_request_label.setVisible(True)
        self.raw_request_text.setVisible(True)
        self.payload1_label.setVisible(True)
        self.payload1_text.setVisible(True)
        self.load_payload1_button.setVisible(True)
        self.generate_payload1_button.setVisible(True)
        self.payload2_label.setVisible(True)
        self.payload2_text.setVisible(True)
        self.load_payload2_button.setVisible(True)
        self.generate_payload2_button.setVisible(True)
        self.ClasterBomb_button.setVisible(True)
        

        self.response_label.setVisible(False)
        self.response_table.setVisible(False)
        self.response_body_label.setVisible(False)
        self.response_body_text.setVisible(False)
        self.search_button.setVisible(False)
        self.stop_button.setVisible(False)
        

        # self.ClasterBomb_button.setText("Run ClasterBomb Attack")
        self.sniper_running = False

    def add_response_to_table(self, request, payload1, payload2, status_code, error, response_received, length, timeout, comment):
        row_position = self.response_table.rowCount()
        self.response_table.insertRow(row_position)
        self.response_table.setItem(row_position, 0, QTableWidgetItem(str(request)))
        self.response_table.setItem(row_position, 1, QTableWidgetItem(payload1))
        self.response_table.setItem(row_position, 2, QTableWidgetItem(payload2))
        self.response_table.setItem(row_position, 3, QTableWidgetItem(str(status_code)))
        self.response_table.setItem(row_position, 4, QTableWidgetItem(str(response_received)))
        self.response_table.setItem(row_position, 5, QTableWidgetItem(error))
        self.response_table.setItem(row_position, 6, QTableWidgetItem(str(length)))
        self.response_table.setItem(row_position, 7, QTableWidgetItem(comment))  # Add comment to table

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
                self.response_table.setItem(row, 7, QTableWidgetItem("Found"))
            else:
                self.response_table.setItem(row, 7, QTableWidgetItem("Not Found"))


