from Service import BaseService
from PyQt5.QtWidgets import QPushButton, QLineEdit, QTextEdit
from PyQt5.QtCore import QObject, pyqtSlot, QThreadPool
from requests import Response
from Core.Lfi import LfiWorker
from Widgets import ErrorDialog
from Helpers import DialogRunnable
from typing import Callable


class LfiService(BaseService):
    def __init__(self, main: QObject, button: QPushButton, output: QTextEdit, toggle_fun: Callable) -> None:
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

    def start(self, url: str, cookies: str, is_verbose: bool = False, is_windows: bool = False):
        if not (self.validator.url(url).string(cookies, True).bool(is_verbose, True).bool(is_windows, True).validate()):
            return
        # self.button.setDisabled(True)

        self.worker = LfiWorker(self.main, url=url, cookies=cookies,is_verbose=is_verbose,is_windows=is_windows)
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
