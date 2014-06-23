# -*- coding: utf-8 -*-

# Delimiters of generic URI components, see
# http://tools.ietf.org/html/rfc3986#section-3
GENERIC_DELIMITERS = (":", "/", "?", "#", "[", "]", "@")

# Delimiters of subcomponents
SUB_DELIMITERS = ("!", "$", "&", "'", "(", ")", "*", "+", ",", ";", "=")
RESERVED_CHARS = general_delimiters + sub_delimiters
