# -*- coding: utf-8 -*-
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
import re


def normalize_scheme(scheme):
    return scheme.lower()


def normalize_authority(authority):
    return normalize_percent_characters(authority)


def normalize_path(path):
    path = normalize_percent_characters(path)
    return remove_dot_segments(path)


def normalize_query(query):
    query = normalize_percent_characters(query)
    return query


def normalize_fragment(fragment):
    fragment = normalize_percent_characters(fragment)
    return fragment


PERCENT_MATCHER = re.compile('%[A-Fa-f0-9]{2}')


def normalize_percent_characters(s):
    """All percent characters should be upper-cased.

    For example, ``"%3afoo%DF%ab"`` should be turned into ``"%3Afoo%DF%AB"``.
    """
    matches = set(PERCENT_MATCHER.findall(s))
    for m in matches:
        if not m.isupper():
            s = s.replace(m, m.upper())
    return s


def remove_dot_segments(s):
    # See http://tools.ietf.org/html/rfc3986#section-5.2.4 for pseudo-code
    segments = s.split('/')
    output = []
    for segment in segments:
        if segment == '.':
            continue
        elif segment == '..' and output:
            output.pop()
        elif segment or segment == '':
            output.append(segment)
    return '/'.join(output)
