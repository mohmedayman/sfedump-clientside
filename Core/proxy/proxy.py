import subprocess


from Helpers import StoppableThread
from PyQt5 import QtCore
from typing import Optional
import os


class ProxyWorker(QtCore.QThread):
    output_signal = QtCore.pyqtSignal(str)
    error_signal = QtCore.pyqtSignal(str)
    kill_signal = QtCore.pyqtSignal(bool)
    terminate_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        QtCore.QThread.__init__(self, parent)

        self.terminate_signal.connect(self.on_terminate_signal)
        self.process = None
        self.is_terminated = False

    @QtCore.pyqtSlot(str)
    def on_terminate_signal(self, event: str):
        if event == "terminate":
            self.is_terminated = True
            self.process.terminate()
            self.kill_signal.emit(True)

            self.exit()

    def run(self):

        # Start capturing packets with the initial filter condition

        self.process = subprocess.Popen(
            ["mitmdump", "-q", "-s", "./script.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.getcwd()+"/Core/proxy"

        )
        while not self.is_terminated:

            output = self.process.stdout.readline().decode().strip()
            
            if not output:
                continue

            # Implement your packet processing logic here
            self.output_signal.emit(output)

        # Wait for the tcpdump process to finish
            # self.process.wait()
