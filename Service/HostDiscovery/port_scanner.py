from PyQt5.QtCore import QThread, pyqtSignal
from Service import BaseService
from PyQt5.QtWidgets import QPushButton, QTextEdit
from requests import Response
from pyqtspinner import WaitingSpinner
from Core.host_discovery import port_scanner
from PyQt5.QtCore import QRunnable, QThread, QMetaObject, Q_ARG, Qt, QProcess
from PyQt5.QtCore import pyqtSlot, QThreadPool, QObject
from Options.host_discovery import PortScannerEnum, PortListTypeEnum


class portScannerService(BaseService):
    def __init__(self, main, button: QPushButton, output: QTextEdit):
        super().__init__(main)
        self.button = button
        self.output = output

    def before_request(self):
        self.button.setDisabled(True)

    @pyqtSlot(list)
    def onResponse(self, data):
        self.spinner.stop()
        self.button.setDisabled(False)

        formatted_data = '\n'.join(data)
        self.output.setText(formatted_data)

    def portScanner(self, target, type, port_list_type, ports):
        is_validated = self.validator \
            .target(target) \
            .isin(port_list_type, [e.value for e in PortListTypeEnum]) \
            .isin(type, [e.value for e in PortScannerEnum]) \
            .validate()
        if not is_validated:
            return
            """ data = {"ip_address": target, "type": type,
                    "port_list_type": port_list_type, "ports": ports}
            self.request("post", "/host-discover/port-scanner",
                         json=data) """
        port_type = PortListTypeEnum[port_list_type]

        if port_type == PortListTypeEnum.top and int(ports[0]) > 1000:
            ports[0] = 1000

        self.before_request()
        self.spinner.start()
        runnable = Runnable(self, target, int(
            PortScannerEnum[type]), int(port_type), ports)
        QThreadPool.globalInstance().start(runnable)


class Runnable(QRunnable):
    def __init__(self, main, target, type, portType, ports):
        QRunnable.__init__(self)
        self.main = main
        self.type = type
        self.target = target
        self.portType = portType
        self.ports = ports

    def run(self):

        r = port_scanner(self.target, self.type, self.portType, self.ports)

        QThread.msleep(1000)
        QMetaObject.invokeMethod(self.main, "onResponse",
                                 Qt.QueuedConnection,
                                 Q_ARG(list, r))
