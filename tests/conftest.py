# -*- coding: utf-8 -*-
import itertools
import sys

import pytest

SNOWMAN = b'\xe2\x98\x83'

valid_hosts = [
    '[21DA:00D3:0000:2F3B:02AA:00FF:FE28:9C5A]',
    '[::1]',
    '[::1%25lo]',  # With ZoneID
    '[FF02:0:0:0:0:0:0:2%25en01]',  # With ZoneID
    '[FF02:30:0:0:0:0:0:5%25en1]',  # With ZoneID
    '[FF02:30:0:0:0:0:0:5%25%26]',  # With ZoneID
    '[FF02:30:0:0:0:0:0:5%2525]',  # With ZoneID
    '[21DA:D3:0:2F3B:2AA:FF:FE28:9C5A]',
    '[FE80::2AA:FF:FE9A:4CA2]',
    '[FF02::2]',
    '[FFFF::]',
    '[FF02:3::5]',
    '[FF02:0:0:0:0:0:0:2]',
    '[FF02:30:0:0:0:0:0:5]',
    '127.0.0.1',
    'www.example.com',
    'localhost',
    'http-bin.org',
    '%2Fvar%2Frun%2Fsocket',
    '6g9m8V6',  # Issue #48
    ]

invalid_hosts = [
    '[FF02::3::5]',  # IPv6 can only have one ::
    '[FADF:01]',  # Not properly compacted (missing a :)
    '[FADF:01%en0]',  # Not properly compacted (missing a :), Invalid ZoneID
    '[FADF::01%]',  # Empty Zone ID
    'localhost:80:80:80',  # Too many ports
    '256.256.256.256',  # Invalid IPv4 Address
    SNOWMAN.decode('utf-8')
    ]

equivalent_hostnames = [
    'example.com',
    'eXample.com',
    'example.COM',
    'EXAMPLE.com',
    'ExAMPLE.com',
    'eXample.COM',
    'example.COM',
    'EXAMPLE.COM',
    'ExAMPLE.COM',
]
equivalent_schemes = [
    'https',
    'HTTPS',
    'HttPs',
    'hTTpS',
    'HtTpS',
]
equivalent_schemes_and_hostnames = list(itertools.product(
    equivalent_schemes,
    equivalent_hostnames,
))


@pytest.fixture(params=valid_hosts)
def basic_uri(request):
    return 'http://%s' % request.param


@pytest.fixture(params=equivalent_schemes_and_hostnames)
def uri_to_normalize(request):
    return '%s://%s' % request.param


@pytest.fixture(params=valid_hosts)
def basic_uri_with_port(request):
    return 'ftp://%s:21' % request.param


@pytest.fixture(params=valid_hosts)
def uri_with_port_and_userinfo(request):
    return 'ssh://user:pass@%s:22' % request.param


@pytest.fixture(params=valid_hosts)
def uri_with_port_and_tricky_userinfo(request):
    return 'ssh://%s@%s:22' % ('user%20!=:pass', request.param)


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


@pytest.fixture(params=valid_hosts)
def uri_path_with_percent(request):
    return 'https://%s/%% ' % request.param


@pytest.fixture(params=valid_hosts)
def uri_query_with_percent(request):
    return 'https://%s?a=%%' % request.param


@pytest.fixture(params=valid_hosts)
def uri_fragment_with_percent(request):
    return 'https://%s#perc%%ent' % request.param


sys.path.insert(0, '.')
