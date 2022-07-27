pregex.assertions
------------------------

.. automodule:: pregex.assertions
   :members:
   :undoc-members:

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
of the bitwise OR operator "|", as depicted within the code snippet below:

.. code-block:: python
   
   from pregex.classes import AnyDigit, AnyLowercaseLetter

   pre = AnyDigit() | AnyLowercaseLetter()
   print(pre.get_pattern()) # This will print "[0-9a-z]"

The same goes for negated classes as well:

.. code-block:: python

   from pregex.classes import AnyButDigit, AnyButLowercaseLetter

   pre = AnyButDigit() | AnyButLowercaseLetter()
   print(pre.get_pattern()) # This will print "[^0-9a-z]"

However, combining a regular and a negated class together cause a
"CannotBeCombinedException" to be thrown.

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

------------------------

pregex.groups
------------------------
This module contains all necessary classes that are used to construct both types
of groups, capturing and non-capturing, as well as classes that relate to any
other group-related concept, such as backreferences. In general, one should not
have to concern themselves with grouping, as patterns are automatically grouped
into non-capturing groups whenever this is deemed as necessary. Consider for
instance the code snippet below, where in the first case the "?" quanitifer is
applied to the pattern directly, whereas in the second case, the pattern is wrapped
within a non-capturing group:

.. code-block:: python

   from pregex.quantifiers import Optional

   print(Optional("a").get_pattern()) # This prints "a?"
   print(Optional("aa").get_pattern()) # This prints "(?:aa)?"

Even so, one can also explicitly construct a non-capturing group out of every
pattern if one wishes to do so:

.. code-block:: python

   from pregex.groups import NonCapturingGroup
   from pregex.quantifiers import Optional

   print(NonCapturingGroup(Optional("a")).get_pattern()) # This prints "(?:a)?"

You'll find however that "CapturingGroup" is probably the most important class
of this module, as it is used to create a capturing group out of any pattern,
so that some specific part of the pattern is captured separately whenever a match
occurs.

.. code-block:: python

   from pregex.groups import CapturingGroup

   pre = AnyLetter() + CapturingGroup(AnyLetter()) + AnyLetter()

   print(pre.get_groups("abc def")) # This prints "[('b'), ('e')]"


.. automodule:: pregex.groups
   :members:
   :undoc-members:

------------------------

pregex.operators
-----------------------
This module contains two operators, namely "Concat" and "Either", of which
you'll probably just need the latter, as pattern concatenation can also be
done via the overloaded addition operator "+", which produces code that is
much more easy to read.

.. code-block:: python

   from pregex.classes import AnyDigit
   from pregex.operators import Concat

   pre = AnyDigit()
   s = "text"

   concat = Concat(pre, s).get_pattern()
   better_concat = (pre + s).get_pattern()

   print(concat == better_concat) # This prints 'True'

.. automodule:: pregex.operators
   :members:
   :undoc-members:

------------------------

pregex.pre
-----------------

.. automodule:: pregex.pre
   :members:
   :undoc-members:

------------------------

pregex.quantifiers
-------------------------
All classes of this module are used in order to declare that a pattern is to be
repeated a number of times, where each class represents a slightly different
repetition rule. Out of these classes, you probably can ignore "Exactly" which
is used in order to dictate that a pattern is to be repeated an exact number of times,
as this rule can also be expressed via the use of the overloaded multiplication
operator "*", which produces much simpler and easy to read code:

.. code-block:: python

   from pregex.quantifiers import Exactly
   from pregex.tokens import Literal

   lit = Literal("text")

   pre1 = Exactly(lit, n=3)
   pre2 = 3 * lit

   print(pre1.get_pattern() == pre2.get_pattern()) # This prints 'True'.

.. automodule:: pregex.quantifiers
   :members:
   :undoc-members:
------------------------

pregex.tokens
--------------------
This module contains a number of classes that represent special characters,
as for example are the "newline" character, the "carriage return" character,
etc... In this module one will also find the "Literal" class, which can be used
in order to convert a string into a RegEx pattern. This class wraps the provided
string, escaping any characters it might contain that require to be escaped
so that the provided string is a valid RegEx pattern.

.. code-block:: python

   from pregex.tokens import Literal

   lit = Literal("hello.")
   print(lit.get_pattern()) # This prints "hello\."

However, you probably won't need to explicitly wrap a string within a "Literal"
instance, as this is done automatically whenever a string interacts with a "Pregex"
instance in any way.

.. code-block:: python

   from pregex.tokens import Literal
   from pregex.quantifiers import Optional

   pre = Optional("hello.") + "world."
   print(pre.get_pattern()) # This prints "(?:hello\.)?world\."

.. automodule:: pregex.tokens
   :members:
   :undoc-members: