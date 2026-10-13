"""Handwritten synthetic characterization example; not a generator or SDK library."""
import json
import unittest
from urllib.parse import quote, urlencode


class ApiFailure(Exception):
    def __init__(self, status, body, request_id):
        super().__init__(f"HTTP {status}")
        self.status, self.body, self.request_id = status, body, request_id


class ExampleClient:
    def __init__(self, transport, tenant, token):
        self.transport, self.tenant, self.token = transport, tenant, token

    def request(self, method, path, query=None, body=None):
        # This toy contract has JSON bodies and no retry or network policy.
        target = path + ("?" + urlencode(query) if query else "")
        headers = {"Authorization": "Bearer " + self.token, "X-Tenant": self.tenant}
        encoded = json.dumps(body).encode() if body is not None else None
        status, response_headers, payload = self.transport(method, target, headers, encoded)
        if status == 204:
            return None
        result = json.loads(payload)
        if not 200 <= status < 300:
            raise ApiFailure(status, result, response_headers.get("X-Request-ID"))
        return result

    def item(self, identifier):
        return self.request("GET", "/items/" + quote(identifier, safe=""))

    def pages(self, max_pages=2):
        cursor = None
        result = []
        for _ in range(max_pages):
            page = self.request("GET", "/items", {"cursor": cursor} if cursor else None)
            result.extend(page["items"])
            cursor = page.get("next_cursor")
            if cursor is None:
                return result
        raise ValueError("page bound reached")


class Characterization(unittest.TestCase):
    def setUp(self):
        self.requests = []
        self.responses = [(200, {}, b'{"items":[],"next_cursor":null}')]

        def transport(method, target, headers, body):
            self.requests.append((method, target, headers, body))
            return self.responses.pop(0)

        self.transport = transport
        self.client = ExampleClient(transport, "tenant-a", "fake-a")

    def test_path_encoding(self):
        self.client.item("a/b ?")
        self.assertEqual(self.requests[0][1], "/items/a%2Fb%20%3F")

    def test_query_encoding(self):
        self.client.request("GET", "/items", {"cursor": "a+b/="})
        self.assertEqual(self.requests[0][1], "/items?cursor=a%2Bb%2F%3D")

    def test_client_headers_are_separate(self):
        self.responses.append((200, {}, b'{}'))
        self.client.item("x")
        ExampleClient(self.transport, "tenant-b", "fake-b").item("x")
        self.assertEqual(self.requests[0][2], {"Authorization": "Bearer fake-a", "X-Tenant": "tenant-a"})
        self.assertEqual(self.requests[1][2], {"Authorization": "Bearer fake-b", "X-Tenant": "tenant-b"})

    def test_null_and_omitted(self):
        self.client.request("POST", "/items", body={"label": None})
        self.assertEqual(json.loads(self.requests[0][3]), {"label": None})
        self.assertNotIn("optional", json.loads(self.requests[0][3]))

    def test_no_content(self):
        self.responses = [(204, {}, b'')]
        self.assertIsNone(self.client.request("DELETE", "/items/x"))

    def test_error_preserves_status_body_and_id(self):
        self.responses = [(429, {"X-Request-ID": "synthetic-1"}, b'{"code":"limited"}')]
        with self.assertRaises(ApiFailure) as caught:
            self.client.item("x")
        self.assertEqual((caught.exception.status, caught.exception.body, caught.exception.request_id),
                         (429, {"code": "limited"}, "synthetic-1"))
        self.assertEqual(len(self.requests), 1)

    def test_unknown_enum_is_preserved(self):
        self.responses = [(200, {}, b'{"state":"future"}')]
        self.assertEqual(self.client.item("x"), {"state": "future"})

    def test_page_termination(self):
        self.responses = [(200, {}, b'{"items":[1],"next_cursor":"b+"}'),
                          (200, {}, b'{"items":[2],"next_cursor":null}')]
        self.assertEqual(self.client.pages(), [1, 2])
        self.assertEqual(self.requests[1][1], "/items?cursor=b%2B")

    def test_page_bound(self):
        self.responses = [(200, {}, b'{"items":[],"next_cursor":"same"}')]*2
        with self.assertRaisesRegex(ValueError, "page bound reached"):
            self.client.pages()
        self.assertEqual(len(self.requests), 2)

    def test_failed_mutation_is_not_retried(self):
        calls = []

        def uncertain(*request):
            calls.append(request)
            raise TimeoutError("synthetic uncertain outcome")

        with self.assertRaises(TimeoutError):
            ExampleClient(uncertain, "tenant-a", "fake-a").request("POST", "/jobs", body={})
        self.assertEqual(len(calls), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
