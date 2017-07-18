.. _validating:

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

Allowing Only Trusted Domains and Schemes
-----------------------------------------

Let's assume that we're building something that takes user input for a URL and
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

Preventing Leaks of User Credentials
------------------------------------

Next, let's imagine that we want to prevent leaking user credentials. In that
case, we want to ensure that there is no password in the user information
portion of the authority. In that case, our new validator would look like this:

.. doctest::

    >>> from rfc3986 import validators, uri_reference
    >>> user_url = 'https://github.com/sigmavirus24/rfc3986'
    >>> validator = validators.Validator().allow_schemes(
    ...     'https',
    ... ).allow_hosts(
    ...     'github.com',
    ... ).forbid_use_of_password()
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
    >>> validator.validate(uri_reference(
    ...     'https://sigmavirus24@github.com'
    ... ))
    >>> validator.validate(uri_reference(
    ...     'https://sigmavirus24:not-my-real-password@github.com'
    ... ))
    Traceback (most recent call last):
    ...
    rfc3986.exceptions.PasswordForbidden

Requiring the Presence of Components
------------------------------------

Up until now, we have assumed that we will get a URL that has the appropriate
components for validation. For example, we assume that we will have a URL that
has a scheme and hostname. However, our current validation doesn't require
those items exist.

.. doctest::

    >>> from rfc3986 import validators, uri_reference
    >>> user_url = 'https://github.com/sigmavirus24/rfc3986'
    >>> validator = validators.Validator().allow_schemes(
    ...     'https',
    ... ).allow_hosts(
    ...     'github.com',
    ... ).forbid_use_of_password()
    >>> validator.validate(uri_reference('//github.com'))
    >>> validator.validate(uri_reference('https:/'))

In the first case, we have a host name but no scheme and in the second we have
a scheme and a path but no host. If we want to ensure that those components
are there and that they are *always* what we allow, then we must add one last
item to our validator:

.. doctest::

    >>> from rfc3986 import validators, uri_reference
    >>> user_url = 'https://github.com/sigmavirus24/rfc3986'
    >>> validator = validators.Validator().allow_schemes(
    ...     'https',
    ... ).allow_hosts(
    ...     'github.com',
    ... ).forbid_use_of_password(
    ... ).require_presence_of(
    ...     'scheme', 'host',
    ... )
    >>> validator.validate(uri_reference('//github.com'))
    Traceback (most recent call last):
    ...
    rfc3986.exceptions.MissingComponentError
    >>> validator.validate(uri_reference('https:/'))
    Traceback (most recent call last):
    ...
    rfc3986.exceptions.MissingComponentError
    >>> validator.validate(uri_reference('https://github.com'))
    >>> validator.validate(uri_reference(
    ...     'https://github.com/sigmavirus24/rfc3986'
    ... ))


Checking the Validity of Components
-----------------------------------

As of version 1.1.0, |rfc3986| allows users to check the validity of a URI
Reference using a :class:`~rfc3986.validators.Validator`. Along with the above 
examples we can also check that a URI is valid per :rfc:`3986`. The validation
of the components is pre-determined so all we need to do is specify which 
components we want to validate:

.. doctest::

    >>> from rfc3986 import validators, uri_reference
    >>> valid_uri = uri_reference('https://github.com/')
    >>> validator = validators.Validator().allow_schemes(
    ...     'https',
    ... ).allow_hosts(
    ...     'github.com',
    ... ).forbid_use_of_password(
    ... ).require_presence_of(
    ...     'scheme', 'host',
    ... ).check_validity_of(
    ...     'scheme', 'host', 'path',
    ... )
    >>> validator.validate(valid_uri)
    >>> invalid_uri = valid_uri.copy_with(path='/#invalid/path')
    >>> validator.validate(invalid_uri)
    Traceback (most recent call last):
    ...
    rfc3986.exceptions.InvalidComponentsError

Paths are not allowed to contain a ``#`` character unless it's
percent-encoded. This is why our ``invalid_uri`` raises an exception when we
attempt to validate it.


.. links
.. _validating an email address:
    http://haacked.com/archive/2007/08/21/i-knew-how-to-validate-an-email-address-until-i.aspx/
