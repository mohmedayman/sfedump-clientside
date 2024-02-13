import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QPushButton, QTextEdit,QTableWidget, QTableWidgetItem, QComboBox,QMessageBox,QLineEdit,QCheckBox,QListWidget,QFileDialog
from PyQt5.QtGui import QIcon

def setup_target_tab(parent):
        layout = QVBoxLayout()

        # Target label
        target_label = QLabel("Target")
        layout.addWidget(target_label)

        # Host and port input fields
        host_label = QLabel("Host:")
        parent.host_input = QTextEdit()
        layout.addWidget(host_label)
        layout.addWidget(parent.host_input)

        port_label = QLabel("Port:")
        parent.port_input = QTextEdit()
        layout.addWidget(port_label)
        layout.addWidget(parent.port_input)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        clear_button = QPushButton("Clear")

        save_button.clicked.connect(lambda:save_target(parent))
        clear_button.clicked.connect(lambda:clear_target(parent))

        button_layout.addWidget(save_button)
        button_layout.addWidget(clear_button)
        layout.addLayout(button_layout)

        # Display table button
        display_button = QPushButton("Display Hosts Table")
        display_button.clicked.connect(lambda:display_table(parent))
        layout.addWidget(display_button)

        parent.target_tab.setLayout(layout)

    # Table widget for displaying hosts and ports
        parent.table_widget = QTableWidget()
        parent.table_widget.setColumnCount(2)
        parent.table_widget.setHorizontalHeaderLabels(["Host", "Port"])

def save_target(parent):
        host = parent.host_input.toPlainText()
        port = parent.port_input.toPlainText()
        if host and port:
            # Add data to the table
            row_position = parent.table_widget.rowCount()
            parent.table_widget.insertRow(row_position)
            parent.table_widget.setItem(row_position, 0, QTableWidgetItem(host))
            parent.table_widget.setItem(row_position, 1, QTableWidgetItem(port))

            print(f"Saved target: Host - {host}, Port - {port}")
            # You can add logic here to save the target to a file or database
        else:
            print("Please provide both host and port.")

def clear_target(parent):
        parent.host_input.clear()
        parent.port_input.clear()

def display_table(parent):
        parent.table_widget.setWindowIcon(QIcon('icon.jpeg'))
        parent.table_widget.show()