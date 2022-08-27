#######################
Importing Practices
#######################

Due to the relatively large number of modules contained within pregex,
having to import each class individually can quickly become extremely annoying.
For this reason, it is suggested that one handles their imports by
including the following statements at the top of their Python script:

* ``from pregex.core import *`` - Imports all core modules by using short aliases.
  More specifically:

  * Module :py:mod:`pregex.core.assertions` is imported as ``asr``
  * Module :py:mod:`pregex.core.classes` is imported as ``cl``
  * Module :py:mod:`pregex.core.groups` is imported as ``gr``
  * Module :py:mod:`pregex.core.operators` is imported as ``op``
  * Module :py:mod:`pregex.core.quantifiers` is imported as ``qu``
  * Module :py:mod:`pregex.core.tokens` is imported as ``tk``
  * Classes :class:`pregex.core.pre.Pregex` and :class:`pregex.core.pre.Empty` are imported as is.

  Take a look at the example below to better understand how this works:

  .. code-block:: python

	from pregex.core import *

	pre = op.Either("Hello", "Bye") + " World" + qu.Optional("!")

	pre.print_pattern() # This prints "(?:Hello|Bye) World!?"

  It is recommended that you follow this practice as besides the fact that
  it saves you the trouble of having to import from each module separately,
  it also ensures that you are aware of the module that each class belongs in,
  which in turn reveals a lot in regards to the class's functionality and how
  it can be used.

* ``from pregex.meta import *`` - Directly imports every class defined within any
  one of the *meta* modules.


Finally, one is also able to replace both of the above import statements
with a single statement, namely ``from pregex import *``.