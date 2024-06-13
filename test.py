import typing


class ParseResultMixin:
    def geturl(self):
        """Shim to match the standard library method."""
        return self.unsplit()

    @property
    def hostname(self):
        """Shim to match the standard library."""
        return self.host

    @property
    def netloc(self):
        """Shim to match the standard library."""
        return self.authority

    @property
    def params(self):
        """Shim to match the standard library."""
        return self.query


class _ParseResultBase(typing.NamedTuple, typing.Generic[typing.AnyStr]):
    scheme: typing.Optional[typing.AnyStr]
    userinfo: typing.Optional[typing.AnyStr]
    host: typing.AnyStr
    port: typing.Optional[typing.AnyStr]
    path: typing.Optional[typing.AnyStr]
    query: typing.Optional[typing.AnyStr]
    fragment: typing.Optional[typing.AnyStr]


class ParseResult(_ParseResultBase[str], ParseResultMixin):
    encoding: str

    def __new__(
        cls,
        scheme: str,
        userinfo: str,
        host: str,
        port: str,
        path: str,
        query: str,
        fragment: str,
        uri_ref,
        encoding: str = "utf-8",
    ):
        """Create a new ParseResult instance."""
        self = super().__new__(
            cls,
            scheme or None,
            userinfo or None,
            host,
            port or None,
            path or None,
            query,
            fragment,
        )
        self.encoding = encoding
        self.reference = uri_ref
        return self

result = ParseResult("a", "b", "c", "d", "e", "f", "g", "h",)
result.thing = "hello"
print(result.thing)
print(result.__dict__)