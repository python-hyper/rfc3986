"""Module containing the implementation of the URIReference class."""
# -*- coding: utf-8 -*-
# Copyright (c) 2014 Rackspace
# Copyright (c) 2015 Ian Stapleton Cordasco
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

from . import compat
from . import misc
from . import normalizers
from . import uri


class IRIReference(namedtuple('IRIReference', misc.URI_COMPONENTS), uri.URIMixin):

    slots = ()

    def __new__(cls, scheme, authority, path, query, fragment,
                encoding='utf-8'):
        """Create a new URIReference."""
        ref = super(IRIReference, cls).__new__(
            cls,
            scheme or None,
            authority or None,
            path or None,
            query,
            fragment)
        ref.encoding = encoding
        return ref

    def _match_subauthority(self):
        return misc.ISUBAUTHORITY_MATCHER.match(self.authority)

    @classmethod
    def from_string(cls, iri_string, encoding='utf-8'):
        """Parse a URI reference from the given unicode URI string.

        :param str iri_string: Unicode IRI to be parsed into a reference.
        :param str encoding: The encoding of the string provided
        :returns: :class:`URIReference` or subclass thereof
        """
        iri_string = compat.to_str(iri_string, encoding)

        split_iri = misc.IRI_MATCHER.match(iri_string).groupdict()
        return cls(
            split_iri['scheme'], split_iri['authority'],
            normalizers.encode_component(split_iri['path'], encoding),
            normalizers.encode_component(split_iri['query'], encoding),
            normalizers.encode_component(split_iri['fragment'], encoding),
            encoding,
        )

    def encode(self, idna_encoder=None):
        """
        Encodes an IRIReference into a URIReference instance

        :rtype: uri.URIReference
        :returns: A URI reference
        """
        authority = self.authority
        if idna_encoder is not None and self.authority:
            authority = compat.to_str(idna_encoder(self.host))
            if self.userinfo is not None:
                authority = normalizers.encode_component(self.userinfo, self.encoding) + '@' + authority
            if self.port is not None:
                authority += ":" + str(self.port)

        return uri.URIReference(self.scheme,
                                authority,
                                path=self.path,
                                query=self.query,
                                fragment=self.fragment,
                                encoding=self.encoding)
