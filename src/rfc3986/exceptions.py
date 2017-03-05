# -*- coding: utf-8 -*-
"""Exceptions module for rfc3986."""


class RFC3986Exception(Exception):
    """Base class for all rfc3986 exception classes."""

    pass


class InvalidAuthority(RFC3986Exception):
    """Exception when the authority string is invalid."""

    def __init__(self, authority):
        """Initialize the exception with the invalid authority."""
        super(InvalidAuthority, self).__init__(
            "The authority ({0}) is not valid.".format(authority))


class InvalidPort(RFC3986Exception):
    """Exception when the port is invalid."""

    def __init__(self, port):
        """Initialize the exception with the invalid port."""
        super(InvalidPort, self).__init__(
            'The port ("{0}") is not valid.'.format(port))


class ResolutionError(RFC3986Exception):
    """Exception to indicate a failure to resolve a URI."""

    def __init__(self, uri):
        """Initialize the error with the failed URI."""
        super(ResolutionError, self).__init__(
            "{0} is not an absolute URI.".format(uri.unsplit()))
