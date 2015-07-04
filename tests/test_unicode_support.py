# -*- coding: utf-8 -*-

from rfc3986 import uri_reference
from rfc3986 import urlparse


SNOWMAN = b'\xe2\x98\x83'


def test_unicode_uri():
    url_bytestring = b'http://example.com?utf8=' + SNOWMAN
    unicode_url = url_bytestring.decode('utf-8')
    uri = uri_reference(unicode_url)
    assert uri.is_valid() is True
    assert uri == 'http://example.com?utf8=%E2%98%83'


def test_unicode_uri_passed_as_bytes():
    url_bytestring = b'http://example.com?utf8=' + SNOWMAN
    uri = uri_reference(url_bytestring)
    assert uri.is_valid() is True
    assert uri == 'http://example.com?utf8=%E2%98%83'


def test_unicode_authority():
    url_bytestring = b'http://' + SNOWMAN + b'.com'
    unicode_url = url_bytestring.decode('utf-8')
    uri = uri_reference(unicode_url)
    assert uri.is_valid() is False
    assert uri == unicode_url


def test_unicode_hostname():
    url_bytestring = b'http://' + SNOWMAN + b'.com'
    parsed = urlparse(url_bytestring)
    assert parsed
