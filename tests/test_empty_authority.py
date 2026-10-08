import pytest

from rfc3986 import iri_reference
from rfc3986 import uri_reference
from rfc3986 import urlparse
from rfc3986.parseresult import ParseResult
from rfc3986.parseresult import ParseResultBytes


@pytest.mark.parametrize("parse", [uri_reference, iri_reference, urlparse])
@pytest.mark.parametrize(
    "text", ["foo:///", "file:///tmp/a", "//", "///a?x#y"]
)
def test_empty_authority_round_trip(parse, text):
    reference = parse(text)
    assert reference.authority == ""
    assert reference.unsplit() == text
    assert (
        reference.copy_with(fragment="new").unsplit()
        == text.split("#")[0] + "#new"
    )


@pytest.mark.parametrize("text", ["foo:///", "file:///tmp/a", "//"])
def test_normalization_and_encoding_preserve_empty_authority(text):
    assert uri_reference(text).normalize().unsplit() == text
    assert iri_reference(text).encode().unsplit() == text
    assert urlparse(text).encode().unsplit() == text.encode()


@pytest.mark.parametrize("text", ["foo:/", "/tmp/a", "a", ""])
def test_absent_authority_remains_absent(text):
    reference = uri_reference(text)
    assert reference.authority is None
    assert reference.normalize().authority is None
    assert reference.unsplit() == text


@pytest.mark.parametrize("cls", [ParseResult, ParseResultBytes])
def test_from_parts_distinguishes_empty_and_absent_host(cls):
    absent = cls.from_parts(scheme="foo", path="/a")
    empty = cls.from_parts(scheme="foo", host="", path="/a")

    def as_string(value):
        return value.decode() if isinstance(value, bytes) else value

    assert as_string(absent.unsplit()) == "foo:/a"
    assert as_string(empty.unsplit()) == "foo:///a"


@pytest.mark.parametrize(
    "relative, base, expected",
    [
        ("///new", "foo://example.com/old", "foo:///new"),
        ("new", "foo://", "foo:///new"),
        ("", "foo://", "foo://"),
    ],
)
def test_resolve_with_empty_authority(relative, base, expected):
    result = uri_reference(relative).resolve_with(base)
    assert result.authority == ""
    assert result.unsplit() == expected
