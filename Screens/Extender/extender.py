import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QPushButton, QTextEdit,QTableWidget, QTableWidgetItem, QComboBox,QMessageBox,QLineEdit,QCheckBox,QListWidget,QFileDialog

def setup_extender_tab(parent):
        layout = QVBoxLayout()

        # Extender label
        extender_label = QLabel("Extender")
        layout.addWidget(extender_label)

        # List widget to display loaded extensions
        parent.extension_list = QListWidget()
        layout.addWidget(parent.extension_list)

        # Load and Unload buttons
        button_layout = QHBoxLayout()
        load_button = QPushButton("Load Extension")
        unload_button = QPushButton("Unload Extension")
        configure_button = QPushButton("Configure Extension")
        run_button = QPushButton("Run Extension")

        load_button.clicked.connect(lambda:load_extension(parent))
        unload_button.clicked.connect(lambda:unload_extension(parent))
        configure_button.clicked.connect(lambda:configure_extension(parent))
        run_button.clicked.connect(lambda:run_extension(parent))

        button_layout.addWidget(load_button)
        button_layout.addWidget(unload_button)
        button_layout.addWidget(configure_button)
        button_layout.addWidget(run_button)
        layout.addLayout(button_layout)

        parent.extender_tab.setLayout(layout)

def load_extension(parent):
        pass

def unload_extension(parent):
        pass
    
def configure_extension(parent):
        pass

def run_extension(parent):
        pass
