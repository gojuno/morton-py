Morton Pack/Unpack Library
==========================

Basics
------

Check `wikipedia <https://en.wikipedia.org/wiki/Z-order_curve>`_ for details.

Example
-------

.. code-block:: python

    import morton

    m = morton.Morton(dimensions=2, bits=32)
    code = m.pack(13, 42)    # pack two values
    values = m.unpack(code)  # should get back 13 and 42
