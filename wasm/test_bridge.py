import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# These are protocol tests: the application is replaced, so no database or
# configured Django project is required. Browser tests exercise real Django.
with patch("django.core.wsgi.get_wsgi_application"):
    from wasm import bridge


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.cookie_file = Path(self.directory.name) / "cookies.json"
        self.enterContext(patch.object(bridge, "cookie_file", self.cookie_file))
        self.enterContext(patch.object(bridge, "cookies", {}))

    def request(
        self, *, url="https://demo.example/", method="GET", headers=(), body=b""
    ):
        return bridge.handle_request(
            json.dumps({"url": url, "method": method, "headers": headers}), body
        )

    def test_binary_multipart_and_unicode_path(self):
        body = b"--boundary\r\n" + bytes(range(256)) + b"\r\n--boundary--"
        content_type = "multipart/form-data; boundary=boundary"

        def application(environ, start_response):
            self.assertEqual(environ["wsgi.input"].read(), body)
            self.assertEqual(environ["CONTENT_TYPE"], content_type)
            self.assertEqual(environ["CONTENT_LENGTH"], str(len(body)))
            self.assertEqual(environ["PATH_INFO"].encode("latin-1").decode(), "/café/")
            self.assertEqual(environ["QUERY_STRING"], "q=%22%5C%0A")
            self.assertEqual(environ["HTTP_X_CSRFTOKEN"], "token")
            self.assertEqual(environ["wsgi.url_scheme"], "https")
            start_response(
                "201 Created", [("Content-Type", "application/octet-stream")]
            )
            return [body[:50], body[50:]]

        with patch.object(bridge, "application", application):
            response = self.request(
                url="https://demo.example/caf%C3%A9/?q=%22%5C%0A",
                method="POST",
                headers=[("content-type", content_type), ("x-csrftoken", "token")],
                body=body,
            )
        self.assertEqual(response["status"], 201)
        self.assertEqual(response["body"], body)

    def test_multiple_cookies_persist_and_logout_removes_session(self):
        def login(environ, start_response):
            start_response(
                "302 Found",
                [
                    ("Location", "/admin/"),
                    ("Set-Cookie", "sessionid=abc; HttpOnly; Path=/"),
                    ("Set-Cookie", "messages=hello; Path=/"),
                ],
            )
            return [b""]

        with patch.object(bridge, "application", login):
            response = self.request()
        self.assertEqual(response["headers"], [("Location", "/admin/")])
        self.assertEqual(
            json.loads(self.cookie_file.read_text()),
            {"sessionid": "abc", "messages": "hello"},
        )

        def logout(environ, start_response):
            self.assertEqual(environ["HTTP_COOKIE"], "sessionid=abc; messages=hello")
            start_response(
                "302 Found", [("Set-Cookie", "sessionid=; Max-Age=0; Path=/")]
            )
            return [b""]

        with patch.object(bridge, "application", logout):
            self.request(headers=[("cookie", "unrelated=host-cookie")])
        self.assertEqual(
            json.loads(self.cookie_file.read_text()), {"messages": "hello"}
        )

    def test_closes_streaming_response(self):
        closed = []

        def application(environ, start_response):
            start_response("200 OK", [("Content-Type", "application/pdf")])
            try:
                yield b"first"
                yield b"second"
            finally:
                closed.append(True)

        with patch.object(bridge, "application", application):
            response = self.request()
        self.assertEqual(response["body"], b"firstsecond")
        self.assertEqual(closed, [True])


if __name__ == "__main__":
    unittest.main()
