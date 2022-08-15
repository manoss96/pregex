import pregex.pre as _pre
import pregex.exceptions as _ex
from pregex.quantifiers import Exactly as _Exactly


__doc__ = """
All classes within this module "assert" something about the provided pattern
without having to match any additional characters. For example, :class:`MatchAtStart` ensures
that the provided pattern matches only when it is found at the start of the string,
while :class:`NotFollowedBy` asserts that a match must not be followed by one or more
specified patterns. Another thing you should keep in mind is that assertions cannot be
quantified, as attempting that will cause a ``CannotBeQuantifiedException`` exception
to be thrown. The only exception to this is the :class:`~pregex.quantifiers.Optional`
quantifier.

Classes & methods
===========================================

Below are listed all classes within :py:mod:`pregex.assertions`
along with any possible methods they may possess.
"""


class __Assertion(_pre.Pregex):
    '''
    Constitutes the base class for `__Anchor` and `__Lookaround` classes.

    :param str pattern: The RegEx pattern which represents the assertion.
    '''
    def __init__(self, pattern: str):
        '''
        Constitutes the base class for `__Anchor` and `__Lookaround` classes.

        :param str pattern: The RegEx pattern which represents the assertion.
        '''
        super().__init__(pattern, escape=False)


class __Anchor(__Assertion):
    '''
    Constitutes the base class for all `anchor` classes that are part of this module.

    :param Pregex | str pre: A Pregex instance or string representing the `anchor` pattern.
    :param (Pregex => str) transform: A `transform` function for the provided pattern.
    '''
    def __init__(self, pre: _pre.Pregex or str, transform):
        '''
        Constitutes the base class for all `anchor` classes that are part of this module.

        :param Pregex | str pre: A Pregex instance or string representing the `anchor` pattern.
        :param (Pregex => str) transform: A `transform` function for the provided pattern.
        '''
        super().__init__(transform(__class__._to_pregex(pre)))


class __PositiveLookaround(__Assertion):
    '''
    Constitutes the base class for classes ``FollowedBy`` and ``PrecededBy`` \
        that are part of this module.

    :param Pregex | str pre1: A Pregex instance or string representing the `match` pattern.
    :param Pregex | str pre2: A Pregex instance or string representing the `assertion` pattern.
    :param (Pregex, Pregex => str) transform: A `transform` function for the provided patterns.
    '''
    def __init__(self, pre1: _pre.Pregex or str, pre2: _pre.Pregex or str, transform):
        '''
        Constitutes the base class for classes ``FollowedBy`` and ``PrecededBy`` \
            that are part of this module.

        :param Pregex | str pre1: A Pregex instance or string representing the `match` pattern.
        :param Pregex | str pre2: A Pregex instance or string representing the `assertion` pattern.
        :param (Pregex, Pregex => str) transform: A `transform` function for the provided patterns.
        '''
        pre1 = __class__._to_pregex(pre1)
        pre2 = __class__._to_pregex(pre2)
        super().__init__(transform(pre1, pre2))


class __NegativeLookaround(__Assertion):
    '''
    Constitutes the base class for classes ``NotFollowedBy`` and ``NotPrecededBy`` \
        that are part of this module.

    :param Pregex | str pre1: A Pregex instance or string representing the `match` pattern.
    :param Pregex | str *pres: One or more Pregex instances or strings representing the `assertion` patterns.
    :param (tuple[Pregex | str] => str) transform: A `transform` function for the provided patterns.

    :raises LessThanTwoArgumentsException: Less than two arguments are provided.
    '''
    def __init__(self, pres: tuple[_pre.Pregex or str], transform) -> _pre.Pregex:
        '''
        Constitutes the base class for classes ``NotFollowedBy`` and ``NotPrecededBy`` \
            that are part of this module.

        :param Pregex | str pre1: A Pregex instance or string representing the `match` pattern.
        :param Pregex | str *pres: One or more Pregex instances or strings representing the `assertion` patterns.
        :param (tuple[Pregex | str] => str) transform: A `transform` function for the provided patterns.

        :raises LessThanTwoArgumentsException: Less than two arguments are provided.
        '''
        if len(pres) < 2:
            raise _ex.LessThanTwoArgumentsException()
        result = __class__._to_pregex(pres[0])
        for pre in pres[1:]:
            result = _pre.Pregex(transform(result, __class__._to_pregex(pre)), escape=False)
        super().__init__(str(result))


class MatchAtStart(__Anchor):
    '''
    Matches the provided pattern only if said pattern is at the start of the string.

    :param Pregex | str pre: The pattern that is to be matched.
    '''

    def __init__(self, pre: _pre.Pregex or str):
        '''
        Matches the provided pattern only if said pattern is at the start of the string.

        :param Pregex | str pre: The pattern that is to be matched.
        '''
        super().__init__(pre, lambda pre: str(pre._match_at_start()))


class MatchAtEnd(__Anchor):
    '''
    Matches the provided pattern only if said pattern is at the end of the string.

    :param Pregex | str pre: The pattern that is to be matched.
    '''

    def __init__(self, pre: _pre.Pregex or str):
        '''
        Matches the provided pattern only if said pattern is at the end of the string.

        :param Pregex | str pre: The pattern that is to be matched.
        '''
        super().__init__(pre, lambda pre: str(pre._match_at_end()))


class MatchAtLineStart(__Anchor):
    '''
    Matches the provided pattern only if said pattern is at the start of a line.

    :param Pregex | str pre: The pattern that is to be matched.

    :note: Uses meta character ``^`` since the `MULTILINE` flag is considered on.
    '''

    def __init__(self, pre: _pre.Pregex or str):
        '''
        Matches the provided pattern only if said pattern is at the end of the string.

        :param Pregex | str pre: The pattern that is to be matched.

        :note: Uses meta character ``^`` since the `MULTILINE` flag is considered on.
        '''
        super().__init__(pre, lambda pre: str(pre._match_at_line_start()))


class MatchAtLineEnd(__Anchor):
    '''
    Matches the provided pattern only if said pattern is at the end of a line.

    :param Pregex | str pre: The pattern that is to be matched.

    :note: Uses meta character ``$`` since the `MULTILINE` flag is considered on.
    '''

    def __init__(self, pre: _pre.Pregex or str):
        '''
        Matches the provided pattern only if said pattern is at the end of a line.

        :param Pregex | str pre: The pattern that is to be matched.

        :note: Uses meta character ``$`` since the `MULTILINE` flag is considered on.
        '''
        super().__init__(pre, lambda pre: str(pre._match_at_line_end()))


class WordBoundary(__Anchor):
    '''
    Asserts that the position, at which it is placed, \
    must constitute a word boundary.
    '''

    def __init__(self):
        '''
        Asserts that the position, at which it is placed, \
        must constitute a word boundary.
        '''
        super().__init__(_pre.Empty(), lambda pre: str(pre + _pre.Pregex("\\b", escape=False)))


class NonWordBoundary(__Anchor):
    '''
    Asserts that the position, at which it is placed, \
    must not constitute a word boundary.
    '''

    def __init__(self):
        '''
        Asserts that the position, at which it is placed, \
        must not constitute a word boundary.
        '''
        super().__init__(_pre.Empty(), lambda pre: str(pre + _pre.Pregex("\\B", escape=False)))


class FollowedBy(__PositiveLookaround):
    '''
    Matches pattern ``pre1`` only if it is followed by pattern ``pre2``, \
    without the latter being included into the match.

    :param Pregex | str pre1: The pattern that is to be matched.
    :param Pregex | str pre2: The pattern that must follow pattern ``pre1`` \
        in order for it to be considered a match.
    '''

    def __init__(self, pre1: _pre.Pregex or str, pre2: _pre.Pregex or str):
        '''
        Matches pattern ``pre1`` only if it is followed by pattern ``pre2``, \
        without the latter being included into the match.

        :param Pregex | str pre1: The pattern that is to be matched.
        :param Pregex | str pre2: The pattern that must follow pattern ``pre1`` \
            in order for it to be considered a match.
        '''
        super().__init__(pre1, pre2, lambda pre1, pre2: str(pre1._followed_by(pre2)))


class NotFollowedBy(__NegativeLookaround):
    '''
    Matches pattern ``pre`` only if it is not followed by any one of \
    the rest of the provided patterns.

    :param Pregex | str pre: The pattern that is to be matched.
    :param Pregex | str \*pres: One or more patterns, none of which must \
        come right after ``pre`` in order for it to be considered a match.
    '''

    def __init__(self, pre: _pre.Pregex or str, *pres: _pre.Pregex or str):
        '''
        Matches pattern ``pre`` only if it is not followed by any one of \
        rest of the provided patterns.

        :param Pregex | str pre: The pattern that is to be matched.
        :param Pregex | str \*pres: One or more patterns, none of which must \
            come right after ``pre`` in order for it to be considered a match.
        '''
        super().__init__((pre, *pres), lambda pre1, pre2: str(pre1._not_followed_by(pre2)))


class PrecededBy(__PositiveLookaround):
    '''
    Matches pattern ``pre1`` only if it is preceded by pattern ``pre2``, \
    without the latter being included into the match.

    :param Pregex | str pre1: The pattern that is to be matched.
    :param Pregex | str pre2: The pattern that must precede pattern ``pre1`` \
        in order for it to be considered a match.

    :raises NonFixedWidthPatternException: A class that represents a non-fixed-width \
        pattern is provided as parameter ``pre2``.
    '''

    def __init__(self, pre1: _pre.Pregex or str, pre2: _pre.Pregex or str):
        '''
        Matches pattern ``pre1`` only if it is preceded by pattern ``pre2``, \
        without the latter being included into the match.

        :param Pregex | str pre1: The pattern that is to be matched.
        :param Pregex | str pre2: The pattern that must precede pattern ``pre1`` \
            in order for it to be considered a match.

        :raises NonFixedWidthPatternException: A class that represents a non-fixed-width \
            pattern is provided as parameter ``pre2``.
        '''
        if isinstance(pre2, _pre.Pregex):
            if pre2._get_type() == _pre._Type.Quantifier and (not isinstance(pre2, _Exactly)):
                raise _ex.NonFixedWidthPatternException(self, pre2)
        super().__init__(pre1, pre2, lambda pre1, pre2: str(pre1._preceded_by(pre2)))


class NotPrecededBy(__NegativeLookaround):
    '''
    Matches pattern ``pre`` only if it is not preceded by any one of \
    the rest of the provided patterns.

    :param Pregex | str pre: The pattern that is to be matched.
    :param Pregex | str \*pres: One or more patterns, none of which must \
        come right before ``pre`` in order for it to be considered a match.

    :raises NonFixedWidthPatternException: At least one of the provided classes \
        in ``pres`` represents a non-fixed-width pattern.
    '''

    def __init__(self, pre: _pre.Pregex or str, *pres: _pre.Pregex or str):
        '''
        Matches pattern ``pre`` only if it is not preceded by any one of \
        the rest of the provided patterns.

        :param Pregex | str pre: The pattern that is to be matched.
        :param Pregex | str \*pres: One or more patterns, none of which must \
            come right before ``pre`` in order for it to be considered a match.

        :raises NonFixedWidthPatternException: At least one of the provided classes \
            in ``pres`` represents a non-fixed-width pattern.
        '''
        for p in pres:
            if isinstance(p, _pre.Pregex):
                if p._get_type() == _pre._Type.Quantifier and (not isinstance(p, _Exactly)):
                    raise _ex.NonFixedWidthPatternException(self, p)
        super().__init__((pre, *pres), lambda pre1, pre2: str(pre1._not_preceded_by(pre2)))