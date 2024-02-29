from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QPushButton

def setup_scanning_tab(scanning_tab):
        # Create sub-tabs for scanning
        sub_tabs = QTabWidget()

        host_discovery_tab = QWidget()
        port_scanning_tab = QWidget()
        enumeration_tab = QWidget()

        sub_tabs.addTab(host_discovery_tab, "Host Discovery")
        sub_tabs.addTab(port_scanning_tab, "Port Scanning")
        sub_tabs.addTab(enumeration_tab, "Enumeration")

       

        # Add sub-tabs and button to the scanning tab layout
        layout = QVBoxLayout()
        layout.addWidget(sub_tabs)
        

        scanning_tab.setLayout(layout)

def setup_host_discovery_tab():
        pass
def setup_port_scanning_tab():
        pass
def setup_enumeration_tab():
        pass