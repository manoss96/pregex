import re as _re
import pregex.core.pre as _pre
import pregex.core.exceptions as _ex


__doc__ = """
This module contains all necessary classes that are used to construct both capturing
and non-capturing groups, as well as any other class that relates to group-related
concepts, such as backreferences and conditionals.

Pattern grouping
-------------------------------------------
In general, one should not have to concern themselves with pattern grouping,
as patterns are automatically wrapped within non-capturing groups whenever this is
deemed necessary. Consider for instance the following code snippet:

.. code-block:: python

   from pregex.core.quantifiers import Optional

   Optional("a").print_pattern() # This prints "a?"
   Optional("aa").print_pattern() # This prints "(?:aa)?"

In the first case, quantifier :class:`~pregex.core.quantifiers.Optional` is applied to the pattern
directly, whereas in the second case the pattern is placed into a non-capturing group
so that "aa" is quantified as a whole. Even so, one can also explicitly construct a
non-capturing group out of any pattern if one wishes to do so by making use of the
:class:`Group` class:

.. code-block:: python

   from pregex.core.groups import Group
   from pregex.core.quantifiers import Optional

   Optional(Group("a")).print_pattern() # This prints "(?:a)?"

Capturing patterns
-------------------------------------------

You'll find however that :class:`Capture` is probably the most important class
of this module, as it is used to create a capturing group out of a pattern,
so that said pattern is also captured separately whenever a match occurs.

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


class __Group(_pre.Pregex):
    '''
    Constitutes the base class for all classes that are part of this module.

    :param Pregex | str pre: A Pregex instance or string representing the pattern \
        that is to be groupped.
    :param (Pregex => str) transform: A `transform` function for the provided pattern.

    :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
        ``Pregex`` instance nor a string.
    '''
    def __init__(self, pre: _pre.Pregex or str, transform) -> _pre.Pregex:
        '''
        Constitutes the base class for all classes that are part of this module.

        :param Pregex | str pre: A Pregex instance or string representing the pattern \
            that is to be groupped.
        :param (Pregex => str) transform: A `transform` function for the provided pattern.

        :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
            ``Pregex`` instance nor a string.
        '''
        pattern = transform(__class__._to_pregex(pre))
        super().__init__(pattern, escape=False)


class Capture(__Group):
    '''
    Creates a capturing group out of the provided pattern.

    :param Pregex | str pre: The pattern out of which the capturing group is created.
    :param str name: The name that is assigned to the captured group for backreference purposes. \
        A value of ``None`` indicates that no name is to be assigned to the group. Defaults to ``None``.

    :raises InvalidArgumentTypeException:
        - Parameter ``pre`` is neither a ``Pregex`` instance nor a string.
        - Parameter ``name`` is neither a string nor ``None``.
    :raises InvalidCapturingGroupNameException: Parameter ``name`` is not a valid \
        capturing-group name. Such name must contain word characters only and start \
        with a non-digit character.

    :note:
        - Creating a capturing group out of a capturing group does nothing to it.
        - Creating a capturing group out of a non-capturing group converts it to a capturing group.
        - Creating a named capturing group out of an unnamed capturing group, assigns a name to it.
        - Creating a named capturing group out of a named capturing group, changes the group's name.
    '''

    def __init__(self, pre: _pre.Pregex or str, name: str = None):
        '''
        Creates a capturing group out of the provided pattern.

        :param Pregex | str pre: The pattern out of which the capturing group is created.
        :param str name: The name that is assigned to the captured group for backreference purposes. \
            A value of ``None`` indicates that no name is to be assigned to the group. Defaults to ``None``.

        :raises InvalidArgumentTypeException:
            - Parameter ``pre`` is neither a ``Pregex`` instance nor a string.
            - Parameter ``name`` is neither a string nor ``None``.
        :raises InvalidCapturingGroupNameException: Parameter ``name`` is not a valid \
            capturing-group name. Such name must contain word characters only and start \
            with a non-digit character.

        :note:
            - Creating a capturing group out of a capturing group does nothing to it.
            - Creating a capturing group out of a non-capturing group converts it to a capturing group.
            - Creating a named capturing group out of an unnamed capturing group, assigns a name to it.
            - Creating a named capturing group out of a named capturing group, changes the group's name.
        '''
        if name is not None:
            if not isinstance(name, str):
                message = "Provided argument \"name\" is not a string."
                raise _ex.InvalidArgumentTypeException(message)
            if _re.fullmatch("[A-Za-z_]\w*", name) is None:
                raise _ex.InvalidCapturingGroupNameException(name)
        super().__init__(pre, lambda pre: pre._capturing_group(name))


class Group(__Group):
    '''
    Creates a non-capturing group out of the provided pattern.

    :param Pregex | str pre: The expression out of which the non-capturing group is created.

    :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
        ``Pregex`` instance nor a string.

    :note:
        - Creating a non-capturing group out of a non-capturing group does nothing to it.
        - Creating a non-capturing group out of a capturing group converts it to a non-capturing group.
    '''

    def __init__(self, pre: _pre.Pregex or str):
        '''
        Creates a non-capturing group out of the provided pattern.

        :param Pregex | str pre: The expression out of which the non-capturing group is created.

        :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
            ``Pregex`` instance nor a string.

        :note:
            - Creating a non-capturing group out of a non-capturing group does nothing to it.
            - Creating a non-capturing group out of a capturing group converts it to a non-capturing group.
        '''
        super().__init__(pre, lambda pre: pre._non_capturing_group())


class Backreference(__Group):
    '''
    Creates a backreference to some previously declared named capturing group.\
    A backreference matches the same text as the text that was most recently \
    matched by the capturing group with the specified name.

    :param str name: The name of the referenced capturing group.

    :raises InvalidArgumentTypeException: Parameter ``name`` is not a string.
    :raises InvalidCapturingGroupNameException: Parameter ``name`` is not a valid \
        capturing-group name. Such name must contain word characters only and start \
        with a non-digit character.
    '''

    def __init__(self, name: str):
        '''
        Creates a backreference to some previously declared named capturing group.\
        A backreference matches the same text as the text that was most recently \
        matched by the capturing group with the specified name.

        :param str name: The name of the referenced capturing group.

        :raises InvalidArgumentTypeException: Parameter ``name`` is not a string.
        :raises InvalidCapturingGroupNameException: Parameter ``name`` is not a valid \
            capturing-group name. Such name must contain word characters only and start \
            with a non-digit character.
        '''
        if not isinstance(name, str):
            message = "Provided argument \"name\" is not a string."
            raise _ex.InvalidArgumentTypeException(message)
        if _re.fullmatch("[A-Za-z_][A-Za-z_0-9]*", name) is None:
            raise _ex.InvalidCapturingGroupNameException(name)
        super().__init__(name, lambda s : f"(?P={s})")

    
class Conditional(__Group):
    '''
    Given the name of a capturing group, matches ``pre1`` only if said capturing group has \
    been previously matched. Furthermore, if a second pattern ``pre2`` is provided, then this \
    pattern is matched in case the referenced capturing group was not matched, though one \
    should be aware that for this to be possible, the referenced capturing group must be optional.

    :param str name: The name of the referenced capturing group.
    :param Pregex | str pre1: The pattern that is to be matched in case condition is true.
    :param Pregex | str pre2: The pattern that is to be matched in case condition is false. \
        Defaults to ``None``.

    :raises InvalidArgumentTypeException:
        - Parameter ``name`` is not a string.
        - Parameter ``pre1`` is neither a ``Pregex`` instance nor a string.
        - Parameter ``pre2`` is neither a ``Pregex`` instance nor a string nor ``None``.
    :raises InvalidCapturingGroupNameException: Parameter ``name`` is not a valid \
        capturing-group name. Such name must contain word characters only and start \
        with a non-digit character.
    '''

    def __init__(self, name: str, pre1: _pre.Pregex or str, pre2: _pre.Pregex or str = None):
        '''
        Given the name of a capturing group, matches ``pre1`` only if said capturing group has \
        been previously matched. Furthermore, if a second pattern ``pre2`` is provided, then this \
        pattern is matched in case the referenced capturing group was not matched, though one \
        should be aware that for this to be possible, the referenced capturing group must be optional.

        :param str name: The name of the referenced capturing group.
        :param Pregex | str pre1: The pattern that is to be matched in case condition is true.
        :param Pregex | str pre2: The pattern that is to be matched in case condition is false. \
            Defaults to ``None``.

        :raises InvalidArgumentTypeException:
            - Parameter ``name`` is not a string.
            - Parameter ``pre1`` is neither a ``Pregex`` instance nor a string.
            - Parameter ``pre2`` is neither a ``Pregex`` instance nor a string nor ``None``.
        :raises InvalidCapturingGroupNameException: Parameter ``name`` is not a valid \
            capturing-group name. Such name must contain word characters only and start \
            with a non-digit character.
        '''
        if not isinstance(name, str):
            message = "Provided argument \"name\" is not a string."
            raise _ex.InvalidArgumentTypeException(message)
        if _re.fullmatch("[A-Za-z_][\w]*", name) is None:
            raise _ex.InvalidCapturingGroupNameException(name)
        super().__init__(name, lambda s: f"(?({s}){pre1}{'|' + str(pre2) if pre2 != None else ''})")