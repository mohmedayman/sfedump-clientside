import sys
from navBar import *
from proxy import * 
from target import *
from sequencer import *
from intruder import *
from repeater import *
from decoder import *
from comparer import *
from extender import *
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
        setup_sequencer_tab(self)
        setup_decoder_tab(self)
        setup_intruder_tab(self)
        setup_repeater_tab(self)
        setup_comparer_tab(self)
        setup_extender_tab(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
