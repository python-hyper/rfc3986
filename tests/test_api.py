from rfc3986.api import is_valid_uri
from rfc3986.api import normalize_uri
from rfc3986.api import uri_reference
from rfc3986.api import URIReference


def test_uri_reference():
    assert isinstance(uri_reference("http://example.com"), URIReference)


def test_is_valid_uri():
    assert is_valid_uri("http://example.com") is True


def test_normalize_uri():
    assert normalize_uri("HTTP://EXAMPLE.COM") == "http://example.com"
