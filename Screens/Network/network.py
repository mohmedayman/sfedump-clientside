from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QPushButton
from Screens.Scanner.scanner import *
from Screens.Sniffer.sniffer import *
from Screens.Exploiter.exploiter import *

def setup_network_tab(parent):
    sub_tabs = QTabWidget()

    sniffer_tab = QWidget()
    scanning_tab = QWidget()
    exploiter_tab = QWidget()

    sub_tabs.addTab(scanning_tab, "Scanning")
    sub_tabs.addTab(sniffer_tab, "Sniffer")
    sub_tabs.addTab(exploiter_tab, "Exploiter")

       

        # Add sub-tabs and button to the scanning tab layout
    layout = QVBoxLayout()
    layout.addWidget(sub_tabs)
        

    parent.network_tab.setLayout(layout)
    setup_scanning_tab(scanning_tab)
    setup_sniffer_tab(sniffer_tab)
    setup_exploiter_tab(exploiter_tab)