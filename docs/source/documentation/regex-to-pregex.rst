###################
Regex to Pregex
###################

In this section you will learn about the :class:`~pregex.core.pre.Pregex` class,
and how instances of this class can be effectively combined together in order
to construct complex RegEx patterns while maintaining readability.

Understanding Pregex
============================================

The basic idea behind PRegEx is to provide higher-level abstractions
of RegEx patterns that are easier to read and to work with.

.. code-block:: python

   from pregex.core.quantifiers import Optional
   from pregex.core.groups import Capture
   from pregex.core.operators import Either

   Optional # Stands for quantifier '?'
   Capture # Stands for capturing group '(...)'
   Either # Stands for alternation '|'

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
   a_or_b: Pregex = Either("a", "b")

   # This is a Pregex instance as well!
   digit_followed_by_either_a_or_b: Pregex = FollowedBy(digit, a_or_b)

Being wrapped within instances of the same type allows for these Pregex
patterns to be easily combined together into even more complex patterns.
Consider for example the code snippet below where we construct a Pregex
pattern that will match either any word that starts with "ST" or "st",
or any 3-digit integer number:

.. code-block:: python

   from pregex.core.operators import Either
   from pregex.core.quantifiers import OneOrMore
   from pregex.core.assertions import WordBoundary
   from pregex.core.classes import AnyLetter, AnyDigit

   starts_with_st = Either("ST", "st") + OneOrMore(AnyLetter())

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

   pre = Pregex("Hello.")

   pre.print_pattern() # This prints 'Hello\.'

Nevertheless, you probably won't need to do this often since any string that interacts
with a Pregex instance in any way is automatically converted into a Pregex instance itself:

.. code-block:: python

   from pregex.core.pre import Pregex
   from pregex.core.quantifiers import Optional

   # These two statements are equivalent.
   pre1 = Optional(Pregex("Hello."))
   pre2 = Optional("Hello.")

Manually wrapping strings within Pregex instances can however be of use when one wishes
to explicitly define their own RegEx pattern. In that case, one must also not forget
to set the class's constructor ``escape`` parameter to ``False``, in order to disable
character-escaping:

.. code-block:: python

   from pregex.core.pre import Pregex

   pre = Pregex("[a-z].?", escape=False)

   pre.print_pattern() # This prints '[a-z].?'   

Concatenating patterns with `+`
============================================
There exists a separate :class:`~pregex.core.operators.Concat` class,
which is specifically used to concatenate two or more patterns together.
However, one can also achieve the same result by making use of Pregex's
overloaded addition operator ``+``.

.. code-block:: python

   from pregex.core.pre import Pregex
   from pregex.core.quantifiers import Optional

   pre = Pregex("a") + Pregex("b") + Optional("c")

   print(pre.get_pattern()) # This prints 'abc?'

This of course works with simple strings as well, as long as there
is at least one Pregex instance involved in the operation:

.. code-block:: python

   from pregex.core.quantifiers import Optional

   pre = "a" + "b" + Optional("c")

   print(pre.get_pattern()) # This prints 'abc?'

Concatenating patterns this way is encouraged as it leads to much more
easy-to-read code.

Repeating patterns with `*`
============================================
:class:`Pregex` has one more overloaded operator, namely the multiplication operator
``*``, which essentially replaces class :class:`~pregex.core.quantifiers.Exactly`.
By using this operator on a Pregex instance, one indicates that a pattern is to be
repeated an exact number of times:

.. code-block:: python

   from pregex.core.pre import Pregex

   pre = 3 * Pregex("a")

   print(pre.get_pattern()) # This prints 'a{3}'

Check out :class:`~pregex.core.pre.Pregex` to learn what other methods this class
has to offer.
