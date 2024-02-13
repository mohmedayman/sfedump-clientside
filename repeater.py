import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QPushButton, QTextEdit,QTableWidget, QTableWidgetItem, QComboBox,QMessageBox,QLineEdit,QCheckBox,QListWidget,QFileDialog

def setup_repeater_tab(parent):
        layout = QVBoxLayout()

        # Repeater label
        repeater_label = QLabel("Repeater")
        layout.addWidget(repeater_label)

        # Request and response text areas
        parent.repeater_request_text_edit = QTextEdit()
        parent.repeater_response_text_edit = QTextEdit()
        layout.addWidget(QLabel("Request:"))
        layout.addWidget(parent.repeater_request_text_edit)
        layout.addWidget(QLabel("Response:"))
        layout.addWidget(parent.repeater_response_text_edit)

        # HTTP methods combo box
        parent.http_methods_combo = QComboBox()
        parent.http_methods_combo.addItems(["GET", "POST", "PUT", "DELETE"])
        layout.addWidget(parent.http_methods_combo)

        # Headers input
        parent.headers_label = QLabel("Headers:")
        parent.headers_text_edit = QTextEdit()
        layout.addWidget(parent.headers_label)
        layout.addWidget(parent.headers_text_edit)

        # Content type combo box
        parent.content_type_combo = QComboBox()
        parent.content_type_combo.addItems(["application/json", "application/xml", "text/plain"])
        layout.addWidget(QLabel("Content Type:"))
        layout.addWidget(parent.content_type_combo)

        # Authentication input
        parent.auth_label = QLabel("Authentication:")
        parent.username_input = QLineEdit()
        parent.password_input = QLineEdit()
        parent.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(parent.auth_label)
        layout.addWidget(parent.username_input)
        layout.addWidget(parent.password_input)

        # Send, Save, and Clear buttons
        button_layout = QHBoxLayout()
        send_button = QPushButton("Send")
        save_button = QPushButton("Save")
        clear_button = QPushButton("Clear")

        send_button.clicked.connect(lambda:send_request(parent))
        save_button.clicked.connect(lambda:save_request(parent))
        clear_button.clicked.connect(lambda:clear_fields(parent))

        button_layout.addWidget(send_button)
        button_layout.addWidget(save_button)
        button_layout.addWidget(clear_button)
        layout.addLayout(button_layout)

        parent.repeater_tab.setLayout(layout)

def send_request(parent):
       #logic
       pass

def save_request(parent):
        # Placeholder for saving the request to a file
        pass

def clear_fields(parent):
        # Clearing the request and response text areas
        parent.repeater_request_text_edit.clear()
        parent.repeater_response_text_edit.clear()
        parent.headers_text_edit.clear()
        parent.username_input.clear()
        parent.password_input.clear()
    
