# coding: utf-8

import pytest
import rfc3986
from rfc3986.exceptions import InvalidAuthority

try:
    import idna
except ImportError:
    idna = None


requires_idna = pytest.mark.skipif(idna is None, reason="This test requires the 'idna' module")


@requires_idna
@pytest.mark.parametrize(
    ["iri", "uri"],
    [
        (u'http://Bücher.de', u'http://xn--bcher-kva.de'),
        (u'http://faß.de', u'http://xn--fa-hia.de'),
        (u'http://βόλος.com', u'http://xn--nxasmm1c.com'),
        (u'http://ශ්\u200dරී.com', u'http://xn--10cl1a0b660p.com'),
        (u'http://نامه\u200cای.com', u'http://xn--mgba3gch31f060k.com'),
        (u'http://gOoGle.com', u'http://google.com'),
        (u'http://ẞ.com', u'http://xn--zca.com'),
        (u'http://ẞ.foo.com', u'http://xn--zca.foo.com')
    ]
)
def test_encode_iri(iri, uri):
    assert rfc3986.iri_reference(iri).encode().unsplit() == uri


@requires_idna
@pytest.mark.parametrize("iri", [
    u'http://♥.net',
    u'http://\u0378.net',
    u'http://㛼.com',
    u'http://abc..def'
])
def test_encode_invalid_iri(iri):
    iri_ref = rfc3986.iri_reference(iri)
    with pytest.raises(InvalidAuthority):
        iri_ref.encode()
