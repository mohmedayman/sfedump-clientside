from Service import BaseService
from PyQt5.QtWidgets import QPushButton,  QVBoxLayout
from PyQt5.QtCore import QObject, pyqtSlot, QThreadPool, Qt
from requests import Response
from Core.proxy import ProxyWorker
from Widgets import ErrorDialog
from Helpers import DialogRunnable
from typing import Callable
from ast import literal_eval
from Screens.Proxy import ProxyResBox

from mitmproxy import http


class ProxyService(BaseService):
    def __init__(self, main: QObject, button: QPushButton, output: QVBoxLayout, toggle_fun: Callable) -> None:
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

    def start(self, ):

        self.button.setDisabled(True)

        # self.worker = NetworkSniffer(self.main, interface, filter)

        self.worker = ProxyWorker(self.main)
        self.toggle_fun()
        self.worker.start()
        self.worker.output_signal.connect(self.on_output_signal)
        self.worker.error_signal.connect(self.on_error_signal)
        self.worker.kill_signal.connect(self.on_kill_signal)

    def clearOutput(self):
        while self.output.count():
            child = self.output.takeAt(0)
            if child.widget():
                 child.widget().deleteLater()
        self.output.addStretch()

    
    def kill(self):
        self.worker.terminate_signal.emit("terminate")

    @pyqtSlot(str)
    def on_output_signal(self, output: str):
        output = literal_eval(output)
        # self.output.append(str(output['response']['headers']))
        box = ProxyResBox(flow_dict=output)
        self.output.insertWidget(
            len(self.output) - 1, box.generateBox(), alignment=Qt.AlignTop)

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
