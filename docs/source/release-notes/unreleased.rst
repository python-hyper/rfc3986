2.x.y - 202z-aa-bb
------------------

- Preserve the leading slash required by RFC 3986 when removing dot segments
  from rootless paths, fixing resolution against bases such as
  ``scheme:foo/bar``. See `issue #84`_.

.. links below here

.. _issue #84: https://github.com/python-hyper/rfc3986/issues/84
