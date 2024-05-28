from urllib.parse import urlunsplit, urlparse, parse_qs

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

    def extract_data(self, raw_request):
        lines = raw_request.split("\n")
        method = lines[0].split()[0]
        if method.lower() == "post":
            for line in lines:
                if line.lower().startswith("content-type:"):
                    content_type = line.split(":", 1)[1].strip()
                    if content_type.lower() == "application/x-www-form-urlencoded":
                        # Find the data line
                        data_line = lines[lines.index(line) + 1]
                        return data_line
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

    def parse_raw_headers(self, raw_request):
        headers = {}
        lines = raw_request.split("\n")
        for line in lines[1:]:
            if not line.strip():
                break  # Stop when an empty line is encountered
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()
        return headers
