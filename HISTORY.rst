0.4.0 -- 2016-08-20
-------------------

- Add ``ParseResult.from_parts`` and ``ParseResultBytes.from_parts`` class
  methods to easily create a ParseResult

- When using regular expressions, use ``[0-9]`` instead of ``\d`` to avoid
  finding ports with "numerals" that are not valid in a port

0.3.1 -- 2015-12-15
-------------------

- Preserve empty query strings during normalization

0.3.0 -- 2015-10-20
-------------------

- Read README and HISTORY files using the appropriate codec so rfc3986 can be
  installed on systems with locale's other than utf-8 (specifically C)

- Replace the standard library's urlparse behaviour

0.2.2 -- 2015-05-27
-------------------

- Update the regular name regular expression to accept all of the characters
  allowed in the RFC. Closes bug #11 (Thanks Viktor Haag). Previously URIs
  similar to "http://http-bin.org" would be considered invalid.

0.2.1 -- 2015-03-20
-------------------

- Check that the bytes of an IPv4 Host Address are within the valid range.
  Otherwise, URIs like "http://256.255.255.0/v1/resource" are considered
  valid.

- Add 6 to the list of unreserved characters. It was previously missing.
  Closes bug #9

0.2.0 -- 2014-06-30
-------------------

- Add support for requiring components during validation. This includes adding
  parameters ``require_scheme``, ``require_authority``, ``require_path``,
  ``require_path``, ``require_query``, and ``require_fragment`` to
  ``rfc3986.is_valid_uri`` and ``URIReference#is_valid``.

0.1.0 -- 2014-06-27
-------------------

- Initial Release includes validation and normalization of URIs
