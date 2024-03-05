from Service import BaseService
from PyQt5.QtWidgets import QPushButton, QLineEdit,QTextEdit
from PyQt5.QtCore import QObject
from requests import Response


class IPScannerService(BaseService):
    def __init__(self, main: QObject, button: QPushButton, output: QTextEdit) -> None:
        super().__init__(main)
        self.button = button
        self.output = output

    def before_request(self):
        self.button.setDisabled(True)

    def onError(self):
        self.button.setDisabled(False)

    def onResponse(self, **kwargs):
        res: Response = kwargs['response']
        self.button.setDisabled(False)
        data = res.json()['data']
        formatted_data = '\n'.join(data)
        self.output.setText(formatted_data)

    def ip_scanner(self, target: str,type: str):

        if self.validator.ip(target).validate():
            self.request("get", "/host-discover/ip-scanner",
                         params={"ip_address": target,"type":type})
