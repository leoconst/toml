Python TOML interface
#####################

TOML_ reader and writer.


Encoding
--------

You can convert mappings to strings with ``to_string``:

.. code:: python

    >>> toml.to_string({'table': {'a': 4, 'b': .1}})
    '\n[table]\na = 4\nb = 0.1'

You can also write directly to files with ``to_path``:

.. code:: python

    >>> toml.to_path('config.toml', {'table': {'a': 4, 'b': .1}})


Decoding
--------

You can convert TOML to mappings with ``from_string``:

.. code:: python

    >>> toml.from_string('[config]\ninteger = 2\nfloat = 3.1\nstring = "abc"')
    {'config': {'integer': 2, 'float': 3.1, 'string': 'abc'}}

And you can read directly from a file path with ``from_path``:

.. code:: python

    >>> toml.from_path('config.toml')



.. _TOML: https://github.com/toml-lang/toml