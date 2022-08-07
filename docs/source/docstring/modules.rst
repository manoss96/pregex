*******
pregex
*******

In this page you can learn about each one of pregex's core modules
and how to effectively use them in order to build complex RegEx patterns.

Before diving into the modules themselves, it is important to know that due to the
large number of classes contained within this package, one can simply include
**from pregex import \*** at the top of their Python script, which results
in all of pregex's core modules being imported by using short aliases.
More specifically:

- Module **pregex.assert** is imported as **asr**.
- Module **pregex.classes** is imported as **cl**.
- Module **pregex.groups** is imported as **gr**.
- Module **pregex.operators** is imported as **op**.
- Module **pregex.quantifiers** is imported as **qu**.
- Module **pregex.tokens** is imported as **tk**.
- Class **pregex.pre.Pregex** is imported as is.

Take a look at the example below to better understand how this works:

.. code-block:: python

	from pregex import *

	pre = op.Either("Hello", "Bye") + " World" + qu.Optional("!")

	print(pre.get_pattern()) # This prints "(?:Hello|Bye) World!?"


It is recommended that you follow this practice as besides the fact that
it saves you the trouble of having to import from each module separately,
it also ensures that you are aware of the module that each class belongs in,
which in turn reveals a lot in regards to the class's functionality and how
it can be used.

==================================

Click on any one of pregex's core modules to learn more about it!

.. toctree::
   :maxdepth: 4

   pregex
