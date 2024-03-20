from Helpers.apis import API
from PyQt5.QtCore import QRunnable, QThread, QMetaObject, Q_ARG, Qt, QProcess
from requests import Response


class RequestRunnable(QRunnable):
    def __init__(self, main, method, mUrl, *args, **kwargs):
        QRunnable.__init__(self)
        self.method = method
        self.mUrl = mUrl
        self.args = args
        self.kwargs = kwargs
        self.main = main
        self.api = API()

    def run(self):

        r = self.api.request(self.method, self.mUrl,
                             *self.args, **self.kwargs)
        
        QThread.msleep(1000)
        QMetaObject.invokeMethod(self.main, "setResponse",
                                 Qt.QueuedConnection,
                                 Q_ARG(Response, r))
