from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox, QTextEdit, QSpacerItem, QSizePolicy
from Widgets.InputBox import *
from Widgets.ResponseBox import *
from Widgets.SendButton import *
from Widgets.FunctionalButton import *
from Widgets.TargetInput import *
from Widgets.CheckBox import *
from Service.Web_vulnerability import open_redirect
from Service.Web_vulnerability import click_jacking
from Options.web_vulnerability import ExtraTypeEnum
from Service.Web_vulnerability import ExtraService



class DashboardWidget(QWidget):
    def __init__(self, parent=None):
        super(DashboardWidget, self).__init__(parent)

        # Main layout
        main_layout = QVBoxLayout(self)

        # Left side - Vulnerabilities section
        left_layout = QVBoxLayout()
        url_layout=QVBoxLayout()
        vulnerabilities_layout = QVBoxLayout()
        target_label = QLabel("URL:")
        self.target_input = TargetInput()
        self.target_input.setPlaceholderText("domain name")
        self.label=QLabel("Select vulnerabilities:")
        self.Open_redirect_checkbox = CheckBox("Open redirect")
        self.Click_jacking_checkbox = CheckBox("Click jacking")
        self.XSS_checkbox = CheckBox("XSS")
        self.XXE_checkbox = CheckBox("XXE")
        self.XPathcheckbox = CheckBox("XPath")
        self.SSTI_checkbox = CheckBox("SSTI")
        self.CRLF_checkbox = CheckBox("CRLF")
        self.CachePoisoning_checkbox = CheckBox("Cache poisoning")
        self.Bypass403_checkbox = CheckBox("Bypass403")
        url_layout.addWidget(target_label)
        url_layout.addWidget(self.target_input)
        vulnerabilities_layout.addWidget(self.label)
        vulnerabilities_layout.addWidget(self.Open_redirect_checkbox)
        vulnerabilities_layout.addWidget(self.Click_jacking_checkbox)
        vulnerabilities_layout.addWidget(self.XSS_checkbox)
        vulnerabilities_layout.addWidget(self.XXE_checkbox)
        vulnerabilities_layout.addWidget(self.XPathcheckbox)
        vulnerabilities_layout.addWidget(self.SSTI_checkbox)
        vulnerabilities_layout.addWidget(self.CRLF_checkbox)
        vulnerabilities_layout.addWidget(self.CachePoisoning_checkbox)
        vulnerabilities_layout.addWidget(self.Bypass403_checkbox)
        left_layout.addLayout(url_layout)
        left_layout.addLayout(vulnerabilities_layout)


        buttons_layout = QVBoxLayout()
        self.select_all_button = FunctionalButton("Select All")
        self.start_button = SendButton("Start")
        self.start_button.setText("start")
        buttons_layout.addWidget(self.select_all_button)
        buttons_layout.addWidget(self.start_button)
        left_layout.addLayout(buttons_layout)

        left_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addLayout(left_layout,1)

        # Right side - Text edit box
        right_layout = QVBoxLayout()
        self.response_label = QLabel("Response:")
        self.text_edit = ResponseBox()
        right_layout.addWidget(self.response_label)
        right_layout.addWidget(self.text_edit)
        main_layout.addLayout(right_layout,1)
        #apis
        self.api1 = open_redirect.OpenRedirectService(self, button=self.start_button, output=self.text_edit)
        self.api2=click_jacking.ClickJackingService(self, button=self.start_button, output=self.text_edit)
        self.api3 = ExtraService(self, button=self.start_button, output=self.text_edit, type=ExtraTypeEnum.xxe)
        self.api4 = ExtraService(self, button=self.start_button, output=self.text_edit, type=ExtraTypeEnum.xss)
        self.api5 = ExtraService(self, button=self.start_button, output=self.text_edit, type=ExtraTypeEnum.xpath)
        self.api6 = ExtraService(self, button=self.start_button, output=self.text_edit, type=ExtraTypeEnum.ssti)
        self.api7 = ExtraService(self, button=self.start_button, output=self.text_edit, type=ExtraTypeEnum.crlf)
        self.api8 = ExtraService(self, button=self.start_button, output=self.text_edit, type=ExtraTypeEnum.cache_poisoning)
        self.api9 = ExtraService(self, button=self.start_button, output=self.text_edit, type=ExtraTypeEnum.bypass_403)



        # Connect buttons to functions
        self.select_all_button.clicked.connect(self.select_all_vulnerabilities)
        self.start_button.clicked.connect(self.start_vulnerabilities)

    def select_all_vulnerabilities(self):
        self.Open_redirect_checkbox.setChecked(True)
        self.Click_jacking_checkbox.setChecked(True)
        self.XSS_checkbox.setChecked(True)
        self.XXE_checkbox.setChecked(True)
        self.XPathcheckbox.setChecked(True)
        self.SSTI_checkbox.setChecked(True)
        self.CRLF_checkbox.setChecked(True)
        self.CachePoisoning_checkbox.setChecked(True)
        self.Bypass403_checkbox.setChecked(True)

    def start_vulnerabilities(self):
        # Code to start the selected vulnerabilities
        if self.Open_redirect_checkbox.isChecked():
            self.api1.open_redirect(
            self.target_input.text())
        if self.Click_jacking_checkbox.isChecked():
            self.api2.clickJacking(self.target_input.text(),"true")
        if self.XSS_checkbox.isChecked():
            self.api4.request_extra(self.target_input.text())
        if self.XXE_checkbox.isChecked():
            self.api3.request_extra(self.target_input.text())
        if self.XPathcheckbox.isChecked():
            self.api5.request_extra(self.target_input.text())
        if self.SSTI_checkbox.isChecked():
            self.api6.request_extra(self.target_input.text())
        if self.CRLF_checkbox.isChecked():
            self.api7.request_extra(self.target_input.text())
        if self.CachePoisoning_checkbox.isChecked():
            self.api8.request_extra(self.target_input.text())
        if self.Bypass403_checkbox.isChecked():
            self.api9.request_extra(self.target_input.text())