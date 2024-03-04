from typing import Optional, List
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QLabel, QTextEdit, QDialogButtonBox, QVBoxLayout


class ErrorDialog(QDialog):
    def __init__(self, title: Optional[str], errors: Optional[List[dict]], *args, **kwargs):
        QDialog.__init__(self, *args, **kwargs)
        layout = QVBoxLayout()

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)

        # label = QLabel(title)

        errors = "\n".join(
            list(map(lambda dic: dic.get("message", ""), errors)))

        text_box = QTextEdit(errors)
        text_box.setReadOnly(True)

        # layout.addWidget(label)
        layout.addWidget(text_box)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)
        self.setWindowTitle(title)

        self.show()
