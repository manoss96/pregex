pregex.assertions
------------------------

.. automodule:: pregex.assertions
   :members:
   :undoc-members:
   :show-inheritance:

------------------------

pregex.classes
---------------------
All classes within this module represent the so-called Regex "character classes",
which can be used in order to define a set or "class" of characters that can be matched.
A character class can be either one of the following two types:

	1. **Regular class**: This type of class represents the "[...]" pattern, 
	   which can be translated as "match every character defined within the
	   brackets". You can tell regular classes by their name, which follows
	   the "Any*" pattern.


	2. **Negated class**: This type of class represents the "[^...]" pattern, 
	   which can be translated as "match every character except for those 
	   defined within the brackets". You can tell negated classes by their name, 
	   which follows the "AnyBut*" pattern.

**Combining Classes**

Classes of the same type can be combined together in order to get the union of
the sets of characters they represent. This can be easily done though the use 
of the bitwise OR operator "|". For example:

.. code-block:: python
   
   from pregex.classes import AnyDigit, AnyLowercaseLetter

   pre = AnyDigit() | AnyLowercaseLetter()
   print(pre.get_pattern()) # This will print "[0-9a-z]"

The same goes for negated classes as well:

.. code-block:: python

   from pregex.classes import AnyButDigit, AnyButLowercaseLetter

   pre = AnyButDigit() | AnyButLowercaseLetter()
   print(pre.get_pattern()) # This will print "[^0-9a-z]"

However, combining a regular and a negated class together will throw a
"CannotBeCombinedException":

.. code-block:: python

   from pregex.classes import AnyDigit, AnyButLowercaseLetter

   pre = AnyDigit() | AnyButLowercaseLetter() # This is not OK!


**Negating Classes**

You should also know that every class can be negated through the use of the
bitwise NOT operator "~":

.. code-block:: python

   from pregex.classes import AnyDigit

   pre = ~ AnyDigit()
   print(pre.get_pattern()) # This will print "[^0-9]"

Negated classes can be negated as well, however you should probably avoid
this as it doesn't help much in making the code any more easy to read.

.. code-block:: python

   from pregex.classes import AnyButDigit

   pre = ~ AnyButDigit()
   print(pre.get_pattern()) # This will print "[0-9]"

Therefore, in order to create a negated class one can either negate a regular "Any*"
class by placing "~" in front of it, or use its "AnyBut*" negated class equivalent.
The result is entirely the same and which one you'll choose is just a matter of choice.

.. automodule:: pregex.classes
   :members:
   :undoc-members:
   :show-inheritance:

------------------------

pregex.groups
--------------------

.. automodule:: pregex.groups
   :members:
   :undoc-members:
   :show-inheritance:

------------------------

pregex.operators
-----------------------

This module contains two operators, namely "Concat" and "Either", of which
you'll probably just need the latter, as pattern concatenation is recommended
that is done via the overloaded addition operator "+".

.. code-block:: python

   from pregex.classes import AnyDigit
   from pregex.operators import Concat

   pre = AnyDigit()
   s = "text"

   concat = Concat(pre, s).get_pattern()
   better_concat = (pre + s).get_pattern()

   print(bad_concat == good_concat) # This prints 'True'

.. automodule:: pregex.operators
   :members:
   :undoc-members:
   :show-inheritance:

------------------------

pregex.pre
-----------------

.. automodule:: pregex.pre
   :members:
   :undoc-members:
   :show-inheritance:

------------------------

pregex.quantifiers
-------------------------

.. automodule:: pregex.quantifiers
   :members:
   :undoc-members:
   :show-inheritance:

------------------------

pregex.tokens
--------------------

.. automodule:: pregex.tokens
   :members:
   :undoc-members:
   :show-inheritance: