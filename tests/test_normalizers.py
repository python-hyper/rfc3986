# -*- coding: utf-8 -*-
from rfc3986.normalizers import normalize_scheme, normalize_percent_characters


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
