# -*- coding: utf-8 -*-
import pytest

from rfc3986.uri import URIReference
from rfc3986.normalizers import (
    normalize_scheme, normalize_percent_characters,
    remove_dot_segments, encode_component, normalize_host
    )


def test_normalize_scheme():
    assert 'http' == normalize_scheme('htTp')
    assert 'http' == normalize_scheme('http')
    assert 'http' == normalize_scheme('HTTP')


def test_normalize_percent_characters():
    expected = '%3Athis_should_be_lowercase%DF%AB%4C'
    assert expected == normalize_percent_characters(
        '%3athis_should_be_lowercase%DF%ab%4c')
    assert expected == normalize_percent_characters(
        '%3Athis_should_be_lowercase%DF%AB%4C')
    assert expected == normalize_percent_characters(
        '%3Athis_should_be_lowercase%DF%aB%4C')


paths = [
    # (Input, expected output)
    ('/foo/bar/.', '/foo/bar/'),
    ('/foo/bar/', '/foo/bar/'),
    ('/foo/bar', '/foo/bar'),
    ('./foo/bar', 'foo/bar'),
    ('/./foo/bar', '/foo/bar'),
    ('/foo%20bar/biz%2Abaz', '/foo%20bar/biz%2Abaz'),
    ('../foo/bar', 'foo/bar'),
    ('/../foo/bar', '/foo/bar'),
    ('a/./b/../b/%63/%7Bfoo%7D', 'a/b/%63/%7Bfoo%7D'),
    ('//a/./b/../b/%63/%7Bfoo%7D', '//a/b/%63/%7Bfoo%7D'),
    ('mid/content=5/../6', 'mid/6'),
    ('/a/b/c/./../../g', '/a/g'),
    ]


@pytest.fixture(params=paths)
def path_fixture(request):
    return request.param


@pytest.fixture(params=paths)
def uris(request):
    to_norm, normalized = request.param
    return (URIReference(None, None, to_norm, None, None),
            URIReference(None, None, normalized, None, None))


def test_remove_dot_segments(path_fixture):
    to_normalize, expected = path_fixture
    assert expected == remove_dot_segments(to_normalize)


def test_normalized_equality(uris):
    assert uris[0] == uris[1]


def test_hostname_normalization():
    assert (URIReference(None, 'EXAMPLE.COM', None, None, None) ==
            URIReference(None, 'example.com', None, None, None))


@pytest.mark.parametrize(
    ['authority', 'expected_authority'],
    [
    ('user%2aName@EXAMPLE.COM', 'user%2AName@example.com'),
    ('[::1%eth0]', '[::1%25eth0]')
    ]
)
def test_authority_normalization(authority, expected_authority):
    uri = URIReference(
        None, authority, None, None, None).normalize()
    assert uri.authority == expected_authority


def test_fragment_normalization():
    uri = URIReference(
        None, 'example.com', None, None, 'fiz%DF').normalize()
    assert uri.fragment == 'fiz%DF'


@pytest.mark.parametrize(
    ["component", "encoded_component"],
    [
    ('/%', '/%25'),
    ('/%a', '/%25a'),
    ('/%ag', '/%25ag'),
    ('/%af', '/%af'),
    ('/%20/%', '/%2520/%25'),
    ('/%20%25', '/%20%25'),
    ('/%21%22%23%ah%12%ff', '/%2521%2522%2523%25ah%2512%25ff'),
    ]
)
def test_detect_percent_encoded_component(component, encoded_component):
    assert encode_component(component, 'utf-8') == encoded_component


@pytest.mark.parametrize(
    ["host", "normalized_host"],
    [
    ('LOCALHOST', 'localhost'),
    ('[::1%eth0]', '[::1%25eth0]'),
    ('[::1%25]', '[::1%2525]'),
    ('[::1%%25]', '[::1%25%25]'),
    ('[::1%25%25]', '[::1%25%25]'),
    ('[::Af%Ff]', '[::af%25Ff]'),
    ('[::Af%%Ff]', '[::af%25%Ff]'),
    ('[::Af%25Ff]', '[::af%25Ff]'),
    ]
)
def test_normalize_host(host, normalized_host):
    assert normalize_host(host) == normalized_host
