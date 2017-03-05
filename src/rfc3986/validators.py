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
"""Module containing the validation logic for rfc3986."""
from . import misc


def is_valid(value, matcher, require):
    """Determine if a value is valid based on the provided matcher.

    :param str value:
        Value to validate.
    :param matcher:
        Compiled regular expression to use to validate the value.
    :param require:
        Whether or not the value is required.
    """
    if require:
        return (value is not None
                and matcher.match(value))

    # require is False and value is not None
    return value is None or matcher.match(value)


def authority_is_valid(authority, host=None, require=False):
    """Determine if the authority string is valid.

    :param str authority:
        The authority to validate.
    :param str host:
        (optional) The host portion of the authority to validate.
    :param bool require:
        (optional) Specify if authority must not be None.
    :returns:
        ``True`` if valid, ``False`` otherwise
    :rtype:
        bool
    """
    validated = is_valid(authority, misc.SUBAUTHORITY_MATCHER, require)
    if validated and host is not None and misc.IPv4_MATCHER.match(host):
        return valid_ipv4_host_address(host)
    return validated


def scheme_is_valid(scheme, require=False):
    """Determine if the scheme is valid.

    :param str scheme:
        The scheme string to validate.
    :param bool require:
        (optional) Set to ``True`` to require the presence of a scheme.
    :returns:
        ``True`` if the scheme is valid. ``False`` otherwise.
    :rtype:
        bool
    """
    return is_valid(scheme, misc.SCHEME_MATCHER, require)


def path_is_valid(path, require=False):
    """Determine if the path component is valid.

    :param str path:
        The path string to validate.
    :param bool require:
        (optional) Set to ``True`` to require the presence of a path.
    :returns:
        ``True`` if the path is valid. ``False`` otherwise.
    :rtype:
        bool
    """
    return is_valid(path, misc.PATH_MATCHER, require)


def query_is_valid(query, require=False):
    """Determine if the query component is valid.

    :param str query:
        The query string to validate.
    :param bool require:
        (optional) Set to ``True`` to require the presence of a query.
    :returns:
        ``True`` if the query is valid. ``False`` otherwise.
    :rtype:
        bool
    """
    return is_valid(query, misc.QUERY_MATCHER, require)


def fragment_is_valid(fragment, require=False):
    """Determine if the fragment component is valid.

    :param str fragment:
        The fragment string to validate.
    :param bool require:
        (optional) Set to ``True`` to require the presence of a fragment.
    :returns:
        ``True`` if the fragment is valid. ``False`` otherwise.
    :rtype:
        bool
    """
    return is_valid(fragment, misc.FRAGMENT_MATCHER, require)


def valid_ipv4_host_address(host):
    """Determine if the given host is a valid IPv4 address."""
    # If the host exists, and it might be IPv4, check each byte in the
    # address.
    return all([0 <= int(byte, base=10) <= 255 for byte in host.split('.')])
