import pregex.pre as _pre
import pregex.assertions as _assertions
import pregex.exceptions as _exceptions


class __Quantifier(_pre.Pregex):
    '''
    Every "Quantifier" class must inherit from this class.
    '''
    def __init__(self, pre: str or _pre.Pregex, is_greedy: bool, transform) -> '__Quantifier':
        if isinstance(pre, (_assertions.MatchAtStart, _assertions.MatchAtLineStart,
            _assertions.MatchAtEnd, _assertions.MatchAtLineEnd)):
            raise _exceptions.NotQuantifiableException(pre)
        pre = transform(__class__._to_pregex(pre), is_greedy)
        super().__init__(str(pre), pre._get_group_on_concat(), pre._get_group_on_quantify())


class Optional(__Quantifier):
    '''
    Matches the provided pattern zero or one times.
    '''

    def __init__(self, pre: str or _pre.Pregex, is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern zero or one times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a "Pregex" subtype instance.
        :param bool is_greedy: Indicates whether to declare this quantifier as lazy. \
            When declared as such, the regex engine will try to match \
            the expression as few times as possible.
        '''
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre._optional(is_greedy))


class Indefinite(__Quantifier):
    '''
    Matches the provided pattern zero or more times.
    '''

    def __init__(self, pre: str or _pre.Pregex, is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern zero or more times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a "Pregex" subtype instance.
        :param bool is_greedy: Indicates whether to declare this quantifier as lazy. \
            When declared as such, the regex engine will try to match \
            the expression as few times as possible.
        '''
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre._indefinite(is_greedy))


class Enforced(__Quantifier):
    '''
    Matches the provided pattern one or more times.
    '''

    def __init__(self, pre: str or _pre.Pregex, is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern one or more times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a "Pregex" subtype instance.
        :param bool is_greedy: Indicates whether to declare this quantifier as lazy. \
            When declared as such, the regex engine will try to match \
            the expression as few times as possible.
        '''
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre._enforced(is_greedy))


class Exactly(__Quantifier):
    '''
    Matches the provided pattern an exact number of times.
    '''

    def __init__(self, pre: str or _pre.Pregex, n: int) -> _pre.Pregex:
        '''
        Matches the provided pattern an exact number of times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a "Pregex" subtype instance.
        :param int n: The number of times that the provided expression is to be matched.
        '''
        super().__init__(pre, False, lambda pre, _: pre._exactly(n))


class AtLeast(__Quantifier):
    '''
    Matches the provided pattern a minimum number of times.
    '''

    def __init__(self, pre: str or _pre.Pregex, n: int, is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern a minimum number of times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a "Pregex" subtype instance.
        :param int n: The minimum number of times that the provided pattern is to be matched.
        :param bool is_greedy: Indicates whether to declare this quantifier as lazy. \
            When declared as such, the regex engine will try to match \
            the expression as few times as possible.
        '''
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre._at_least(n, is_greedy))


class AtMost(__Quantifier):
    '''
    Matches the provided pattern a maximum number of times.
    '''

    def __init__(self, pre: str or _pre.Pregex, n: int, is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided pattern a maximum number of times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a "Pregex" subtype instance.
        :param int n: The maximum number of times that the provided pattern is to be matched.
        :param bool is_greedy: Indicates whether to declare this quantifier as lazy. \
            When declared as such, the regex engine will try to match \
            the expression as few times as possible.
        '''
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre._at_most(n, is_greedy))


class AtLeastAtMost(__Quantifier):
    '''
    Matches the provided expression between a minimum and a maximum number of times.
    '''

    def __init__(self, pre: str or _pre.Pregex, min: int, max: int, is_greedy: bool = True) -> _pre.Pregex:
        '''
        Matches the provided expression between a minimum and a maximum number of times.

        :param Pregex | str pre: The pattern that is to be matched, provided either as a string \
            or wrapped within a "Pregex" subtype instance.
        :param min: The minimum number of times that the provided pattern is to be matched.
        :param max: The maximum number of times that the provided pattern is to be matched.
        :param bool is_greedy: Indicates whether to declare this quantifier as lazy. \
            When declared as such, the regex engine will try to match \
            the expression as few times as possible.
        '''
        super().__init__(pre, is_greedy, lambda pre, is_greedy: pre._at_least_at_most(min, max, is_greedy))