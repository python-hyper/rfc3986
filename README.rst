rfc3986
=======

A Python implementation of `RFC 3986`_ including validation and authority 
parsing. Coming soon: `Reference Resolution <http://tools.ietf.org/html/rfc3986#section-5>`_.

Example Usage
-------------

To parse a URI into a convenient named tuple, you can simply::

    from rfc3986 import uri_reference

    example = uri_reference('http://example.com')
    email = uri_reference('mailto:user@domain.com')
    ssh = uri_reference('ssh://user@git.openstack.org:29418/openstack/keystone.git')

With a parsed URI you can access data about the components::

    print(example.scheme)  # => http
    print(email.path)  # => user@domain.com
    print(ssh.userinfo)  # => user
    print(ssh.host)  # => git.openstack.org
    print(ssh.port)  # => 29418

It can also parse URIs with unicode present::

    uni = uri_reference(b'http://httpbin.org/get?utf8=\xe2\x98\x83')  # ☃
    print(uni.query)  # utf8=%E2%98%83

With a parsed URI you can also validate it::

    if ssh.is_valid():
        subprocess.call(['git', 'clone', ssh.unsplit()])

You can also take a parsed URI and normalize it::

    mangled = uri_reference('hTTp://exAMPLe.COM')
    print(mangled.scheme)  # => hTTp
    print(mangled.authority)  # => exAMPLe.COM

    normal = mangled.normalize()
    print(normal.scheme)  # => http
    print(mangled.authority)  # => example.com

But these two URIs are (functionally) equivalent::

    if normal == mangled:
        webbrowser.open(normal.unsplit())

Your paths, queries, and fragments are safe with us though::

    mangled = uri_reference('hTTp://exAMPLe.COM/Some/reallY/biZZare/pAth')
    normal = mangled.normalize()
    assert normal == 'hTTp://exAMPLe.COM/Some/reallY/biZZare/pAth'
    assert normal == 'http://example.com/Some/reallY/biZZare/pAth'
    assert normal != 'http://example.com/some/really/bizzare/path'

If you do not actually need a real reference object and just want to normalize
your URI::

    from rfc3986 import normalize_uri

    assert (normalize_uri('hTTp://exAMPLe.COM/Some/reallY/biZZare/pAth') ==
            'http://example.com/Some/reallY/biZZare/pAth')

You can also very simply validate a URI::

    from rfc3986 import is_valid_uri

    assert is_valid_uri('hTTp://exAMPLe.COM/Some/reallY/biZZare/pAth')

.. _RFC 3986: http://tools.ietf.org/html/rfc3986
