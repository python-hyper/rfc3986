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
"""Module containing compiled regular expressions and constants.

This module contains important constants, patterns, and compiled regular
expressions for parsing and validating URIs and their components.
"""

import dataclasses
import re
import typing as t

from . import abnf_regexp

if t.TYPE_CHECKING:
    # Break a circular import.
    from . import uri


@dataclasses.dataclass(frozen=True)
class URIReferenceBase:
    """The dataclass used as a superclass for URIReference and IRIReference."""

    scheme: t.Optional[str]
    authority: t.Optional[str]
    path: t.Optional[str]
    query: t.Optional[str]
    fragment: t.Optional[str]

    def __iter__(self):
        """Iterate over the main components of this URI reference.

        In order: scheme, authority, path, query, fragment.
        """
        yield self.scheme
        yield self.authority
        yield self.path
        yield self.query
        yield self.fragment


important_characters = {
    "generic_delimiters": abnf_regexp.GENERIC_DELIMITERS,
    "sub_delimiters": abnf_regexp.SUB_DELIMITERS,
    # We need to escape the '*' in this case
    "re_sub_delimiters": abnf_regexp.SUB_DELIMITERS_RE,
    "unreserved_chars": abnf_regexp.UNRESERVED_CHARS,
    # We need to escape the '-' in this case:
    "re_unreserved": abnf_regexp.UNRESERVED_RE,
}

# For details about delimiters and reserved characters, see:
# http://tools.ietf.org/html/rfc3986#section-2.2
GENERIC_DELIMITERS = abnf_regexp.GENERIC_DELIMITERS_SET
SUB_DELIMITERS = abnf_regexp.SUB_DELIMITERS_SET
RESERVED_CHARS = abnf_regexp.RESERVED_CHARS_SET
# For details about unreserved characters, see:
# http://tools.ietf.org/html/rfc3986#section-2.3
UNRESERVED_CHARS = abnf_regexp.UNRESERVED_CHARS_SET
NON_PCT_ENCODED = abnf_regexp.NON_PCT_ENCODED_SET

URI_MATCHER = re.compile(abnf_regexp.URL_PARSING_RE)

SUBAUTHORITY_MATCHER = re.compile(
    f"^(?:(?P<userinfo>{abnf_regexp.USERINFO_RE})@)?"  # userinfo
    f"(?P<host>{abnf_regexp.HOST_PATTERN})"  # host
    f"(?::(?P<port>{abnf_regexp.PORT_RE}))?$"  # port
)


HOST_MATCHER = re.compile("^" + abnf_regexp.HOST_RE + "$")
IPv4_MATCHER = re.compile("^" + abnf_regexp.IPv4_RE + "$")
IPv6_MATCHER = re.compile(r"^\[" + abnf_regexp.IPv6_ADDRZ_RFC4007_RE + r"\]$")

# Used by host validator
IPv6_NO_RFC4007_MATCHER = re.compile(r"^\[%s\]$" % (abnf_regexp.IPv6_ADDRZ_RE))

# Matcher used to validate path components
PATH_MATCHER = re.compile(abnf_regexp.PATH_RE)


# ##################################
# Query and Fragment Matcher Section
# ##################################

QUERY_MATCHER = re.compile(abnf_regexp.QUERY_RE)

FRAGMENT_MATCHER = QUERY_MATCHER

# Scheme validation, see: http://tools.ietf.org/html/rfc3986#section-3.1
SCHEME_MATCHER = re.compile(f"^{abnf_regexp.SCHEME_RE}$")

RELATIVE_REF_MATCHER = re.compile(
    rf"^{abnf_regexp.RELATIVE_PART_RE}"
    rf"(\?{abnf_regexp.QUERY_RE})?"
    rf"(#{abnf_regexp.FRAGMENT_RE})?$"
)

# See http://tools.ietf.org/html/rfc3986#section-4.3
ABSOLUTE_URI_MATCHER = re.compile(
    rf"^{abnf_regexp.COMPONENT_PATTERN_DICT['scheme']}:"
    rf"{abnf_regexp.HIER_PART_RE}"
    rf"(\?{abnf_regexp.QUERY_RE[1:-1]})?$"
)

# ###############
# IRIs / RFC 3987
# ###############

IRI_MATCHER = re.compile(abnf_regexp.URL_PARSING_RE)

ISUBAUTHORITY_MATCHER = re.compile(
    f"^(?:(?P<userinfo>{abnf_regexp.IUSERINFO_RE})@)?"  # iuserinfo
    f"(?P<host>{abnf_regexp.IHOST_RE})"  # ihost
    f":?(?P<port>{abnf_regexp.PORT_RE})?$"  # port
)


# Path merger as defined in http://tools.ietf.org/html/rfc3986#section-5.2.3
def merge_paths(base_uri: "uri.URIReference", relative_path: str) -> str:
    """Merge a base URI's path with a relative URI's path."""
    if base_uri.path is None and base_uri.authority is not None:
        return "/" + relative_path
    else:
        path = base_uri.path or ""
        index = path.rfind("/")
        return path[:index] + "/" + relative_path


UseExisting: t.Any = object()
