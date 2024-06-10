import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout,QTableWidget,QHeaderView, QTableWidgetItem, QInputDialog, QHBoxLayout, QLabel,QFileDialog, QLineEdit, QPushButton, QTextEdit, QWidget, QTabWidget
import requests
from PyQt5.QtCore import Qt, QObject
from Widgets.InputBox import *
from Widgets.ResponseBox import *
from Widgets.SendButton import *
from Widgets.FunctionalButton import *
from Widgets.StopButton import StopButton
from Widgets.TargetInput import *
import itertools
from urllib.parse import urlunsplit, urlparse, parse_qs
from Screens.http_request_parser import HTTPRequestParser

class PitchForkTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_PitchFork_tab()

    def setup_PitchFork_tab(self):
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

        hbox1=QHBoxLayout()
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

        hbox2=QHBoxLayout()
        self.load_payload2_button = FunctionalButton()
        self.load_payload2_button.setText("Load payload2")
        self.load_payload2_button.clicked.connect(self.load_payload2)
        hbox2.addWidget(self.load_payload2_button)
        self.generate_payload2_button = FunctionalButton()
        self.generate_payload2_button.setText("Generate Payload2")
        self.generate_payload2_button.clicked.connect(self.generate_payload2)
        hbox2.addWidget(self.generate_payload2_button)
        layout.addLayout(hbox2)

        self.PitchFork_button = SendButton()
        self.PitchFork_button.setText("Run PitchFork attack")
        self.PitchFork_button.clicked.connect(self.run_PitchFork_attack)
        layout.addWidget(self.PitchFork_button)

       # Response section
        self.response_label = QLabel("Response:")
        layout.addWidget(self.response_label)

        self.response_table = QTableWidget()
        self.response_table.setColumnCount(8)  # Add "Comment" column
        self.response_table.setHorizontalHeaderLabels(
            ["Request", "Payload1","Payload2" ,"Status code", "Response received", "Error", "Length", "Comment"]
        )
        self.response_table.itemSelectionChanged.connect(self.display_response_body)
        self.response_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.response_table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: rgb(245, 245, 245);border: 1px solid rgb(245, 245, 245); }")
        self.response_table.setAlternatingRowColors(True)
        self.response_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.response_table)

        self.response_body_label = QLabel("Response Body:")
        layout.addWidget(self.response_body_label)
        self.response_body_text = ResponseBox()
        layout.addWidget(self.response_body_text)

        self.response_bodies = []  # List to store response bodies

        self.search_button = FunctionalButton("Search response")
        self.search_button.clicked.connect(self.search_response)
        layout.addWidget(self.search_button)
        self.stop_button = StopButton()
        self.stop_button.setText("Stop PitchFork Attack")
        self.stop_button.clicked.connect(self.stop_PitchFork_attack)
        self.stop_button.setVisible(False)
        layout.addWidget(self.stop_button)
        self.response_label.setVisible(False)
        self.response_table.setVisible(False)
        self.response_body_label.setVisible(False)
        self.response_body_text.setVisible(False)
        self.search_button.setVisible(False)
        self.setLayout(layout)

    def load_payload1(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Payload1", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                self.payload1_values = [line.strip() for line in file.readlines()]
            self.payload1_text.setPlainText(",".join(self.payload1_values))

    def load_payload2(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Payload2", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r') as file:
                self.payload2_values = [line.strip() for line in file.readlines()]
            self.payload2_text.setPlainText(",".join(self.payload2_values))

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

    def run_PitchFork_attack(self):
        # Show response section
        self.response_label.setVisible(True)
        self.response_table.setVisible(True)
        self.response_body_label.setVisible(True)
        self.response_body_text.setVisible(True)
        self.search_button.setVisible(True)
        self.stop_button.setVisible(True)


        # Hide input fields and disable buttons
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
        self.PitchFork_button.setVisible(False)

        # Execute attack
        raw_request = self.raw_request_text.toPlainText()
        if not raw_request:
            QMessageBox.warning(self, "Error", "Please enter a valid HTTP request.")
            return

        if not hasattr(self, 'payload1_values') or not hasattr(self, 'payload2_values'):
            QMessageBox.warning(self, "Error", "Please load or generate both payload 1 and payload 2 files.")
            return

        max_length = max(len(self.payload1_values), len(self.payload2_values))
        self.payload1_values += [""] * (max_length - len(self.payload1_values))
        self.payload2_values += [""] * (max_length - len(self.payload2_values))

        parser = HTTPRequestParser()
        index = 0
        for value1, value2 in zip(self.payload1_values, self.payload2_values):
            updated_request = raw_request.replace("$value1$", value1).replace("$value2$", value2)
            url = parser.extract_url(updated_request)
            data = parser.extract_data(updated_request)
            parameters = parser.extract_parameters(updated_request)
            headers = parser.parse_raw_headers(updated_request)

            if not url:
                self.add_response_to_table(index, value1, value2, "-", "Invalid URL", "-", "-", "-", "-")
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

                self.add_response_to_table(index, value1, value2, response.status_code, "-", response.elapsed.microseconds / 1000, len(response.content), "-", "-")
                self.response_bodies.append(response.text)

            except Exception as e:
                self.add_response_to_table(index, value1, value2, "Error", str(e), "-", "-", "-", "-")
                self.response_bodies.append("Error: " + str(e))

            index = index + 1

    def stop_PitchFork_attack(self):
        # Hide response section
        self.response_label.setVisible(False)
        self.response_table.setVisible(False)
        self.response_body_label.setVisible(False)
        self.response_body_text.setVisible(False)
        self.search_button.setVisible(False)
        self.stop_button.setVisible(False)


        # Show input fields and enable buttons
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
        self.PitchFork_button.setVisible(True)

    def add_response_to_table(self, request, payload1,payload2, status_code, error, response_received, length,timeout ,comment):
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