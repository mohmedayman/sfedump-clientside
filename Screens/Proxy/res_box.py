from mitmproxy import http
from PyQt5.QtCore import Qt, QObject
from PyQt5 import QtWidgets, QtGui, QtCore

from Widgets import CollapsibleBox
from Widgets.ResponseBox import *
from .form_texts import req_text, res_text


class ProxyResBox:
    def __init__(self, flow_dict: dict) -> None:
        self.req = http.Request.from_state(flow_dict['request'])
        self.res = http.Response.from_state(flow_dict['response'])

    def generateBox(self) -> CollapsibleBox:
        # print(self.req, self.res)
        box = CollapsibleBox(self.req.url[:150])
        color = QtGui.QColor(*[216 for _ in range(3)])

        lay = QtWidgets.QHBoxLayout()
        reqBox = ResponseBox()
        reqBox.setStyleSheet(
            "background-color: {}; color : black;".format(color.name())
        )
        reqBox.setAlignment(QtCore.Qt.AlignCenter)

        reqBox.setText(req_text.format(
            method=self.req.method,
            path=self.req.path,
            http_version=self.req.data.http_version.decode(),
            host=self.req.host_header,
            headers='\n'.join(str(k).capitalize()+": "+str(v)
                              for k, v in self.req.headers.items() if k.lower() != "cookie"),
            cookie=";".join(map(lambda cookie: str(
                cookie[0])+"="+str(cookie[1]), self.req._get_cookies())),
            content=self.req.get_text()
        ).strip()
        )

        resBox = ResponseBox()
        resBox.setStyleSheet(
            "background-color: {}; color : black;".format(color.name())
        )
        resBox.setAlignment(QtCore.Qt.AlignCenter)

        resBox.setText(res_text.format(
            http_version=self.res.http_version,
            code=self.res.status_code,
            reason=self.res.reason,
            headers='\n'.join(str(k)+": "+str(v)
                              for k, v in self.res.headers.items()),
            content=self.res.get_text()
        ).strip()
        )
        lay.addWidget(reqBox)
        lay.addWidget(resBox)

        box.setContentLayout(lay)

        return box
