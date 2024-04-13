import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QPushButton, QTextEdit,QTableWidget, QTableWidgetItem, QComboBox,QMessageBox,QLineEdit,QCheckBox,QListWidget,QFileDialog
from Screens.Repeater.repeater import RepeaterTab
def createNavBar(parent):
    # Create tabs
        parent.dashboard_tab = QWidget()
        parent.proxy_tab = QWidget()
        # parent.target_tab = QWidget()
        parent.intruder_tab = QWidget()
        parent.repeater_tab = RepeaterTab()
        #parent.sequencer_tab = QWidget()
        parent.decoder_tab = QWidget()
        #parent.comparer_tab = QWidget()
        parent.extender_tab = QWidget()
        parent.network_tab = QWidget()
        parent.web_vulnerability_tab = QWidget()
        parent.dns_tab = QWidget()

        # Add tabs to tab widget
        parent.tabs.addTab(parent.dashboard_tab, "Dashboard")
        parent.tabs.addTab(parent.proxy_tab, "Proxy")
        # parent.tabs.addTab(parent.target_tab, "Target")
        parent.tabs.addTab(parent.intruder_tab, "Intruder")
        parent.tabs.addTab(parent.repeater_tab, "Repeater")
        #parent.tabs.addTab(parent.sequencer_tab, "Sequencer")
        parent.tabs.addTab(parent.decoder_tab, "Decoder")
        #parent.tabs.addTab(parent.comparer_tab, "Comparer")
        parent.tabs.addTab(parent.extender_tab, "Extender")
        parent.tabs.addTab(parent.web_vulnerability_tab, "Web vulnerability")
        parent.tabs.addTab(parent.network_tab, "Network")
        parent.tabs.addTab(parent.dns_tab, "DNS")