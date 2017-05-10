===============
 Parsing a URI
===============

There are two ways to parse a URI with |rfc3986|

#. :meth:`rfc3986.api.uri_reference`

   This is best when you're **not** replacing existing usage of
   :mod:`urllib.parse`. This also provides convenience methods around safely
   normalizing URIs passed into it.

#. :meth:`rfc3986.api.urlparse`

   This is best suited to completely replace :func:`urllib.parse.urlparse`.
   It returns a class that should be indistinguishable from
   :class:`urllib.parse.ParseResult`

Let's look at some code samples.


Some Examples
=============

First we'll parse the URL that points to the repository for this project.

.. testsetup:: *

    import rfc3986
    url = rfc3986.urlparse('https://github.com/sigmavirus24/rfc3986')
    uri = rfc3986.uri_reference('https://github.com/sigmavirus24/rfc3986')

.. code-block:: python

    url = rfc3986.urlparse('https://github.com/sigmavirus24/rfc3986')


Then we'll replace parts of that URL with new values:

.. testcode:: ex0

    print(url.copy_with(
        userinfo='username:password',
        port='443',
    ).unsplit())

.. testoutput:: ex0

    https://username:password@github.com:443/sigmavirus24/rfc3986

This, however, does not change the current ``url`` instance of
:class:`~rfc3986.parseresult.ParseResult`. As the method name might suggest,
we're copying that instance and then overriding certain attributes.
In fact, we can make as many copies as we like and nothing will change.

.. testcode:: ex1

    print(url.copy_with(
        scheme='ssh',
        userinfo='git',
    ).unsplit())

.. testoutput:: ex1

    ssh://git@github.com/sigmavirus24/rfc3986

.. testcode:: ex1

    print(url.scheme)

.. testoutput:: ex1

    https

We can do similar things with URI References as well.

.. code-block:: python

    uri = rfc3986.uri_reference('https://github.com/sigmavirus24/rfc3986')

.. testcode:: ex2

    print(uri.copy_with(
        authority='username:password@github.com:443',
        path='/sigmavirus24/github3.py',
    ).unsplit())

.. testoutput:: ex2

    https://username:password@github.com:443/sigmavirus24/github3.py

However, URI References may have some unexpected behaviour based strictly on
the RFC.

Finally, if you want to remove a component from a URI, you may pass ``None``
to remove it, for example:

.. testcode:: ex3

    print(uri.copy_with(path=None).unsplit())

.. testoutput:: ex3

    https://github.com

This will work on both URI References and Parse Results.


And Now For Something Slightly Unusual
======================================

If you are familiar with GitHub, GitLab, or a similar service, you may have
interacted with the "SSH URL" for some projects. For this project,
the SSH URL is:

.. code::

    git@github.com:sigmavirus24/rfc3986


Let's see what happens when we parse this.

.. code-block:: pycon

    >>> rfc3986.uri_reference('git@github.com:sigmavirus24/rfc3986')
    URIReference(scheme=None, authority=None,
    path=u'git@github.com:sigmavirus24/rfc3986', query=None, fragment=None)

There's no scheme present, but it is apparent to our (human) eyes that
``git@github.com`` should not be part of the path. This is one of the areas
where :mod:`rfc3986` suffers slightly due to its strict conformance to
:rfc:`3986`. In the RFC, an authority must be preceded by ``//``. Let's see
what happens when we add that to our URI

.. code-block:: pycon

    >>> rfc3986.uri_reference('//git@github.com:sigmavirus24/rfc3986')
    URIReference(scheme=None, authority=u'git@github.com:sigmavirus24',
    path=u'/rfc3986', query=None, fragment=None)

Somewhat better, but not much.

.. note::

    The maintainers of :mod:`rfc3986` are working to discern better ways to
    parse these less common URIs in a reasonable and sensible way without
    losing conformance to the RFC.
