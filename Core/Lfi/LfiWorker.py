from Helpers import StoppableThread
from PyQt5 import QtCore
from typing import Optional
import json
import requests


class LfiWorker(QtCore.QThread):
    output_signal = QtCore.pyqtSignal(str)
    error_signal = QtCore.pyqtSignal(str)
    kill_signal = QtCore.pyqtSignal(bool)
    terminate_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent, url: str, cookies: str, is_verbose: bool = False, is_windows: bool = False):
        QtCore.QThread.__init__(self, parent)
        self.url = url
        self.is_windows = is_windows
        self.is_verbose = is_verbose
        self.cookies = cookies
        self.terminate_signal.connect(self.on_terminate_signal)
        self.is_terminated = False

    @QtCore.pyqtSlot(str)
    def on_terminate_signal(self, event: str):
        if event == "terminate":
            self.is_terminated = True
            self.kill_signal.emit(True)

            self.exit()

    def run(self):
        with open("Core/Lfi/payloads.json", 'r') as f:
            elements = json.load(f)

        if self.is_windows:
            self.output_signal.emit("[*] Using windows server payloads")
            matches = elements["windows"]
            payloads = elements['windows'].keys()
            prefixes = elements['windowsPrefix']
        else:
            self.output_signal.emit("[*] Using linux server payloads")
            matches = elements["linux"]
            payloads = elements['linux'].keys()
            prefixes = elements['linuxPrefix']

        urls = [self.url + prefix for prefix in prefixes]

        # Counter to track the number of packets captured

        self.start_engine(urls=urls, payloads=payloads, matches=matches,
                          input_cookies=self.cookies, is_verbose=self.is_verbose)

    def start_engine(self, urls, payloads, matches, input_cookies, is_verbose):

        cookies = {}
        if input_cookies:
            for cookie in input_cookies.strip().split(';'):
                name, value = cookie.split('=')
                cookies[name.strip()] = value.strip()
            self.output_signal.emit(str(cookies))
        else:
            self.output_signal.emit("[*] No cookie set, continuing...")

        count_matched = 0
        i = 0
        for payload in payloads:
            if self.is_terminated:
                break
            for url in urls:
                if self.is_terminated:
                    break
                urlTarget = url + payload
                r = requests.get(urlTarget, cookies=cookies)
                # QThread.msleep(1000)
                if is_verbose:
                    self.output_signal.emit('GET [{0}] {1}'.format(
                        r.status_code, urlTarget))

                for match in matches[payload]:
                    if self.is_terminated:
                        break
                    if match in r.text:
                        self.output_signal.emit(
                            "Interesting: " + url + payload)
                        count_matched += 1
                    if "syntax error" in r.text:
                        self.output_signal.emit("PHP error: " + url + payload)

                i = i+1

        if self.is_terminated:
            return
        if count_matched == 0:
            self.output_signal.emit("[-] Nothing found")

        self.output_signal.emit("[*] Scan completed")
