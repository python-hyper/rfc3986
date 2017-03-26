.. _narrative:

====================
 User Documentation
====================

|rfc3986| has several API features and convenience methods. The core of
|rfc3986|'s API revolves around parsing, validating, and building URIs.

There is an API to provide compatibility with :mod:`urllib.parse`, there is an
API to parse a URI as a URI Reference, there's an API to provide validation of
URIs, and finally there's an API to build URIs.

.. note::

    There's presently no support for IRIs as defined in :rfc:`3987`.

|rfc3986| parses URIs much differently from :mod:`urllib.parse` so users may
see some subtle differences with very specific URLs that contain rough
edgecases. Regardless, we do our best to implement the same API so you should
be able to seemlessly swap |rfc3986| for ``urlparse``.


.. toctree::
    :maxdepth: 2

    user/parsing
    user/validating
    user/building
