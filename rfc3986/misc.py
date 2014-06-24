# -*- coding: utf-8 -*-

# Delimiters of generic URI components, see
# http://tools.ietf.org/html/rfc3986#section-3
GENERIC_DELIMITERS = (":", "/", "?", "#", "[", "]", "@")

# Delimiters of subcomponents
SUB_DELIMITERS = ("!", "$", "&", "'", "(", ")", "*", "+", ",", ";", "=")
RESERVED_CHARS = general_delimiters + sub_delimiters


scheme_pattern = '\w[\w\d+-.]*'
authority_pattern = '[^/?#]+'
path_pattern = '.*'  # FIXME
userinfo_pattern = ''

expression = ('(?P<scheme>{scheme}):(//(?P<authority>{authority})|'
              '(?P<path>{path}))').format({
                  'scheme': scheme_pattern,
                  'authority': authority_pattern,
                  'path': path_pattern,
                  })
