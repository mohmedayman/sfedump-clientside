from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QTabWidget,QWidget
from PyQt5.QtCore import Qt, QObject
from Service import DNS
from Widgets.SearchButton import *
from Widgets.ClearButton import *
from Widgets.ResponseBox import *
from Widgets.TargetInput import *
from Screens.Scanner.HostDiscovery.ip_scanner import *
from Screens.Scanner.HostDiscovery.port_scanner import *
from Screens.Scanner.HostDiscovery.service_scanner import *
from Screens.Scanner.HostDiscovery.footprinting import *

def setup_host_discovery_tab(self: QObject, host_discovery_tab):
     # Create sub-tabs for scanning
        self.sub_tabs = QTabWidget()

        ip_scanner_tab = QWidget()
        port_scanner_tab = QWidget()
        service_scanner_tab = QWidget()
        footprinting_tab = QWidget()

        self.sub_tabs.addTab(ip_scanner_tab, "Ip scanner")
        self.sub_tabs.addTab(port_scanner_tab, "Port Scanner")
        self.sub_tabs.addTab(service_scanner_tab, "Service scanner")
        self.sub_tabs.addTab(footprinting_tab, "Footprinting")

       

        # Add sub-tabs and button to the scanning tab layout
        layout = QVBoxLayout()
        layout.addWidget(self.sub_tabs)
        

        host_discovery_tab.setLayout(layout)
        setup_ip_scanner_tab(host_discovery_tab,ip_scanner_tab)
        setup_port_scanner_tab(host_discovery_tab,port_scanner_tab)
        setup_service_scanner_tab(host_discovery_tab,service_scanner_tab)
        setup_footprinting_tab(host_discovery_tab,footprinting_tab)
        
