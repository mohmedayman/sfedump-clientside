from Service import BaseService
from PyQt5.QtWidgets import QPushButton, QLineEdit, QTextEdit
from PyQt5.QtCore import QObject, pyqtSlot, QThreadPool
from requests import Response
from Core.mitm import Arper
from Widgets import ErrorDialog
from Helpers import DialogRunnable


class MITMService(BaseService):
    def __init__(self, main: QObject, button: QPushButton, output: QTextEdit) -> None:
        super().__init__(main)
        self.button = button
        self.output = output
        self.proc = None

    def before_request(self):
        self.button.setDisabled(True)

    def onError(self):
        self.button.setDisabled(False)

    def onResponse(self, **kwargs):
        res: Response = kwargs['response']
        self.button.setDisabled(False)
        print(res)

    def start(self, target: str, gateway: str):
        if not (self.validator.ip(target).validate() and self.validator.ip(gateway).validate()):
            return
        self.button.setDisabled(True)

        self.worker = Arper(self.main, target, gateway, "eth0", True)
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
            self.output.append("TERMINATED")
            self.worker.quit()
            self.worker.exit()
            #self.worker.terminate()
            self.button.setDisabled(False)

    @pyqtSlot(str)
    def on_error_signal(self, error: str):
        self.button.setDisabled(False)
        dlg = ErrorDialog('Error Occurred', [{'message': error}])
        runnable = DialogRunnable(self, dlg)
        QThreadPool.globalInstance().start(runnable)
        self.kill()
