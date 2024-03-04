

from abc import abstractmethod
from Helpers import API,Validator,RequestRunnable, DialogRunnable
from pyqtspinner import WaitingSpinner
from PyQt5.QtCore import pyqtSlot, QThreadPool, QObject
from requests import Response
from PyQt5.QtCore import QObject
from Widgets import ErrorDialog


class BaseService(QObject):
    def __init__(self, main: QObject):
        super(BaseService, self).__init__()
        self.api = API()
        self.main = main
        self.validator = Validator(main)
        self.spinner = WaitingSpinner(main)

    @abstractmethod
    def before_request(self):
        pass

    @abstractmethod
    def onResponse(self, **kwargs):
        pass

    @abstractmethod
    def onError(self):
        pass

    def request(self, method, url, *args, **kwargs):
        runnable = RequestRunnable(
            self, method, url, *args, **kwargs)

        self.before_request()
        self.spinner.start()
        QThreadPool.globalInstance().start(runnable)

    @pyqtSlot(Response)
    def setResponse(self, data: Response):
        self.spinner.stop()
        if not data.ok:
            json = data.json()
            dlg = ErrorDialog(json.get(
                'detail', 'Error Occurred'), json.get('errors', {}))
            runnable = DialogRunnable(self, dlg)
            QThreadPool.globalInstance().start(runnable)
            
            self.onError()

        else:
            self.onResponse(**{"response": data})

        # self.adjustSize()
