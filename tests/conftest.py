# -*- coding: utf-8 -*-
import sys

import pytest

SNOWMAN = b'\xe2\x98\x83'

valid_hosts = [
    '[21DA:00D3:0000:2F3B:02AA:00FF:FE28:9C5A]', '[::1]',
    '[21DA:D3:0:2F3B:2AA:FF:FE28:9C5A]', '[FE80::2AA:FF:FE9A:4CA2]',
    '[FF02::2]', '[FF02:3::5]', '[FF02:0:0:0:0:0:0:2]',
    '[FF02:30:0:0:0:0:0:5]', '127.0.0.1', 'www.example.com', 'localhost',
    'http-bin.org',
    ]

invalid_hosts = [
    '[FF02::3::5]',  # IPv6 can only have one ::
    '[FADF:01]',  # Not properly compacted (missing a :)
    'localhost:80:80:80',  # Too many ports
    '256.256.256.256',  # Invalid IPv4 Address
    SNOWMAN.decode('utf-8')
    ]


@pytest.fixture(params=valid_hosts)
def basic_uri(request):
    return 'http://%s' % request.param


@pytest.fixture(params=valid_hosts)
def basic_uri_with_port(request):
    return 'ftp://%s:21' % request.param


@pytest.fixture(params=valid_hosts)
def uri_with_port_and_userinfo(request):
    return 'ssh://user:pass@%s:22' % request.param


@pytest.fixture(params=valid_hosts)
def basic_uri_with_path(request):
    return 'http://%s/path/to/resource' % request.param


@pytest.fixture(params=valid_hosts)
def uri_with_path_and_query(request):
    return 'http://%s/path/to/resource?key=value' % request.param


@pytest.fixture(params=valid_hosts)
def uri_with_everything(request):
    return 'https://user:pass@%s:443/path/to/resource?key=value#fragment' % (
        request.param)


@pytest.fixture(params=valid_hosts)
def relative_uri(request):
    return '//%s' % request.param


@pytest.fixture
def absolute_path_uri():
    return '/path/to/file'


@pytest.fixture(params=invalid_hosts)
def invalid_uri(request):
    return 'https://%s' % request.param

sys.path.insert(0, '.')
