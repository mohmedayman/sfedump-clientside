import sys
from Widgets.navBar import *
from Screens.Dashboard.dashboard import *
from Screens.Proxy.proxy import *
from Screens.Target.target import *
from Screens.Sequencer.sequencer import *
from Screens.Intruder.intruder import *
from Screens.Repeater.repeater import *
from Screens.Decoder.decoder import *
from Screens.Comparer.comparer import *
from Screens.Extender.extender import *
from Screens.Network.network import *
from Screens.DNS.dns import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox, QLineEdit, QCheckBox, QListWidget, QFileDialog
from PyQt5.QtGui import QIcon


class MainApp(QMainWindow):
    def __init__(self,app):
        super().__init__()
        self.app = app

        self.setWindowTitle("Burp Suite Application")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("assets/imgs/icon.jpeg"))
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
        # setup_sequencer_tab(self)
        setup_decoder_tab(self)
        setup_intruder_tab(self)
        setup_repeater_tab(self)
        # setup_comparer_tab(self)
        setup_extender_tab(self)
        # setup_scanning_tab(self)
        # setup_sniffer_tab(self)
        # setup_exploiter_tab(self)
        setup_network_tab(self)
        setup_dashboard_tab(self)
        setup_dns_tab(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp(app)
    main_app.show()
    sys.exit(app.exec_())
