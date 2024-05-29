from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox
from PyQt5.QtCore import Qt, QObject
from PyQt5 import QtWidgets, QtGui, QtCore
from Widgets.SearchButton import *
from Widgets.ClearButton import *
from Widgets.ResponseBox import *
from Widgets.TargetInput import *
from Widgets.StopButton import *
from Service.proxy import ProxyService
from typing import Optional
from Widgets import CollapsibleBox
import random


def setup_proxy_tab(parent):

    def toggle_buttons(force_stop: Optional[bool] = None):

        search_button.setVisible(not search_button.isVisible())
        stop_button.setVisible(not stop_button.isVisible())

        if force_stop is not None:
            search_button.setVisible(not force_stop)
            stop_button.setVisible(force_stop)

    """
    res_box = ResponseBox()
    response_label = QLabel("Response:") """
    button_layout = QHBoxLayout()
    search_button = SearchButton(title="Start")
    stop_button = StopButton(title="Stop")
    clear_button = ClearButton()

    # clear_button.clicked.connect(res_box.clear_text)
    

    vlay = QtWidgets.QVBoxLayout()
    boxes_layout = QtWidgets.QVBoxLayout()
    """ for i in range(10):
        box = CollapsibleBox("Collapsible Box Header-{}".format(i))
        boxes_layout.addWidget(box)
        lay = QtWidgets.QVBoxLayout()
        for j in range(80):
            label = QtWidgets.QLabel("{}".format(j))
            color = QtGui.QColor(*[random.randint(0, 255) for _ in range(3)])
            label.setStyleSheet(
                "background-color: {}; color : white;".format(color.name())
            )
            label.setAlignment(QtCore.Qt.AlignCenter)
            lay.addWidget(label)

        box.setContentLayout(lay) """

    button_layout.addWidget(search_button)
    button_layout.addWidget(stop_button)
    button_layout.addWidget(clear_button)

    boxes_layout.addStretch()

    # vlay.addLayout(vlay)
    vlay.addLayout(button_layout)
    vlay.addLayout(boxes_layout)
    boxes_layout.setDirection(QtWidgets.QBoxLayout.Direction.TopToBottom)

    service = ProxyService(parent, button=search_button,
                           toggle_fun=toggle_buttons, output=boxes_layout)

    search_button.clicked.connect(lambda _: service.start())
    stop_button.clicked.connect(lambda: service.kill())
    clear_button.clicked.connect(lambda: service.clearOutput())

    # Hide the stop button initially
    stop_button.hide()

    parent.proxy_tab.setLayout(vlay)
