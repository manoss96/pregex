import pregex.pre as _pre
import pregex.exceptions as _ex


__doc__ = """
Every class within this module is used to declare that a pattern is to be
matched a number of times, with each class representing a slightly different
pattern-repetition rule.

Classes & methods
-------------------------------------------

Below are listed all classes within :py:mod:`pregex.quantifiers`
along with any possible methods they may possess.
"""


class __Quantifier(_pre.Pregex):
    '''
    Constitutes the base class for all classes that are part of this module.

    :param Pregex | str pre: A Pregex instance or string representing the pattern \
        that is to be quantified.
    :param (Pregex => str) transform: A `transform` function for the provided pattern.

    :raises CannotBeQuantifiedException: ``self`` is not an instance of class ``Optional`` and \
        the provided pattern represents an "assertion".
    '''
    def __init__(self, pre: _pre.Pregex or str, is_greedy: bool, transform) -> '__Quantifier':
        '''
        Constitutes the base class for all classes that are part of this module.

        :param Pregex | str pre: A Pregex instance or string representing the pattern \
            that is to be quantified.
        :param (Pregex => str) transform: A `transform` function for the provided pattern.

        :raises CannotBeQuantifiedException: ``self`` is not an instance of class ``Optional`` and \
            the provided pattern represents an "assertion".
        '''
        if (not isinstance(self, Optional)) and issubclass(pre.__class__, _pre.Pregex) \
            and pre._get_type() == _pre._Type.Assertion:
            raise _ex.CannotBeQuantifiedException(pre)
        pattern = transform(__class__._to_pregex(pre), is_greedy)
        super().__init__(pattern, escape=False)


class Optional(__Quantifier):
    '''
    Matches the provided pattern once or not at all.

    :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
        or wrapped within a ``Pregex`` subtype instance.
    :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
        When declared as such, the regex engine will try to match \
        the expression as many times as possible. Defaults to ``True``.
    '''

    def __init__(self, pre: _pre.Pregex or str, is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern once or not at all.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a ``Pregex`` subtype instance.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.
        '''
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre._optional(is_greedy))


class Indefinite(__Quantifier):
    '''
    Matches the provided pattern zero or more times.

    :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
        or wrapped within a ``Pregex`` subtype instance.
    :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
        When declared as such, the regex engine will try to match \
        the expression as many times as possible. Defaults to ``True``.

    :raises CannotBeQuantifiedException: This class is applied to an "assertion" pattern.
    '''

    def __init__(self, pre: _pre.Pregex or str, is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern zero or more times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a ``Pregex`` subtype instance.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.

        :raises CannotBeQuantifiedException: This class is applied to an "assertion" pattern.
        '''
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre._indefinite(is_greedy))


class OneOrMore(__Quantifier):
    '''
    Matches the provided pattern one or more times.

    :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
        or wrapped within a ``Pregex`` subtype instance.
    :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
        When declared as such, the regex engine will try to match \
        the expression as many times as possible. Defaults to ``True``.

    :raises CannotBeQuantifiedException: This class is applied to an "assertion" pattern.
    '''

    def __init__(self, pre: _pre.Pregex or str, is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern one or more times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a ``Pregex`` subtype instance.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.

        :raises CannotBeQuantifiedException: This class is applied to an "assertion" pattern.
        '''
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre._one_or_more(is_greedy))


class Exactly(__Quantifier):
    '''
    Matches the provided pattern an exact number of times.

    :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
        or wrapped within a ``Pregex`` subtype instance.
    :param int n: The exact number of times that the provided pattern is to be matched.

    :raises InvalidArgumentTypeException: Parameter ``n`` is not an integer.
    :raises InvalidArgumentValueException: Parameter ``n`` is less than zero.
    :raises CannotBeQuantifiedException: This class is applied to an "assertion" pattern.
    '''

    def __init__(self, pre: _pre.Pregex or str, n: int) -> _pre.Pregex:
        '''
        Matches the provided pattern an exact number of times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a ``Pregex`` subtype instance.
        :param int n: The exact number of times that the provided pattern is to be matched.

        :raises InvalidArgumentTypeException: Parameter ``n`` is not an integer.
        :raises InvalidArgumentValueException: Parameter ``n`` is less than zero.
        :raises CannotBeQuantifiedException: This class is applied to an "assertion" pattern.
        '''
        if not isinstance(n, int) or isinstance(n, bool):
            message = "Provided argument \"n\" is not an integer."
            raise _ex.InvalidArgumentTypeException(message)
        if n < 0:
            message = "Parameter \"n\" isn't allowed to be negative."
            raise _ex.InvalidArgumentValueException(message)
        super().__init__(pre, False, lambda pre, _: pre._exactly(n))


class AtLeast(__Quantifier):
    '''
    Matches the provided pattern a minimum number of times.

    :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
        or wrapped within a ``Pregex`` subtype instance.
    :param int n: The minimum number of times that the provided pattern is to be matched.
    :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
        When declared as such, the regex engine will try to match \
        the expression as many times as possible. Defaults to ``True``.

    :raises InvalidArgumentTypeException: Parameter ``n`` is not an integer.
    :raises InvalidArgumentValueException: Parameter ``n`` is less than zero.
    :raises CannotBeQuantifiedException: This class is applied to an "assertion" pattern.
    '''

    def __init__(self, pre: _pre.Pregex or str, n: int, is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern a minimum number of times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a ``Pregex`` subtype instance.
        :param int n: The minimum number of times that the provided pattern is to be matched.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.

        :raises InvalidArgumentTypeException: Parameter ``n`` is not an integer.
        :raises InvalidArgumentValueException: Parameter ``n`` is less than zero.
        :raises CannotBeQuantifiedException: This class is applied to an "assertion" pattern.
        '''
        if not isinstance(n, int) or isinstance(n, bool):
            message = "Provided argument \"n\" is not an integer."
            raise _ex.InvalidArgumentTypeException(message)
        if n < 0:
            message = "Parameter \"n\" isn't allowed to be negative."
            raise _ex.InvalidArgumentValueException(message)
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre._at_least(n, is_greedy))


class AtMost(__Quantifier):
    '''
    Matches the provided pattern a maximum number of times.

    :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
        or wrapped within a ``Pregex`` subtype instance.
    :param int n | None: The maximum number of times that the provided pattern is to be matched.
    :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
        When declared as such, the regex engine will try to match \
        the expression as many times as possible. Defaults to ``True``.

    :raises InvalidArgumentTypeException: Parameter ``n`` is not an integer.
    :raises InvalidArgumentValueException: Parameter ``n`` is less than zero.
    :raises CannotBeQuantifiedException: This class is applied to an "assertion" pattern.

    :note: Setting ``n`` equal to ``None`` indicates that there is no upper limit to the number of \
        times the pattern is to be repeated.
    '''

    def __init__(self, pre: _pre.Pregex or str, n: int, is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern a maximum number of times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a ``Pregex`` subtype instance.
        :param int n | None: The maximum number of times that the provided pattern is to be matched.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.

        :raises InvalidArgumentTypeException: Parameter ``n`` is not an integer.
        :raises InvalidArgumentValueException: Parameter ``n`` is less than zero.
        :raises CannotBeQuantifiedException: This class is applied to an "assertion" pattern.

        :note: Setting ``n`` equal to ``None`` indicates that there is no upper limit to the number of \
            times the pattern is to be repeated.
        '''
        if not isinstance(n, int) or isinstance(n, bool):
            if n is not None:
                message = "Provided argument \"n\" is neither an integer nor \"None\"."
                raise _ex.InvalidArgumentTypeException(message)
        elif n < 0:
            message = "Parameter \"n\" isn't allowed to be negative."
            raise _ex.InvalidArgumentValueException(message)
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre._at_most(n, is_greedy))


class AtLeastAtMost(__Quantifier):
    '''
    Matches the provided expression between a minimum and a maximum number of times.

    :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
        or wrapped within a ``Pregex`` subtype instance.
    :param int min: The minimum number of times that the provided pattern is to be matched.
    :param int | None max: The maximum number of times that the provided pattern is to be matched.
    :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
        When declared as such, the regex engine will try to match \
        the expression as many times as possible. Defaults to ``True``.

    :raises InvalidArgumentTypeException: Either one of parameters ``min`` or ``max`` is not an integer.
    :raises InvalidArgumentValueException: Either parameter ``min`` or ``max`` is less than zero, \
        or parameter ``min`` has a greater value than parameter ``max``.
    :raises CannotBeQuantifiedException: This class is applied to an "assertion" pattern.

    :note: 
        - Parameter ``is_greedy`` has no effect in the case that ``min`` equals ``max``.
        - Setting ``max`` equal to ``None`` indicates that there is no upper limit to the number of \
            times the pattern is to be repeated.
    '''

    def __init__(self, pre: _pre.Pregex or str, min: int, max: int, is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided expression between a minimum and a maximum number of times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a ``Pregex`` subtype instance.
        :param int min: The minimum number of times that the provided pattern is to be matched.
        :param int | None max: The maximum number of times that the provided pattern is to be matched.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.

        :raises InvalidArgumentTypeException: Either one of parameters ``min`` or ``max`` is not an integer.
        :raises InvalidArgumentValueException: Either parameter ``min`` or ``max`` is less than zero, \
            or parameter ``min`` has a greater value than parameter ``max``.
        :raises CannotBeQuantifiedException: This class is applied to an "assertion" pattern.

        :note: 
            - Parameter ``is_greedy`` has no effect in the case that ``min`` equals ``max``.
            - Setting ``max`` equal to ``None`` indicates that there is no upper limit to the number of \
                times the pattern is to be repeated.
        '''
        if not isinstance(min, int) or isinstance(min, bool):
            message = "Provided argument \"min\" is not an integer."
            raise _ex.InvalidArgumentTypeException(message)
        elif min < 0:
            message = "Parameter \"min\" isn't allowed to be negative."
            raise _ex.InvalidArgumentValueException(message)
        elif not isinstance(max, int) or isinstance(max, bool):
            if max is not None:
                message = "Provided argument \"max\" is neither an integer nor \"None\"."
                raise _ex.InvalidArgumentTypeException(message)
        elif max < 0:
            message = "Parameter \"max\" isn't allowed to be negative."
            raise _ex.InvalidArgumentValueException(message)
        elif max < min:
            message = "The value of parameter \"max\" isn't allowed to be"
            message += " less than the value of parameter \"min\"."
            raise _ex.InvalidArgumentValueException(message)
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre._at_least_at_most(min, max, is_greedy))