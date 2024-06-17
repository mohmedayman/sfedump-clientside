req_text = """
{method} {path} {http_version}
Host:{host}
{headers}
Cookie:{cookie}

{content}
"""

res_text = """
{http_version} {code} {reason}

{headers}

{content}
"""