# -*- coding: utf-8 -*-
import pytest

from rfc3986 import exceptions
from rfc3986 import parseresult
from rfc3986 import uri_reference
from rfc3986 import urlparse


SNOWMAN = b'\xe2\x98\x83'
SNOWMAN_PARAMS = b'http://example.com?utf8=' + SNOWMAN
SNOWMAN_HOST = b'http://' + SNOWMAN + b'.com'
SNOWMAN_IDNA_HOST = 'http://xn--n3h.com'

INVALID_PORTS = ['443:80', '443:80:443', 'abcdef', 'port', '43port']


def test_unicode_uri():
    url_bytestring = SNOWMAN_PARAMS
    unicode_url = url_bytestring.decode('utf-8')
    uri = uri_reference(unicode_url)
    assert uri.is_valid() is True
    assert uri == 'http://example.com?utf8=%E2%98%83'


def test_unicode_uri_passed_as_bytes():
    url_bytestring = SNOWMAN_PARAMS
    uri = uri_reference(url_bytestring)
    assert uri.is_valid() is True
    assert uri == 'http://example.com?utf8=%E2%98%83'


def test_unicode_authority():
    url_bytestring = SNOWMAN_HOST
    unicode_url = url_bytestring.decode('utf-8')
    uri = uri_reference(unicode_url)
    assert uri.is_valid() is False
    assert uri == unicode_url


def test_urlparse_a_unicode_hostname():
    url_bytestring = SNOWMAN_HOST
    unicode_url = url_bytestring.decode('utf-8')
    parsed = urlparse(url_bytestring)
    assert parsed.host == unicode_url[7:]


def test_unsplit_idna_a_unicode_hostname():
    parsed = urlparse(SNOWMAN_HOST)
    assert parsed.unsplit(use_idna=True) == SNOWMAN_IDNA_HOST


def test_strict_urlparsing():
    with pytest.raises(exceptions.InvalidAuthority):
        parseresult.ParseResult.from_string(SNOWMAN_HOST)


@pytest.mark.parametrize('port', INVALID_PORTS)
def test_port_parsing(port):
    with pytest.raises(exceptions.InvalidPort):
        urlparse('https://httpbin.org:{0}/get'.format(port))
