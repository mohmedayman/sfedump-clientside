from urllib.parse import urlunsplit, urlparse, parse_qs
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from mitmproxy.net.http import headers

import re


class HTTPRequestParser:
    def extract_url(self, raw_request):
        lines = raw_request.split("\n")
        first_line_parts = lines[0].split()
        if len(first_line_parts) >= 2:
            method, path = first_line_parts[0], first_line_parts[1]
            host = None
            for line in lines[1:]:
                if line.lower().startswith("host:"):
                    host = line.split(":", 1)[1].strip()
                    break
            if host:
                scheme = "https" if "https://" in path else "http"
                url = urlunsplit((scheme, host, path, "", ""))
                return url
        return None

    def extract_data(self, raw_request: str):
        lines = raw_request.split("\n")
        method = lines[0].split()[0]

        if method.lower() == "post":
            for line in lines:
                if line.lower().startswith("content-type:"):
                    content_type = line.split(":", 1)[1].strip()

                    if "application/x-www-form-urlencoded" in content_type.lower():
                        # Find the data line
                        data_line = lines[lines.index(line) + 1]
                        return {'data': data_line}
                    elif "application/json" in content_type.lower():
                        return {'data': json.loads(lines[-1])}
                    elif "multipart/form-data" in content_type.lower():
                        last_header = list(self.parse_raw_headers(
                            raw_request, with_strip=False).items())[-1]
                        form_data = raw_request[raw_request.find("\n",
                                                                 raw_request.find(last_header[1])):]
                        form_data_byte = form_data.encode()
                        ct = headers.parse_content_type(content_type)
                        if not ct:
                            return {}
                        try:
                            boundary = ct[2]["boundary"].encode("ascii")
                        except (KeyError, UnicodeError):
                            return {}
                        rx = re.compile(rb'\bname="([^"]+)"')
                        r = {}
                        if form_data_byte is not None:
                            for i in form_data_byte.split(b"--" + boundary):
                                parts = i.splitlines()
                                if len(parts) > 1 and parts[0][0:2] != b"--":
                                    match = rx.search(parts[1])
                                    if match:
                                        key = match.group(1)
                                        value = b"".join(
                                            parts[3 + parts[2:].index(b""):])
                                        r[key.decode()] = value.decode()

                        return {'data': MultipartEncoder(fields=r, boundary=boundary)}

        return None

    def extract_parameters(self, raw_request):
        lines = raw_request.split("\n")
        method = lines[0].split()[0]
        if method.lower() == "get":
            url = lines[0].split()[1]
            parsed_url = urlparse(url)
            query_string = parsed_url.query
            parameters = parse_qs(query_string)
            return parameters
        return None

    def parse_raw_headers(self, raw_request, with_strip=True) -> dict:
        headers = {}
        lines = raw_request.split("\n")
        for line in lines[1:]:
            if not line.strip():
                break  # Stop when an empty line is encountered
            key, value = line.split(":", 1)
            if with_strip:
                headers[key.strip()] = value.strip()
            else:
                headers[key] = value
        return headers

    def extract_cookie(self, raw_request) -> dict:
        headers = self.parse_raw_headers(raw_request)
        cookie_str = None
        for key, value in headers.items():
            if key.lower() == 'cookie':
                cookie_str = value
                break

        if not cookie_str:
            return {}

        cookie_dict = {}
        for cookie_pair in cookie_str.split(';'):
            (key, value) = cookie_pair.split('=')
            cookie_dict[key.strip()] = value.strip()

        return cookie_dict
