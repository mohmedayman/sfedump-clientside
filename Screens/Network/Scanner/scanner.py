from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QPushButton
from Screens.Network.Scanner.HostDiscovery.host_discovery import *
from PyQt5.QtCore import Qt, QObject


def setup_scanning_tab(self: QObject,scanning_tab):
        # Create sub-tabs for scanning
        self.sub_tabs = QTabWidget()

        host_discovery_tab = QWidget()
        port_scanning_tab = QWidget()
        enumeration_tab = QWidget()

        self.sub_tabs.addTab(host_discovery_tab, "Host Discovery")
        self.sub_tabs.addTab(port_scanning_tab, "Port Scanning")
        self.sub_tabs.addTab(enumeration_tab, "Enumeration")

       

        # Add sub-tabs and button to the scanning tab layout
        layout = QVBoxLayout()
        layout.addWidget(self.sub_tabs)
        

        scanning_tab.setLayout(layout)
        setup_host_discovery_tab(scanning_tab,host_discovery_tab)
def setup_port_scanning_tab():
        pass
def setup_enumeration_tab():
        pass