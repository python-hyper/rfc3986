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
from . import exceptions
from . import misc
from . import normalizers
from . import uri


try:
    import idna
except ImportError:
    idna = None


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

    def __eq__(self, other):
        """Compare this reference to another."""
        other_ref = other
        if isinstance(other, tuple):
            other_ref = self.__class__(*other)
        elif not isinstance(other, IRIReference):
            try:
                other_ref = self.__class__.from_string(other)
            except TypeError:
                raise TypeError(
                    'Unable to compare {0}() to {1}()'.format(
                        type(self).__name__, type(other).__name__))

        # See http://tools.ietf.org/html/rfc3986#section-6.2
        naive_equality = tuple(self) == tuple(other_ref)
        return naive_equality or self.normalized_equality(other_ref)

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
        if authority:
            if idna_encoder is None:
                if idna is None:
                    raise exceptions.MissingDependencyError(
                        "Could not import the 'idna' module and the IRI hostname requires encoding"
                    )
                else:
                    def idna_encoder(x):
                        try:
                            return idna.encode(x, strict=True, std3_rules=True)
                        except idna.IDNAError:
                            raise exceptions.InvalidAuthority(self.authority)

            authority = ""
            if self.host:
                authority = ".".join([compat.to_str(idna_encoder(part.lower())) for part in self.host.split(".")])
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
