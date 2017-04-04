=================
 Validating URIs
=================

While not as difficult as `validating an email address`_, validating URIs is
tricky. Different parts of the URI allow different characters. Those sets
sometimes overlap and othertimes they don't and it's not very convenient.
Luckily, |rfc3986| makes validating URIs far simpler.

Example Usage
=============

First we need to create an instance of a
:class:`~rfc3986.validators.Validator` which takes no parameters. After that
we can call methods on the instance to indicate what we want to validate.

Let's assume that we're building something that takes user input for a URl and
we want to ensure that URL is only ever using a specific domain with https. In
that case, our code would look like this:

.. doctest::

    >>> from rfc3986 import validators, uri_reference
    >>> user_url = 'https://github.com/sigmavirus24/rfc3986'
    >>> validator = validators.Validator().allow_schemes(
    ...     'https',
    ... ).allow_hosts(
    ...     'github.com',
    ... )
    >>> validator.validate(uri_reference(
    ...     'https://github.com/sigmavirus24/rfc3986'
    ... ))
    >>> validator.validate(uri_reference(
    ...     'https://github.com/'
    ... ))
    >>> validator.validate(uri_reference(
    ...     'http://example.com'
    ... ))
    Traceback (most recent call last):
    ...
    rfc3986.exceptions.UnpermittedComponentError

First notice that we can easily reuse our validator object for each URL.
This allows users to not have to constantly reconstruct Validators for each
bit of user input. Next, we have three different URLs that we validate:

#. ``https://github.com/sigmavirus24/rfc3986``
#. ``https://github.com/``
#. ``http://example.com``

As it stands, our validator will allow the first two URLs to pass but will
fail the third. This is specifically because we only allow URLs using
``https`` as a scheme and ``github.com`` as the domain name.

.. _validating an email address:
    http://haacked.com/archive/2007/08/21/i-knew-how-to-validate-an-email-address-until-i.aspx/
