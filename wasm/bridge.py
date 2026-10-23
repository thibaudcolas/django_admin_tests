"""A byte-preserving WSGI bridge. No request data is evaluated as Python code."""

import io
import json
import sys
from http.cookies import SimpleCookie
from pathlib import Path
from urllib.parse import unquote, urlsplit

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
cookie_file = Path("/persist/cookies.json")
cookies = json.loads(cookie_file.read_text()) if cookie_file.exists() else {}


def handle_request(metadata_json, body):
    metadata = json.loads(metadata_json)
    url = urlsplit(metadata["url"])
    body = bytes(body)
    environ = {
        "REQUEST_METHOD": metadata["method"],
        "SCRIPT_NAME": "",
        "PATH_INFO": unquote(url.path, encoding="utf-8")
        .encode("utf-8")
        .decode("latin-1"),
        "QUERY_STRING": url.query,
        "SERVER_NAME": url.hostname,
        "SERVER_PORT": str(url.port or (443 if url.scheme == "https" else 80)),
        "SERVER_PROTOCOL": "HTTP/1.1",
        "wsgi.version": (1, 0),
        "wsgi.url_scheme": url.scheme,
        "wsgi.input": io.BytesIO(body),
        "wsgi.errors": sys.stderr,
        "wsgi.multithread": False,
        "wsgi.multiprocess": False,
        "wsgi.run_once": False,
        "CONTENT_LENGTH": str(len(body)),
    }
    for name, value in metadata["headers"]:
        key = name.upper().replace("-", "_")
        if key not in {"CONTENT_TYPE", "CONTENT_LENGTH"}:
            key = "HTTP_" + key
        environ[key] = value
    # Browser cookies are deliberately ignored: this demo has its own session.
    environ["HTTP_COOKIE"] = "; ".join(
        f"{key}={value}" for key, value in cookies.items()
    )
    if metadata.get("referrer"):
        environ["HTTP_REFERER"] = metadata["referrer"]

    response = {}

    def start_response(status, headers, exc_info=None):
        if exc_info:
            raise exc_info[1].with_traceback(exc_info[2])
        response["status"] = int(status.split()[0])
        response["headers"] = []
        for name, value in headers:
            if name.lower() == "set-cookie":
                parsed = SimpleCookie()
                parsed.load(value)
                for key, morsel in parsed.items():
                    if morsel["max-age"] == "0":
                        cookies.pop(key, None)
                    else:
                        cookies[key] = morsel.value
            else:
                response["headers"].append((name, value))

    result = application(environ, start_response)
    try:
        response["body"] = b"".join(result)
    finally:
        if hasattr(result, "close"):
            result.close()
    cookie_file.write_text(json.dumps(cookies))
    return response
