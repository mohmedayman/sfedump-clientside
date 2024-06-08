from PyQt5.QtWidgets import QMainWindow,QVBoxLayout,QTabWidget,QWidget
from PyQt5.QtCore import Qt
from Screens.Intruder.Sniper.sniper import SniperTab
from Screens.Intruder.Claster_bomb.claster_bomb import ClasterBombTab
from Screens.Intruder.Pitch_fork.pitch_fork import PitchForkTab

def setup_intruder_tab(parent):
    sub_tabs = QTabWidget()

    sniper_tab = SniperTab()
    claster_bom_tab = ClasterBombTab()
    pitch_fork_tab = PitchForkTab()
    # pitch_fork_tab=QWidget()

    sub_tabs.addTab(sniper_tab, "Sniper")
    sub_tabs.addTab(claster_bom_tab, "Claster bom")
    sub_tabs.addTab(pitch_fork_tab, "Pitch fork")

       

        # Add sub-tabs and button to the scanning tab layout
    layout = QVBoxLayout()
    layout.addWidget(sub_tabs)
        

    parent.intruder_tab.setLayout(layout)
    # setup_sniper_tab(parent, sniper_tab)
    # setup_claster_bom_tab(parent,claster_bom_tab)
    # setup_pitch_fork_tab(parent,pitch_fork_tab)