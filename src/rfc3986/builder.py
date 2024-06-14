# Copyright (c) 2017 Ian Stapleton Cordasco
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
"""Module containing the logic for the URIBuilder object."""

import typing as t
from urllib.parse import parse_qsl
from urllib.parse import urlencode

from . import compat
from . import normalizers
from . import uri
from . import uri_reference

# Copied from urllib.parse in typeshed.
_QueryType = t.Union[
    t.Mapping[t.Any, t.Any],
    t.Mapping[t.Any, t.Sequence[t.Any]],
    t.Sequence[t.Tuple[t.Any, t.Any]],
    t.Sequence[t.Tuple[t.Any, t.Sequence[t.Any]]],
]


class URIBuilder:
    """Object to aid in building up a URI Reference from parts.

    .. note::

        This object should be instantiated by the user, but it's recommended
        that it is not provided with arguments. Instead, use the available
        method to populate the fields.

    """

    def __init__(
        self,
        scheme: t.Optional[str] = None,
        userinfo: t.Optional[str] = None,
        host: t.Optional[str] = None,
        port: t.Optional[str] = None,
        path: t.Optional[str] = None,
        query: t.Optional[str] = None,
        fragment: t.Optional[str] = None,
    ):
        """Initialize our URI builder.

        :param str scheme:
            (optional)
        :param str userinfo:
            (optional)
        :param str host:
            (optional)
        :param int port:
            (optional)
        :param str path:
            (optional)
        :param str query:
            (optional)
        :param str fragment:
            (optional)
        """
        self.scheme = scheme
        self.userinfo = userinfo
        self.host = host
        self.port = port
        self.path = path
        self.query = query
        self.fragment = fragment

    def __repr__(self):
        """Provide a convenient view of our builder object."""
        return (
            f"URIBuilder(scheme={self.scheme}, userinfo={self.userinfo}, "
            f"host={self.host}, port={self.port}, path={self.path}, "
            f"query={self.query}, fragment={self.fragment})"
        )

    @classmethod
    def from_uri(
        cls, reference: t.Union[uri.URIReference, str]
    ) -> compat.Self:
        """Initialize the URI builder from another URI.

        Takes the given URI reference and creates a new URI builder instance
        populated with the values from the reference. If given a string it will
        try to convert it to a reference before constructing the builder.
        """
        if not isinstance(reference, uri.URIReference):
            reference = uri_reference(reference)
        return cls(
            scheme=reference.scheme,
            userinfo=reference.userinfo,
            host=reference.host,
            port=reference.port,
            path=reference.path,
            query=reference.query,
            fragment=reference.fragment,
        )

    def add_scheme(self, scheme: str) -> compat.Self:
        """Add a scheme to our builder object.

        After normalizing, this will generate a new URIBuilder instance with
        the specified scheme and all other attributes the same.

        .. code-block:: python

            >>> URIBuilder().add_scheme('HTTPS')
            URIBuilder(scheme='https', userinfo=None, host=None, port=None,
                    path=None, query=None, fragment=None)

        """
        scheme = normalizers.normalize_scheme(scheme)
        return type(self)(
            scheme=scheme,
            userinfo=self.userinfo,
            host=self.host,
            port=self.port,
            path=self.path,
            query=self.query,
            fragment=self.fragment,
        )

    def add_credentials(
        self,
        username: str,
        password: t.Optional[str],
    ) -> compat.Self:
        """Add credentials as the userinfo portion of the URI.

        .. code-block:: python

            >>> URIBuilder().add_credentials('root', 's3crete')
            URIBuilder(scheme=None, userinfo='root:s3crete', host=None,
                    port=None, path=None, query=None, fragment=None)

            >>> URIBuilder().add_credentials('root', None)
            URIBuilder(scheme=None, userinfo='root', host=None,
                    port=None, path=None, query=None, fragment=None)
        """
        if username is None:  # pyright: ignore [reportUnnecessaryComparison] # Maintain behavior; users may disregard type hint.
            raise ValueError("Username cannot be None")
        userinfo = normalizers.normalize_username(username)

        if password is not None:
            userinfo = f"{userinfo}:{normalizers.normalize_password(password)}"

        return type(self)(
            scheme=self.scheme,
            userinfo=userinfo,
            host=self.host,
            port=self.port,
            path=self.path,
            query=self.query,
            fragment=self.fragment,
        )

    def add_host(self, host: str) -> compat.Self:
        """Add hostname to the URI.

        .. code-block:: python

            >>> URIBuilder().add_host('google.com')
            URIBuilder(scheme=None, userinfo=None, host='google.com',
                    port=None, path=None, query=None, fragment=None)

        """
        return type(self)(
            scheme=self.scheme,
            userinfo=self.userinfo,
            host=normalizers.normalize_host(host),
            port=self.port,
            path=self.path,
            query=self.query,
            fragment=self.fragment,
        )

    def add_port(self, port: t.Union[str, int]) -> compat.Self:
        """Add port to the URI.

        .. code-block:: python

            >>> URIBuilder().add_port(80)
            URIBuilder(scheme=None, userinfo=None, host=None, port='80',
                    path=None, query=None, fragment=None)

            >>> URIBuilder().add_port(443)
            URIBuilder(scheme=None, userinfo=None, host=None, port='443',
                    path=None, query=None, fragment=None)

        """
        port_int = int(port)
        if port_int < 0:
            raise ValueError(
                "ports are not allowed to be negative. You provided "
                f"{port_int}"
            )
        if port_int > 65535:
            raise ValueError(
                "ports are not allowed to be larger than 65535. "
                f"You provided {port_int}"
            )

        return type(self)(
            scheme=self.scheme,
            userinfo=self.userinfo,
            host=self.host,
            port=f"{port_int}",
            path=self.path,
            query=self.query,
            fragment=self.fragment,
        )

    def add_path(self, path: str) -> compat.Self:
        """Add a path to the URI.

        .. code-block:: python

            >>> URIBuilder().add_path('sigmavirus24/rfc3985')
            URIBuilder(scheme=None, userinfo=None, host=None, port=None,
                    path='/sigmavirus24/rfc3986', query=None, fragment=None)

            >>> URIBuilder().add_path('/checkout.php')
            URIBuilder(scheme=None, userinfo=None, host=None, port=None,
                    path='/checkout.php', query=None, fragment=None)

        """
        if not path.startswith("/"):
            path = f"/{path}"

        return type(self)(
            scheme=self.scheme,
            userinfo=self.userinfo,
            host=self.host,
            port=self.port,
            path=normalizers.normalize_path(path),
            query=self.query,
            fragment=self.fragment,
        )

    def extend_path(self, path: str) -> compat.Self:
        """Extend the existing path value with the provided value.

        .. versionadded:: 1.5.0

        .. code-block:: python

            >>> URIBuilder(path="/users").extend_path("/sigmavirus24")
            URIBuilder(scheme=None, userinfo=None, host=None, port=None,
                    path='/users/sigmavirus24', query=None, fragment=None)

            >>> URIBuilder(path="/users/").extend_path("/sigmavirus24")
            URIBuilder(scheme=None, userinfo=None, host=None, port=None,
                    path='/users/sigmavirus24', query=None, fragment=None)

            >>> URIBuilder(path="/users/").extend_path("sigmavirus24")
            URIBuilder(scheme=None, userinfo=None, host=None, port=None,
                    path='/users/sigmavirus24', query=None, fragment=None)

            >>> URIBuilder(path="/users").extend_path("sigmavirus24")
            URIBuilder(scheme=None, userinfo=None, host=None, port=None,
                    path='/users/sigmavirus24', query=None, fragment=None)

        """
        existing_path = self.path or ""
        path = "{}/{}".format(existing_path.rstrip("/"), path.lstrip("/"))

        return self.add_path(path)

    def add_query_from(self, query_items: _QueryType) -> compat.Self:
        """Generate and add a query a dictionary or list of tuples.

        .. code-block:: python

            >>> URIBuilder().add_query_from({'a': 'b c'})
            URIBuilder(scheme=None, userinfo=None, host=None, port=None,
                    path=None, query='a=b+c', fragment=None)

            >>> URIBuilder().add_query_from([('a', 'b c')])
            URIBuilder(scheme=None, userinfo=None, host=None, port=None,
                    path=None, query='a=b+c', fragment=None)

        """
        query = normalizers.normalize_query(urlencode(query_items))

        return type(self)(
            scheme=self.scheme,
            userinfo=self.userinfo,
            host=self.host,
            port=self.port,
            path=self.path,
            query=query,
            fragment=self.fragment,
        )

    def extend_query_with(self, query_items: _QueryType) -> compat.Self:
        """Extend the existing query string with the new query items.

        .. versionadded:: 1.5.0

        .. code-block:: python

            >>> URIBuilder(query='a=b+c').extend_query_with({'a': 'b c'})
            URIBuilder(scheme=None, userinfo=None, host=None, port=None,
                    path=None, query='a=b+c&a=b+c', fragment=None)

            >>> URIBuilder(query='a=b+c').extend_query_with([('a', 'b c')])
            URIBuilder(scheme=None, userinfo=None, host=None, port=None,
                    path=None, query='a=b+c&a=b+c', fragment=None)
        """
        original_query_items = parse_qsl(self.query or "")
        if not isinstance(query_items, t.Sequence):
            query_items = list(query_items.items())

        return self.add_query_from([*original_query_items, *query_items])

    def add_query(self, query: str) -> compat.Self:
        """Add a pre-formated query string to the URI.

        .. code-block:: python

            >>> URIBuilder().add_query('a=b&c=d')
            URIBuilder(scheme=None, userinfo=None, host=None, port=None,
                    path=None, query='a=b&c=d', fragment=None)

        """
        return type(self)(
            scheme=self.scheme,
            userinfo=self.userinfo,
            host=self.host,
            port=self.port,
            path=self.path,
            query=normalizers.normalize_query(query),
            fragment=self.fragment,
        )

    def add_fragment(self, fragment: str) -> compat.Self:
        """Add a fragment to the URI.

        .. code-block:: python

            >>> URIBuilder().add_fragment('section-2.6.1')
            URIBuilder(scheme=None, userinfo=None, host=None, port=None,
                    path=None, query=None, fragment='section-2.6.1')

        """
        return type(self)(
            scheme=self.scheme,
            userinfo=self.userinfo,
            host=self.host,
            port=self.port,
            path=self.path,
            query=self.query,
            fragment=normalizers.normalize_fragment(fragment),
        )

    def finalize(self) -> uri.URIReference:
        """Create a URIReference from our builder.

        .. code-block:: python

            >>> URIBuilder().add_scheme('https').add_host('github.com'
            ...     ).add_path('sigmavirus24/rfc3986').finalize().unsplit()
            'https://github.com/sigmavirus24/rfc3986'

            >>> URIBuilder().add_scheme('https').add_host('github.com'
            ...     ).add_path('sigmavirus24/rfc3986').add_credentials(
            ...     'sigmavirus24', 'not-re@l').finalize().unsplit()
            'https://sigmavirus24:not-re%40l@github.com/sigmavirus24/rfc3986'

        """
        return uri.URIReference(
            self.scheme,
            normalizers.normalize_authority(
                (self.userinfo, self.host, self.port)
            ),
            self.path,
            self.query,
            self.fragment,
        )

    def geturl(self) -> str:
        """Generate the URL from this builder.

        .. versionadded:: 1.5.0

        This is an alternative to calling :meth:`finalize` and keeping the
        :class:`rfc3986.uri.URIReference` around.
        """
        return self.finalize().unsplit()
