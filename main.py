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
from Screens.Web_vulnerability.Web_vulnerability import *
from Screens.Web_vulnerability.JWT.jwt import *
from Screens.DNS.dns import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QTableWidget, QTableWidgetItem, QComboBox, QMessageBox, QLineEdit, QCheckBox, QListWidget, QFileDialog
from PyQt5.QtGui import QIcon


class MainApp(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.scroll = QtWidgets.QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()

        self.setWindowTitle("Penteration testing platform")

        self.setGeometry(100, 100, 1200, 850)
        self.setWindowIcon(QIcon("assets/images/icon.jpeg"))
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Create a tab widget
        self.tabs = QTabWidget()
        #main_layout = QVBoxLayout()
        self.vbox.addWidget(self.tabs)
        self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        createNavBar(self)

        # Add content to tabs
        setup_proxy_tab(self)
        # setup_target_tab(self)
        # setup_sequencer_tab(self)
        setup_decoder_tab(self)
        setup_intruder_tab(self)
        # setup_repeater_tab()
        # setup_comparer_tab(self)
        setup_extender_tab(self)
        # setup_scanning_tab(self)
        # setup_sniffer_tab(self)
        # setup_exploiter_tab(self)
        setup_web_vulnerability_tab(self)
        setup_jwt_tab(self)
        setup_network_tab(self)
        # setup_dashboard_tab(self)
        setup_dns_tab(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp(app)
    main_app.show()
    sys.exit(app.exec_())
