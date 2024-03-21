from Service import BaseService
from PyQt5.QtWidgets import QPushButton, QLineEdit,QTextEdit
from PyQt5.QtCore import QObject
from requests import Response


class ZoneTranferService(BaseService):
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
        formatted_data = ""

        if isinstance(data, list):
            if data:
                formatted_data = ""
                for item in data:
                    formatted_data += f"\"Name\": {item['name']}\n"
                    formatted_data += f"\"Code\": {item['code']}\n"
                    formatted_data += f"\"Data\": {item['data']}\n\n"
            else:
                formatted_data = "(empty)"
        else:
            formatted_data = str(data)

        self.output.setText(formatted_data)



    def zone_tranfer(self, target: str):

        if self.validator.domain(target).validate():

            self.request("get", "/enums/zone-transfer",
                         params={"domain": target})
