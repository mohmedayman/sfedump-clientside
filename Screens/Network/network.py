from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QPushButton

from Screens.Network.Scanner.scanner import *
from Screens.Network.Sniffer.sniffer import *
from Screens.Vulnerability_scanning.vulnerability_scanning import *
from Screens.Network.Exploiter.exploiter import *
from Screens.Network.MITM import *


def setup_network_tab(parent):
    parent.sub_tabs = QTabWidget()

    sniffer_tab = QWidget()
    scanning_tab = QWidget()
    mitm_tab = QWidget()
    vulnerability_scanning_tab = QWidget()

    parent.sub_tabs.addTab(scanning_tab, "Scanning")
    parent.sub_tabs.addTab(vulnerability_scanning_tab, "Vulnerability scanning")
    parent.sub_tabs.addTab(sniffer_tab, "Sniffer")
    parent.sub_tabs.addTab(mitm_tab, "MITM")
       

        # Add sub-tabs and button to the scanning tab layout

    layout = QVBoxLayout()
    layout.addWidget(parent.sub_tabs)

    parent.network_tab.setLayout(layout)
    setup_scanning_tab(parent, scanning_tab)

    setup_sniffer_tab(parent,sniffer_tab)
    setup_mitm_tab(parent,mitm_tab)
    #setup_exploiter_tab(exploiter_tab)

    setup_vulnerability_scanning_tab(parent,vulnerability_scanning_tab)

