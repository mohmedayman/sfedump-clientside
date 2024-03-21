from typing import Optional, List
import validators as validators
from Helpers import DialogRunnable
from PyQt5.QtCore import QThreadPool, QObject
from Widgets import ErrorDialog
import re

class Validator():
    def __init__(self, parent):
        self.errors = []
        self.parent = parent

    def domain(self, domain: Optional[str], nullable: Optional[bool] = False):
        if nullable and not domain:
            return self

        val = validators.domain(domain)
        if not val:
            self.errors.append("Invalid Domain")

        return self
    def ip(self, ip: Optional[str], nullable: Optional[bool] = False):
        if nullable and not ip:
            return self

        val = validators.ipv4(ip)
        if not val:
            self.errors.append("Invalid IP-address")

        return self
    
    def validate_cpe(self, cpe: Optional[str], nullable: Optional[bool] = False):
        if nullable and not cpe:
            return self
        pattern = r'^cpe:[a-zA-Z0-9_\-\.\:\/]+[aho]:[a-zA-Z0-9_\-\.\/]+:[a-zA-Z0-9_\-\.\/]+$'
        if not re.match(pattern, cpe):
            self.errors.append("Invalid Cpe")

        return self

    def isin(self, value: Optional[any], values: List, nullable: Optional[bool] = False):
        if nullable and not value:
            return self

        if value not in values:
            self.errors.append(
                f"value should be one of the following {values}")

        return self

    def validate(self):

        if len(self.errors) > 0:
            dlg = ErrorDialog('Validation Error Occurred', list(
                map(lambda e: {"message": str(e)}, self.errors)))

            self.errors = []
            runnable = DialogRunnable(self, dlg)
            QThreadPool.globalInstance().start(runnable)
            return False

        return True
