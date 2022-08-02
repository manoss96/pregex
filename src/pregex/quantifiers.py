import pregex.pre as _pre
import pregex.assertions as _assertions
import pregex.exceptions as _exceptions


class __Quantifier(_pre.Pregex):
    '''
    Constitutes the base class for every class within "quantifiers.py".
    '''
    def __init__(self, pre: _pre.Pregex or str, is_greedy: bool, transform) -> '__Quantifier':
        if issubclass(pre.__class__, _pre.Pregex):
            if pre._get_type() in (__class__._PatternType.Assertion, __class__._PatternType.Quantifier):
                raise _exceptions.CannotBeQuantifiedException(pre)
        pre = transform(__class__._to_pregex(pre), is_greedy)
        super().__init__(str(pre), escape=False)
        self._set_type(__class__._PatternType.Quantifier)


class Optional(__Quantifier):
    '''
    Matches the provided pattern zero or one times.

    :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
        or wrapped within a "Pregex" subtype instance.
    :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
        When declared as such, the regex engine will try to match \
        the expression as many times as possible. Defaults to 'True'.
    '''

    def __init__(self, pre: _pre.Pregex or str, is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern zero or one times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a "Pregex" subtype instance.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to 'True'.
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
    '''

    def __init__(self, pre: _pre.Pregex or str, is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern zero or more times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a "Pregex" subtype instance.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to 'True'.
        '''
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre._indefinite(is_greedy))


class AtLeastOnce(__Quantifier):
    '''
    Matches the provided pattern one or more times.

    :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
        or wrapped within a "Pregex" subtype instance.
    :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
        When declared as such, the regex engine will try to match \
        the expression as many times as possible. Defaults to 'True'.
    '''

    def __init__(self, pre: _pre.Pregex or str, is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern one or more times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a "Pregex" subtype instance.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to 'True'.
        '''
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre._at_least_once(is_greedy))


class Exactly(__Quantifier):
    '''
    Matches the provided pattern an exact number of times.

    :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
        or wrapped within a "Pregex" subtype instance.
    :param int n: The exact number of times that the provided pattern is to be matched.
    '''

    def __init__(self, pre: _pre.Pregex or str, n: int) -> _pre.Pregex:
        '''
        Matches the provided pattern an exact number of times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a "Pregex" subtype instance.
        :param int n: The exact number of times that the provided pattern is to be matched.
        '''
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
        '''
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
        '''
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
        '''
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre._at_least_at_most(min, max, is_greedy))