# -*- coding: utf-8 -*-
from rfc3986.uri import URIReference
from rfc3986.misc import merge_paths


def test_merge_paths_with_base_path_without_base_authority():
    """Demonstrate merging with a base URI without an authority."""
    base = URIReference(scheme=None,
                        authority=None,
                        path='/foo/bar/bogus',
                        query=None,
                        fragment=None)
    expected = '/foo/bar/relative'
    assert merge_paths(base, 'relative') == expected


def test_merge_paths_with_base_authority_and_path():
    """Demonstrate merging with a base URI with an authority and path."""
    base = URIReference(scheme=None,
                        authority='authority',
                        path='/foo/bar/bogus',
                        query=None,
                        fragment=None)
    expected = '/foo/bar/relative'
    assert merge_paths(base, 'relative') == expected


def test_merge_paths_without_base_authority_or_path():
    """Demonstrate merging with a base URI without an authority or path."""
    base = URIReference(scheme=None,
                        authority=None,
                        path=None,
                        query=None,
                        fragment=None)
    expected = '/relative'
    assert merge_paths(base, 'relative') == expected


def test_merge_paths_with_base_authority_without_path():
    """Demonstrate merging with a base URI without an authority or path."""
    base = URIReference(scheme=None,
                        authority='authority',
                        path=None,
                        query=None,
                        fragment=None)
    expected = '/relative'
    assert merge_paths(base, 'relative') == expected
