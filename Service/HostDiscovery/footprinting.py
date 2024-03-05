from Service import BaseService
from PyQt5.QtWidgets import QPushButton, QLineEdit,QTextEdit
from PyQt5.QtCore import QObject
from requests import Response
from urllib.parse import urlparse

class footprintingService(BaseService):
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
        formatted_data=self.format_data(data,formatted_data)
        self.output.setText(formatted_data)

    def footprinting(self, target: str,type: str):

        if self.validator.domain(urlparse(target).netloc).validate():
            if(type=="GET"):
                self.request("get", "/host-discover/footprinting",
                            params={"url": target,"method":type})
            elif(type=="POST"):
                self.request("post", "/host-discover/footprinting",
                            params={"url": target,"method":type})
    
    def format_data(self,data,formatted_data):
        # Iterate over the keys in the data dictionary
        for key, value in data.items():
            # If the value is a dictionary, format its key-value pairs
            if isinstance(value, dict):
                formatted_data += f"[{key.capitalize()}]:\n"
                for sub_key, sub_value in value.items():
                    formatted_data += f"- {sub_key}: {sub_value}\n"
                formatted_data += "\n"
            # If the value is not a dictionary, simply add it to the formatted data
            else:
                formatted_data += f"[{key.capitalize()}]: {value}\n"

        return formatted_data

