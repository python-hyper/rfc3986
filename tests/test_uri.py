# -*- coding: utf-8 -*-
import pytest

from rfc3986.exceptions import InvalidAuthority
from rfc3986.uri import URIReference


valid_hosts = [
    '[21DA:00D3:0000:2F3B:02AA:00FF:FE28:9C5A]', '[::1]',
    '[21DA:D3:0:2F3B:2AA:FF:FE28:9C5A]', '[FE80::2AA:FF:FE9A:4CA2]',
    '[FF02::2]', '[FF02:3::5]', '[FF02:0:0:0:0:0:0:2]',
    '[FF02:30:0:0:0:0:0:5]', '127.0.0.1', 'www.example.com', 'localhost'
    ]



@pytest.fixture(params=valid_hosts)
def basic_uri(request):
    return 'http://%s' % request.param


@pytest.fixture(params=valid_hosts)
def basic_uri_with_port(request):
    return 'ftp://%s:21' % request.param


@pytest.fixture(params=valid_hosts)
def uri_with_port_and_userinfo(request):
    return 'ssh://user:pass@%s:22' % request.param


@pytest.fixture(params=valid_hosts)
def basic_uri_with_path(request):
    return 'http://%s/path/to/resource' % request.param


@pytest.fixture(params=valid_hosts)
def uri_with_path_and_query(request):
    return 'http://%s/path/to/resource?key=value' % request.param


@pytest.fixture(params=valid_hosts)
def uri_with_everything(request):
    return 'https://user:pass@%s:443/path/to/resource?key=value#fragment' % (
        request.param)


@pytest.fixture(params=valid_hosts)
def relative_uri(request):
    return '//%s' % request.param


@pytest.fixture
def absolute_path_uri():
    return '/path/to/file'


@pytest.fixture
def invalid_ipv6():
    return 'https://[FADF:01]'


class TestURIReferenceParsesURIs:
    """Tests for URIReference handling of URIs."""
    def test_handles_basic_uri(self, basic_uri):
        """Test that URIReference can handle a simple URI."""
        uri = URIReference.from_string(basic_uri)
        assert uri.scheme == 'http'
        assert uri.authority == basic_uri[7:]  # len('http://')
        assert uri.host == uri.authority
        assert uri.path == ''
        assert uri.query is None
        assert uri.fragment is None
        assert uri.port is None
        assert uri.userinfo is None

    def test_handles_basic_uri_with_port(self, basic_uri_with_port):
        """Test that URIReference can handle a simple URI with a port."""
        uri = URIReference.from_string(basic_uri_with_port)
        assert uri.scheme == 'ftp'
        assert uri.authority == basic_uri_with_port[6:]  # len('ftp://')
        assert uri.host != uri.authority
        assert uri.port == '21'
        assert uri.path == ''
        assert uri.query is None
        assert uri.fragment is None
        assert uri.userinfo is None

    def test_handles_uri_with_port_and_userinfo(
            self, uri_with_port_and_userinfo):
        """
        Test that URIReference can handle a URI with a port and userinfo.
        """
        uri = URIReference.from_string(uri_with_port_and_userinfo)
        assert uri.scheme == 'ssh'
        # 6 == len('ftp://')
        assert uri.authority == uri_with_port_and_userinfo[6:]
        assert uri.host != uri.authority
        assert uri.port == '22'
        assert uri.path == ''
        assert uri.query is None
        assert uri.fragment is None
        assert uri.userinfo == 'user:pass'

    def test_handles_basic_uri_with_path(self, basic_uri_with_path):
        """Test that URIReference can handle a URI with a path."""
        uri = URIReference.from_string(basic_uri_with_path)
        assert uri.scheme == 'http'
        assert basic_uri_with_path == (uri.scheme + '://' + uri.authority
                                       + uri.path)
        assert uri.host == uri.authority
        assert uri.path == '/path/to/resource'
        assert uri.query is None
        assert uri.fragment is None
        assert uri.userinfo is None
        assert uri.port is None

    def test_handles_uri_with_path_and_query(self, uri_with_path_and_query):
        """
        Test that URIReference can handle a URI with a path and query.
        """
        uri = URIReference.from_string(uri_with_path_and_query)
        assert uri.scheme == 'http'
        assert uri.host == uri.authority
        assert uri.path == '/path/to/resource'
        assert uri.query == 'key=value'
        assert uri.fragment is None
        assert uri.userinfo is None
        assert uri.port is None

    def test_handles_uri_with_everything(self, uri_with_everything):
        """
        Test that URIReference can handle and with everything in it.
        """
        uri = URIReference.from_string(uri_with_everything)
        assert uri.scheme == 'https'
        assert uri.path == '/path/to/resource'
        assert uri.query == 'key=value'
        assert uri.fragment == 'fragment'
        assert uri.userinfo == 'user:pass'
        assert uri.port == '443'

    def test_authority_info_raises_InvalidAuthority(self, invalid_ipv6):
        """Test that an invalid IPv6 is caught by authority_info()."""
        uri = URIReference.from_string(invalid_ipv6)
        with pytest.raises(InvalidAuthority):
            uri.authority_info()

    def test_handles_relative_uri(self, relative_uri):
        """Test that URIReference can handle a relative URI."""
        uri = URIReference.from_string(relative_uri)
        assert uri.scheme is None
        assert uri.authority == relative_uri[2:]

    def test_handles_absolute_path_uris(self, absolute_path_uri):
        """Test that URIReference can handle a path-only URI."""
        uri = URIReference.from_string(absolute_path_uri)
        assert uri.path == absolute_path_uri
