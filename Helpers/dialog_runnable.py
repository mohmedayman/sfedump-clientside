from Helpers.apis import API
from PyQt5.QtCore import QRunnable, QThread, QMetaObject, Q_ARG, Qt
from requests import Response


class DialogRunnable(QRunnable):
    def __init__(self,main, dialog):
        QRunnable.__init__(self)
        self.dialog = dialog
        self.main = main
       

    def run(self):

        self.dialog.exec()
        