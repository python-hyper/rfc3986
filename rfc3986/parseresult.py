# -*- coding: utf-8 -*-
# Copyright (c) 2015 Ian Cordasco
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from collections import namedtuple

from . import exceptions
from . import normalizers
from . import uri

PARSED_COMPONENTS = ('scheme', 'userinfo', 'host', 'port', 'path', 'query',
                     'fragment')


class ParseResult(namedtuple('ParseResult', PARSED_COMPONENTS)):
    slots = ()

    def __new__(cls, scheme, userinfo, host, port, path, query, fragment,
                uri_ref, encoding='utf-8'):
        parse_result = super(ParseResult, cls).__new__(
            cls,
            scheme or None,
            userinfo or None,
            host,
            port or None,
            path or None,
            query or None,
            fragment or None)
        parse_result.encoding = encoding
        parse_result.reference = uri_ref
        return parse_result

    @classmethod
    def from_string(cls, uri_string, encoding='utf-8', strict=True):
        """Parse a URI from the given unicode URI string.

        :param str uri_string: Unicode URI to be parsed into a reference.
        :param str encoding: The encoding of the string provided
        :param bool strict: Parse strictly according to :rfc:`3986` if True.
            If False, parse similarly to the standard library's urlparse
            function.
        :returns: :class:`ParseResult` or subclass thereof
        """
        reference = uri.URIReference.from_string(uri_string, encoding)
        try:
            subauthority = reference.authority_info()
        except exceptions.InvalidAuthority:
            if strict:
                raise
            userinfo, host, port = split_authority(reference.authority)
        else:
            # Thanks to Richard Barrell for this idea:
            # https://twitter.com/0x2ba22e11/status/617338811975139328
            userinfo, host, port = (subauthority.get(p)
                                    for p in ('userinfo', 'host', 'port'))

        if port:
            try:
                port = int(port)
            except ValueError:
                raise exceptions.InvalidPort(port)

        return cls(scheme=reference.scheme,
                   userinfo=userinfo,
                   host=host,
                   port=port,
                   path=reference.path,
                   query=reference.query,
                   fragment=reference.fragment,
                   uri_ref=reference,
                   encoding=encoding)

    @property
    def authority(self):
        """Normalized authority generated from the subauthority parts."""
        _authority = getattr(self, '_authority', None)
        if _authority is None:
            _authority = self._authority = normalizers.normalize_authority(
                (self.userinfo, self.host, self.port)
            )
        return _authority

    def _generate_authority(self, attributes):
        # I swear I did not align the comparisons below. That's just how they
        # happened to align based on pep8 and attribute lengths.
        userinfo, host, port = (attributes[p]
                                for p in ('userinfo', 'host', 'port'))
        if (self.userinfo != userinfo or
                self.host != host or
                self.port != port):
            return normalizers.normalize_authority((userinfo, host, port))
        return self.authority

    def copy_with(self, scheme=None, userinfo=None, host=None, port=None,
                  path=None, query=None, fragment=None):
        attributes = zip(PARSED_COMPONENTS,
                         (scheme, userinfo, host, port, path, query, fragment))
        attrs_dict = {}
        for name, value in attributes:
            if value is None:
                value = getattr(self, name)
            attrs_dict[name] = value
        authority = self._generate_authority(attrs_dict)
        ref = self.reference.copy_with(scheme=attrs_dict.get('scheme'),
                                       authority=authority,
                                       path=attrs_dict.get('path'),
                                       query=attrs_dict.get('query'),
                                       fragment=attrs_dict.get('fragment'))
        return ParseResult(uri_ref=ref, **attrs_dict)

    def geturl(self):
        """Standard library shim to the unsplit method."""
        return self.unsplit()

    @property
    def hostname(self):
        """Standard library shim for the host portion of the URI."""
        return self.host

    @property
    def netloc(self):
        """Standard library shim for the authority portion of the URI."""
        return self.authority

    @property
    def params(self):
        """Standard library shim for the query portion of the URI."""
        return self.query

    def unsplit(self, use_idna=False):
        """Create a URI string from the components.

        :returns: The parsed URI reconstituted as a string.
        :rtype: str
        """
        parse_result = self
        if use_idna:
            hostbytes = self.host.encode('idna')
            host = hostbytes.decode(self.encoding)
            parse_result = self.copy_with(host=host)
        return parse_result.reference.unsplit()


def split_authority(authority):
    # Initialize our expected return values
    userinfo = host = port = None
    # Initialize an extra var we may need to use
    extra_host = None
    # Set-up rest in case there is no userinfo portion
    rest = authority

    if u'@' in authority:
        userinfo, rest = authority.rsplit(u'@', 1)

    # Handle IPv6 host addresses
    if rest.startswith(u'['):
        host, rest = rest.split(u']', 1)

    if ':' in rest:
        extra_host, port = rest.split(u':', 1)
    elif not host and rest:
        host = rest

    if extra_host and not host:
        host = extra_host

    return userinfo, host, port