# -*- coding: utf-8 -*-
import pytest

from rfc3986.uri import URIReference
from rfc3986.normalizers import (
    normalize_scheme, normalize_percent_characters, remove_dot_segments
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


def test_authority_normalization():
    uri = URIReference(
        None, 'user%2aName@EXAMPLE.COM', None, None, None).normalize()
    assert uri.authority == 'user%2AName@example.com'


def test_fragment_normalization():
    uri = URIReference(
        None, 'example.com', None, None, 'fiz%DF').normalize()
    assert uri.fragment == 'fiz%DF'
