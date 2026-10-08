import pytest

from rfc3986 import exceptions
from rfc3986 import uri_reference
from rfc3986 import validators


@pytest.mark.parametrize("text", [".://", "1:a", ":a", "a_b:c", "a%20b:c"])
def test_relative_first_segment_cannot_contain_colon(text):
    reference = uri_reference(text)
    assert reference.scheme is None
    with pytest.raises(exceptions.InvalidComponentsError):
        validators.Validator().check_validity_of("path").validate(reference)
    assert not reference.path_is_valid()
    assert not reference.is_valid()


@pytest.mark.parametrize(
    "text",
    ["./a:b", "/a:b", "a/b:c", "a%3Ab", "a:b", "urn:a:b", "", "?q=a:b"],
)
def test_colons_remain_valid_outside_relative_first_segment(text):
    reference = uri_reference(text)
    validators.Validator().check_validity_of("path").validate(reference)
    assert reference.path_is_valid()
    assert reference.is_valid()


def test_component_validation_does_not_infer_uri_context():
    assert validators.path_is_valid("a:b")


def test_path_validation_remains_opt_in():
    validators.Validator().validate(uri_reference(".://"))


def test_required_path_still_rejects_missing_path():
    assert not uri_reference("https://example.com").path_is_valid(require=True)
