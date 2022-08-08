import pregex.pre as _pre
import pregex.exceptions as _exceptions


class __Quantifier(_pre.Pregex):
    '''
    Constitutes the base class for every class within "quantifiers.py".

    :raises CannotBeQuantifiedException: This class is applied to an instance that represents an "assertion" pattern.
    '''
    def __init__(self, pre: _pre.Pregex or str, is_greedy: bool, transform) -> '__Quantifier':
        if (not isinstance(self, Optional)) and issubclass(pre.__class__, _pre.Pregex) and pre._get_type() == _pre._Type.Assertion:
            raise _exceptions.CannotBeQuantifiedException(pre)
        pattern = transform(__class__._to_pregex(pre), is_greedy)
        super().__init__(pattern, escape=False)


class Optional(__Quantifier):
    '''
    Matches the provided pattern once or not at all.

    :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
        or wrapped within a "Pregex" subtype instance.
    :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
        When declared as such, the regex engine will try to match \
        the expression as many times as possible. Defaults to 'True'.

    :raises CannotBeQuantifiedException: This class is applied to an instance that represents an "assertion" pattern.
    '''

    def __init__(self, pre: _pre.Pregex or str, is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern once or not at all.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a "Pregex" subtype instance.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to 'True'.

        :raises CannotBeQuantifiedException: This class is applied to an instance that represents an "assertion" pattern.
        '''
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre._optional(is_greedy))


class Indefinite(__Quantifier):
    '''
    Matches the provided pattern zero or more times.

    :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
        or wrapped within a "Pregex" subtype instance.
    :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
        When declared as such, the regex engine will try to match \
        the expression as many times as possible. Defaults to 'True'.

    :raises CannotBeQuantifiedException: This class is applied to an instance that represents an "assertion" pattern.
    '''

    def __init__(self, pre: _pre.Pregex or str, is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern zero or more times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a "Pregex" subtype instance.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to 'True'.

        :raises CannotBeQuantifiedException: This class is applied to an instance that represents an "assertion" pattern.
        '''
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre._indefinite(is_greedy))


class OneOrMore(__Quantifier):
    '''
    Matches the provided pattern one or more times.

    :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
        or wrapped within a "Pregex" subtype instance.
    :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
        When declared as such, the regex engine will try to match \
        the expression as many times as possible. Defaults to 'True'.

    :raises CannotBeQuantifiedException: This class is applied to an instance that represents an "assertion" pattern.
    '''

    def __init__(self, pre: _pre.Pregex or str, is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern one or more times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a "Pregex" subtype instance.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to 'True'.

        :raises CannotBeQuantifiedException: This class is applied to an instance that represents an "assertion" pattern.
        '''
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre._one_or_more(is_greedy))


class Exactly(__Quantifier):
    '''
    Matches the provided pattern an exact number of times.

    :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
        or wrapped within a "Pregex" subtype instance.
    :param int n: The exact number of times that the provided pattern is to be matched.

    :raises NonIntegerArgumentException: Parameter 'n' is not an integer.
    :raises NonPositiveArgumentException: Parameter 'n' is less than one.
    :raises CannotBeQuantifiedException: This class is applied to an instance that represents an "assertion" pattern.
    '''

    def __init__(self, pre: _pre.Pregex or str, n: int) -> _pre.Pregex:
        '''
        Matches the provided pattern an exact number of times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a "Pregex" subtype instance.
        :param int n: The exact number of times that the provided pattern is to be matched.

        :raises NonIntegerArgumentException: Parameter 'n' is not an integer.
        :raises NonPositiveArgumentException: Parameter 'n' is less than one.
        :raises CannotBeQuantifiedException: This class is applied to an instance that represents an "assertion" pattern.
        '''
        if not isinstance(n, int) or isinstance(n, bool):
            raise _exceptions.NonIntegerArgumentException(n)
        if n < 1:
            raise _exceptions.NonPositiveArgumentException(n)
        super().__init__(pre, False, lambda pre, _: pre._exactly(n))


class AtLeast(__Quantifier):
    '''
    Matches the provided pattern a minimum number of times.

    :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
        or wrapped within a "Pregex" subtype instance.
    :param int n: The minimum number of times that the provided pattern is to be matched.
    :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
        When declared as such, the regex engine will try to match \
        the expression as many times as possible. Defaults to 'True'.

    :raises NonIntegerArgumentException: Parameter 'n' is not an integer.
    :raises NegativeArgumentException: Parameter 'n' is less than zero.
    :raises CannotBeQuantifiedException: This class is applied to an instance that represents an "assertion" pattern.
    '''

    def __init__(self, pre: _pre.Pregex or str, n: int, is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern a minimum number of times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a "Pregex" subtype instance.
        :param int n: The minimum number of times that the provided pattern is to be matched.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to 'True'.

        :raises NonIntegerArgumentException: Parameter 'n' is not an integer.
        :raises NegativeArgumentException: Parameter 'n' is less than zero.
        :raises CannotBeQuantifiedException: This class is applied to an instance that represents an "assertion" pattern.
        '''
        if not isinstance(n, int) or isinstance(n, bool):
            raise _exceptions.NonIntegerArgumentException(n)
        if n < 0:
            raise _exceptions.NegativeArgumentException(n)
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre._at_least(n, is_greedy))


class AtMost(__Quantifier):
    '''
    Matches the provided pattern a maximum number of times.

    :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
        or wrapped within a "Pregex" subtype instance.
    :param int n: The maximum number of times that the provided pattern is to be matched.
    :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
        When declared as such, the regex engine will try to match \
        the expression as many times as possible. Defaults to 'True'.

    :raises NonIntegerArgumentException: Parameter 'n' is not an integer.
    :raises NonPositiveArgumentException: Parameter 'n' is less than one.
    :raises CannotBeQuantifiedException: This class is applied to an instance that represents an "assertion" pattern.
    '''

    def __init__(self, pre: _pre.Pregex or str, n: int, is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern a maximum number of times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a "Pregex" subtype instance.
        :param int n: The maximum number of times that the provided pattern is to be matched.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to 'True'.

        :raises NonIntegerArgumentException: Parameter 'n' is not an integer.
        :raises NonPositiveArgumentException: Parameter 'n' is less than one.
        :raises CannotBeQuantifiedException: This class is applied to an instance that represents an "assertion" pattern.
        '''
        if not isinstance(n, int) or isinstance(n, bool):
            raise _exceptions.NonIntegerArgumentException(n)
        if n < 1:
            raise _exceptions.NonPositiveArgumentException(n)
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre._at_most(n, is_greedy))


class AtLeastAtMost(__Quantifier):
    '''
    Matches the provided expression between a minimum and a maximum number of times.

    :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
        or wrapped within a "Pregex" subtype instance.
    :param int min: The minimum number of times that the provided pattern is to be matched.
    :param int max: The maximum number of times that the provided pattern is to be matched.
    :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
        When declared as such, the regex engine will try to match \
        the expression as many times as possible. Defaults to 'True'.

    :raises NonIntegerArgumentException: Either one of parameters 'min' or 'max' is not an integer.
    :raises NegativeArgumentException: 'min' is less than zero.
    :raises NonPositiveArgumentException: 'max' is less than one.
    :raises MinGreaterThanMaxException: 'min' is greater than max.
    :raises CannotBeQuantifiedException: This class is applied to an instance that represents an "assertion" pattern.
    '''

    def __init__(self, pre: _pre.Pregex or str, min: int, max: int, is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided expression between a minimum and a maximum number of times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a "Pregex" subtype instance.
        :param int min: The minimum number of times that the provided pattern is to be matched.
        :param int max: The maximum number of times that the provided pattern is to be matched.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to 'True'.

        :raises NonIntegerArgumentException: Either one of parameters 'min' or 'max' is not an integer.
        :raises NegativeArgumentException: 'min' is less than zero.
        :raises NonPositiveArgumentException: 'max' is less than one.
        :raises MinGreaterThanMaxException: 'min' is greater than max.
        :raises CannotBeQuantifiedException: This class is applied to an instance that represents an "assertion" pattern.
        '''
        if not isinstance(min, int) or isinstance(min, bool):
            raise _exceptions.NonIntegerArgumentException(min)
        if not isinstance(max, int) or isinstance(max, bool):
            raise _exceptions.NonIntegerArgumentException(max)
        if min < 0:
            raise _exceptions.NegativeArgumentException(min)
        elif max < 1:
            raise _exceptions.NonPositiveArgumentException(max)
        elif max < min:
            raise _exceptions.MinGreaterThanMaxException(min, max)
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre._at_least_at_most(min, max, is_greedy))