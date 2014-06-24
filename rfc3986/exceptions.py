# -*- coding: utf-8 -*-
class RFC3986Exception(Exception):
    pass


class InvalidAuthority(RFC3986Exception):
    def __init__(self, authority):
        super(InvalidAuthority, self).__init__(
            "The authority ({0}) is not valid.".format(authority))
