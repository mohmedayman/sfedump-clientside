from PyQt5.QtWidgets import QMainWindow,QVBoxLayout,QHBoxLayout,QLabel,QLineEdit,QComboBox
from PyQt5.QtCore import Qt

def setup_reverse_lookup_tab(reverse_lookup_tab):
    layout = QVBoxLayout()
        # Add input box and dropdown list
    input_layout = QHBoxLayout()
    target_label = QLabel("Target:")
    target_input = QLineEdit()
    input_layout.addWidget(target_label,alignment=Qt.AlignTop)
    input_layout.addWidget(target_input,alignment=Qt.AlignTop)

    options_label = QLabel("Options:")
    options_dropdown = QComboBox()
    options_dropdown.addItem("Option 1")
    options_dropdown.addItem("Option 2")
    options_dropdown.addItem("Option 3")
    
    input_layout.addWidget(options_label,alignment=Qt.AlignTop)
    input_layout.addWidget(options_dropdown,alignment=Qt.AlignTop)

    layout.addLayout(input_layout)
    reverse_lookup_tab.setLayout(layout)
    options_dropdown.setFixedWidth(int((input_layout.sizeHint().width())*0.8))