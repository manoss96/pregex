###################
Covering the Basics
###################

In this section you will learn about the :class:`~pregex.core.pre.Pregex` class,
and how instances of this class can be effectively combined together in order
to construct complex RegEx patterns.

Understanding Pregex
============================================

The basic idea behind PRegEx is to provide higher-level abstractions
of RegEx patterns that are easier to read and to work with.

.. code-block:: python

   from pregex.core.quantifiers import Optional
   from pregex.core.groups import Capture
   from pregex.core.operators import Either

   Optional('a') # Stands for quantifier 'a?'
   Capture('a') # Stands for capturing group '(a)'
   Either('a', 'b') # Stands for alternation 'a|b'

Besides representing RegEx patterns, these abstractions must also be able to
serve as individual units that can be built upon. This is made possible by
having a single base class, namely :class:`~pregex.core.pre.Pregex`, from which
all other classes inherit.

.. code-block:: python

   from pregex.core.pre import Pregex
   from pregex.core.classes import AnyDigit
   from pregex.core.operators import Either
   from pregex.core.assertions import FollowedBy

   # These are both Pregex instances.
   digit: Pregex = AnyDigit()
   a_or_b: Pregex = Either('a', 'b')

   # This is a Pregex instance as well!
   digit_followed_by_either_a_or_b: Pregex = FollowedBy(digit, a_or_b)

Being wrapped within instances of the same type allows for these Pregex
patterns to be easily combined together into even more complex patterns.
Consider for example the code snippet below where we construct a Pregex
pattern that will match either any word that starts with "ST" or "st",
or any three-digit integer number:

.. code-block:: python

   from pregex.core.operators import Either
   from pregex.core.quantifiers import OneOrMore
   from pregex.core.assertions import WordBoundary
   from pregex.core.classes import AnyLetter, AnyDigit

   starts_with_st = Either('ST', 'st') + OneOrMore(AnyLetter())

   three_digit_integer = (AnyDigit() - '0') + (2 * AnyDigit())

   pre = WordBoundary() + Either(starts_with_st, three_digit_integer) + WordBoundary()

By both using PRegEx's human-friendly syntax and breaking down the pattern into simpler
subpatterns, it is not hard to tell how this pattern is constructed, as well as what its
purpose is. Furthermore, the resulting pattern is a Pregex instance itself, and as such,
it has access to all of the class's methods:

.. code-block:: python

   pre.print_pattern() # This prints '\b(?:(?:ST|st)[A-Za-z]+|[1-9]\d{2})\b'
   print(pre.get_matches('STACK station pastry must 012 446 3462')) # This prints "['STACK', 'station', '446']"


Converting a string into a Pregex instance
============================================
In general, one can wrap any string within a Pregex instance by passing it as a 
parameter to the class's constructor. By doing this, any characters of the provided
string that require escaping are automatically escaped.

.. code-block:: python

   from pregex.core.pre import Pregex

   pre = Pregex('Hello.')

   pre.print_pattern() # This prints 'Hello\.'

Nevertheless, you probably won't need to do this often since any string that interacts
with a Pregex instance in any way is automatically converted into a Pregex instance itself:

.. code-block:: python

   from pregex.core.pre import Pregex
   from pregex.core.quantifiers import Optional

   # These two statements are equivalent.
   pre1 = Optional(Pregex('Hello.'))
   pre2 = Optional('Hello.')

Manually wrapping strings within Pregex instances can however be of use when one wishes
to explicitly define their own RegEx pattern. In that case, one must also not forget
to set the class's constructor ``escape`` parameter to ``False``, in order to disable
character-escaping:

.. code-block:: python

   from pregex.core.pre import Pregex

   pre = Pregex('[a-z].?', escape=False)

   pre.print_pattern() # This prints '[a-z].?'   

Concatenating patterns with "+"
============================================
There exists a separate :class:`~pregex.core.operators.Concat` class,
which is specifically used to concatenate two or more patterns together.
However, one can also achieve the same result by making use of Pregex's
overloaded addition operator ``+``.

.. code-block:: python

   from pregex.core.pre import Pregex
   from pregex.core.quantifiers import Optional

   pre = Pregex('a') + Pregex('b') + Optional('c')

   print(pre.get_pattern()) # This prints 'abc?'

This of course works with simple strings as well, as long as there
is at least one Pregex instance involved in the operation:

.. code-block:: python

   from pregex.core.quantifiers import Optional

   pre = 'a' + 'b' + Optional('c')

   print(pre.get_pattern()) # This prints 'abc?'

Concatenating patterns this way is encouraged as it leads to much more
easy-to-read code.

Repeating patterns with "*"
============================================
:class:`Pregex` has one more overloaded operator, namely the multiplication operator
``*``, which essentially replaces class :class:`~pregex.core.quantifiers.Exactly`.
By using this operator on a Pregex instance, one indicates that a pattern is to be
repeated an exact number of times:

.. code-block:: python

   from pregex.core.pre import Pregex

   pre = 3 * Pregex('a')

   print(pre.get_pattern()) # This prints 'a{3}'

As it is the case with the addition operator ``+``, it is recommended
that one also makes use of the multiplication operator ``*`` whenever
possible.


Pattern chaining
==================
Apart from PRegEx's standard pattern-building API which involves
wrapping strings and Pregex instances within other Pregex instances,
there also exists a more functional-like approach to constructing patterns.
More specifically, every Pregex instance has access to a number of methods
that can be used so as to apply basic RegEx operators to its underlying
pattern, through which process a brand new Pregex instance is generated.

.. code-block:: python

  from pregex.core.classes import AnyLetter()
  from pregex.core.quantifiers import Optional()

  letter = AnyLetter()

  # Both statements are equivalent.
  optional_letter_1 = Optional(letter)
  optional_letter_2 = letter.optional()

By chaining many of these methods together, it is also possible
to construct more complex patterns. This technique is called
*pattern chaining*:

.. code-block:: python

  from pregex.core.pre import Empty

  pre = Empty() \
      .concat('a') \
      .either('b') \
      .one_or_more() \
      .concat('c') \
      .optional() \
      .concat('d') \
      .match_at_line_start() \
      .match_at_line_end()

  pre.print_pattern() # This prints '^(?:(?:a|b)+c)?d$'

It is generally recommended that you use the standard API when dealing
with larger patterns, as it provides a way of building patterns that is
usually easier to read. Be that as it may, there do exist several case
where pattern chaining is the better choice of the two. In the end, it's
just a matter of choice!

Check out :class:`~pregex.core.pre.Pregex` to learn what other methods this class
has to offer.