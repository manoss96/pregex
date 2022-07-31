*******
pregex
*******

In this page you can learn about each one of PRegEx's core modules
and how to effectively use them in order to build complex RegEx patterns.

Before diving into the modules themselves, it is important to know that due to the
large number of classes contained within this package, one can simply include
"from pregex import *" at the top of their Python script, which results
in all of pregex's core modules being imported by using short aliases.
More specifically:

- "assert.py" is imported as "asr".
- "classes.py" is imported as "cl".
- "groups.py" is imported as "gr".
- "operators.py" is imported as "op".
- "quantifiers.py" is imported as "qu".
- "tokens.py" is imported as "tk".

Take a look at the example below to better understand how this works:

.. code-block:: python

	from pregex import *

	pre = op.Either("Hello", "Bye") + " World" + qu.Optional("!")

	print(pre.get_pattern()) # This prints "(?:Hello|Bye) World\!?"

It is recommended that you follow this practice so that each time you use
a class you are aware of the module it belongs in, as this reveals a lot about
each class' functionality and how it can be used.

==================================

You can click on any one of pregex's core modules to learn more about it!

.. toctree::
   :maxdepth: 4

   pregex
