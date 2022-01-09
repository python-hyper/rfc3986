import sys

import pytest

import rfc3986
from rfc3986.exceptions import InvalidAuthority

try:
    import idna
except ImportError:
    idna = None


requires_idna = pytest.mark.skipif(
    idna is None, reason="This test requires the 'idna' module"
)
iri_to_uri = pytest.mark.parametrize(
    ["iri", "uri"],
    [
        ("http://Bücher.de", "http://xn--bcher-kva.de"),
        ("http://faß.de", "http://xn--fa-hia.de"),
        (
            "http://βόλος.com/β/ό?λ#ος",
            "http://xn--nxasmm1c.com/%CE%B2/%CF%8C?%CE%BB#%CE%BF%CF%82",
        ),
        ("http://ශ්\u200dරී.com", "http://xn--10cl1a0b660p.com"),
        ("http://نامه\u200cای.com", "http://xn--mgba3gch31f060k.com"),
        ("http://Bü:ẞ@gOoGle.com", "http://B%C3%BC:%E1%BA%9E@gOoGle.com"),
        ("http://ẞ.com:443", "http://xn--zca.com:443"),
        ("http://ẞ.foo.com", "http://xn--zca.foo.com"),
        ("http://Bẞ.com", "http://xn--b-qfa.com"),
        (
            "http+unix://%2Ftmp%2FTEST.sock/get",
            "http+unix://%2Ftmp%2FTEST.sock/get",
        ),
    ],
)


@requires_idna
@iri_to_uri
def test_encode_iri(iri, uri):
    assert rfc3986.iri_reference(iri).encode().unsplit() == uri


@iri_to_uri
def test_iri_equality(iri, uri):
    assert rfc3986.iri_reference(iri) == iri


def test_iri_equality_special_cases():
    assert rfc3986.iri_reference("http://Bü:ẞ@βόλος.com/β/ό?λ#ος") == (
        "http",
        "Bü:ẞ@βόλος.com",
        "/%CE%B2/%CF%8C",
        "%CE%BB",
        "%CE%BF%CF%82",
    )

    with pytest.raises(TypeError):
        rfc3986.iri_reference("http://ẞ.com") == 1


@requires_idna
@pytest.mark.parametrize(
    "iri",
    [
        "http://♥.net",
        "http://\u0378.net",
        pytest.param(
            "http://㛼.com",
            marks=pytest.mark.skipif(
                sys.version_info < (3, 3) and sys.maxunicode <= 0xFFFF,
                reason="Python configured without UCS-4 support",
            ),
        ),
    ],
)
def test_encode_invalid_iri(iri):
    iri_ref = rfc3986.iri_reference(iri)
    with pytest.raises(InvalidAuthority):
        iri_ref.encode()
