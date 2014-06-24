# -*- coding: utf-8 -*-
import re

# For details about delimiters, see:
# http://tools.ietf.org/html/rfc3986#section-2.2
GENERIC_DELIMITERS = set((":", "/", "?", "#", "[", "]", "@"))
SUB_DELIMITERS = set(("!", "$", "&", "'", "(", ")", "*", "+", ",", ";", "="))
RESERVED_CHARS = GENERIC_DELIMITERS.union(SUB_DELIMITERS)
UNRESERVED_CHARS = set(
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    '0123456789-._~'
    )

# Extracted from http://tools.ietf.org/html/rfc3986#appendix-B
pattern_dict = {
    'scheme': '[^:/?#]+',
    'authority': '[^/?#]*',
    'path': '[^?#]*',
    'query': '[^#]*',
    'fragment': '.*',
    }

# See http://tools.ietf.org/html/rfc3986#appendix-B
# In this case, we name each of the important matches so we can use
# SRE_Match#groupdict to parse the values out if we so choose. This is also
# modified to ignore other matches that are not important to the parsing of
# the reference so we can also simply use SRE_Match#groups.
expression = ('(?:(?P<scheme>{scheme}):)?(?://(?P<authority>{authority}))?'
              '(?P<path>{path})(?:\?(?P<query>{query}))?'
              '(?:#(?P<fragment>{fragment}))?').format(**pattern_dict)

URI_MATCHER = re.compile(expression)

# Host patterns, see: http://tools.ietf.org/html/rfc3986#section-3.2.2
# The pattern for a regular name, e.g.,  www.google.com, api.github.com
reg_name = '[\w\d.]+'
# The pattern for an IPv4 address, e.g., 192.168.255.255, 127.0.0.1,
ipv4 = '(\d{1,3}.){3}\d{1,3}'
# Hexadecimal characters used in each piece of an IPv6 address
hexdig = '[0-9A-Fa-f]{1,4}'
# Least-significant 32 bits of an IPv6 address
ls32 = '({hex}:{hex}|{ipv4})'.format(hex=hexdig, ipv4=ipv4)
# Substitutions into the following patterns for IPv6 patterns defined
# http://tools.ietf.org/html/rfc3986#page-20
subs = {'hex': hexdig, 'ls32': ls32}

variations = [
    '(%(hex)s:){6}%(ls32)s' % subs,
    '::(%(hex)s:){5}%(ls32)s' % subs,
    '(%(hex)s)?::(%(hex)s:){4}%(ls32)s' % subs,
    '((%(hex)s:)?%(hex)s)?::(%(hex)s:){3}%(ls32)s' % subs,
    '((%(hex)s){0,2}:%(hex)s)?::(%(hex)s:){2}%(ls32)s' % subs,
    '((%(hex)s){0,3}:%(hex)s)?::%(hex)s:%(ls32)s' % subs,
    '((%(hex)s){0,4}:%(hex)s)?::%(ls32)s' % subs,
    '((%(hex)s){0,5}:%(hex)s)?::%(hex)s' % subs,
    '((%(hex)s){0,6}:%(hex)s)?::' % subs,
    ]

ipv6 = '(({0})|({1})|({2})|({3})|({4})|({5})|({6})|({7}))'.format(*variations)

# Pattern for matching the host piece of the authority
HOST_PATTERN = '({0}|{1}|\[{2}\])'.format(reg_name, ipv4, ipv6)

SUBAUTHORITY_MATCHER = re.compile((
    '^(?:(?P<userinfo>[{0}%:]+)@)?'  # userinfo
    '(?P<host>{1}?)'  # host
    ':?(?P<port>\d+)?$'  # port
    ).format(''.join(UNRESERVED_CHARS), HOST_PATTERN))

# These are enumerated for the named tuple used as a superclass of
# URIReference
URI_COMPONENTS = ['scheme', 'authority', 'path', 'query', 'fragment']
