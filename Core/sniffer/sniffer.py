import subprocess


from Helpers import StoppableThread
from PyQt5 import QtCore
from typing import Optional


class NetworkSniffer(QtCore.QThread):
    output_signal = QtCore.pyqtSignal(str)
    error_signal = QtCore.pyqtSignal(str)
    kill_signal = QtCore.pyqtSignal(bool)
    terminate_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent, interface: Optional[str] = "eth0", filter_condition: Optional[str] = None):
        QtCore.QThread.__init__(self, parent)
        self.filter_condition = filter_condition
        self.interface = interface
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
        tcpdump_cmd = ['tcpdump', '-i', self.interface,
                       '-nn', '-l', '-v', '-X', self.filter_condition]
        self.process = subprocess.Popen(
            tcpdump_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Counter to track the number of packets captured

        # Read the output of tcpdump in real-time
        while not self.is_terminated:
            # Read a line from tcpdump output
            output = self.process.stdout.readline().decode().strip()

            # Process the captured packet
            if not output:
                continue

            # Implement your packet processing logic here
            self.output_signal.emit(output)

        # Wait for the tcpdump process to finish
            #self.process.wait()
