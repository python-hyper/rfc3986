==========================
 Miscellaneous Submodules
==========================

There are several submodules in |rfc3986| that are not meant to be exposed to 
users directly but which are valuable to document, regardless.

.. data:: rfc3986.misc.UseExisting

    A sentinel object to make certain APIs simpler for users.

.. module:: rfc3986.abnf_regexp

The :mod:`rfc3986.abnf_regexp` module contains the regular expressions written
from the RFC's ABNF. The :mod:`rfc3986.misc` module contains compiled regular
expressions from :mod:`rfc3986.abnf_regexp` and previously contained those
regular expressions.

.. data:: rfc3986.abnf_regexp.GEN_DELIMS
.. data:: rfc3986.abnf_regexp.GENERIC_DELIMITERS

    The string containing all of the generic delimiters as defined on
    `page 13 <https://tools.ietf.org/html/rfc3986#page-13>`__.

.. data:: rfc3986.abnf_regexp.GENERIC_DELIMITERS_SET

    :data:`rfc3986.abnf_regexp.GEN_DELIMS` represented as a :class:`set`.

.. data:: rfc3986.abnf_regexp.SUB_DELIMS
.. data:: rfc3986.abnf_regexp.SUB_DELIMITERS

    The string containing all of the 'sub' delimiters as defined on
    `page 13 <https://tools.ietf.org/html/rfc3986#page-13>`__.

.. data:: rfc3986.abnf_regexp.SUB_DELIMITERS_SET

    :data:`rfc3986.abnf_regexp.SUB_DELIMS` represented as a :class:`set`.

.. data:: rfc3986.abnf_regexp.SUB_DELIMITERS_RE

    :data:`rfc3986.abnf_regexp.SUB_DELIMS` with the ``*`` escaped for use in
    regular expressions.

.. data:: rfc3986.abnf_regexp.RESERVED_CHARS_SET

    A :class:`set` constructed of :data:`GEN_DELIMS` and :data:`SUB_DELIMS`.
    This union is defined on `page 13
    <https://tools.ietf.org/html/rfc3986#page-13>`__.

.. data:: rfc3986.abnf_regexp.ALPHA

    The string of upper- and lower-case letters in USASCII.

.. data:: rfc3986.abnf_regexp.DIGIT

    The string of digits 0 through 9.

.. data:: rfc3986.abnf_regexp.UNRESERVED
.. data:: rfc3986.abnf_regexp.UNRESERVED_CHARS

    The string of unreserved characters defined in :rfc:`3986#section-2.3`.

.. data:: rfc3986.abnf_regexp.UNRESERVED_CHARS_SET

    :data:`rfc3986.abnf_regexp.UNRESERVED_CHARS` represented as a
    :class:`set`.

.. data:: rfc3986.abnf_regexp.NON_PCT_ENCODED_SET

    The non-percent encoded characters represented as a :class:`set`.

.. data:: rfc3986.abnf_regexp.UNRESERVED_RE

    Optimized regular expression for unreserved characters.

.. data:: rfc3986.abnf_regexp.SCHEME_RE

    Stricter regular expression to match and validate the scheme part
    of a URI.

.. data:: rfc3986.abnf_regexp.COMPONENT_PATTERN_DICT

    Dictionary with regular expressions to match various components in
    a URI. Except for :data:`rfc3986.abnf_regexp.SCHEME_RE`, all patterns
    are from :rfc:`3986#appendix-B`.

.. data:: rfc3986.abnf_regexp.URL_PARSING_RE

    Regular expression compposed from the components in
    :data:`rfc3986.abnf_regexp.COMPONENT_PATTERN_DICT`.

.. data:: rfc3986.abnf_regexp.HEXDIG_RE

    Hexadecimal characters used in each piece of an IPv6 address.
    See :rfc:`3986#section-3.2.2`.

.. data:: rfc3986.abnf_regexp.LS32_RE

    Lease significant 32 bits of an IPv6 address.
    See :rfc:`3986#section-3.2.2`.

.. data:: rfc3986.abnf_regexp.REG_NAME
.. data:: rfc3986.abnf_regexp.REGULAR_NAME_RE

    The pattern for a regular name, e.g., ``www.google.com``,
    ``api.github.com``.
    See :rfc:`3986#section-3.2.2`.

.. data:: rfc3986.abnf_regexp.IPv4_RE

    The pattern for an IPv4 address, e.g., ``192.168.255.255``.
    See :rfc:`3986#section-3.2.2`.

.. data:: rfc3986.abnf_regexp.IPv6_RE

    The pattern for an IPv6 address, e.g., ``::1``.
    See :rfc:`3986#section-3.2.2`.

.. data:: rfc3986.abnf_regexp.IPv_FUTURE_RE

    A regular expression to parse out IPv Futures.
    See :rfc:`3986#section-3.2.2`.

.. data:: rfc3986.abnf_regexp.IP_LITERAL_RE

    Pattern to match IPv6 addresses and IPv Future addresses.
    See :rfc:`3986#section-3.2.2`.

.. data:: rfc3986.abnf_regexp.HOST_RE
.. data:: rfc3986.abnf_regexp.HOST_PATTERN

    Pattern to match and validate the host piece of an authority.
    This is composed of

    - :data:`rfc3986.abnf_regexp.REG_NAME`
    - :data:`rfc3986.abnf_regexp.IPv4_RE`
    - :data:`rfc3986.abnf_regexp.IP_LITERAL_RE`

    See :rfc:`3986#section-3.2.2`.

.. data:: rfc3986.abnf_regexp.USERINFO_RE

    Pattern to match and validate the user information portion of
    an authority component.

    See :rfc:`3986#section-3.2.2`.

.. data:: rfc3986.abnf_regexp.PORT_RE

    Pattern to match and validate the port portion of an authority
    component.

    See :rfc:`3986#section-3.2.2`.

.. data:: rfc3986.abnf_regexp.PCT_ENCODED
.. data:: rfc3986.abnf_regexp.PERCENT_ENCODED

    Regular expression to match percent encoded character values.

.. data:: rfc3986.abnf_regexp.PCHAR

    Regular expression to match printable characters.

.. data:: rfc3986.abnf_regexp.PATH_RE

    Regular expression to match and validate the path component of a URI.

    See :rfc:`3986#section-3.3`.

.. data:: rfc3986.abnf_regexp.PATH_EMPTY
.. data:: rfc3986.abnf_regexp.PATH_ROOTLESS
.. data:: rfc3986.abnf_regexp.PATH_NOSCHEME
.. data:: rfc3986.abnf_regexp.PATH_ABSOLUTE
.. data:: rfc3986.abnf_regexp.PATH_ABEMPTY

    Components of the :data:`rfc3986.abnf_regexp.PATH_RE`.

    See :rfc:`3986#section-3.3`.

.. data:: rfc3986.abnf_regexp.QUERY_RE

    Regular expression to parse and validate the query component of a URI.

.. data:: rfc3986.abnf_regexp.FRAGMENT_RE

    Regular expression to parse and validate the fragment component of a URI.

.. data:: rfc3986.abnf_regexp.RELATIVE_PART_RE

    Regular expression to parse the relative URI when resolving URIs.

.. data:: rfc3986.abnf_regexp.HIER_PART_RE

    The hierarchical part of a URI. This regular expression is used when
    resolving relative URIs.

    See :rfc:`3986#section-3`.

.. module:: rfc3986.misc

.. data:: rfc3986.misc.URI_MATCHER

    Compiled version of :data:`rfc3986.abnf_regexp.URL_PARSING_RE`.

.. data:: rfc3986.misc.SUBAUTHORITY_MATCHER

    Compiled compilation of :data:`rfc3986.abnf_regexp.USERINFO_RE`,
    :data:`rfc3986.abnf_regexp.HOST_PATTERN`,
    :data:`rfc3986.abnf_regexp.PORT_RE`.

.. data:: rfc3986.misc.SCHEME_MATCHER

    Compiled version of :data:`rfc3986.abnf_regexp.SCHEME_RE`.

.. data:: rfc3986.misc.IPv4_MATCHER

    Compiled version of :data:`rfc3986.abnf_regexp.IPv4_RE`.

.. data:: rfc3986.misc.PATH_MATCHER

    Compiled version of :data:`rfc3986.abnf_regexp.PATH_RE`.

.. data:: rfc3986.misc.QUERY_MATCHER

    Compiled version of :data:`rfc3986.abnf_regexp.QUERY_RE`.

.. data:: rfc3986.misc.RELATIVE_REF_MATCHER

    Compiled compilation of :data:`rfc3986.abnf_regexp.SCHEME_RE`,
    :data:`rfc3986.abnf_regexp.HIER_PART_RE`,
    :data:`rfc3986.abnf_regexp.QUERY_RE`.
