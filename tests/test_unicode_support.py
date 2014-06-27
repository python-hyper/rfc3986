# -*- coding: utf-8 -*-

from rfc3986 import uri_reference


def test_unicode_uri():
    url_bytestring = b'http://example.com?utf8=\xe2\x98\x83'
    unicode_url = url_bytestring.decode('utf-8')
    uri = uri_reference(unicode_url)
    assert uri.is_valid() is True
    assert uri == 'http://example.com?utf8=%E2%98%83'


def test_unicode_uri_passed_as_bytes():
    url_bytestring = b'http://example.com?utf8=\xe2\x98\x83'
    uri = uri_reference(url_bytestring)
    assert uri.is_valid() is True
    assert uri == 'http://example.com?utf8=%E2%98%83'


def test_unicode_authority():
    url_bytestring = b'http://\xe2\x98\x83.com'
    unicode_url = url_bytestring.decode('utf-8')
    uri = uri_reference(unicode_url)
    assert uri.is_valid() is False
    assert uri == unicode_url
