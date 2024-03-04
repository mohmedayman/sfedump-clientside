from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, QObject
from Service import DNS


def setup_lookup_tab(self: QObject, lookup_tab):
    button = QPushButton(text="Search")
    res_box = QLineEdit()

    api = DNS.DNSService(lookup_tab, button=button, output=res_box)
    layout = QVBoxLayout()
    # dial = Dialog("get", "/enums/dns/lookup")

    # Add input box and dropdown list
    input_layout = QHBoxLayout()
    target_label = QLabel("Target:")
    target_input = QLineEdit()
    input_layout.addWidget(target_label, alignment=Qt.AlignTop)
    input_layout.addWidget(target_input, alignment=Qt.AlignTop)

    input_layout.addWidget(res_box, alignment=Qt.AlignTop)

    button.clicked.connect(lambda _: api.lookup(
        target_input.text()))
    input_layout.addWidget(button, alignment=Qt.AlignTop)

    layout.addLayout(input_layout)
    lookup_tab.setLayout(layout)
    # options_dropdown.setFixedWidth(int((input_layout.sizeHint().width())*0.8))
