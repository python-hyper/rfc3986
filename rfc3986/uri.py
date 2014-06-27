# -*- coding: utf-8 -*-
# Copyright (c) 2014 Rackspace
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

from .compat import to_str
from .exceptions import InvalidAuthority
from .misc import (
    FRAGMENT_MATCHER, PATH_MATCHER, QUERY_MATCHER, SCHEME_MATCHER,
    SUBAUTHORITY_MATCHER, URI_MATCHER, URI_COMPONENTS
    )
from .normalizers import (
    encode_component, normalize_scheme, normalize_authority, normalize_path,
    normalize_query, normalize_fragment
    )


class URIReference(namedtuple('URIReference', URI_COMPONENTS)):
    slots = ()

    def __new__(cls, scheme, authority, path, query, fragment):
        return super(URIReference, cls).__new__(
            cls,
            scheme or None,
            authority or None,
            path or None,
            query or None,
            fragment or None)

    def __eq__(self, other):
        other_ref = other
        if isinstance(other, tuple):
            other_ref = URIReference(*other)
        elif not isinstance(other, URIReference):
            try:
                other_ref = URIReference.from_string(other)
            except TypeError:
                raise TypeError(
                    'Unable to compare URIReference() to {0}()'.format(
                        type(other).__name__))

        # See http://tools.ietf.org/html/rfc3986#section-6.2
        naive_equality = tuple(self) == tuple(other_ref)
        return naive_equality or self.normalized_equality(other_ref)

    @classmethod
    def from_string(cls, uri_string, encoding='utf-8'):
        """Parse a URI reference from the given unicode URI string.

        :param str uri_string: Unicode URI to be parsed into a reference.
        :param str encoding: The encoding of the string provided
        :returns: :class:`URIReference` or subclass thereof
        """
        uri_string = to_str(uri_string, encoding)

        split_uri = URI_MATCHER.match(uri_string).groupdict()
        return URIReference(split_uri['scheme'], split_uri['authority'],
                            encode_component(split_uri['path'], encoding),
                            encode_component(split_uri['query'], encoding),
                            encode_component(split_uri['fragment'], encoding))

    def authority_info(self):
        """Returns a dictionary with the ``userinfo``, ``host``, and ``port``.

        If the authority is not valid, it will raise a ``InvalidAuthority``
        Exception.

        :returns:
            ``{'userinfo': 'username:password', 'host': 'www.example.com',
            'port': '80'}``
        :rtype: dict
        :raises InvalidAuthority: If the authority is not ``None`` and can not
            be parsed.
        """
        if not self.authority:
            return {'userinfo': None, 'host': None, 'port': None}

        match = SUBAUTHORITY_MATCHER.match(self.authority)

        if match is None:
            # In this case, we have an authority that was parsed from the URI
            # Reference, but it cannot be further parsed by our
            # SUBAUTHORITY_MATCHER. In this case it must not be a valid
            # authority.
            raise InvalidAuthority(self.authority)

        return match.groupdict()

    @property
    def host(self):
        """If present, a string representing the host."""
        try:
            authority = self.authority_info()
        except InvalidAuthority:
            return None
        return authority['host']

    @property
    def port(self):
        """If present, the port (as a string) extracted from the authority."""
        try:
            authority = self.authority_info()
        except InvalidAuthority:
            return None
        return authority['port']

    @property
    def userinfo(self):
        """If present, the userinfo extracted from the authority."""
        try:
            authority = self.authority_info()
        except InvalidAuthority:
            return None
        return authority['userinfo']

    def is_valid(self):
        """Determines if the URI is valid.

        :returns: ``True`` if the URI is valid. ``False`` otherwise.
        :rtype: bool
        """
        validators = [self.authority_is_valid, self.scheme_is_valid,
                      self.path_is_valid, self.query_is_valid,
                      self.fragment_is_valid]
        return all(v() for v in validators)

    def authority_is_valid(self):
        """Determines if the authority component is valid.

        :returns: ``True`` if the authority is valid. ``False`` otherwise.
        :rtype: bool
        """
        if (self.authority is None or
                SUBAUTHORITY_MATCHER.match(self.authority)):
            return True
        return False

    def scheme_is_valid(self):
        """Determines if the scheme component is valid.

        :returns: ``True`` if the scheme is valid. ``False`` otherwise.
        :rtype: bool
        """
        if self.scheme is None or SCHEME_MATCHER.match(self.scheme):
            return True
        return False

    def path_is_valid(self):
        """Determines if the path component is valid.

        :returns: ``True`` if the path is valid. ``False`` otherwise.
        :rtype: bool
        """
        if self.path is None or PATH_MATCHER.match(self.path):
            return True
        return False

    def query_is_valid(self):
        """Determines if the query component is valid.

        :returns: ``True`` if the query is valid. ``False`` otherwise.
        :rtype: bool
        """
        if self.query is None or QUERY_MATCHER.match(self.query):
            return True
        return False

    def fragment_is_valid(self):
        """Determines if the fragment component is valid.

        :returns: ``True`` if the fragment is valid. ``False`` otherwise.
        :rtype: bool
        """
        if self.fragment is None or FRAGMENT_MATCHER.match(self.fragment):
            return True
        return False

    def normalize(self):
        """Normalize this reference as described in Section 6.2.2

        This is not an in-place normalization. Instead this creates a new
        URIReference.

        :returns: A new reference object with normalized components.
        :rtype: URIReference
        """
        # See http://tools.ietf.org/html/rfc3986#section-6.2.2 for logic in
        # this method.
        return URIReference(normalize_scheme(self.scheme or ''),
                            normalize_authority(
                                (self.userinfo, self.host, self.port)),
                            normalize_path(self.path or ''),
                            normalize_query(self.query or ''),
                            normalize_fragment(self.fragment or ''))

    def normalized_equality(self, other_ref):
        """Compare this URIReference to another URIReference.

        :param URIReference other_ref: (required), The reference with which
            we're comparing.
        :returns: ``True`` if the references are equal, ``False`` otherwise.
        :rtype: bool
        """
        return tuple(self.normalize()) == tuple(other_ref.normalize())

    def unsplit(self):
        """Create a URI string from the components.

        :returns: The URI Reference reconstituted as a string.
        :rtype: str
        """
        # See http://tools.ietf.org/html/rfc3986#section-5.3
        result_list = []
        if self.scheme:
            result_list.extend([self.scheme, ':'])
        if self.authority:
            result_list.extend(['//', self.authority])
        if self.path:
            result_list.append(self.path)
        if self.query:
            result_list.extend(['?', self.query])
        if self.fragment:
            result_list.extend(['#', self.fragment])
        return ''.join(result_list)
