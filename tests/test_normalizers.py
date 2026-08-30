import pytest

from rfc3986 import normalize_uri
from rfc3986.normalizers import encode_component
from rfc3986.normalizers import normalize_host
from rfc3986.normalizers import normalize_percent_characters
from rfc3986.normalizers import normalize_scheme
from rfc3986.normalizers import remove_dot_segments
from rfc3986.uri import URIReference

UNRESERVED = (
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
)


def test_normalize_scheme():
    assert "http" == normalize_scheme("htTp")
    assert "http" == normalize_scheme("http")
    assert "http" == normalize_scheme("HTTP")


def test_normalize_percent_characters():
    expected = "%3Athis_should_be_lowercase%DF%ABL"
    assert expected == normalize_percent_characters(
        "%3athis_should_be_lowercase%DF%ab%4c"
    )
    assert expected == normalize_percent_characters(
        "%3Athis_should_be_lowercase%DF%AB%4C"
    )
    assert expected == normalize_percent_characters(
        "%3Athis_should_be_lowercase%DF%aB%4C"
    )


def test_normalize_percent_characters_decodes_unreserved():
    for char in UNRESERVED:
        assert normalize_percent_characters(f"%{ord(char):02X}") == char
        assert normalize_percent_characters(f"%{ord(char):02x}") == char


def test_normalize_percent_characters_keeps_other_octets():
    for octet in range(256):
        if chr(octet) in UNRESERVED:
            continue
        assert normalize_percent_characters(f"%{octet:02X}") == f"%{octet:02X}"


def test_normalize_percent_characters_keeps_sub_delimiters():
    sub_delimiters = "%21%24%26%27%28%29%2A%2B%2C%3B%3D"
    assert sub_delimiters == normalize_percent_characters(sub_delimiters)


def test_normalize_percent_characters_is_idempotent():
    samples = ("%41%42%43", "%3A%2F%DF%AB%7e", "%7Efoo%21%2B", "a/b/%2E%2E")
    for sample in samples:
        once = normalize_percent_characters(sample)
        assert once == normalize_percent_characters(once)


paths = [
    # (Input, expected output)
    ("/foo/bar/.", "/foo/bar/"),
    ("/foo/bar/", "/foo/bar/"),
    ("/foo/bar", "/foo/bar"),
    ("./foo/bar", "foo/bar"),
    ("/./foo/bar", "/foo/bar"),
    ("/foo%20bar/biz%2Abaz", "/foo%20bar/biz%2Abaz"),
    ("../foo/bar", "foo/bar"),
    ("/../foo/bar", "/foo/bar"),
    ("a/./b/../b/%63/%7Bfoo%7D", "a/b/%63/%7Bfoo%7D"),
    ("//a/./b/../b/%63/%7Bfoo%7D", "//a/b/%63/%7Bfoo%7D"),
    ("mid/content=5/../6", "mid/6"),
    ("/a/b/c/./../../g", "/a/g"),
]


@pytest.fixture(params=paths)
def path_fixture(request):
    return request.param


@pytest.fixture(params=paths)
def uris(request):
    to_norm, normalized = request.param
    return (
        URIReference(None, None, to_norm, None, None),
        URIReference(None, None, normalized, None, None),
    )


def test_remove_dot_segments(path_fixture):
    to_normalize, expected = path_fixture
    assert expected == remove_dot_segments(to_normalize)


def test_normalized_equality(uris):
    assert uris[0] == uris[1]


def test_normalized_equality_with_unreserved_percent_encoding():
    assert URIReference(None, None, "/%7Efoo", None, None) == URIReference(
        None, None, "/~foo", None, None
    )
    assert URIReference(None, None, "/%41%42%43", None, None) == URIReference(
        None, None, "/ABC", None, None
    )


def test_hostname_normalization():
    assert URIReference(None, "EXAMPLE.COM", None, None, None) == URIReference(
        None, "example.com", None, None, None
    )


@pytest.mark.parametrize(
    ["authority", "expected_authority"],
    [
        ("user%2aName@EXAMPLE.COM", "user%2AName@example.com"),
        ("[::1%eth0]", "[::1%25eth0]"),
        ("user%41%7e@EXAMPLE.COM", "userA~@example.com"),
        ("user%21@EXAMPLE.COM", "user%21@example.com"),
    ],
)
def test_authority_normalization(authority, expected_authority):
    uri = URIReference(None, authority, None, None, None).normalize()
    assert uri.authority == expected_authority


def test_fragment_normalization():
    uri = URIReference(
        None, "example.com", None, None, "fiz%DF%7e"
    ).normalize()
    assert uri.fragment == "fiz%DF~"


def test_normalize_path_decodes_before_dot_segment_removal():
    assert (
        URIReference(None, None, "/a/%2E%2E/b", None, None).normalize().path
        == "/b"
    )


def test_normalize_uri_api():
    assert (
        normalize_uri("http://example.com/%7Efoo/%41?q=%7E#%2D")
        == "http://example.com/~foo/A?q=~#-"
    )


@pytest.mark.parametrize(
    ["component", "encoded_component"],
    [
        ("/%", "/%25"),
        ("/~", "/~"),
        ("/%a", "/%25a"),
        ("/%ag", "/%25ag"),
        ("/%af", "/%af"),
        ("/%20/%", "/%2520/%25"),
        ("/%20%25", "/%20%25"),
        ("/%21%22%23%ah%12%ff", "/%2521%2522%2523%25ah%2512%25ff"),
    ],
)
def test_detect_percent_encoded_component(component, encoded_component):
    assert encode_component(component, "utf-8") == encoded_component


@pytest.mark.parametrize(
    ["host", "normalized_host"],
    [
        ("LOCALHOST", "localhost"),
        ("[::1%eth0]", "[::1%25eth0]"),
        ("[::1%25]", "[::1%2525]"),
        ("[::1%%25]", "[::1%25%25]"),
        ("[::1%25%25]", "[::1%25%25]"),
        ("[::Af%Ff]", "[::af%25Ff]"),
        ("[::Af%%Ff]", "[::af%25%Ff]"),
        ("[::Af%25Ff]", "[::af%25Ff]"),
    ],
)
def test_normalize_host(host, normalized_host):
    assert normalize_host(host) == normalized_host
