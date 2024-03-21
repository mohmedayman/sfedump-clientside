from PyQt5.QtCore import QThread, pyqtSignal
from Service import BaseService
from PyQt5.QtWidgets import QPushButton, QTextEdit
from requests import Response
from pyqtspinner import WaitingSpinner


class portScannerService(BaseService):
    def __init__(self, main, button: QPushButton, output: QTextEdit):
        super().__init__(main)
        self.button = button
        self.output = output

    def before_request(self):
        self.button.setDisabled(True)
        print("disabled")

    def onResponse(self, **kwargs):
        response: Response = kwargs['response']
        self.button.setDisabled(False)

        if response.status_code == 200:
            self.output.setText("Successful Request")
        elif response.status_code == 400:
            self.output.setText("Bad Request")
        else:
            self.output.setText("Validation Error")

    def portScanner(self, target, type, port_list_type, ports):

        if self.validator.ip(target).validate():
            data = {"ip_address": target, "type": type,
                    "port_list_type": port_list_type, "ports": ports}
            self.request("post", "/host-discover/port-scanner",
                         json=data)
