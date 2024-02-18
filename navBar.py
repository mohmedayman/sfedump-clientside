import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QPushButton, QTextEdit,QTableWidget, QTableWidgetItem, QComboBox,QMessageBox,QLineEdit,QCheckBox,QListWidget,QFileDialog

def createNavBar(parent):
    # Create tabs
        parent.dashboard_tab = QWidget()
        parent.proxy_tab = QWidget()
        parent.target_tab = QWidget()
        parent.intruder_tab = QWidget()
        parent.repeater_tab = QWidget()
        #parent.sequencer_tab = QWidget()
        parent.decoder_tab = QWidget()
        #parent.comparer_tab = QWidget()
        parent.extender_tab = QWidget()
        parent.scanning_tab = QWidget()
        parent.sniffer_tab = QWidget()
        parent.exploiter_tab = QWidget()

        # Add tabs to tab widget
        parent.tabs.addTab(parent.dashboard_tab, "Dashboard")
        parent.tabs.addTab(parent.proxy_tab, "Proxy")
        parent.tabs.addTab(parent.target_tab, "Target")
        parent.tabs.addTab(parent.intruder_tab, "Intruder")
        parent.tabs.addTab(parent.repeater_tab, "Repeater")
        #parent.tabs.addTab(parent.sequencer_tab, "Sequencer")
        parent.tabs.addTab(parent.decoder_tab, "Decoder")
        #parent.tabs.addTab(parent.comparer_tab, "Comparer")
        parent.tabs.addTab(parent.extender_tab, "Extender")
        parent.tabs.addTab(parent.scanning_tab, "Scanning")
        parent.tabs.addTab(parent.sniffer_tab, "Sniffer")
        parent.tabs.addTab(parent.exploiter_tab, "Exploiter")