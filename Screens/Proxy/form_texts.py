req_text = """
{method} {path} {http_version}
Host:{host}
{headers}

{content}
"""

res_text = """
{http_version} {code} {reason}

{headers}

{content}
"""