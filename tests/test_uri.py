# -*- coding: utf-8 -*-
import pytest

from rfc3986.exceptions import InvalidAuthority, ResolutionError
from rfc3986.misc import URI_MATCHER
from rfc3986.uri import URIReference


valid_hosts = [
    '[21DA:00D3:0000:2F3B:02AA:00FF:FE28:9C5A]', '[::1]',
    '[21DA:D3:0:2F3B:2AA:FF:FE28:9C5A]', '[FE80::2AA:FF:FE9A:4CA2]',
    '[FF02::2]', '[FF02:3::5]', '[FF02:0:0:0:0:0:0:2]',
    '[FF02:30:0:0:0:0:0:5]', '127.0.0.1', 'www.example.com', 'localhost'
    ]

invalid_hosts = [
    '[FF02::3::5]',  # IPv6 can only have one ::
    '[FADF:01]',  # Not properly compacted (missing a :)
    'localhost:80:80:80',  # Too many ports
    '256.256.256.256'  # Invalid IPv4 Address
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


@pytest.fixture(params=invalid_hosts)
def invalid_uri(request):
    return 'https://%s' % request.param


@pytest.fixture
def scheme_and_path_uri():
    return 'mailto:user@example.com'


class TestURIReferenceParsesURIs:
    """Tests for URIReference handling of URIs."""
    def test_handles_basic_uri(self, basic_uri):
        """Test that URIReference can handle a simple URI."""
        uri = URIReference.from_string(basic_uri)
        assert uri.scheme == 'http'
        assert uri.authority == basic_uri[7:]  # len('http://')
        assert uri.host == uri.authority
        assert uri.path is None
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
        assert uri.path is None
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
        assert uri.path is None
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

    def test_authority_info_raises_InvalidAuthority(self, invalid_uri):
        """Test that an invalid IPv6 is caught by authority_info()."""
        uri = URIReference.from_string(invalid_uri)
        with pytest.raises(InvalidAuthority):
            uri.authority_info()

    def test_attributes_catch_InvalidAuthority(self, invalid_uri):
        """Test that an invalid IPv6 is caught by authority_info()."""
        uri = URIReference.from_string(invalid_uri)
        assert uri.host is None
        assert uri.userinfo is None
        assert uri.port is None

    def test_handles_relative_uri(self, relative_uri):
        """Test that URIReference can handle a relative URI."""
        uri = URIReference.from_string(relative_uri)
        assert uri.scheme is None
        assert uri.authority == relative_uri[2:]

    def test_handles_absolute_path_uri(self, absolute_path_uri):
        """Test that URIReference can handle a path-only URI."""
        uri = URIReference.from_string(absolute_path_uri)
        assert uri.path == absolute_path_uri
        assert uri.authority_info() == {
            'userinfo': None,
            'host': None,
            'port': None,
            }

    def test_handles_scheme_and_path_uri(self, scheme_and_path_uri):
        """Test that URIReference can handle a `scheme:path` URI."""
        uri = URIReference.from_string(scheme_and_path_uri)
        assert uri.path == 'user@example.com'
        assert uri.scheme == 'mailto'
        assert uri.query is None
        assert uri.host is None
        assert uri.port is None
        assert uri.userinfo is None
        assert uri.authority is None


class TestURIValidation:
    # Valid URI tests
    def test_basic_uri_is_valid(self, basic_uri):
        uri = URIReference.from_string(basic_uri)
        assert uri.is_valid() is True

    def test_basic_uri_requiring_scheme(self, basic_uri):
        uri = URIReference.from_string(basic_uri)
        assert uri.is_valid(require_scheme=True) is True

    def test_basic_uri_requiring_authority(self, basic_uri):
        uri = URIReference.from_string(basic_uri)
        assert uri.is_valid(require_authority=True) is True

    def test_uri_with_everything_requiring_path(self, uri_with_everything):
        uri = URIReference.from_string(uri_with_everything)
        assert uri.is_valid(require_path=True) is True

    def test_uri_with_everything_requiring_query(self, uri_with_everything):
        uri = URIReference.from_string(uri_with_everything)
        assert uri.is_valid(require_query=True) is True

    def test_uri_with_everything_requiring_fragment(self,
                                                    uri_with_everything):
        uri = URIReference.from_string(uri_with_everything)
        assert uri.is_valid(require_fragment=True) is True

    def test_basic_uri_with_port_is_valid(self, basic_uri_with_port):
        uri = URIReference.from_string(basic_uri_with_port)
        assert uri.is_valid() is True

    def test_uri_with_port_and_userinfo_is_valid(self,
                                                 uri_with_port_and_userinfo):
        uri = URIReference.from_string(uri_with_port_and_userinfo)
        assert uri.is_valid() is True

    def test_basic_uri_with_path_is_valid(self, basic_uri_with_path):
        uri = URIReference.from_string(basic_uri_with_path)
        assert uri.is_valid() is True

    def test_uri_with_path_and_query_is_valid(self, uri_with_path_and_query):
        uri = URIReference.from_string(uri_with_path_and_query)
        assert uri.is_valid() is True

    def test_uri_with_everything_is_valid(self, uri_with_everything):
        uri = URIReference.from_string(uri_with_everything)
        assert uri.is_valid() is True

    def test_relative_uri_is_valid(self, relative_uri):
        uri = URIReference.from_string(relative_uri)
        assert uri.is_valid() is True

    def test_absolute_path_uri_is_valid(self, absolute_path_uri):
        uri = URIReference.from_string(absolute_path_uri)
        assert uri.is_valid() is True

    def test_scheme_and_path_uri_is_valid(self, scheme_and_path_uri):
        uri = URIReference.from_string(scheme_and_path_uri)
        assert uri.is_valid() is True

    # Invalid URI tests
    def test_invalid_uri_is_not_valid(self, invalid_uri):
        uri = URIReference.from_string(invalid_uri)
        assert uri.is_valid() is False

    def test_invalid_scheme(self):
        uri = URIReference('123', None, None, None, None)
        assert uri.is_valid() is False

    def test_invalid_path(self):
        uri = URIReference(None, None, 'foo#bar', None, None)
        assert uri.is_valid() is False

    def test_invalid_query_component(self):
        uri = URIReference(None, None, None, 'foo#bar', None)
        assert uri.is_valid() is False

    def test_invalid_fragment_component(self):
        uri = URIReference(None, None, None, None, 'foo#bar')
        assert uri.is_valid() is False


class TestURIReferenceUnsplits:
    def test_basic_uri_unsplits(self, basic_uri):
        uri = URIReference.from_string(basic_uri)
        assert uri.unsplit() == basic_uri

    def test_basic_uri_with_port_unsplits(self, basic_uri_with_port):
        uri = URIReference.from_string(basic_uri_with_port)
        assert uri.unsplit() == basic_uri_with_port

    def test_uri_with_port_and_userinfo_unsplits(self,
                                                 uri_with_port_and_userinfo):
        uri = URIReference.from_string(uri_with_port_and_userinfo)
        assert uri.unsplit() == uri_with_port_and_userinfo

    def test_basic_uri_with_path_unsplits(self, basic_uri_with_path):
        uri = URIReference.from_string(basic_uri_with_path)
        assert uri.unsplit() == basic_uri_with_path

    def test_uri_with_path_and_query_unsplits(self, uri_with_path_and_query):
        uri = URIReference.from_string(uri_with_path_and_query)
        assert uri.unsplit() == uri_with_path_and_query

    def test_uri_with_everything_unsplits(self, uri_with_everything):
        uri = URIReference.from_string(uri_with_everything)
        assert uri.unsplit() == uri_with_everything

    def test_relative_uri_unsplits(self, relative_uri):
        uri = URIReference.from_string(relative_uri)
        assert uri.unsplit() == relative_uri

    def test_absolute_path_uri_unsplits(self, absolute_path_uri):
        uri = URIReference.from_string(absolute_path_uri)
        assert uri.unsplit() == absolute_path_uri

    def test_scheme_and_path_uri_unsplits(self, scheme_and_path_uri):
        uri = URIReference.from_string(scheme_and_path_uri)
        assert uri.unsplit() == scheme_and_path_uri


class TestURIReferenceComparesToStrings:
    def test_basic_uri(self, basic_uri):
        uri = URIReference.from_string(basic_uri)
        assert uri == basic_uri

    def test_basic_uri_with_port(self, basic_uri_with_port):
        uri = URIReference.from_string(basic_uri_with_port)
        assert uri == basic_uri_with_port

    def test_uri_with_port_and_userinfo(self, uri_with_port_and_userinfo):
        uri = URIReference.from_string(uri_with_port_and_userinfo)
        assert uri == uri_with_port_and_userinfo

    def test_basic_uri_with_path(self, basic_uri_with_path):
        uri = URIReference.from_string(basic_uri_with_path)
        assert uri == basic_uri_with_path

    def test_uri_with_path_and_query(self, uri_with_path_and_query):
        uri = URIReference.from_string(uri_with_path_and_query)
        assert uri == uri_with_path_and_query

    def test_uri_with_everything(self, uri_with_everything):
        uri = URIReference.from_string(uri_with_everything)
        assert uri == uri_with_everything

    def test_relative_uri(self, relative_uri):
        uri = URIReference.from_string(relative_uri)
        assert uri == relative_uri

    def test_absolute_path_uri(self, absolute_path_uri):
        uri = URIReference.from_string(absolute_path_uri)
        assert uri == absolute_path_uri

    def test_scheme_and_path_uri(self, scheme_and_path_uri):
        uri = URIReference.from_string(scheme_and_path_uri)
        assert uri == scheme_and_path_uri


class TestURIReferenceComparesToTuples:
    def to_tuple(self, uri):
        return URI_MATCHER.match(uri).groups()

    def test_basic_uri(self, basic_uri):
        uri = URIReference.from_string(basic_uri)
        assert uri == self.to_tuple(basic_uri)

    def test_basic_uri_with_port(self, basic_uri_with_port):
        uri = URIReference.from_string(basic_uri_with_port)
        assert uri == self.to_tuple(basic_uri_with_port)

    def test_uri_with_port_and_userinfo(self, uri_with_port_and_userinfo):
        uri = URIReference.from_string(uri_with_port_and_userinfo)
        assert uri == self.to_tuple(uri_with_port_and_userinfo)

    def test_basic_uri_with_path(self, basic_uri_with_path):
        uri = URIReference.from_string(basic_uri_with_path)
        assert uri == self.to_tuple(basic_uri_with_path)

    def test_uri_with_path_and_query(self, uri_with_path_and_query):
        uri = URIReference.from_string(uri_with_path_and_query)
        assert uri == self.to_tuple(uri_with_path_and_query)

    def test_uri_with_everything(self, uri_with_everything):
        uri = URIReference.from_string(uri_with_everything)
        assert uri == self.to_tuple(uri_with_everything)

    def test_relative_uri(self, relative_uri):
        uri = URIReference.from_string(relative_uri)
        assert uri == self.to_tuple(relative_uri)

    def test_absolute_path_uri(self, absolute_path_uri):
        uri = URIReference.from_string(absolute_path_uri)
        assert uri == self.to_tuple(absolute_path_uri)

    def test_scheme_and_path_uri(self, scheme_and_path_uri):
        uri = URIReference.from_string(scheme_and_path_uri)
        assert uri == self.to_tuple(scheme_and_path_uri)


def test_uri_comparison_raises_TypeError(basic_uri):
    uri = URIReference.from_string(basic_uri)
    with pytest.raises(TypeError):
        uri == 1


class TestURIReferenceComparesToURIReferences:
    def test_same_basic_uri(self, basic_uri):
        uri = URIReference.from_string(basic_uri)
        assert uri == uri

    def test_different_basic_uris(self, basic_uri, basic_uri_with_port):
        uri = URIReference.from_string(basic_uri)
        assert (uri == URIReference.from_string(basic_uri_with_port)) is False


class TestURIReferenceIsAbsolute:
    def test_basic_uris_are_absolute(self, basic_uri):
        uri = URIReference.from_string(basic_uri)
        assert uri.is_absolute() is True

    def test_basic_uris_with_ports_are_absolute(self, basic_uri_with_port):
        uri = URIReference.from_string(basic_uri_with_port)
        assert uri.is_absolute() is True

    def test_basic_uris_with_paths_are_absolute(self, basic_uri_with_path):
        uri = URIReference.from_string(basic_uri_with_path)
        assert uri.is_absolute() is True

    def test_uri_with_everything_are_not_absolute(self, uri_with_everything):
        uri = URIReference.from_string(uri_with_everything)
        assert uri.is_absolute() is False

    def test_absolute_paths_are_not_absolute_uris(self, absolute_path_uri):
        uri = URIReference.from_string(absolute_path_uri)
        assert uri.is_absolute() is False


# @pytest.fixture(params=[
#     basic_uri, basic_uri_with_port, basic_uri_with_path,
#     scheme_and_path_uri, uri_with_path_and_query
#     ])
# @pytest.fixture(params=[absolute_path_uri, relative_uri])


class TestURIReferencesResolve:
    def test_with_basic_and_relative_uris(self, basic_uri, relative_uri):
        R = URIReference.from_string(relative_uri)
        B = URIReference.from_string(basic_uri)
        T = R.resolve_with(basic_uri)
        assert T.scheme == B.scheme
        assert T.host == R.host
        assert T.path == R.path

    def test_with_basic_and_absolute_path_uris(self, basic_uri,
                                               absolute_path_uri):
        R = URIReference.from_string(absolute_path_uri)
        B = URIReference.from_string(basic_uri).normalize()
        T = R.resolve_with(B)
        assert T.scheme == B.scheme
        assert T.host == B.host
        assert T.path == R.path

    def test_with_basic_uri_and_relative_path(self, basic_uri):
        R = URIReference.from_string('foo/bar/bogus')
        B = URIReference.from_string(basic_uri).normalize()
        T = R.resolve_with(B)
        assert T.scheme == B.scheme
        assert T.host == B.host
        assert T.path == '/' + R.path

    def test_basic_uri_with_path_and_relative_path(self, basic_uri_with_path):
        R = URIReference.from_string('foo/bar/bogus')
        B = URIReference.from_string(basic_uri_with_path).normalize()
        T = R.resolve_with(B)
        assert T.scheme == B.scheme
        assert T.host == B.host

        index = B.path.rfind('/')
        assert T.path == B.path[:index] + '/' + R.path

    def test_uri_with_everything_raises_exception(self, uri_with_everything):
        R = URIReference.from_string('foo/bar/bogus')
        B = URIReference.from_string(uri_with_everything)
        with pytest.raises(ResolutionError):
            R.resolve_with(B)

    def test_basic_uri_resolves_itself(self, basic_uri):
        R = URIReference.from_string(basic_uri)
        B = URIReference.from_string(basic_uri)
        T = R.resolve_with(B)
        assert T == B

    def test_differing_schemes(self, basic_uri):
        R = URIReference.from_string('https://example.com/path')
        B = URIReference.from_string(basic_uri)
        T = R.resolve_with(B)
        assert T.scheme == R.scheme

    def test_resolve_pathless_fragment(self, basic_uri):
        R = URIReference.from_string('#fragment')
        B = URIReference.from_string(basic_uri)
        T = R.resolve_with(B)
        assert T.path is None
        assert T.fragment == 'fragment'

    def test_resolve_pathless_query(self, basic_uri):
        R = URIReference.from_string('?query')
        B = URIReference.from_string(basic_uri)
        T = R.resolve_with(B)
        assert T.path is None
        assert T.query == 'query'
