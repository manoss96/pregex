import pregex.pre as _pre

class __Anchor(_pre.Pregex):
    '''
    Every "Anchor" class must inherit from this class.
    '''

    def __init__(self, pre: str or _pre.Pregex, transform):
        pre = __class__._to_pregex(pre)
        super().__init__(transform(pre), group_on_concat=False)


class __Lookaround(_pre.Pregex):
    '''
    Every "Lookaround" class must inherit from this class.
    '''

    def __init__(self, pre1: str or _pre.Pregex, pre2: str or _pre.Pregex, transform):
        pre1, pre2 = __class__._to_pregex(pre1), __class__._to_pregex(pre2)
        super().__init__(transform(pre1, pre2), group_on_concat=False, group_on_quantify=True)


class MatchAtStart(__Anchor):
    '''
    Matches the provided pattern only if said pattern is at the start of the string.

    NOTE: Cannot be quantified.
    '''

    def __init__(self, pre: str or _pre.Pregex):
        '''
        Matches the provided pattern only if said pattern is at the start of the string.

        :param Pregex | str pre: The pattern that is to be matched.

        NOTE: Cannot be quantified.
        '''
        super().__init__(pre, lambda pre: str(pre._match_at_start()))


class MatchAtEnd(__Anchor):
    '''
    Matches the provided pattern only if said pattern is at the end of the string.

    NOTE: Cannot be quantified.
    '''

    def __init__(self, pre: str or _pre.Pregex):
        '''
        Matches the provided pattern only if said pattern is at the end of the string.

        :param Pregex | str pre: The pattern that is to be matched.

        NOTE: Cannot be quantified.
        '''
        super().__init__(pre, lambda pre: str(pre._match_at_end()))


class MatchAtLineStart(__Anchor):
    '''
    Matches the provided pattern only if said pattern is at the start of a line.

    NOTE: 
        - Cannot be quantified.
        - Uses meta character "^" since the "MULTILINE" flag is considered on.
    '''

    def __init__(self, pre: str or _pre.Pregex):
        '''
        Matches the provided pattern only if said pattern is at the end of the string.

        :param Pregex | str pre: The pattern that is to be matched.

        NOTE: 
            - Cannot be quantified.
            - Uses meta character "^" since the "MULTILINE" flag is considered on.
        '''
        super().__init__(pre, lambda pre: str(pre._match_at_line_start()))


class MatchAtLineEnd(__Anchor):
    '''
    Matches the provided pattern only if said pattern is at the end of a line.

    NOTE: 
        - Cannot be quantified.
        - Uses meta character "$" since the "MULTILINE" flag is considered on.
    '''

    def __init__(self, pre: str or _pre.Pregex):
        '''
        Matches the provided pattern only if said pattern is at the end of a line.

        :param Pregex | str pre: The pattern that is to be matched.

        NOTE: 
            - Cannot be quantified.
            - Uses meta character "$" since the "MULTILINE" flag is considered on.
        '''
        super().__init__(pre, lambda pre: str(pre._match_at_line_end()))


class MatchAtWordBoundary(__Anchor):
    '''
    Matches the provided pattern only if said pattern has \
    a word boundary on both its sides.
    '''

    def __init__(self, pre: str or _pre.Pregex):
        '''
        Matches the provided pattern only if said pattern has \
        a word boundary on both its sides.

        :param Pregex | str pre: The pattern that is to be matched.
        '''
        super().__init__(pre, lambda pre: str(pre._match_at_word_boundary()))

class MatchAtLeftWordBoundary(__Anchor):
    '''
    Matches the provided pattern only when said pattern has \
    a word boundary on its left side.
    '''

    def __init__(self, pre: str or _pre.Pregex):
        '''
        Matches the provided pattern only if said pattern has \
        a word boundary on its left side.

        :param Pregex | str pre: The pattern that is to be matched.
        '''
        super().__init__(pre, lambda pre: str(pre._match_at_left_word_boundary()))


class MatchAtRightWordBoundary(__Anchor):
    '''
    Matches the provided pattern only when said pattern has \
    a word boundary on its right side.
    '''

    def __init__(self, pre: str or _pre.Pregex):
        '''
        Matches the provided pattern only if said pattern has \
        a word boundary on its right side.

        :param Pregex | str pre: The pattern that is to be matched.
        '''
        super().__init__(pre, lambda pre: str(pre._match_at_right_word_boundary()))


class FollowedBy(__Lookaround):
    '''
    Matches pattern 'pre1' only if it is followed by pattern 'pre2', \
    without the latter being included into the match.
    '''

    def __init__(self, pre1: str or _pre.Pregex, pre2: str or _pre.Pregex):
        '''
        Matches pattern 'pre1' only if it is followed by pattern 'pre2', \
        without the latter being included into the match.

        :param Pregex | str pre1: The pattern that is to be matched.
        :param Pregex | str pre2: The pattern that must follow pattern 'pre1'.
        '''
        super().__init__(pre1, pre2, lambda pre1, pre2: str(pre1._followed_by(pre2)))


class NotFollowedBy(__Lookaround):
    '''
    Matches pattern 'pre1' only if it is not followed by pattern 'pre2', \
    without the latter being included into the match.
    '''

    def __init__(self, pre1: str or _pre.Pregex, pre2: str or _pre.Pregex):
        '''
        Matches pattern 'pre1' only if it is not followed by pattern 'pre2', \
        without the latter being included into the match.

        :param Pregex | str pre1: The pattern that is to be matched.
        :param Pregex | str pre2: The pattern that must not follow pattern 'pre1'.
        '''
        super().__init__(pre1, pre2, lambda pre1, pre2: str(pre1._not_followed_by(pre2)))


class PrecededBy(__Lookaround):
    '''
    Matches pattern 'pre1' only if it is preceded by pattern 'pre2', \
    without the latter being included into the match.
    '''

    def __init__(self, pre1: str or _pre.Pregex, pre2: str or _pre.Pregex):
        '''
        Matches pattern 'pre1' only if it is preceded by pattern 'pre2', \
        without the latter being included into the match.

        :param Pregex | str pre1: The pattern that is to be matched.
        :param Pregex | str pre2: The pattern that must precede pattern 'pre1'.
        '''
        super().__init__(pre1, pre2, lambda pre1, pre2: str(pre1._preceded_by(pre2)))


class NotPrecededBy(__Lookaround):
    '''
    Matches pattern 'pre1' only if it is not preceded by pattern 'pre2', \
    without the latter being included into the match.
    '''

    def __init__(self, pre1: str or _pre.Pregex, pre2: str or _pre.Pregex):
        '''
        Matches pattern 'pre1' only if it is not preceded by pattern 'pre2', \
        without the latter being included into the match.

        :param Pregex | str pre1: The pattern that is to be matched.
        :param Pregex | str pre2: The pattern that must not precede pattern 'pre1'.
        '''
        super().__init__(pre1, pre2, lambda pre1, pre2: str(pre1._not_preceded_by(pre2)))