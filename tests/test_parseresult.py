# -*- coding: utf-8 -*-
# Copyright (c) 2015 Ian Cordasco
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
from rfc3986 import parseresult as pr

from . import base


class TestParseResultParsesURIs(base.BaseTestParsesURIs):
    test_class = pr.ParseResult


class TestParseResultUnsplits(base.BaseTestUnsplits):
    test_class = pr.ParseResult


class TestStdlibShims:
    def test_uri_with_everything(self, uri_with_everything):
        uri = pr.ParseResult.from_string(uri_with_everything)
        assert uri.host == uri.hostname
        assert uri.netloc == uri.authority
        assert uri.query == uri.params
        assert uri.geturl() == uri.unsplit()


def test_creates_a_copy_with_a_new_path(uri_with_everything):
    uri = pr.ParseResult.from_string(uri_with_everything)
    new_uri = uri.copy_with(path='/parse/result/tests/are/fun')
    assert new_uri.path == '/parse/result/tests/are/fun'


def test_creates_a_copy_with_a_new_port(basic_uri):
    uri = pr.ParseResult.from_string(basic_uri)
    new_uri = uri.copy_with(port=443)
    assert new_uri.port == 443
