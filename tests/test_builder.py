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
"""Module containing the tests for the URIBuilder object."""
import pytest

from rfc3986 import builder


def test_builder_default():
    """Verify the default values."""
    uribuilder = builder.URIBuilder()
    assert uribuilder.scheme is None
    assert uribuilder.userinfo is None
    assert uribuilder.host is None
    assert uribuilder.port is None
    assert uribuilder.path is None
    assert uribuilder.query is None
    assert uribuilder.fragment is None


def test_repr():
    """Verify our repr looks like our class."""
    uribuilder = builder.URIBuilder()
    assert repr(uribuilder).startswith('URIBuilder(scheme=None')


@pytest.mark.parametrize('scheme', [
    'https',
    'hTTps',
    'Https',
    'HtTpS',
    'HTTPS',
])
def test_add_scheme(scheme):
    """Verify schemes are normalized when added."""
    uribuilder = builder.URIBuilder().add_scheme(scheme)
    assert uribuilder.scheme == 'https'


@pytest.mark.parametrize('username, password, userinfo', [
    ('user', 'pass', 'user:pass'),
    ('user', None, 'user'),
    ('user@domain.com', 'password', 'user%40domain.com:password'),
    ('user', 'pass:word', 'user:pass%3Aword'),
])
def test_add_credentials(username, password, userinfo):
    """Verify we normalize usernames and passwords."""
    uribuilder = builder.URIBuilder().add_credentials(username, password)
    assert uribuilder.userinfo == userinfo


def test_add_credentials_requires_username():
    """Verify one needs a username to add credentials."""
    with pytest.raises(ValueError):
        builder.URIBuilder().add_credentials(None, None)


@pytest.mark.parametrize('hostname', [
    'google.com',
    'GOOGLE.COM',
    'gOOgLe.COM',
    'goOgLE.com',
])
def test_add_host(hostname):
    """Verify we normalize hostnames in add_host."""
    uribuilder = builder.URIBuilder().add_host(hostname)
    assert uribuilder.host == 'google.com'
