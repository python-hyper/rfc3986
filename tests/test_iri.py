# coding: utf-8

import pytest
import rfc3986
import sys
from rfc3986.exceptions import InvalidAuthority

try:
    import idna
except ImportError:
    idna = None


requires_idna = pytest.mark.skipif(idna is None, reason="This test requires the 'idna' module")
iri_to_uri = pytest.mark.parametrize(
    ["iri", "uri"],
    [
        (u'http://Bücher.de', u'http://xn--bcher-kva.de'),
        (u'http://faß.de', u'http://xn--fa-hia.de'),
        (u'http://βόλος.com/β/ό?λ#ος', u'http://xn--nxasmm1c.com/%CE%B2/%CF%8C?%CE%BB#%CE%BF%CF%82'),
        (u'http://ශ්\u200dරී.com', u'http://xn--10cl1a0b660p.com'),
        (u'http://نامه\u200cای.com', u'http://xn--mgba3gch31f060k.com'),
        (u'http://Bü:ẞ@gOoGle.com', u'http://B%C3%BC:%E1%BA%9E@gOoGle.com'),
        (u'http://ẞ.com:443', u'http://xn--zca.com:443'),
        (u'http://ẞ.foo.com', u'http://xn--zca.foo.com'),
        (u'http://Bẞ.com', u'http://xn--b-qfa.com'),
        (u'http+unix://%2Ftmp%2FTEST.sock/get', 'http+unix://%2Ftmp%2FTEST.sock/get'),
    ]
)


@requires_idna
@iri_to_uri
def test_encode_iri(iri, uri):
    assert rfc3986.iri_reference(iri).encode().unsplit() == uri


@iri_to_uri
def test_iri_equality(iri, uri):
    assert rfc3986.iri_reference(iri) == iri


def test_iri_equality_special_cases():
    assert rfc3986.iri_reference(u"http://Bü:ẞ@βόλος.com/β/ό?λ#ος") == \
           (u"http", u"Bü:ẞ@βόλος.com", u"/%CE%B2/%CF%8C", u"%CE%BB", u"%CE%BF%CF%82")

    with pytest.raises(TypeError):
        rfc3986.iri_reference(u"http://ẞ.com") == 1


@requires_idna
@pytest.mark.parametrize("iri", [
    u'http://♥.net',
    u'http://\u0378.net',
    pytest.param(
        u'http://㛼.com',
        marks=pytest.mark.skipif(
            sys.version_info < (3, 3) and sys.maxunicode <= 0xFFFF,
            reason="Python configured without UCS-4 support"
        )
    ),
])
def test_encode_invalid_iri(iri):
    iri_ref = rfc3986.iri_reference(iri)
    with pytest.raises(InvalidAuthority):
        iri_ref.encode()
