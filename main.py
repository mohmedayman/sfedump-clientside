import sys
from navBar import *
from Screens.Dashboard.dashboard import *
from Screens.Proxy.proxy import * 
from Screens.Target.target import *
from Screens.Sequencer.sequencer import *
from Screens.Intruder.intruder import *
from Screens.Repeater.repeater import *
from Screens.Decoder.decoder import *
from Screens.Comparer.comparer import *
from Screens.Extender.extender import *
from Screens.Scanner.scanner import *
from Screens.Sniffer.sniffer import *
from Screens.Exploiter.exploiter import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QPushButton, QTextEdit,QTableWidget, QTableWidgetItem, QComboBox,QMessageBox,QLineEdit,QCheckBox,QListWidget,QFileDialog
from PyQt5.QtGui import QIcon


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Burp Suite Application")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("icon.jpeg"))
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Create a tab widget
        self.tabs = QTabWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        main_widget.setLayout(main_layout)

        createNavBar(self)

        # Add content to tabs
        setup_proxy_tab(self)
        setup_target_tab(self)
        #setup_sequencer_tab(self)
        setup_decoder_tab(self)
        setup_intruder_tab(self)
        setup_repeater_tab(self)
        #setup_comparer_tab(self)
        setup_extender_tab(self)
        setup_scanning_tab(self)
        setup_sniffer_tab(self)
        setup_exploiter_tab(self)
        setup_dashboard_tab(self)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
