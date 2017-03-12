# -*- coding: utf-8 -*-
# Copyright (c) 2017 Ian Cordasco
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
from . import normalizers


class URIBuilder(object):
    """Object to aid in building up a URI Reference from parts.

    .. note::

        This object should be instantiated by the user, but it's recommended
        that it is not provided with arguments. Instead, use the available
        method to populate the fields.

    """

    def __init__(self, scheme=None, userinfo=None, host=None, port=None,
                 path=None, query=None, fragment=None):
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
        formatstr = ('URIBuilder(scheme={b.scheme}, userinfo={b.userinfo}, '
                     'host={b.host}, port={b.port}, path={b.path}, '
                     'query={b.query}, fragment={b.fragment})')
        return formatstr.format(b=self)

    def add_scheme(self, scheme):
        """Add a scheme to our builder object.

        After normalizing, this will generate a new URIBuilder instance with
        the specified scheme and all other attributes the same.

        .. code-block:: python

            >>> URIBuilder().add_scheme('HTTPS')
            URIBuilder(scheme='https', userinfo=None, host=None, port=None,
                    path=None, query=None, fragment=None)

        """
        scheme = normalizers.normalize_scheme(scheme)
        return URIBuilder(
            scheme=scheme,
            userinfo=self.userinfo,
            host=self.host,
            port=self.port,
            path=self.path,
            query=self.query,
            fragment=self.fragment,
        )

    def add_credentials(self, username, password):
        """Add credentials as the userinfo portion of the URI.

        .. code-block:: python

            >>> URIBuilder().add_credentials('root', 's3crete')
            URIBuilder(scheme=None, userinfo='root:s3crete', host=None,
                    port=None, path=None, query=None, fragment=None)

            >>> URIBuilder().add_credentials('root', None)
            URIBuilder(scheme=None, userinfo='root', host=None,
                    port=None, path=None, query=None, fragment=None)
        """
        if username is None:
            raise ValueError('Username cannot be None')
        userinfo = normalizers.normalize_username(username)

        if password is not None:
            userinfo += ':{}'.format(normalizers.normalize_password(password))

        return URIBuilder(
            scheme=self.scheme,
            userinfo=userinfo,
            host=self.host,
            port=self.port,
            path=self.path,
            query=self.query,
            fragment=self.fragment,
        )
