pregex.pre
-----------------
This module contains a single class, namely "Pregex", which constitutes the base
class for every other class within the "pregex" package. This means that all methods
of this class are also defined for every other class as well.

**Converting a string to a Pregex instance**

In general, one can wrap any string within a "Pregex" instance by passing it as a 
parameter to the class's constructor. By doing this, any characters of the provided
string that might need escaping are automatically escaped.

.. code-block:: python

   from pregex.pre import Pregex

   pre = Pregex("Hello.")

   print(pre.get_pattern()) # This prints 'Hello\.'

However, you probably won't need to do this often since any string that interacts with a
"Pregex" instance in any way is automatically converted into a "Pregex" instance itself:

.. code-block:: python

   from pregex.pre import Pregex
   from pregex.quantifiers import Optional

   # These two statements are equivalent.
   pre1 = Optional(Pregex("Hello."))
   pre2 = Optional("Hello.")

Finally, you should also know that character-escaping can also be disabled when wrapping a string
within a "Pregex" instance. This can be used for example in order to explicitly define
your own RegEx patterns:

.. code-block:: python

   from pregex.pre import Pregex

   pre = Pregex("[a-z].?", escape=False)

   print(pre.get_pattern()) # This prints '[a-z].?'


**Concatenating patterns with "+"**

Instead of using class "pregex.operators.Concat" in order to concatenate "Pregex"
instances, one is also able to make use of the overloaded addition operator "+" 
as seen in the example below:

.. code-block:: python

   from pregex.pre import Pregex
   from pregex.quantifiers import Optional

   pre = Pregex("a") + Pregex("b") + Optional("c")

   print(pre.get_pattern()) # This prints 'abc?'

This of course works with simple strings as well, as long as there
is at least one "Pregex" instance involved in the operation:

.. code-block:: python

   from pregex.quantifiers import Optional

   pre = "a" + "b" + Optional("c")

   print(pre.get_pattern()) # This prints 'abc?'

Concatenating patterns this way is encouraged as it leads to much more easy-to-read code.

**Repeating patterns with "*"**

The "Pregex" class has one more overloaded operator, namely the multiplication
operator "*", which essentially replaces the functionality of class
"pregex.quantifiers.Exactly". By using this operator on a "Pregex" instance, one
indicates that a pattern is to be repeated an exact number of times:

.. code-block:: python

   from pregex.pre import Pregex

   pre = 3 * Pregex("Hi")

   print(pre.get_pattern()) # This prints '(?:Hi){3}'

Now that you've taken a first look at the "Pregex" class, check out its
methods below to see what else this class has to offer!

.. automodule:: pregex.pre
   :members:
   :undoc-members:

------------------------

pregex.assertions
------------------------
All classes within this module "assert" something about the provided pattern
without having to match any additional characters. For example, "MatchAtStart" ensures
that the provided pattern matches only when it is found at the start of the string,
while "NotFollowedBy" asserts that any match with the provided pattern must not be followed
by some other specified pattern. Another things you should keep in mind is that assertions
cannot be quantified, as attempting that will cause a "CannotBeQuantifiedException"
exception to be thrown.


.. automodule:: pregex.assertions
   :members:
   :undoc-members:

------------------------

pregex.classes
---------------------
All classes within this module represent the so-called RegΕx "character classes",
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

**Class Unions**

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

However, attempting to get the union of a regular class and a negated class
causes a "CannotBeUnionedException" to be thrown.

.. code-block:: python

   from pregex.classes import AnyDigit, AnyButLowercaseLetter

   pre = AnyDigit() | AnyButLowercaseLetter() # This is not OK!

**Subtracting Classes**

Subtraction is another operation that is exclusive to classes and is achieved via
the overloaded subtraction operator "-". This feature comes in handy when one wishes
to construct a class that would be tiresome to construct otherwise. Consider for
example the class of all word characters except for alphabetic characters "Cc" and
"Gg", as well as the digit "3". Constructing said class via subtraction is extremely
easy:

.. code-block:: python

   from pregex.classes import AnyWordChar, AnyFrom

   pre = AnyWordChar() - AnyFrom('C', 'c', 'G', 'g', '3')

This is the returned pattern when invoking 'pre.get_pattern()'. It is evident
that building the following pattern through multiple class unions would be
more time consuming and prone to errors.

.. code-block:: python

	[A-BD-FH-Za-bd-fh-z0-24-9_]

It should be noted that just like in the case of class unions, one is only 
allowed to subtract a regular class from a regular class or a negated class
from a negated class, as any other attempt will cause a "CannotBeSubtractedException"
to be thrown.

.. code-block:: python

   from pregex.classes import AnyWordChar, AnyButLowercaseLetter

   pre = AnyWordChar() - AnyButLowercaseLetter() # This is not OK!

**Negating Classes**

Finally, it is good to know that every regular class can be negated through
the use of the bitwise NOT operator "~":

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
other group-related concept, such as backreferences and conditionals. In general,
one should not have to concern themselves with grouping, as patterns are automatically
grouped into non-capturing groups whenever this is deemed necessary. Consider for
instance the code snippet below, where in the first case the "Optional" quanitifer is
applied to the pattern directly, whereas in the second case, the pattern is wrapped
within a non-capturing group:

.. code-block:: python

   from pregex.quantifiers import Optional

   print(Optional("a").get_pattern()) # This prints "a?"
   print(Optional("aa").get_pattern()) # This prints "(?:aa)?"

Even so, one can also explicitly construct a non-capturing group out of any
pattern if one wishes to do so:

.. code-block:: python

   from pregex.groups import NonCapturingGroup
   from pregex.quantifiers import Optional

   print(NonCapturingGroup(Optional("a")).get_pattern()) # This prints "(?:a)?"

You'll find however that "CapturingGroup" is probably the most important class
of this module, as it is used to create a capturing group out of a pattern,
so that said pattern is also captured separately whenever a match occurs.

.. code-block:: python

   from pregex.groups import CapturingGroup
   from pregex.classes import AnyLetter

   pre = AnyLetter() + CapturingGroup(AnyLetter()) + AnyLetter()

   print(pre.get_groups("abc def")) # This prints "[('b'), ('e')]"


.. automodule:: pregex.groups
   :members:
   :undoc-members:

------------------------

pregex.operators
-----------------------
This module contains two operators, namely "Concat" and "Either", the former
of which is used to concatenate two or more patterns, whereas the latter constitutes
the alternation operator, which is used whenever either one of the provided patterns
can be matched.

.. automodule:: pregex.operators
   :members:
   :undoc-members:

------------------------

pregex.quantifiers
-------------------------
Every class within this module is used to declare that a pattern is to be
matched a number of times, with each class representing a slightly different
pattern-repetition rule.

.. automodule:: pregex.quantifiers
   :members:
   :undoc-members:

------------------------

pregex.tokens
--------------------
This module contains a number of classes that represent special characters.
Each token represents one and only one character. It is recommended that you
use the classes of this module instead of providing their corresponding characters
as strings on your own, as this might lead to all sorts of errors due to escaping.

.. automodule:: pregex.tokens
   :members:
   :undoc-members: