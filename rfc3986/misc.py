# -*- coding: utf-8 -*-
import re

important_characters = {
    'generic_delimiters': ":/?#[]@",
    'sub_delimiters': "!$&'()*+,;=",
    'unreserved_chars': ('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
                         '012345789._~-')
    }
# For details about delimiters and reserved characters, see:
# http://tools.ietf.org/html/rfc3986#section-2.2
GENERIC_DELIMITERS = set(important_characters['generic_delimiters'])
SUB_DELIMITERS = set(important_characters['sub_delimiters'])
RESERVED_CHARS = GENERIC_DELIMITERS.union(SUB_DELIMITERS)
# For details about unreserved characters, see:
# http://tools.ietf.org/html/rfc3986#section-2.3
UNRESERVED_CHARS = set(important_characters['unreserved_chars'])

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

ipv_future = 'v[0-9A-Fa-f]+.[%s]+' % (
    'A-Za-z0-9._~\-' +  # We need to escape the '-' in this case
    "!$&'()\*+,;=" +  # We need to escape the '*' in this case
    ':')

ip_literal = '\[({0}|{1})\]'.format(ipv6, ipv_future)

# Pattern for matching the host piece of the authority
HOST_PATTERN = '({0}|{1}|{2})'.format(reg_name, ipv4, ip_literal)

SUBAUTHORITY_MATCHER = re.compile((
    '^(?:(?P<userinfo>[A-Za-z0-9_.~\-%:]+)@)?'  # userinfo
    '(?P<host>{0}?)'  # host
    ':?(?P<port>\d+)?$'  # port
    ).format(HOST_PATTERN))

# These are enumerated for the named tuple used as a superclass of
# URIReference
URI_COMPONENTS = ['scheme', 'authority', 'path', 'query', 'fragment']
