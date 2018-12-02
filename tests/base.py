# -*- coding: utf-8 -*-
# Copyright (c) 2015 Ian Stapleton Cordasco
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


class BaseTestParsesURIs:
    test_class = None

    """Tests for self.test_class handling of URIs."""
    def test_handles_basic_uri(self, basic_uri):
        """Test that self.test_class can handle a simple URI."""
        uri = self.test_class.from_string(basic_uri)
        assert uri.scheme == 'http'
        assert uri.authority == basic_uri[7:]  # len('http://')
        assert uri.host == uri.authority
        assert uri.path is None
        assert uri.query is None
        assert uri.fragment is None
        assert uri.port is None
        assert uri.userinfo is None

    def test_handles_basic_uri_with_port(self, basic_uri_with_port):
        """Test that self.test_class can handle a simple URI with a port."""
        uri = self.test_class.from_string(basic_uri_with_port)
        assert uri.scheme == 'ftp'
        assert uri.authority == basic_uri_with_port[6:]
        assert uri.host != uri.authority
        assert str(uri.port) == '21'
        assert uri.path is None
        assert uri.query is None
        assert uri.fragment is None
        assert uri.userinfo is None

    def test_handles_uri_with_port_and_userinfo(
            self, uri_with_port_and_userinfo):
        """
        Test that self.test_class can handle a URI with a port and userinfo.
        """
        uri = self.test_class.from_string(uri_with_port_and_userinfo)
        assert uri.scheme == 'ssh'
        # 6 == len('ftp://')
        assert uri.authority == uri_with_port_and_userinfo[6:]
        assert uri.host != uri.authority
        assert str(uri.port) == '22'
        assert uri.path is None
        assert uri.query is None
        assert uri.fragment is None
        assert uri.userinfo == 'user:pass'

    def test_handles_tricky_userinfo(
            self, uri_with_port_and_tricky_userinfo):
        """
        Test that self.test_class can handle a URI with unusual
        (non a-z) chars in userinfo.
        """
        uri = self.test_class.from_string(uri_with_port_and_tricky_userinfo)
        assert uri.scheme == 'ssh'
        # 6 == len('ftp://')
        assert uri.authority == uri_with_port_and_tricky_userinfo[6:]
        assert uri.host != uri.authority
        assert str(uri.port) == '22'
        assert uri.path is None
        assert uri.query is None
        assert uri.fragment is None
        assert uri.userinfo == 'user%20!=:pass'

    def test_handles_basic_uri_with_path(self, basic_uri_with_path):
        """Test that self.test_class can handle a URI with a path."""
        uri = self.test_class.from_string(basic_uri_with_path)
        assert uri.scheme == 'http'
        assert basic_uri_with_path == (uri.scheme + '://' + uri.authority
                                       + uri.path)
        assert uri.host == uri.authority
        assert uri.path == '/path/to/resource'
        assert uri.query is None
        assert uri.fragment is None
        assert uri.userinfo is None
        assert uri.port is None

    def test_handles_uri_with_path_and_query(self, uri_with_path_and_query):
        """
        Test that self.test_class can handle a URI with a path and query.
        """
        uri = self.test_class.from_string(uri_with_path_and_query)
        assert uri.scheme == 'http'
        assert uri.host == uri.authority
        assert uri.path == '/path/to/resource'
        assert uri.query == 'key=value'
        assert uri.fragment is None
        assert uri.userinfo is None
        assert uri.port is None

    def test_handles_uri_with_everything(self, uri_with_everything):
        """
        Test that self.test_class can handle and with everything in it.
        """
        uri = self.test_class.from_string(uri_with_everything)
        assert uri.scheme == 'https'
        assert uri.path == '/path/to/resource'
        assert uri.query == 'key=value'
        assert uri.fragment == 'fragment'
        assert uri.userinfo == 'user:pass'
        assert str(uri.port) == '443'

    def test_handles_relative_uri(self, relative_uri):
        """Test that self.test_class can handle a relative URI."""
        uri = self.test_class.from_string(relative_uri)
        assert uri.scheme is None
        assert uri.authority == relative_uri[2:]

    def test_handles_percent_in_path(self, uri_path_with_percent):
        """Test that self.test_class encodes the % character properly."""
        uri = self.test_class.from_string(uri_path_with_percent)
        print(uri.path)
        assert uri.path == '/%25%20'

    def test_handles_percent_in_query(self, uri_query_with_percent):
        uri = self.test_class.from_string(uri_query_with_percent)
        assert uri.query == 'a=%25'

    def test_handles_percent_in_fragment(self, uri_fragment_with_percent):
        uri = self.test_class.from_string(uri_fragment_with_percent)
        assert uri.fragment == 'perc%25ent'


class BaseTestUnsplits:
    test_class = None

    def test_basic_uri_unsplits(self, basic_uri):
        uri = self.test_class.from_string(basic_uri)
        assert uri.unsplit() == basic_uri

    def test_basic_uri_with_port_unsplits(self, basic_uri_with_port):
        uri = self.test_class.from_string(basic_uri_with_port)
        assert uri.unsplit() == basic_uri_with_port

    def test_uri_with_port_and_userinfo_unsplits(self,
                                                 uri_with_port_and_userinfo):
        uri = self.test_class.from_string(uri_with_port_and_userinfo)
        assert uri.unsplit() == uri_with_port_and_userinfo

    def test_basic_uri_with_path_unsplits(self, basic_uri_with_path):
        uri = self.test_class.from_string(basic_uri_with_path)
        assert uri.unsplit() == basic_uri_with_path

    def test_uri_with_path_and_query_unsplits(self, uri_with_path_and_query):
        uri = self.test_class.from_string(uri_with_path_and_query)
        assert uri.unsplit() == uri_with_path_and_query

    def test_uri_with_everything_unsplits(self, uri_with_everything):
        uri = self.test_class.from_string(uri_with_everything)
        assert uri.unsplit() == uri_with_everything

    def test_relative_uri_unsplits(self, relative_uri):
        uri = self.test_class.from_string(relative_uri)
        assert uri.unsplit() == relative_uri

    def test_absolute_path_uri_unsplits(self, absolute_path_uri):
        uri = self.test_class.from_string(absolute_path_uri)
        assert uri.unsplit() == absolute_path_uri
