from Service import BaseService
from PyQt5.QtWidgets import QPushButton, QLineEdit, QTextEdit
from PyQt5.QtCore import QObject
from requests import Response
from Core.host_discovery import ip_scanner
from PyQt5.QtCore import QRunnable, QThread, QMetaObject, Q_ARG, Qt, QProcess
from PyQt5.QtCore import pyqtSlot, QThreadPool, QObject
from Options.host_discovery import IPScannerEnum

class IPScannerService(BaseService):
    def __init__(self, main: QObject, button: QPushButton, output: QTextEdit) -> None:
        super().__init__(main)
        self.button = button
        self.output = output

    def before_request(self):
        self.button.setDisabled(True)

    def onError(self):
        self.button.setDisabled(False)

    @pyqtSlot(list)
    def onResponse(self, data):
        self.spinner.stop()

        self.button.setDisabled(False)

        formatted_data = '\n'.join(data)
        self.output.setText(formatted_data)

    def ip_scanner(self, target: str, type: str):

        
        if not self.validator.target(target).isin(type, [e.value for e in IPScannerEnum]).validate():
            return
        
        self.before_request()
        self.spinner.start()
        runnable = Runnable(self, target, int(IPScannerEnum[type]))
        QThreadPool.globalInstance().start(runnable)


class Runnable(QRunnable):
    def __init__(self, main, target, type):
        QRunnable.__init__(self)
        self.main = main
        self.type = type
        self.target = target

    def run(self):

        r = ip_scanner(self.target, self.type)

        QThread.msleep(1000)
        QMetaObject.invokeMethod(self.main, "onResponse",
                                 Qt.QueuedConnection,
                                 Q_ARG(list, r))
