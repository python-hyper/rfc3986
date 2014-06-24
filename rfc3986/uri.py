# -*- coding: utf-8 -*-
from collections import namedtuple

from .exceptions import InvalidAuthority
from .misc import SUBAUTHORITY_MATCHER, URI_MATCHER, URI_COMPONENTS


class URIReference(namedtuple('URIReference', URI_COMPONENTS)):
    @classmethod
    def from_string(cls, uri_string):
        """Parse a URI reference from the given unicode URI string.

        :param str uri_string: Unicode URI to be parsed into a reference.
        :returns: :class:`URIReference` or subclass thereof
        """
        return URIReference(*URI_MATCHER.match(uri_string).groups())

    def authority_info(self):
        """Returns a dictionary with the ``userinfo``, ``host``, and ``port``.

        If the authority is not valid, it will raise a ``InvalidAuthority``
        Exception.
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
        try:
            authority = self.authority_info()
        except InvalidAuthority:
            return None
        return authority['host']

    @property
    def port(self):
        try:
            authority = self.authority_info()
        except InvalidAuthority:
            return None
        return authority['port']

    @property
    def userinfo(self):
        try:
            authority = self.authority_info()
        except InvalidAuthority:
            return None
        return authority['userinfo']
