###############
Best Practices
###############

This page discusses the best practices that one should
consider following when it comes to using pregex.

Importing
==========

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
  * Class :class:`pregex.core.pre.Pregex` is imported as is.

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


Maintaining readability
=========================

One of the primary benefits of using PRegEx is being able to construct patterns
that are readable, and therefore easier to maintain and update than their
raw RegEx counterparts. This is mainly made possible through PRegEx's human-friendly
syntax. Nevertheless, there exist certain cases where the syntax on its own is not
enough to achieve readability, especially when it comes to building
complex patterns. Consider for example the following Pregex instance:

.. code-block:: python

  from pregex.core import *

  pre: Pregex = \
      op.Enclose(
          op.Either(
              asr.FollowedBy(
                  asr.PrecededBy(
                      qu.OneOrMore(op.Either('+', '-')),
                      2 * (cl.AnyLetter() | (cl.AnyPunctuation() - cl.AnyFrom('+', '-')))
                  ),
                  2 * (cl.AnyLetter() | (cl.AnyPunctuation() - cl.AnyFrom('+', '-')))
              ),
              asr.NotPrecededBy(
                  asr.FollowedBy(
                      qu.OneOrMore(op.Either('+', '-')),
                      2 * cl.AnyDigit()
                  ),
                  op.Either(cl.Any() + AnyDigit(), cl.AnyDigit() + cl.Any())
              ),
              asr.NotFollowedBy(
                  asr.PrecededBy(
                      qu.OneOrMore(op.Either('+', '-')),
                      2 * cl.AnyDigit()
                  ),
                  op.Either(cl.Any() + AnyDigit(), cl.AnyDigit() + cl.Any())
              )
          ),
          2 * (cl.AnyDigit | cl.AnyLetter() | (cl.AnyPunctuation() - cl.AnyFrom('+', '-')))
      )

And this is the RegEx pattern to which the above Pregex instance compiles:

.. code-block::

  [,.-~!-*]{2}(?:(?<=[.-\/,!-*:-~]{2})(?:\+|-)+(?=[.-\/,!-*:-~]{2})|(?<!.\d|\d.)(?:\+|-)+(?=\d{2})|(?<=\d{2})(?:\+|-)+(?!.\d|\d.))[,.-~!-*]{2}

Although it could be argued that this pattern can be more easily
studied while in its Pregex form, at least by people who are not entirely
familiar with RegEx's syntax, it is still not quite clear what it's purpose
is. By following a different pattern-building approach, we are going to
slightly modify the above Pregex instance so that it is a lot more easy
to read, without messing with the underlying RegEx pattern.


Breaking down a pattern
--------------------------
If a pattern is overly complex, one might like to try breaking it down
into simpler subpatterns which can then be stored in variables with
meaningful names. Considering our example above, we can search for any
repeated subpatterns throughout the main pattern and substitute them
with such variables. Furthermore, we are going to replace operator 
:class:`~pregex.core.operators.Enclose` by simply concatenating
the *enclosing* pattern at both the start and the end of the *enclosed* pattern,
as, despite the operator succeeding in making the pattern shorter to write,
it adds an additional layer of nestedness, which we would like to eliminate:

.. code-block:: python

  from pregex.core import *

  one_or_more_signs = qu.OneOrMore(op.Either('+', '-'))

  any_punct_but_signs = cl.AnyPunctuation() - cl.AnyFrom('+', '-')

  any_two_letters_or_punct_but_signs = 2 * (cl.AnyLetter() | any_punct_but_signs)

  any_two_digits = 2 * cl.AnyDigit()

  any_two_char_sequence_containing_digits = op.Either(cl.Any() + AnyDigit(), cl.AnyDigit() + cl.Any())

  any_two_alphanums_or_punct_but_signs = 2 * (cl.AnyDigit() | cl.AnyLetter() | any_punct_but_signs)


  pre: Pregex = \
      any_two_alphanums_or_punct_but_signs + \
      op.Either(
          asr.PrecededBy(
              asr.FollowedBy(
                  one_or_more_signs,
                  any_two_letters_or_punct_but_signs
              ),
              any_two_letters_or_punct_but_signs
          ),
          asr.NotPrecededBy(
              asr.FollowedBy(
                  one_or_more_signs,
                  any_two_digits
              ),
              any_two_char_sequence_containing_digits
          ),
          asr.NotFollowedBy(
              asr.PrecededBy(
                  one_or_more_signs,
                  any_two_digits
                ),
              any_two_char_sequence_containing_digits
          )
      ) + \
      any_two_alphanums_or_punct_but_signs

This new form certainly looks less overwhelming that it did before,
though there is still room for improvement.

Utilizing pattern chaining
--------------------------
In `Pattern chaining <covering-the-basics.html#pattern-chaining>`_ we saw an alternative way
of building patterns, which in certain cases is to be preferred over the standard API,
and it just so happens that lookarounds constitute one of these cases. Here's what our pattern
looks like when we apply the pattern chaining technique in order to impose any lookaround
assertions:


.. code-block:: python

  from pregex.core import *

  one_or_more_signs = qu.OneOrMore(op.Either('+', '-'))

  any_punct_but_signs = cl.AnyPunctuation() - cl.AnyFrom('+', '-')

  any_two_letters_or_punct_but_signs = 2 * (cl.AnyLetter() | any_punct_but_signs)

  any_two_digits = 2 * cl.AnyDigit()

  any_two_char_sequence_containing_digits = op.Either(cl.Any() + AnyDigit(), cl.AnyDigit() + cl.Any())

  any_two_alphanums_or_punct_but_signs = 2 * (cl.AnyDigit() | cl.AnyLetter() | any_punct_but_signs)


  pre: Pregex = \
      any_two_alphanums_or_punct_but_signs + \
      op.Either(
          one_or_more_signs \
              .preceded_by(any_two_letters_or_punct_but_signs) \
              .followed_by(any_two_letters_or_punct_but_signs),
          one_or_more_signs \
              .followed_by(any_two_digits) \
              .not_preceded_by(any_two_char_sequence_containing_digits) \
          one_or_more_signs  \
              .preceded_by(any_two_digits) \
              .not_followed_by(any_two_char_sequence_containing_digits)
      ) + \
      any_two_alphanums_or_punct_but_signs

Having tinkered with the pattern-building process by incorporating what was discussed,
it is now a lot more clear what this pattern is trying to match, which is any sequence
of signs ``+`` and ``-`` that is both preceded and followed by any two-character sequence
of letters, digits and punctuation marks except for ``+`` and ``-``, as long as any digits
that appear within a possible match are:

1. Found exclusively either to the left or to the right of the sign sequence.
2. Occupy the whole two-character sequence.

To give a concrete example, this pattern will match strings like ``a!+#c``, ``a!--12``
and ``12+-+a#``, but it won't work for strings like ``a!#$f``, ``a!+#3`` and ``1!-a#``.

Having read all the above, try adopting these practices yourself when building
patterns with PRegEx so you make the most out of it!
