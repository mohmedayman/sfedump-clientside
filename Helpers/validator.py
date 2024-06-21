from typing import Optional, List
import validators as validators
from Helpers import DialogRunnable
from PyQt5.QtCore import QThreadPool, QObject
from Widgets import ErrorDialog
import re
import ipaddress
import socket


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
    
    def url(self, url: Optional[str], nullable: Optional[bool] = False):
        if nullable and not url:
            return self

        val = validators.url(url)
        if not val:
            self.errors.append("Invalid URL")

        return self

    def ip(self, ip: Optional[str], nullable: Optional[bool] = False):
        if nullable and not ip:
            return self

        val = validators.ipv4(ip)
        if not val:
            self.errors.append("Invalid IP-address")

        return self

    def validate_cpe(self, cpe: Optional[str]):
        pattern = r'^cpe:.*$'
        if not re.match(pattern, cpe):
            self.errors.append("Invalid Cpe")

        return self

    def subnet(self, subnet, nullable: Optional[bool] = False):
        try:
            ipaddress.IPv4Network(subnet)
            return self
        except ValueError:
            self.errors.append("Invalid Subnet")

            return self

    def target(self, target, nullable: Optional[bool] = False):
        try:
            if validators.domain(target) or validators.ipv4(target) or ipaddress.IPv4Network(target):
                return self

            self.errors.append("Invalid target")
            return self
        except socket.error:
            self.errors.append("Invalid target")
            return self
        except ValueError:
            self.errors.append("Invalid target")
            return self

    def isin(self, value: Optional[any], values: List, nullable: Optional[bool] = False):
        if nullable and not value:
            return self

        if value not in values:
            self.errors.append(
                f"value should be one of the following {values}")

        return self

    def string(self, value: Optional[any], nullable: Optional[bool] = False):
        if nullable and not value:
            return self

        if not isinstance(value, str):
            self.errors.append(
                f"value should be string")

        return self

    def bool(self, value: Optional[any], nullable: Optional[bool] = False):
        if nullable and not value:
            return self

        if not isinstance(value, bool):
            self.errors.append(
                f"value should be bool")

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
