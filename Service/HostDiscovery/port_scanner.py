from PyQt5.QtCore import QThread, pyqtSignal
from Service import BaseService
from PyQt5.QtWidgets import QPushButton, QTextEdit
import requests
from pyqtspinner import WaitingSpinner

class PortScannerWorker(QThread):
    finished = pyqtSignal(object)

    def __init__(self, target, type, port_list_type, ports):
        super().__init__()
        self.target = target
        self.type = type
        self.port_list_type = port_list_type
        self.ports = ports

    def run(self):
        data = {"ip_address": self.target, "type": self.type, "port_list_type": self.port_list_type, "ports": self.ports}
        response = requests.post("https://khantarish.com/api/v1/host-discover/port-scanner", json=data)
        self.finished.emit(response)

class portScannerService(BaseService):
    def __init__(self, main, button, output):
        super().__init__(main)
        self.button = button
        self.output = output
        self.spinner2 = WaitingSpinner(main)
        self.worker = None  # Initialize worker as an instance variable

    def before_request(self):
        self.button.setDisabled(True)
        self.spinner2.start()
        print("disabled")

    def onResponse(self, response):
        self.spinner2.stop()
        self.button.setDisabled(False)
        print("enabled")
        if response.status_code == 200:
            self.output.setText("Successful Request")
        elif response.status_code == 400:
            self.output.setText("Bad Request")
        else:
            self.output.setText("Validation Error")

    def portScanner(self, target, type, port_list_type, ports):
        self.before_request()
        print(target)
        print(type)
        print(port_list_type)
        for port in ports:
            print(port)
        if self.validator.ip(target).validate():
            self.worker = PortScannerWorker(target, type, port_list_type, ports)
            self.worker.finished.connect(self.onResponse)
            self.worker.start()
