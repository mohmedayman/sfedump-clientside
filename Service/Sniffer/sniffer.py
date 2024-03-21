from Service import BaseService
from PyQt5.QtWidgets import QPushButton, QLineEdit, QTextEdit
from PyQt5.QtCore import QObject, pyqtSlot, QThreadPool
from requests import Response
from Core.sniffer import NetworkSniffer
from Widgets import ErrorDialog
from Helpers import DialogRunnable
from typing import Callable

class SnifferService(BaseService):
    def __init__(self, main: QObject, button: QPushButton, output: QTextEdit, toggle_fun:Callable) -> None:
        super().__init__(main)
        self.button = button
        self.output = output
        self.toggle_fun = toggle_fun

    def before_request(self):
        self.button.setDisabled(True)

    def onError(self):
        self.button.setDisabled(False)

    def onResponse(self, **kwargs):
        res: Response = kwargs['response']
        self.button.setDisabled(False)
        print(res)

    def start(self, interface: str, filter: str):
        if not (self.validator.isin(interface, ["eth0"], True).validate() and self.validator.string(filter, True).validate()):
            return
        self.button.setDisabled(True)

        self.worker = NetworkSniffer(self.main, interface, filter)
        self.toggle_fun()
        self.worker.start()
        self.worker.output_signal.connect(self.on_output_signal)
        self.worker.error_signal.connect(self.on_error_signal)
        self.worker.kill_signal.connect(self.on_kill_signal)

    def kill(self):
        self.worker.terminate_signal.emit("terminate")

    @pyqtSlot(str)
    def on_output_signal(self, output: str):
        self.output.append(output)

    @pyqtSlot(bool)
    def on_kill_signal(self, is_kill: bool):
        if is_kill:
            self.worker.quit()
            self.worker.exit()
            self.worker.terminate()
            self.toggle_fun(False)
            self.button.setDisabled(False)

    @pyqtSlot(str)
    def on_error_signal(self, error: str):
        self.button.setDisabled(False)
        dlg = ErrorDialog('Error Occurred', [{'message': error}])
        runnable = DialogRunnable(self, dlg)
        QThreadPool.globalInstance().start(runnable)
        self.kill()
