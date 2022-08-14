import pregex.pre as _pre
import pregex.exceptions as _ex
from pregex.quantifiers import Exactly as _Exactly


class __Assertion(_pre.Pregex):
    '''
    Constitutes the base class for "__Anchor" and "__Lookaround" classes.
    '''
    def __init__(self, pattern: str):
        super().__init__(pattern, escape=False)


class __Anchor(__Assertion):
    '''
    Constitutes the base class for every "anchor" classes.
    '''
    def __init__(self, pre: _pre.Pregex or str, transform):
        super().__init__(transform(__class__._to_pregex(pre)))


class __PositiveLookaround(__Assertion):
    '''
    Constitutes the base class for every "positive lookaround" classes.
    '''
    def __init__(self, pre1: _pre.Pregex or str, pre2: _pre.Pregex or str, transform):
        pre1 = __class__._to_pregex(pre1)
        pre2 = __class__._to_pregex(pre2)
        super().__init__(transform(pre1, pre2))


class __NegativeLookaround(__Assertion):
    '''
    Constitutes the base class for every "negative lookaround" class.
    '''

    def __init__(self, pres: tuple[_pre.Pregex or str], transform) -> _pre.Pregex:
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

    :note: Uses meta character "^" since the "MULTILINE" flag is considered on.
    '''

    def __init__(self, pre: _pre.Pregex or str):
        '''
        Matches the provided pattern only if said pattern is at the end of the string.

        :param Pregex | str pre: The pattern that is to be matched.

        :note: Uses meta character "^" since the "MULTILINE" flag is considered on.
        '''
        super().__init__(pre, lambda pre: str(pre._match_at_line_start()))


class MatchAtLineEnd(__Anchor):
    '''
    Matches the provided pattern only if said pattern is at the end of a line.

    :param Pregex | str pre: The pattern that is to be matched.

    :note: Uses meta character "$" since the "MULTILINE" flag is considered on.
    '''

    def __init__(self, pre: _pre.Pregex or str):
        '''
        Matches the provided pattern only if said pattern is at the end of a line.

        :param Pregex | str pre: The pattern that is to be matched.

        :note: Uses meta character "$" since the "MULTILINE" flag is considered on.
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
    Matches pattern 'pre1' only if it is followed by pattern 'pre2', \
    without the latter being included into the match.

    :param Pregex | str pre1: The pattern that is to be matched.
    :param Pregex | str pre2: The pattern that must follow pattern "pre1" \
        in order for it to be considered a match.
    '''

    def __init__(self, pre1: _pre.Pregex or str, pre2: _pre.Pregex or str):
        '''
        Matches pattern 'pre1' only if it is followed by pattern 'pre2', \
        without the latter being included into the match.

        :param Pregex | str pre1: The pattern that is to be matched.
        :param Pregex | str pre2: The pattern that must follow pattern "pre1" \
            in order for it to be considered a match.
        '''
        super().__init__(pre1, pre2, lambda pre1, pre2: str(pre1._followed_by(pre2)))


class NotFollowedBy(__NegativeLookaround):
    '''
    Matches pattern 'pre' only if it is not followed by any one of \
    the rest of the provided patterns.

    :param Pregex | str pre: The pattern that is to be matched.
    :param Pregex | str *pres: One or more patterns, none of which must \
        come right after "pre" in order for it to be considered a match.
    '''

    def __init__(self, pre: _pre.Pregex or str, *pres: _pre.Pregex or str):
        '''
        Matches pattern 'pre' only if it is not followed by any one of \
        rest of the provided patterns.

        :param Pregex | str pre: The pattern that is to be matched.
        :param Pregex | str *pres: One or more patterns, none of which must \
            come right after "pre" in order for it to be considered a match.
        '''
        super().__init__((pre, *pres), lambda pre1, pre2: str(pre1._not_followed_by(pre2)))


class PrecededBy(__PositiveLookaround):
    '''
    Matches pattern "pre1" only if it is preceded by pattern "pre2", \
    without the latter being included into the match.

    :param Pregex | str pre1: The pattern that is to be matched.
    :param Pregex | str pre2: The pattern that must precede pattern "pre1" \
        in order for it to be considered a match.

    :raises NonFixedWidthPatternException: A class that represents a non-fixed-width \
        pattern is provided as parameter "pre2".
    '''

    def __init__(self, pre1: _pre.Pregex or str, pre2: _pre.Pregex or str):
        '''
        Matches pattern "pre1" only if it is preceded by pattern "pre2", \
        without the latter being included into the match.

        :param Pregex | str pre1: The pattern that is to be matched.
        :param Pregex | str pre2: The pattern that must precede pattern "pre1" \
            in order for it to be considered a match.

        :raises NonFixedWidthPatternException: A class that represents a non-fixed-width \
        '''
        if isinstance(pre2, _pre.Pregex):
            if pre2._get_type() == _pre._Type.Quantifier and (not isinstance(pre2, _Exactly)):
                raise _ex.NonFixedWidthPatternException(self, pre2)
        super().__init__(pre1, pre2, lambda pre1, pre2: str(pre1._preceded_by(pre2)))


class NotPrecededBy(__NegativeLookaround):
    '''
    Matches pattern 'pre' only if it is not preceded by any one of \
    the rest of the provided patterns.

    :param Pregex | str pre: The pattern that is to be matched.
    :param Pregex | str *pres: One or more patterns, none of which must \
        come right before "pre" in order for it to be considered a match.

    :raises NonFixedWidthPatternException: At least one of the provided classes \
        in "pres" represents a non-fixed-width pattern.
    '''

    def __init__(self, pre: _pre.Pregex or str, *pres: _pre.Pregex or str):
        '''
        Matches pattern 'pre' only if it is not preceded by any one of \
        the rest of the provided patterns.

        :param Pregex | str pre: The pattern that is to be matched.
        :param Pregex | str *pres: One or more patterns, none of which must \
            come right before "pre" in order for it to be considered a match.

        :raises NonFixedWidthPatternException: At least one of the provided classes \
            in "pres" represents a non-fixed-width pattern.
        '''
        for p in pres:
            if isinstance(p, _pre.Pregex):
                if p._get_type() == _pre._Type.Quantifier and (not isinstance(p, _Exactly)):
                    raise _ex.NonFixedWidthPatternException(self, p)
        super().__init__((pre, *pres), lambda pre1, pre2: str(pre1._not_preceded_by(pre2)))