from pregex.pre import Pregex

class __Anchor(Pregex):
    '''
    Every "Anchor" class must inherit from this class.
    '''

    def __init__(self, pre: str or Pregex, transform):
        pre = __class__._to_pregex(pre)
        super().__init__(transform(pre), group_on_concat=False)


class __Lookaround(Pregex):
    '''
    Every "Lookaround" class must inherit from this class.
    '''

    def __init__(self, pre1: str or Pregex, pre2: str or Pregex, transform):
        pre1 = __class__._to_pregex(pre1)
        super().__init__(transform(pre1, pre2), group_on_concat=False, group_on_quantify=True)


class MatchAtStart(__Anchor):
    '''
    Matches the provided pattern only if said pattern is at the start of the string.
    '''

    def __init__(self, pre: str or Pregex):
        '''
        Matches the provided pattern only if said pattern is at the start of the string.

        :param Pregex | str pre: The pattern that is to be matched.
        '''
        super().__init__(pre, lambda pre: str(pre._match_at_start()))


class MatchAtEnd(__Anchor):
    '''
    Matches the provided pattern only if said pattern is at the end of the string.
    '''

    def __init__(self, pre: str or Pregex):
        '''
        Matches the provided pattern only if said pattern is at the end of the string.

        :param Pregex | str pre: The pattern that is to be matched.
        '''
        super().__init__(pre, lambda pre: str(pre._match_at_end()))


class MatchAtLineStart(__Anchor):
    '''
    Matches the provided pattern only if said pattern is at the start of a line.

    NOTE: Uses meta character "^" since the "MULTILINE" flag is considered on.
    '''

    def __init__(self, pre: str or Pregex):
        '''
        Matches the provided pattern only if said pattern is at the end of the string.

        :param Pregex | str pre: The pattern that is to be matched.

        NOTE: Uses meta character "^" since the "MULTILINE" flag is considered on.
        '''
        super().__init__(pre, lambda pre: str(pre._match_at_line_start()))


class MatchAtLineEnd(__Anchor):
    '''
    Matches the provided pattern only if said pattern is at the end of a line.

    NOTE: Uses meta character "$" since the "MULTILINE" flag is considered on.
    '''

    def __init__(self, pre: str or Pregex):
        '''
        Matches the provided pattern only if said pattern is at the end of a line.

        :param Pregex | str pre: The pattern that is to be matched.

        NOTE: Uses meta character "$" since the "MULTILINE" flag is considered on.
        '''
        super().__init__(pre, lambda pre: str(pre._match_at_line_end()))


class MatchAtWordBoundary(__Anchor):
    '''
    Matches the provided pattern only if said pattern has \
    a word boundary on both its sides.
    '''

    def __init__(self, pre: str or Pregex):
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

    def __init__(self, pre: str or Pregex):
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

    def __init__(self, pre: str or Pregex):
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

    def __init__(self, pre1: str or Pregex, pre2: str or Pregex):
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

    def __init__(self, pre1: str or Pregex, pre2: str or Pregex):
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

    def __init__(self, pre1: str or Pregex, pre2: str or Pregex):
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

    def __init__(self, pre1: str or Pregex, pre2: str or Pregex):
        '''
        Matches pattern 'pre1' only if it is not preceded by pattern 'pre2', \
        without the latter being included into the match.

        :param Pregex | str pre1: The pattern that is to be matched.
        :param Pregex | str pre2: The pattern that must not precede pattern 'pre1'.
        '''
        super().__init__(pre1, pre2, lambda pre1, pre2: str(pre1._not_preceded_by(pre2)))