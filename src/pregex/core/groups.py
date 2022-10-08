__doc__ = """
This module contains all necessary classes that are used to construct both
capturing and non-capturing groups, as well as any other classes which relate
to concepts that are based on groups, such as backreferences and conditionals.

Pattern grouping
-------------------------------------------
In general, one should not have to concern themselves with pattern grouping,
as patterns are automatically wrapped within non-capturing groups whenever this is
deemed necessary. Consider for instance the following code snippet:

.. code-block:: python

   from pregex.core.quantifiers import Optional

   Optional('a').print_pattern() # This prints "a?"
   Optional('aa').print_pattern() # This prints "(?:aa)?"

In the first case, quantifier :class:`~pregex.core.quantifiers.Optional` is applied to
the pattern directly, whereas in the second case the pattern is placed into a non-capturing
group so that "aa" is quantified as a whole. Be that as it may, there exists a separate class,
namely :class:`Group`, through which one is able to explicitly wrap any pattern within
a non-capturing group if they wish to do so:

.. code-block:: python

   from pregex.core.groups import Group
   from pregex.core.quantifiers import Optional

   pre = Group(Optional('a'))

   pre.print_pattern() # This prints "(?:a)?"

This class can also be used so as to apply various RegEx flags, also known \
as *modifiers*, to a pattern. As of yet, the only flag that is supported is
the case-insensitive flag ``i``:

.. code-block:: python

   from pregex.core.groups import Group

   pre = Group('pregex', is_case_insensitive=True)

   # This statement is "True"
   pre.is_exact_match('PRegEx')


Capturing patterns
-------------------------------------------

You'll find however that :class:`Capture` is probably the most important class
of this module, as it is used to create a capturing group out of a pattern,
so that said pattern is captured separately whenever a match occurs.

.. code-block:: python

   from pregex.core.groups import Capture
   from pregex.core.classes import AnyLetter

   pre = AnyLetter() + Capture(2 * AnyLetter())

   text = "abc def"
   print(pre.get_matches(text)) # This prints "['abc', 'def']"
   print(pre.get_captures(text)) # This prints "[('bc'), ('ef')]"

As you can see, capturing is a very useful tool for whenever you are
interested in isolating some specific part of a pattern.

Classes & methods
-------------------------------------------

Below are listed all classes within :py:mod:`pregex.core.groups`
along with any possible methods they may possess.
"""


import re as _re
import pregex.core.pre as _pre
import pregex.core.exceptions as _ex
from typing import Union as _Union
from typing import Optional as _Optional


class __Group(_pre.Pregex):
    '''
    Constitutes the base class for all classes that are part of this module.

    :param Pregex | str pre: A Pregex instance or string representing the pattern \
        that is to be groupped.
    :param (Pregex => str) transform: A `transform` function for the provided pattern.

    :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
        ``Pregex`` instance nor a string.
    '''
    def __init__(self, pre: _Union[_pre.Pregex, str], transform) -> _pre.Pregex:
        '''
        Constitutes the base class for all classes that are part of this module.

        :param Pregex | str pre: A Pregex instance or string representing the pattern \
            that is to be groupped.
        :param (Pregex => str) transform: A `transform` function for the provided pattern.

        :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
            ``Pregex`` instance nor a string.
        '''
        pattern = transform(__class__._to_pregex(pre))
        super().__init__(str(pattern), escape=False)


class Capture(__Group):
    '''
    Creates a capturing group out of the provided pattern.

    :param Pregex | str pre: The pattern out of which the capturing group is created.
    :param str name: The name that is assigned to the captured group \
        for backreference purposes. A value of ``None`` indicates that no name \
        is to be assigned to the group. Defaults to ``None``.

    :raises InvalidArgumentTypeException:
        - Parameter ``pre`` is neither a ``Pregex`` instance nor a string.
        - Parameter ``name`` is neither a string nor ``None``.
    :raises InvalidCapturingGroupNameException: Parameter ``name`` is not a valid \
        capturing group name. Such name must contain word characters only and start \
        with a non-digit character.

    :note:
        - Creating a capturing group out of a capturing group does nothing to it.
        - Creating a capturing group out of a non-capturing group converts it \
            into a capturing group, except if any flags have been applied to it, \
            in which case, the non-capturing group is wrapped within a capturing \
            group as a whole.
        - Creating a named capturing group out of an unnamed capturing group, \
          assigns a name to it.
        - Creating a named capturing group out of a named capturing group, \
          changes the group's name.
    '''

    def __init__(self, pre: _Union[_pre.Pregex, str], name: _Optional[str] = None):
        '''
        Creates a capturing group out of the provided pattern.

        :param Pregex | str pre: The pattern that is to be wrapped \
            within a capturing group.
        :param str name: The name that is assigned to the captured group \
            for backreference purposes. A value of ``None`` indicates that no name \
            is to be assigned to the group. Defaults to ``None``.

        :raises InvalidArgumentTypeException:
            - Parameter ``pre`` is neither a ``Pregex`` instance nor a string.
            - Parameter ``name`` is neither a string nor ``None``.
        :raises InvalidCapturingGroupNameException: Parameter ``name`` is not a valid \
            capturing group name. Such name must contain word characters only and start \
            with a non-digit character.

        :note:
            - Creating a capturing group out of a capturing group does nothing to.
            - Creating a capturing group out of a non-capturing group converts it \
              into a capturing group, except if any flags have been applied to it, \
              in which case, the non-capturing group is wrapped within a capturing \
              group as a whole.
            - Creating a named capturing group out of an unnamed capturing group, \
              assigns a name to it.
            - Creating a named capturing group out of a named capturing group, \
              changes the group's name.
        '''
        super().__init__(pre, lambda pre: pre.capture(name))


class Group(__Group):
    '''
    Creates a non-capturing group out of the provided pattern.

    :param Pregex | str pre: The pattern that is to be wrapped \
        within a non-capturing group.
    :param bool is_case_insensitive: If ``True``, then the "case insensitive" \
        flag is applied to the group so that the pattern within it ignores case \
        when it comes to matching. Defaults to ``False``.

    :raises InvalidArgumentTypeException: Parameter ``pre`` is neither \
        a ``Pregex`` instance nor a string.

    :note:
        - Creating a non-capturing group out of a non-capturing group does nothing, \
          except for remove its flags if it has any.
        - Creating a non-capturing group out of a capturing group converts it into \
          a non-capturing group.
    '''

    def __init__(self, pre: _Union[_pre.Pregex, str], is_case_insensitive: bool = False):
        '''
        Creates a non-capturing group out of the provided pattern.

        :param Pregex | str pre: The pattern that is to be wrapped \
            within a non-capturing group.
        :param bool is_case_insensitive: If ``True``, then the "case insensitive" \
            flag is applied to the group so that the pattern within it ignores case \
            when it comes to matching. Defaults to ``False``.

        :raises InvalidArgumentTypeException: Parameter ``pre`` is neither \
            a ``Pregex`` instance nor a string.

        :note:
            - Creating a non-capturing group out of a non-capturing group does nothing, \
              except for remove its flags if it has any.
            - Creating a non-capturing group out of a capturing group converts it into \
            a non-capturing group.
        '''
        super().__init__(pre, lambda pre: pre.group(is_case_insensitive))


class Backreference(__Group):
    '''
    Creates a backreference to some previously declared capturing group.

    :param int | str ref: A reference to some previously declared capturing group. \
        This parameter can either be an integer, in which case the capturing group \
        is referenced by order, or a string, in which case the capturing group is \
        referenced by name.

    :raises InvalidArgumentTypeException: Parameter ``ref`` is neither an integer \
        nor a string.
    :raises InvalidArgumentValueException: Parameter ``ref`` is an integer but \
        has a value of either less than ``1`` or greater than ``10``.
    :raises InvalidCapturingGroupNameException: Parameter ``ref`` is a string but \
        not a valid capturing group name. Such name must contain word characters \
        only and start with a non-digit character.
    '''

    def __init__(self, ref: _Union[int, str]):
        '''
        Creates a backreference to some previously declared capturing group.

        :param int | str ref: A reference to some previously declared capturing group. \
            This parameter can either be an integer, in which case the capturing group \
            is referenced by order, or a string, in which case the capturing group is \
            referenced by name.

        :raises InvalidArgumentTypeException: Parameter ``ref`` is neither an integer \
            nor a string.
        :raises InvalidArgumentValueException: Parameter ``ref`` is an integer but \
            has a value of either less than ``1`` or greater than ``10``.
        :raises InvalidCapturingGroupNameException: Parameter ``ref`` is a string but \
            not a valid capturing group name. Such name must contain word characters \
            only and start with a non-digit character.
        '''
        if isinstance(ref, int):
            if isinstance(ref, bool):
                message = "Parameter \"ref\" is neither an integer nor a string."
                raise _ex.InvalidArgumentTypeException(message)
            if ref < 1 or ref > 99:
                message = "Parameter \"ref\" cannot be less than 1 or greater than 99."
                raise _ex.InvalidArgumentValueException(message)
            transform = lambda s : f"\\{s}"
        elif isinstance(ref, str):
            if _re.fullmatch("[A-Za-z_][A-Za-z_0-9]*", ref) is None:
                raise _ex.InvalidCapturingGroupNameException(ref)
            transform = lambda s : f"(?P={s})"
        else:
            message = "Parameter \"ref\" is neither an integer nor a string."
            raise _ex.InvalidArgumentTypeException(message)
        super().__init__(str(ref), transform)

    
class Conditional(__Group):
    '''
    Given the name of a capturing group, matches ``pre1`` only if said capturing group has \
    been previously matched. Furthermore, if a second pattern ``pre2`` is provided, then \
    this pattern is matched in case the referenced capturing group was not, though one \
    should be aware that for this to be possible, the referenced capturing group must \
    be optional.

    :param str name: The name of the referenced capturing group.
    :param Pregex | str pre1: The pattern that is to be matched in case condition is true.
    :param Pregex | str pre2: The pattern that is to be matched in case condition \
        is false. Defaults to ``None``.

    :raises InvalidArgumentTypeException:
        - Parameter ``name`` is not a string.
        - Parameter ``pre1`` is neither a ``Pregex`` instance nor a string.
        - Parameter ``pre2`` is neither a ``Pregex`` instance nor a string nor ``None``.
    :raises InvalidCapturingGroupNameException: Parameter ``name`` is not a valid \
        capturing group name. Such name must contain word characters only and start \
        with a non-digit character.
    '''

    def __init__(self, name: str, pre1: _Union[_pre.Pregex, str], pre2: _Optional[_Union[_pre.Pregex, str]] = None):
        '''
        Given the name of a capturing group, matches ``pre1`` only if said capturing group has \
        been previously matched. Furthermore, if a second pattern ``pre2`` is provided, then \
        this pattern is matched in case the referenced capturing group was not, though one \
        should be aware that for this to be possible, the referenced capturing group must \
        be optional.

        :param str name: The name of the referenced capturing group.
        :param Pregex | str pre1: The pattern that is to be matched in case condition is true.
        :param Pregex | str pre2: The pattern that is to be matched in case condition \
            is false. Defaults to ``None``.

        :raises InvalidArgumentTypeException:
            - Parameter ``name`` is not a string.
            - Parameter ``pre1`` is neither a ``Pregex`` instance nor a string.
            - Parameter ``pre2`` is neither a ``Pregex`` instance nor a string nor ``None``.
        :raises InvalidCapturingGroupNameException: Parameter ``name`` is not a valid \
            capturing group name. Such name must contain word characters only and start \
            with a non-digit character.
        '''
        if not isinstance(name, str):
            message = "Provided argument \"name\" is not a string."
            raise _ex.InvalidArgumentTypeException(message)
        if _re.fullmatch("[A-Za-z_][\w]*", name) is None:
            raise _ex.InvalidCapturingGroupNameException(name)
        super().__init__(name, lambda s: f"(?({s}){pre1}{'|' + str(pre2) if pre2 != None else ''})")