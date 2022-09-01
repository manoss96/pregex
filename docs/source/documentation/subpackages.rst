#############
Subpackages
#############

PRegEx's modules are divided into two subpackages, namely ``pregex.core`` and
``pregex.meta``, the former of which predominantly contains modules whose classes
represent some fundamental RegEx operator, whereas the latter acts as a collection
of various classes that build upon those within the core modules in order to provide
ready-made patterns that can be used "straight out of the box".

pregex.core
=================

In order to better understand *core* modules, consider for example
:py:mod:`pregex.core.quantifiers`, all classes of which correspond
to a unique RegEx quantifier:

.. code-block:: python

   from pregex.core.quantifiers import *

   Optional # Represents quantifier '?'
   Indefinite # Represents quantifier '*'
   OneOrMore # Represents quantifier '+'
   Exactly # Represents quantifier '{n}'
   AtLeast # Represents quantifier '{n,}'
   AtMost # Represents quantifier '{,n}'
   AtLeastAtMost # Represents quantifier '{n,m}'

However, not all core modules contain classes that represent some specific
RegEx operator. There is the :py:mod:`pregex.core.tokens` module, whose
classes act as wrappers for various single-character patterns. That is, either
to protect you from any character-escape-related issues that may arise due
to using raw strings containing backslashes, or to save you the trouble of looking
for a specific symbol's Unicode code point, provided of course that there is a
corresponding *Token* class for that symbol.

.. code-block:: python

   from pregex.core.tokens import Newline, Copyright

   # Both of these statements are 'True'.
   Newline().is_exact_match('\n')
   Copyright().is_exact_match('©')


Lastly, there is module :py:mod:`pregex.core.classes` which does not only
offer a number of commonly used RegEx character classes, but a complete
framework for working on these classes as if they were regular sets.

.. code-block:: python

   from pregex.core.classes import AnyLetter, AnyDigit

   letter = AnyLetter() # Represents '[A-Za-z]'
   digit_but_five = AnyDigit() - '5' # Represents '[0-46-9]'
   letter_or_digit_but_five = letter | digit_but_five # Represents '[A-Za-z0-46-9]'
   any_but_letter_or_digit_but_five = ~ letter_or_digit_but_five # Represents '[^A-Za-z0-46-9]'

Click on any one of pregex's *core* modules below to check out its classes:

.. toctree::
   :maxdepth: 1

   modules/core/assertions
   modules/core/classes
   modules/core/groups
   modules/core/operators
   modules/core/pre
   modules/core/quantifiers
   modules/core/tokens

pregex.meta
=================

Unlike *core* modules, whose classes are all independent from each other,
*meta* modules contain classes that effectively combine various
:class:`~pregex.core.pre.Pregex` instances together in order to form
complex patterns that you can then use. Consider for example
:class:`~pregex.meta.essentials.Integer` which enables you to
match any integer within a specified range.

.. code-block:: python

   from pregex.meta.essentials import Integer

   text = "1 5 11 23 77 117 512 789 1011"

   pre = Integer(start=50, end=1000)
   
   print(pre.get_matches(text)) # This prints "['77', '117', '512', '789']"

Classes in *meta* modules therefore offer various patterns that can be useful,
but at the same time hard to build. And remember, no matter the complexity of
a pattern, it remains to be a Pregex instance, and as such, it can always be
extended even further!

.. code-block:: python

   from pregex.core.classes import AnyLetter
   from pregex.meta.essentials import Integer

   pre = AnyLetter() + '.' + Integer(start=50, end=1000)
   text = "a.1 b.5 c.11 d.23 e.77 f.117 g.512 h.789 i.1011"

   print(pre.get_matches(text)) # This prints "['e.77 f.117', 'g.512', 'h.789']"

Click on any one of pregex's *meta* modules below to check out its classes:

.. toctree::
   :maxdepth: 1

   modules/meta/essentials