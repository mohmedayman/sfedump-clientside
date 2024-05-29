from mitmproxy import contentviews
from mitmproxy import flow
from mitmproxy import http
from mitmproxy.addonmanager import Loader

import json


class Script:
    def __init__(self):
        self.num = 0

    def response(self, flow:http.HTTPFlow):
        self.num = self.num + 1
        flow.get_state()
        
        print(flow.get_state())


addons = [Script()]
