# -*- coding: utf-8 -*-
# Copyright (c) 2015 Ian Stapleton Cordasco
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import rfc3986
from rfc3986 import exceptions
from rfc3986 import parseresult as pr

import pytest

from . import base

INVALID_PORTS = ['443:80', '443:80:443', 'abcdef', 'port', '43port']

SNOWMAN = b'\xe2\x98\x83'
SNOWMAN_IDNA_HOST = 'http://xn--n3h.com'


@pytest.mark.parametrize('port', INVALID_PORTS)
def test_port_parsing(port):
    with pytest.raises(exceptions.InvalidPort):
        rfc3986.urlparse('https://httpbin.org:{0}/get'.format(port))


@pytest.mark.parametrize('parts, unsplit', [
    (('https', None, 'httpbin.org'), u'https://httpbin.org'),
    (('https', 'user', 'httpbin.org'), u'https://user@httpbin.org'),
    (('https', None, 'httpbin.org', 443, '/get'),
        u'https://httpbin.org:443/get'),
    (('HTTPS', None, 'HTTPBIN.ORG'), u'https://httpbin.org'),
])
def test_from_parts(parts, unsplit):
    uri = pr.ParseResult.from_parts(*parts)
    assert uri.unsplit() == unsplit


@pytest.mark.parametrize('parts, unsplit', [
    (('https', None, 'httpbin.org'), b'https://httpbin.org'),
    (('https', 'user', 'httpbin.org'), b'https://user@httpbin.org'),
    (('https', None, 'httpbin.org', 443, '/get'),
        b'https://httpbin.org:443/get'),
    (('HTTPS', None, 'HTTPBIN.ORG'), b'https://httpbin.org'),
])
def test_bytes_from_parts(parts, unsplit):
    uri = pr.ParseResultBytes.from_parts(*parts)
    assert uri.unsplit() == unsplit


class TestParseResultParsesURIs(base.BaseTestParsesURIs):
    test_class = pr.ParseResult


class TestParseResultUnsplits(base.BaseTestUnsplits):
    test_class = pr.ParseResult


def test_normalizes_uris_when_using_from_string(uri_to_normalize):
    """Verify we always get the same thing out as we expect."""
    result = pr.ParseResult.from_string(uri_to_normalize,
                                        lazy_normalize=False)
    assert result.scheme == 'https'
    assert result.host == 'example.com'


class TestStdlibShims:
    def test_uri_with_everything(self, uri_with_everything):
        uri = pr.ParseResult.from_string(uri_with_everything)
        assert uri.host == uri.hostname
        assert uri.netloc == uri.authority
        assert uri.query == uri.params
        assert uri.geturl() == uri.unsplit()


def test_creates_a_copy_with_a_new_path(uri_with_everything):
    uri = pr.ParseResult.from_string(uri_with_everything)
    new_uri = uri.copy_with(path='/parse/result/tests/are/fun')
    assert new_uri.path == '/parse/result/tests/are/fun'


def test_creates_a_copy_with_a_new_port(basic_uri):
    uri = pr.ParseResult.from_string(basic_uri)
    new_uri = uri.copy_with(port=443)
    assert new_uri.port == 443


def test_parse_result_encodes_itself(uri_with_everything):
    uri = pr.ParseResult.from_string(uri_with_everything)
    uribytes = uri.encode()
    encoding = uri.encoding
    assert uri.scheme.encode(encoding) == uribytes.scheme
    assert uri.userinfo.encode(encoding) == uribytes.userinfo
    assert uri.host.encode(encoding) == uribytes.host
    assert uri.port == uribytes.port
    assert uri.path.encode(encoding) == uribytes.path
    assert uri.query.encode(encoding) == uribytes.query
    assert uri.fragment.encode(encoding) == uribytes.fragment


class TestParseResultBytes:
    def test_handles_uri_with_everything(self, uri_with_everything):
        uri = pr.ParseResultBytes.from_string(uri_with_everything)
        assert uri.scheme == b'https'
        assert uri.path == b'/path/to/resource'
        assert uri.query == b'key=value'
        assert uri.fragment == b'fragment'
        assert uri.userinfo == b'user:pass'
        assert uri.port == 443
        assert isinstance(uri.authority, bytes) is True

    def test_raises_invalid_authority_for_invalid_uris(self, invalid_uri):
        with pytest.raises(exceptions.InvalidAuthority):
            pr.ParseResultBytes.from_string(invalid_uri)

    @pytest.mark.parametrize('port', INVALID_PORTS)
    def test_raises_invalid_port_non_strict_parse(self, port):
        with pytest.raises(exceptions.InvalidPort):
            pr.ParseResultBytes.from_string(
                'https://httpbin.org:{0}/get'.format(port),
                strict=False
            )

    def test_copy_with_a_new_path(self, uri_with_everything):
        uri = pr.ParseResultBytes.from_string(uri_with_everything)
        new_uri = uri.copy_with(path=b'/parse/result/tests/are/fun')
        assert new_uri.path == b'/parse/result/tests/are/fun'

    def test_copy_with_a_new_unicode_path(self, uri_with_everything):
        uri = pr.ParseResultBytes.from_string(uri_with_everything)
        pathbytes = b'/parse/result/tests/are/fun' + SNOWMAN
        new_uri = uri.copy_with(path=pathbytes.decode('utf-8'))
        assert new_uri.path == (b'/parse/result/tests/are/fun' + SNOWMAN)

    def test_unsplit(self):
        uri = pr.ParseResultBytes.from_string(
            b'http://' + SNOWMAN + b'.com/path',
            strict=False
        )
        idna_encoded = SNOWMAN_IDNA_HOST.encode('utf-8') + b'/path'
        assert uri.unsplit(use_idna=True) == idna_encoded

    def test_eager_normalization_from_string(self):
        uri = pr.ParseResultBytes.from_string(
            b'http://' + SNOWMAN + b'.com/path',
            strict=False,
            lazy_normalize=False,
        )
        assert uri.unsplit() == b'http:/path'

    def test_eager_normalization_from_parts(self):
        uri = pr.ParseResultBytes.from_parts(
            scheme='http', host=SNOWMAN.decode('utf-8'), path='/path',
            lazy_normalize=False,
        )
        assert uri.unsplit() == b'http:/path'
