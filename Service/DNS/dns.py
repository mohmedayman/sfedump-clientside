from Service import BaseService
from PyQt5.QtWidgets import QPushButton, QLineEdit
from PyQt5.QtCore import QObject
from requests import Response


class DNSService(BaseService):
    def __init__(self, main: QObject, button: QPushButton, output: QLineEdit) -> None:
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
        self.output.setText(res.json()['data'])

    def lookup(self, target: str):

        if self.validator.domain(target).validate():

            self.request("get", "/enums/dns/lookup",
                         params={"domain_name": target})
