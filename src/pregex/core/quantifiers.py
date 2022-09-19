__doc__ = """
Every class within this module is used to declare that a pattern is to be
matched a number of times, with each class representing a slightly different
pattern-repetition rule.

Classes & methods
-------------------------------------------

Below are listed all classes within :py:mod:`pregex.core.quantifiers`
along with any possible methods they may possess.
"""


import pregex.core.pre as _pre
from typing import Union as _Union
from typing import Optional as _Optional


class __Quantifier(_pre.Pregex):
    '''
    Constitutes the base class for all classes that are part of this module.

    :param Pregex | str pre: A Pregex instance or string representing the pattern \
        that is to be quantified.
    :param (Pregex => str) transform: A `transform` function for the provided pattern.

    :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
        ``Pregex`` instance nor a string.
    :raises CannotBeRepeatedException: Parameter ``pre`` represents a non-repeatable \
        pattern. Whether this exception is thrown also depends on certain parameter values.

    '''
    def __init__(self, pre: _Union[_pre.Pregex, str], is_greedy: bool, transform) -> '__Quantifier':
        '''
        Constitutes the base class for all classes that are part of this module.

        :param Pregex | str pre: A Pregex instance or string representing the pattern \
            that is to be quantified.
        :param (Pregex => str) transform: A `transform` function for the provided pattern.

        :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
            ``Pregex`` instance nor a string.
        :raises CannotBeRepeatedException: Parameter ``pre`` represents a non-repeatable \
            pattern. Whether this exception is thrown also depends on certain parameter values.
        '''
        pattern = transform(__class__._to_pregex(pre), is_greedy)
        super().__init__(str(pattern), escape=False)


class Optional(__Quantifier):
    '''
    Matches the provided pattern once or not at all.

    :param Pregex | str pre: The pattern that is to be quantified.
    :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
        When declared as such, the regex engine will try to match \
        the expression as many times as possible. Defaults to ``True``.

    :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
        ``Pregex`` instance nor a string.
    '''

    def __init__(self, pre: _Union[_pre.Pregex, str], is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern once or not at all.

        :param Pregex | str pre: The pattern that is to be quantified.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.

        :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
            ``Pregex`` instance nor a string.
        '''
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre.optional(is_greedy))


class Indefinite(__Quantifier):
    '''
    Matches the provided pattern zero or more times.

    :param Pregex | str pre: The pattern that is to be quantified.
    :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
        When declared as such, the regex engine will try to match \
        the expression as many times as possible. Defaults to ``True``.

    :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
        ``Pregex`` instance nor a string.
    :raises CannotBeRepeatedException: Parameter ``pre`` represents a non-repeatable pattern.
    '''

    def __init__(self, pre: _Union[_pre.Pregex, str], is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern zero or more times.

        :param Pregex | str pre: The pattern that is to be quantified.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.

        :raises CannotBeRepeatedException: Parameter ``pre`` represents a non-repeatable pattern.
        '''
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre.indefinite(is_greedy))


class OneOrMore(__Quantifier):
    '''
    Matches the provided pattern one or more times.

    :param Pregex | str pre: The pattern that is to be quantified.
    :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
        When declared as such, the regex engine will try to match \
        the expression as many times as possible. Defaults to ``True``.

    :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
        ``Pregex`` instance nor a string.
    :raises CannotBeRepeatedException: Parameter ``pre`` represents a non-repeatable pattern.
    '''

    def __init__(self, pre: _Union[_pre.Pregex, str], is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern one or more times.

        :param Pregex | str pre: The pattern that is to be quantified.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.

        :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
            ``Pregex`` instance nor a string.
        :raises CannotBeRepeatedException: Parameter ``pre`` represents a non-repeatable pattern.
        '''
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre.one_or_more(is_greedy))


class Exactly(__Quantifier):
    '''
    Matches the provided pattern an exact number of times.

    :param Pregex | str pre: The pattern that is to be quantified.
    :param int n: The exact number of times that the provided pattern is to be matched.

    :raises InvalidArgumentTypeException: 
        - Parameter ``pre`` is neither a ``Pregex`` instance nor a string.
        - Parameter ``n`` is not an integer.
    :raises InvalidArgumentValueException: Parameter ``n`` has a value of less than zero.
    :raises CannotBeRepeatedException: Parameter ``pre`` represents a non-repeatable \
        pattern while parameter ``n`` has been set to a value of greater than ``1``.
    '''

    def __init__(self, pre: _Union[_pre.Pregex, str], n: int) -> _pre.Pregex:
        '''
        Matches the provided pattern an exact number of times.

        :param Pregex | str pre: The pattern that is to be quantified.
        :param int n: The exact number of times that the provided pattern is to be matched.

        :raises InvalidArgumentTypeException: 
            - Parameter ``pre`` is neither a ``Pregex`` instance nor a string.
            - Parameter ``n`` is not an integer.
        :raises InvalidArgumentValueException: Parameter ``n`` has a value of less than zero.
        :raises CannotBeRepeatedException: Parameter ``pre`` represents a non-repeatable \
            pattern while parameter ``n`` has been set to a value of greater than ``1``.
        '''
        super().__init__(pre, False, lambda pre, _: pre.exactly(n))


class AtLeast(__Quantifier):
    '''
    Matches the provided pattern a minimum number of times.

    :param Pregex | str pre: The pattern that is to be quantified.
    :param int n: The minimum number of times that the provided pattern is to be matched.
    :param bool is_greedy: Determines whether to declare this quantifier as greedy. \
        When declared as such, the regex engine will try to match \
        the expression as many times as possible. Defaults to ``True``.

    :raises InvalidArgumentTypeException: 
        - Parameter ``pre`` is neither a ``Pregex`` instance nor a string.
        - Parameter ``n`` is not an integer.
    :raises InvalidArgumentValueException: Parameter ``n`` has a value of less than zero.
    :raises CannotBeRepeatedException: Parameter ``pre`` represents a non-repeatable pattern.
    '''

    def __init__(self, pre: _Union[_pre.Pregex, str], n: int, is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern a minimum number of times.

        :param Pregex | str pre: The pattern that is to be quantified.
        :param int n: The minimum number of times that the provided pattern is to be matched.
        :param bool is_greedy: Determines whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.

        :raises InvalidArgumentTypeException: 
            - Parameter ``pre`` is neither a ``Pregex`` instance nor a string.
            - Parameter ``n`` is not an integer.
        :raises InvalidArgumentValueException: Parameter ``n`` has a value of less than zero.
        :raises CannotBeRepeatedException: Parameter ``pre`` represents a non-repeatable pattern.
        '''
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre.at_least(n, is_greedy))


class AtMost(__Quantifier):
    '''
    Matches the provided pattern up to a maximum number of times.

    :param Pregex | str pre: The pattern that is to be quantified.
    :param int n: The maximum number of times that the provided pattern is to be matched.
    :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
        When declared as such, the regex engine will try to match \
        the expression as many times as possible. Defaults to ``True``.

    :raises InvalidArgumentTypeException: 
        - Parameter ``pre`` is neither a ``Pregex`` instance nor a string.
        - Parameter ``n`` is neither an integer nor ``None``.
    :raises InvalidArgumentValueException: Parameter ``n`` has a value of less than zero.
    :raises CannotBeRepeatedException: Parameter ``pre`` represents a non-repeatable \
        pattern while parameter ``n`` has been set to a value of greater than ``1``.

    :note: Setting ``n`` equal to ``None`` indicates that there is no upper limit to the number of \
        times the pattern is to be repeated.
    '''

    def __init__(self, pre: _Union[_pre.Pregex, str], n: _Optional[int], is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern up to a maximum number of times.

        :param Pregex | str pre: The pattern that is to be quantified.
        :param int n: The maximum number of times that the provided pattern is to be matched.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.

        :raises InvalidArgumentTypeException: 
            - Parameter ``pre`` is neither a ``Pregex`` instance nor a string.
            - Parameter ``n`` is neither an integer nor ``None``.
        :raises InvalidArgumentValueException: Parameter ``n`` has a value of less than zero.
        :raises CannotBeRepeatedException: Parameter ``pre`` represents a non-repeatable \
        pattern while parameter ``n`` has been set to a value of greater than ``1``.

        :note: Setting ``n`` equal to ``None`` indicates that there is no upper limit to the number of \
            times the pattern is to be repeated.
        '''
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre.at_most(n, is_greedy))


class AtLeastAtMost(__Quantifier):
    '''
    Matches the provided expression between a minimum and a maximum number of times.

    :param Pregex | str pre: The pattern that is to be quantified.
    :param int n: The minimum number of times that the provided pattern is to be matched.
    :param int m: The maximum number of times that the provided pattern is to be matched.
    :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
        When declared as such, the regex engine will try to match \
        the expression as many times as possible. Defaults to ``True``.

    :raises InvalidArgumentTypeException: 
        - Parameter ``pre`` is neither a ``Pregex`` instance nor a string.
        - Parameter ``n`` is not an integer.
        - Parameter ``m`` is neither an integer nor ``None``.
    :raises InvalidArgumentValueException:
        - Either parameter ``n`` or ``m`` has a value of less than zero.
        - Parameter ``n`` has a greater value than that of parameter ``m``.
    :raises CannotBeRepeatedException: Parameter ``pre`` represents a non-repeatable \
        pattern while parameter ``m`` has been set to a value of greater than ``1``.

    :note: 
        - Parameter ``is_greedy`` has no effect in the case that ``n`` equals ``m``.
        - Setting ``m`` equal to ``None`` indicates that there is no upper limit to the \
            number of times the pattern is to be repeated.
    '''

    def __init__(self, pre: _Union[_pre.Pregex, str], n: int, m: _Optional[int], is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided expression between a minimum and a maximum number of times.

        :param Pregex | str pre: The pattern that is to be quantified.
        :param int n: The minimum number of times that the provided pattern is to be matched.
        :param int m: The maximum number of times that the provided pattern is to be matched.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.

        :raises InvalidArgumentTypeException: 
            - Parameter ``pre`` is neither a ``Pregex`` instance nor a string.
            - Parameter ``n`` is not an integer.
            - Parameter ``m`` is neither an integer nor ``None``.
        :raises InvalidArgumentValueException:
            - Either parameter ``n`` or ``m`` has a value of less than zero.
            - Parameter ``n`` has a greater value than that of parameter ``m``.
        :raises CannotBeRepeatedException: Parameter ``pre`` represents a non-repeatable \
            pattern while parameter ``m`` has been set to a value of greater than ``1``.

        :note: 
            - Parameter ``is_greedy`` has no effect in the case that ``n`` equals ``m``.
            - Setting ``m`` equal to ``None`` indicates that there is no upper limit to the \
                number of times the pattern is to be repeated.
        '''
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre.at_least_at_most(n, m, is_greedy))