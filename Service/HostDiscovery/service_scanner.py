from Service import BaseService
from PyQt5.QtWidgets import QPushButton, QLineEdit, QTextEdit
from PyQt5.QtCore import QObject
from requests import Response
from Core.host_discovery import service_scanner
from PyQt5.QtCore import QRunnable, QThread, QMetaObject, Q_ARG, Qt, QProcess
from PyQt5.QtCore import pyqtSlot, QThreadPool, QObject
from Options.host_discovery import ServiceScannerEnum


class ServiceScannerService(BaseService):
    def __init__(self, main: QObject, button: QPushButton, output: QTextEdit) -> None:
        super().__init__(main)
        self.button = button
        self.output = output

    def before_request(self):
        self.button.setDisabled(True)

    def onError(self):
        self.button.setDisabled(False)

    @pyqtSlot(dict)
    def onResponse(self, data):
        self.spinner.stop()
        self.button.setDisabled(False)

        formatted_data = ""
        formatted_data = self.format_data(data, formatted_data)
        self.output.setText(formatted_data)

    def service_scanner(self, target: str, type: str):

        if not self.validator.target(target).isin(type, [e.value for e in ServiceScannerEnum]).validate():
            return

        self.before_request()
        self.spinner.start()
        runnable = Runnable(self, target, int(ServiceScannerEnum[type]))
        QThreadPool.globalInstance().start(runnable)

    def format_data(self, data, formatted_data):
        if data["os"]:
            formatted_data += "[Operating System Information]:\n"
            for os_info in data["os"]:
                for key, value in os_info.items():
                    formatted_data += f"{key}: {value}\n"
                formatted_data += "\n"
        else:
            formatted_data += "[Operating System Information]:(empty)\n"
        # Format port information
        if data["ports"]:
            formatted_data += "\n[Ports Information]:\n"
            for port_info in data["ports"]:
                formatted_data += f"Port: {port_info['portid']}\n"
                formatted_data += f"Protocol: {port_info['protocol']}\n"
                formatted_data += f"State: {port_info['state']}\n"
                formatted_data += f"Service: {port_info['service']['name']}\n"
                formatted_data += "Vulnerabilities:\n"
                for vulnerability in port_info['vulnerabilities']:
                    formatted_data += f"- {vulnerability}\n"
                formatted_data += "\n"

        else:
            formatted_data += "\n[Ports Information]:(empty)\n"

        return formatted_data


class Runnable(QRunnable):
    def __init__(self, main, target, type):
        QRunnable.__init__(self)
        self.main = main
        self.type = type
        self.target = target

    def run(self):

        r = service_scanner(self.target, self.type)

        QThread.msleep(1000)
        QMetaObject.invokeMethod(self.main, "onResponse",
                                 Qt.QueuedConnection,
                                 Q_ARG(dict, r))
