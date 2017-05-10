===============
 Building URIs
===============

Constructing URLs often seems simple. There are some problems with
concatenating strings to build a URL:

- Certain parts of the URL disallow certain characters

- Formatting some parts of the URL is tricky and doing it manually isn't fun

To make the experience better |rfc3986| provides the
:class:`~rfc3986.builder.URIBuilder` class to generate valid
:class:`~rfc3986.uri.URIReference` instances. The
:class:`~rfc3986.builder.URIBuilder` class will handle ensuring that each
component is normalized and safe for real world use.


Example Usage
=============

.. note::

    All of the methods on a :class:`~rfc3986.builder.URIBuilder` are
    chainable (except :meth:`~rfc3986.builder.URIBuilder.finalize`).

Let's build a basic URL with just a scheme and host. First we create an
instance of :class:`~rfc3986.builder.URIBuilder`. Then we call
:meth:`~rfc3986.builder.URIBuilder.add_scheme` and
:meth:`~rfc3986.builder.URIBuilder.add_host` with the scheme and host
we want to include in the URL. Then we convert our builder object into
a :class:`~rfc3986.uri.URIReference` and call
:meth:`~rfc3986.uri.URIReference.unsplit`.

.. doctest::

    >>> from rfc3986 import builder
    >>> print(builder.URIBuilder().add_scheme(
    ...     'https'
    ... ).add_host(
    ...     'github.com'
    ... ).finalize().unsplit())
    https://github.com

Each time you invoke a method, you get a new instance of a
:class:`~rfc3986.builder.URIBuilder` class so you can build several different
URLs from one base instance.

.. doctest::

    >>> from rfc3986 import builder
    >>> github_builder = builder.URIBuilder().add_scheme(
    ...     'https'
    ... ).add_host(
    ...     'api.github.com'
    ... )
    >>> print(github_builder.add_path(
    ...     '/users/sigmavirus24'
    ... ).finalize().unsplit())
    https://api.github.com/users/sigmavirus24
    >>> print(github_builder.add_path(
    ...     '/repos/sigmavirus24/rfc3986'
    ... ).finalize().unsplit())
    https://api.github.com/repos/sigmavirus24/rfc3986

|rfc3986| makes adding authentication credentials convenient. It takes care of
making the credentials URL safe. There are some characters someone might want
to include in a URL that are not safe for the authority component of a URL.

.. doctest::

    >>> from rfc3986 import builder
    >>> print(builder.URIBuilder().add_scheme(
    ...     'https'
    ... ).add_host(
    ...     'api.github.com'
    ... ).add_credentials(
    ...     username='us3r',
    ...     password='p@ssw0rd',
    ... ).finalize().unsplit())
    https://us3r:p%40ssw0rd@api.github.com

Further, |rfc3986| attempts to simplify the process of adding query parameters
to a URL. For example, if we were using Elasticsearch, we might do something
like:

.. doctest::

    >>> from rfc3986 import builder
    >>> print(builder.URIBuilder().add_scheme(
    ...     'https'
    ... ).add_host(
    ...     'search.example.com'
    ... ).add_path(
    ...     '_search'
    ... ).add_query_from(
    ...     [('q', 'repo:sigmavirus24/rfc3986'), ('sort', 'created_at:asc')]
    ... ).finalize().unsplit())
    https://search.example.com/_search?q=repo%3Asigmavirus24%2Frfc3986&sort=created_at%3Aasc

Finally, we provide a way to add a fragment to a URL. Let's build up a URL to
view the section of the RFC that refers to fragments:

.. doctest::

    >>> from rfc3986 import builder
    >>> print(builder.URIBuilder().add_scheme(
    ...     'https'
    ... ).add_host(
    ...     'tools.ietf.org'
    ... ).add_path(
    ...     '/html/rfc3986'
    ... ).add_fragment(
    ...     'section-3.5'
    ... ).finalize().unsplit())
    https://tools.ietf.org/html/rfc3986#section-3.5
