from PyQt5.QtWidgets import QMainWindow,QVBoxLayout,QTabWidget,QWidget
from PyQt5.QtCore import Qt
from Screens.DNS.Lookup.lookup import *
from Screens.DNS.Reverse_lookup.reverse_lookup import *
from Screens.DNS.Records.records import *

def setup_dns_tab(parent):
    sub_tabs = QTabWidget()

    lookup_tab = QWidget()
    reverse_lookup_tab = QWidget()
    records_tab = QWidget()

    sub_tabs.addTab(lookup_tab, "Lookup")
    sub_tabs.addTab(reverse_lookup_tab, "Reverse lookup")
    sub_tabs.addTab(records_tab, "Records")

       

        # Add sub-tabs and button to the scanning tab layout
    layout = QVBoxLayout()
    layout.addWidget(sub_tabs)
        

    parent.dns_tab.setLayout(layout)
    setup_lookup_tab(parent, lookup_tab)
    setup_reverse_lookup_tab(parent,reverse_lookup_tab)
    setup_records_tab(parent,records_tab)