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
"""Module containing the urlparse compatibility logic."""
import typing as t
from collections import namedtuple

from . import compat
from . import exceptions
from . import misc
from . import normalizers
from . import uri
from ._typing_compat import Self as _Self

__all__ = ("ParseResult", "ParseResultBytes")

PARSED_COMPONENTS = (
    "scheme",
    "userinfo",
    "host",
    "port",
    "path",
    "query",
    "fragment",
)


class ParseResultMixin(t.Generic[t.AnyStr]):
    if t.TYPE_CHECKING:
        userinfo: t.Optional[t.AnyStr]
        host: t.Optional[t.AnyStr]
        port: t.Optional[int]
        query: t.Optional[t.AnyStr]
        encoding: str

        @property
        def authority(self) -> t.Optional[t.AnyStr]: ...

    def _generate_authority(
        self,
        attributes: t.Dict[str, t.Optional[t.AnyStr]],
    ) -> t.Optional[str]:
        # I swear I did not align the comparisons below. That's just how they
        # happened to align based on pep8 and attribute lengths.
        userinfo, host, port = (
            attributes[p] for p in ("userinfo", "host", "port")
        )
        if self.userinfo != userinfo or self.host != host or self.port != port:
            if port:
                port = f"{port}"
            return normalizers.normalize_authority(
                (
                    compat.to_str(userinfo, self.encoding),
                    compat.to_str(host, self.encoding),
                    port,
                )
            )
        if isinstance(self.authority, bytes):
            return self.authority.decode("utf-8")
        return self.authority

    def geturl(self) -> t.AnyStr:
        """Shim to match the standard library method."""
        return self.unsplit()

    @property
    def hostname(self) -> t.Optional[t.AnyStr]:
        """Shim to match the standard library."""
        return self.host

    @property
    def netloc(self) -> t.Optional[t.AnyStr]:
        """Shim to match the standard library."""
        return self.authority

    @property
    def params(self) -> t.Optional[t.AnyStr]:
        """Shim to match the standard library."""
        return self.query


class ParseResult(
    namedtuple("ParseResult", PARSED_COMPONENTS), ParseResultMixin[str]
):
    """Implementation of urlparse compatibility class.

    This uses the URIReference logic to handle compatibility with the
    urlparse.ParseResult class.
    """

    scheme: t.Optional[str]
    userinfo: t.Optional[str]
    host: t.Optional[str]
    port: t.Optional[int]
    path: t.Optional[str]
    query: t.Optional[str]
    fragment: t.Optional[str]
    encoding: str
    reference: "uri.URIReference"

    def __new__(
        cls,
        scheme: t.Optional[str],
        userinfo: t.Optional[str],
        host: t.Optional[str],
        port: t.Optional[int],
        path: t.Optional[str],
        query: t.Optional[str],
        fragment: t.Optional[str],
        uri_ref: "uri.URIReference",
        encoding: str = "utf-8",
    ) -> _Self:
        """Create a new ParseResult."""
        parse_result = super().__new__(
            cls,
            scheme or None,
            userinfo or None,
            host,
            port or None,
            path or None,
            query,
            fragment,
        )
        parse_result.encoding = encoding
        parse_result.reference = uri_ref
        return parse_result

    @classmethod
    def from_parts(
        cls,
        scheme: t.Optional[str] = None,
        userinfo: t.Optional[str] = None,
        host: t.Optional[str] = None,
        port: t.Optional[t.Union[int, str]] = None,
        path: t.Optional[str] = None,
        query: t.Optional[str] = None,
        fragment: t.Optional[str] = None,
        encoding: str = "utf-8",
    ) -> _Self:
        """Create a ParseResult instance from its parts."""
        authority = ""
        if userinfo is not None:
            authority += userinfo + "@"
        if host is not None:
            authority += host
        if port is not None:
            authority += f":{port}"
        uri_ref = uri.URIReference(
            scheme=scheme,
            authority=authority,
            path=path,
            query=query,
            fragment=fragment,
            encoding=encoding,
        ).normalize()
        userinfo, host, port = authority_from(uri_ref, strict=True)
        return cls(
            scheme=uri_ref.scheme,
            userinfo=userinfo,
            host=host,
            port=port,
            path=uri_ref.path,
            query=uri_ref.query,
            fragment=uri_ref.fragment,
            uri_ref=uri_ref,
            encoding=encoding,
        )

    @classmethod
    def from_string(
        cls,
        uri_string: t.Union[str, bytes],
        encoding: str = "utf-8",
        strict: bool = True,
        lazy_normalize: bool = True,
    ) -> _Self:
        """Parse a URI from the given unicode URI string.

        :param str uri_string: Unicode URI to be parsed into a reference.
        :param str encoding: The encoding of the string provided
        :param bool strict: Parse strictly according to :rfc:`3986` if True.
            If False, parse similarly to the standard library's urlparse
            function.
        :returns: :class:`ParseResult` or subclass thereof
        """
        reference = uri.URIReference.from_string(uri_string, encoding)
        if not lazy_normalize:
            reference = reference.normalize()
        userinfo, host, port = authority_from(reference, strict)

        return cls(
            scheme=reference.scheme,
            userinfo=userinfo,
            host=host,
            port=port,
            path=reference.path,
            query=reference.query,
            fragment=reference.fragment,
            uri_ref=reference,
            encoding=encoding,
        )

    @property
    def authority(self) -> t.Optional[str]:
        """Return the normalized authority."""
        return self.reference.authority

    def copy_with(
        self,
        scheme: t.Optional[str] = misc.UseExisting,
        userinfo: t.Optional[str] = misc.UseExisting,
        host: t.Optional[str] = misc.UseExisting,
        port: t.Optional[t.Union[int, str]] = misc.UseExisting,
        path: t.Optional[str] = misc.UseExisting,
        query: t.Optional[str] = misc.UseExisting,
        fragment: t.Optional[str] = misc.UseExisting,
    ) -> "ParseResult":
        """Create a copy of this instance replacing with specified parts."""
        attributes = zip(
            PARSED_COMPONENTS,
            (scheme, userinfo, host, port, path, query, fragment),
        )
        attrs_dict: t.Dict[str, t.Optional[str]] = {}
        for name, value in attributes:
            if value is misc.UseExisting:
                value = getattr(self, name)
            attrs_dict[name] = value
        authority = self._generate_authority(attrs_dict)
        ref = self.reference.copy_with(
            scheme=attrs_dict["scheme"],
            authority=authority,
            path=attrs_dict["path"],
            query=attrs_dict["query"],
            fragment=attrs_dict["fragment"],
        )
        return ParseResult(uri_ref=ref, encoding=self.encoding, **attrs_dict)

    def encode(self, encoding: t.Optional[str] = None) -> "ParseResultBytes":
        """Convert to an instance of ParseResultBytes."""
        encoding = encoding or self.encoding
        attrs = dict(
            zip(
                PARSED_COMPONENTS,
                (
                    attr.encode(encoding) if hasattr(attr, "encode") else attr
                    for attr in self
                ),
            )
        )
        return ParseResultBytes(
            uri_ref=self.reference, encoding=encoding, **attrs
        )

    def unsplit(self, use_idna: bool = False) -> str:
        """Create a URI string from the components.

        :returns: The parsed URI reconstituted as a string.
        :rtype: str
        """
        parse_result = self
        if use_idna and self.host:
            hostbytes = self.host.encode("idna")
            host = hostbytes.decode(self.encoding)
            parse_result = self.copy_with(host=host)
        return parse_result.reference.unsplit()


class ParseResultBytes(
    namedtuple("ParseResultBytes", PARSED_COMPONENTS), ParseResultMixin[bytes]
):
    """Compatibility shim for the urlparse.ParseResultBytes object."""

    scheme: t.Optional[bytes]
    userinfo: t.Optional[bytes]
    host: t.Optional[bytes]
    port: t.Optional[int]
    path: t.Optional[bytes]
    query: t.Optional[bytes]
    fragment: t.Optional[bytes]
    encoding: str
    reference: "uri.URIReference"
    lazy_normalize: bool

    def __new__(
        cls,
        scheme: t.Optional[bytes],
        userinfo: t.Optional[bytes],
        host: t.Optional[bytes],
        port: t.Optional[int],
        path: t.Optional[bytes],
        query: t.Optional[bytes],
        fragment: t.Optional[bytes],
        uri_ref: "uri.URIReference",
        encoding: str = "utf-8",
        lazy_normalize: bool = True,
    ) -> _Self:
        """Create a new ParseResultBytes instance."""
        parse_result = super().__new__(
            cls,
            scheme or None,
            userinfo or None,
            host,
            port or None,
            path or None,
            query or None,
            fragment or None,
        )
        parse_result.encoding = encoding
        parse_result.reference = uri_ref
        parse_result.lazy_normalize = lazy_normalize
        return parse_result

    @classmethod
    def from_parts(
        cls,
        scheme: t.Optional[str] = None,
        userinfo: t.Optional[str] = None,
        host: t.Optional[str] = None,
        port: t.Optional[t.Union[int, str]] = None,
        path: t.Optional[str] = None,
        query: t.Optional[str] = None,
        fragment: t.Optional[str] = None,
        encoding: str = "utf-8",
        lazy_normalize: bool = True,
    ) -> _Self:
        """Create a ParseResult instance from its parts."""
        authority = ""
        if userinfo is not None:
            authority += userinfo + "@"
        if host is not None:
            authority += host
        if port is not None:
            authority += f":{int(port)}"
        uri_ref = uri.URIReference(
            scheme=scheme,
            authority=authority,
            path=path,
            query=query,
            fragment=fragment,
            encoding=encoding,
        )
        if not lazy_normalize:
            uri_ref = uri_ref.normalize()
        to_bytes = compat.to_bytes
        userinfo, host, port = authority_from(uri_ref, strict=True)
        return cls(
            scheme=to_bytes(scheme, encoding),
            userinfo=to_bytes(userinfo, encoding),
            host=to_bytes(host, encoding),
            port=port,
            path=to_bytes(path, encoding),
            query=to_bytes(query, encoding),
            fragment=to_bytes(fragment, encoding),
            uri_ref=uri_ref,
            encoding=encoding,
            lazy_normalize=lazy_normalize,
        )

    @classmethod
    def from_string(
        cls,
        uri_string: t.Union[str, bytes],
        encoding: str = "utf-8",
        strict: bool = True,
        lazy_normalize: bool = True,
    ) -> _Self:
        """Parse a URI from the given unicode URI string.

        :param str uri_string: Unicode URI to be parsed into a reference.
        :param str encoding: The encoding of the string provided
        :param bool strict: Parse strictly according to :rfc:`3986` if True.
            If False, parse similarly to the standard library's urlparse
            function.
        :returns: :class:`ParseResultBytes` or subclass thereof
        """
        reference = uri.URIReference.from_string(uri_string, encoding)
        if not lazy_normalize:
            reference = reference.normalize()
        userinfo, host, port = authority_from(reference, strict)

        to_bytes = compat.to_bytes
        return cls(
            scheme=to_bytes(reference.scheme, encoding),
            userinfo=to_bytes(userinfo, encoding),
            host=to_bytes(host, encoding),
            port=port,
            path=to_bytes(reference.path, encoding),
            query=to_bytes(reference.query, encoding),
            fragment=to_bytes(reference.fragment, encoding),
            uri_ref=reference,
            encoding=encoding,
            lazy_normalize=lazy_normalize,
        )

    @property
    def authority(self) -> bytes:
        """Return the normalized authority."""
        return self.reference.authority.encode(self.encoding)

    def copy_with(
        self,
        scheme: t.Optional[t.Union[str, bytes]] = misc.UseExisting,
        userinfo: t.Optional[t.Union[str, bytes]] = misc.UseExisting,
        host: t.Optional[t.Union[str, bytes]] = misc.UseExisting,
        port: t.Optional[t.Union[int, str, bytes]] = misc.UseExisting,
        path: t.Optional[t.Union[str, bytes]] = misc.UseExisting,
        query: t.Optional[t.Union[str, bytes]] = misc.UseExisting,
        fragment: t.Optional[t.Union[str, bytes]] = misc.UseExisting,
        lazy_normalize: bool = True,
    ) -> "ParseResultBytes":
        """Create a copy of this instance replacing with specified parts."""
        attributes = zip(
            PARSED_COMPONENTS,
            (scheme, userinfo, host, port, path, query, fragment),
        )
        attrs_dict = {}
        for name, value in attributes:
            if value is misc.UseExisting:
                value = getattr(self, name)
            if not isinstance(value, bytes) and hasattr(value, "encode"):
                value = value.encode(self.encoding)
            attrs_dict[name] = value

        if t.TYPE_CHECKING:
            attrs_dict = t.cast(t.Dict[str, t.Optional[bytes]], attrs_dict)

        authority = self._generate_authority(attrs_dict)
        to_str = compat.to_str
        ref = self.reference.copy_with(
            scheme=to_str(attrs_dict["scheme"], self.encoding),
            authority=to_str(authority, self.encoding),
            path=to_str(attrs_dict["path"], self.encoding),
            query=to_str(attrs_dict["query"], self.encoding),
            fragment=to_str(attrs_dict["fragment"], self.encoding),
        )
        if not lazy_normalize:
            ref = ref.normalize()
        return ParseResultBytes(
            uri_ref=ref,
            encoding=self.encoding,
            lazy_normalize=lazy_normalize,
            **attrs_dict,
        )

    def unsplit(self, use_idna: bool = False) -> bytes:
        """Create a URI bytes object from the components.

        :returns: The parsed URI reconstituted as a string.
        :rtype: bytes
        """
        parse_result = self
        if use_idna and self.host:
            # self.host is bytes, to encode to idna, we need to decode it
            # first
            host = self.host.decode(self.encoding)
            hostbytes = host.encode("idna")
            parse_result = self.copy_with(host=hostbytes)
        if self.lazy_normalize:
            parse_result = parse_result.copy_with(lazy_normalize=False)
        uri = parse_result.reference.unsplit()
        return uri.encode(self.encoding)


def split_authority(
    authority: str,
) -> t.Tuple[t.Optional[str], t.Optional[str], t.Optional[str]]:
    # Initialize our expected return values
    userinfo = host = port = None
    # Initialize an extra var we may need to use
    extra_host = None
    # Set-up rest in case there is no userinfo portion
    rest = authority

    if "@" in authority:
        userinfo, rest = authority.rsplit("@", 1)

    # Handle IPv6 host addresses
    if rest.startswith("["):
        host, rest = rest.split("]", 1)
        host += "]"

    if ":" in rest:
        extra_host, port = rest.split(":", 1)
    elif not host and rest:
        host = rest

    if extra_host and not host:
        host = extra_host

    return userinfo, host, port


def authority_from(
    reference: "uri.URIReference",
    strict: bool,
) -> t.Tuple[t.Optional[str], t.Optional[str], t.Optional[int]]:
    try:
        subauthority = reference.authority_info()
    except exceptions.InvalidAuthority:
        if strict:
            raise
        userinfo, host, port = split_authority(reference.authority)
    else:
        # Thanks to Richard Barrell for this idea:
        # https://twitter.com/0x2ba22e11/status/617338811975139328
        userinfo = subauthority.get("userinfo")
        host = subauthority.get("host")
        port = subauthority.get("port")

    if port:
        if port.isascii() and port.isdigit():
            port = int(port)
        else:
            raise exceptions.InvalidPort(port)
    return userinfo, host, port
