import pregex.core.pre as _pre
import pregex.core.exceptions as _ex
from pregex.core.quantifiers import Exactly as _Exactly


__doc__ = """
All classes within this module "assert" something about the provided pattern
without having to match any additional characters. For example, :class:`MatchAtStart`
ensures that the provided pattern matches only when it is found at the start of the string,
while :class:`NotFollowedBy` asserts that a match must not be followed by one or more
specified patterns. Another thing you should keep in mind is that some of these assertions
cannot be quantified, as attempting that will cause a ``CannotBeQuantifiedException`` exception
to be thrown. The only exception to this is quantifier :class:`~pregex.quantifiers.Optional`,
which can be applied to every assertion as it does not result in the pattern having to be
repeated more than once.

Classes & methods
-------------------------------------------

Below are listed all classes within :py:mod:`pregex.core.assertions`
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

    :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a ``Pregex`` instance \
        nor a string.
    '''
    def __init__(self, pre: _pre.Pregex or str, transform):
        '''
        Constitutes the base class for all `anchor` classes that are part of this module.

        :param Pregex | str pre: A Pregex instance or string representing the `anchor` pattern.
        :param (Pregex => str) transform: A `transform` function for the provided pattern.

        :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a ``Pregex`` instance \
            nor a string.
        '''
        super().__init__(transform(__class__._to_pregex(pre)))


class __PositiveLookaround(__Assertion):
    '''
    Constitutes the base class for classes ``FollowedBy`` and ``PrecededBy`` \
        that are part of this module.

    :param Pregex | str match: A Pregex instance or string representing the `match` pattern.
    :param Pregex | str assertion: A Pregex instance or string representing the `assertion` pattern.
    :param (Pregex, Pregex => str) transform: A `transform` function for the provided patterns.
    '''
    def __init__(self, match: _pre.Pregex or str, assertion: _pre.Pregex or str, transform):
        '''
        Constitutes the base class for classes ``FollowedBy`` and ``PrecededBy`` \
            that are part of this module.

        :param Pregex | str match: A Pregex instance or string representing the `match` pattern.
        :param Pregex | str assertion: A Pregex instance or string representing the `assertion` pattern.
        :param (Pregex, Pregex => str) transform: A `transform` function for the provided patterns.
        '''
        match = __class__._to_pregex(match)
        assertion = __class__._to_pregex(assertion)
        result = match if assertion._get_type() == _pre._Type.Empty \
             else transform(match, assertion)
        super().__init__(str(result))


class __NegativeLookaround(__Assertion):
    '''
    Constitutes the base class for classes ``NotFollowedBy`` and ``NotPrecededBy`` \
        that are part of this module.

    :param Pregex | str *pres: Two or more Pregex instances, the first of which always \
        represents the `match` pattern, while the rest constitute `assertion` patterns.
    :param (tuple[Pregex | str] => str) transform: A `transform` function for the provided patterns.

    :raises NotEnoughArgumentsException: No assertion patterns were provided.
    :raises EmptyNegativeAssertionException: The empty string is provided \
        as one of the assertion patterns.
    '''
    def __init__(self, pres: tuple[_pre.Pregex or str], transform) -> _pre.Pregex:
        '''
        Constitutes the base class for classes ``NotFollowedBy`` and ``NotPrecededBy`` \
            that are part of this module.

        :param Pregex | str *pres: Two or more Pregex instances, the first of which always \
            represents the `match` pattern, while the rest constitute `assertion` patterns.
        :param (tuple[Pregex | str] => str) transform: A `transform` function for the provided patterns.

        :raises NotEnoughArgumentsException: No assertion patterns were provided.
        :raises EmptyNegativeAssertionException: The empty string is provided \
            as one of the assertion patterns.
        '''
        if len(pres) < 2:
            message = "At least one assertion pattern is required."
            raise _ex.NotEnoughArgumentsException(message)
        result = __class__._to_pregex(pres[0])
        for pre in pres[1:]:
            pre = __class__._to_pregex(pre)
            if pre._get_type() == _pre._Type.Empty:
                result = _pre.Empty()
                raise _ex.EmptyNegativeAssertionException()
            result = _pre.Pregex(transform(result, pre), escape=False)
        super().__init__(str(result))


class MatchAtStart(__Anchor):
    '''
    Matches the provided pattern only if said pattern is at the start of the string.

    :param Pregex | str pre: The pattern that is to be matched.

    :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
        ``Pregex`` instance nor a string.

    :note: Cannot have a repeating quantifier applied to it.
    '''

    def __init__(self, pre: _pre.Pregex or str):
        '''
        Matches the provided pattern only if said pattern is at the start of the string.

        :param Pregex | str pre: The pattern that is to be matched.

        :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
            ``Pregex`` instance nor a string.

        :note: Cannot have a repeating quantifier applied to it.
        '''
        super().__init__(pre, lambda pre: str(pre._match_at_start()))


class MatchAtEnd(__Anchor):
    '''
    Matches the provided pattern only if said pattern is at the end of the string.

    :param Pregex | str pre: The pattern that is to be matched.

    :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
        ``Pregex`` instance nor a string.

    :note: Cannot have a repeating quantifier applied to it.
    '''

    def __init__(self, pre: _pre.Pregex or str):
        '''
        Matches the provided pattern only if said pattern is at the end of the string.

        :param Pregex | str pre: The pattern that is to be matched.

        :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
            ``Pregex`` instance nor a string.

        :note: Cannot have a repeating quantifier applied to it.
        '''
        super().__init__(pre, lambda pre: str(pre._match_at_end()))


class MatchAtLineStart(__Anchor):
    '''
    Matches the provided pattern only if said pattern is at the start of a line.

    :param Pregex | str pre: The pattern that is to be matched.

    :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
        ``Pregex`` instance nor a string.

    :note:
        - Cannot have a repeating quantifier applied to it.
        - Uses meta character ``^`` since the `MULTILINE` flag is considered on.
    '''

    def __init__(self, pre: _pre.Pregex or str):
        '''
        Matches the provided pattern only if said pattern is at the end of the string.

        :param Pregex | str pre: The pattern that is to be matched.

        :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
            ``Pregex`` instance nor a string.

        :note:
            - Cannot have a repeating quantifier applied to it.
            - Uses meta character ``^`` since the `MULTILINE` flag is considered on.
        '''
        super().__init__(pre, lambda pre: str(pre._match_at_line_start()))


class MatchAtLineEnd(__Anchor):
    '''
    Matches the provided pattern only if said pattern is at the end of a line.

    :param Pregex | str pre: The pattern that is to be matched.

    :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
        ``Pregex`` instance nor a string.

    :note:
        - Cannot have a repeating quantifier applied to it.
        - Uses meta character ``$`` since the `MULTILINE` flag is considered on.
    '''

    def __init__(self, pre: _pre.Pregex or str):
        '''
        Matches the provided pattern only if said pattern is at the end of a line.

        :param Pregex | str pre: The pattern that is to be matched.

        :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
            ``Pregex`` instance nor a string.

        :note:
            - Cannot have a repeating quantifier applied to it.
            - Uses meta character ``$`` since the `MULTILINE` flag is considered on.
        '''
        super().__init__(pre, lambda pre: str(pre._match_at_line_end()))


class WordBoundary(__Anchor):
    '''
    Asserts that the position, at which an instance of this class is placed, \
    must constitute a word boundary.
    '''

    def __init__(self):
        '''
        Asserts that the position, at which an instance of this class is placed, \
        must constitute a word boundary.
        '''
        super().__init__(_pre.Empty(), lambda pre: str(pre + _pre.Pregex("\\b", escape=False)))


class NonWordBoundary(__Anchor):
    '''
    Asserts that the position, at which an instance of this class is placed, \
    must not constitute a word boundary.
    '''

    def __init__(self):
        '''
        Asserts that the position, at which an instance of this class is placed, \
        must not constitute a word boundary.
        '''
        super().__init__(_pre.Empty(), lambda pre: str(pre + _pre.Pregex("\\B", escape=False)))


class FollowedBy(__PositiveLookaround):
    '''
    Matches pattern ``match`` only if it is followed by pattern \
    ``assertion``, without the latter being included into the match.

    :param Pregex | str match: A Pregex instance or string \
        representing the `match` pattern.
    :param Pregex | str assertion: A Pregex instance or string \
        representing the `assertion` pattern.

    :raises InvalidArgumentTypeException: At least one of the provided arguments \
        is neither a ``Pregex`` instance nor a string.

    :note: Cannot have a repeating quantifier applied to it.
    '''

    def __init__(self, match: _pre.Pregex or str, assertion: _pre.Pregex or str):
        '''
        Matches pattern ``match`` only if it is followed by pattern \
        ``assertion``, without the latter being included into the match.

        :param Pregex | str match: A Pregex instance or string \
            representing the `match` pattern.
        :param Pregex | str assertion: A Pregex instance or string \
            representing the `assertion` pattern.

        :raises InvalidArgumentTypeException: At least one of the provided arguments \
            is neither a ``Pregex`` instance nor a string.

        :note: Cannot have a repeating quantifier applied to it.
        '''
        super().__init__(match, assertion, lambda pre1, pre2: str(pre1._followed_by(pre2)))


class NotFollowedBy(__NegativeLookaround):
    '''
    Matches pattern ``match`` only if it is not followed by any one of \
    the provided ``assertion`` patterns.

    :param Pregex | str match: The pattern that is to be matched.
    :param Pregex | str \*assertions: One or more patterns, none of which must \
        come right after ``match`` in order for it to be considered a match.

    :raises NotEnoughArgumentsException: No assertion patterns were provided.
    :raises InvalidArgumentTypeException: At least one of the provided arguments \
        is neither a ``Pregex`` instance nor a string.
    :raises EmptyNegativeAssertionException: At least one of the provided assertion \
        patterns is the empty-string pattern.
    '''

    def __init__(self, match: _pre.Pregex or str, *assertions: _pre.Pregex or str):
        '''
        Matches pattern ``match`` only if it is not followed by any one of \
        the provided ``assertion`` patterns.

        :param Pregex | str match: The pattern that is to be matched.
        :param Pregex | str \*assertions: One or more patterns, none of which must \
            come right after ``match`` in order for it to be considered a match.

        :raises NotEnoughArgumentsException: No assertion patterns were provided.
        :raises InvalidArgumentTypeException: At least one of the provided arguments \
            is neither a ``Pregex`` instance nor a string.
        :raises EmptyNegativeAssertionException: At least one of the provided assertion \
            patterns is the empty-string pattern.
        '''
        super().__init__((match, *assertions),
            lambda pre1, pre2: str(pre1._not_followed_by(pre2)))


class PrecededBy(__PositiveLookaround):
    '''
    Matches pattern ``match`` only if it is preceded by pattern \
    ``assertion``, without the latter being included into the match.

    :param Pregex | str match: A Pregex instance or string \
        representing the `match` pattern.
    :param Pregex | str assertion: A Pregex instance or string \
        representing the `assertion` pattern.

    :raises InvalidArgumentTypeException: At least one of the provided arguments \
        is neither a ``Pregex`` instance nor a string.
    :raises NonFixedWidthPatternException: A non-fixed-width pattern \
        is provided in place of parameter ``assertion``.

    :note: Cannot have a repeating quantifier applied to it.
    '''

    def __init__(self, match: _pre.Pregex or str, assertion: _pre.Pregex or str):
        '''
        Matches pattern ``match`` only if it is preceded by pattern \
        ``assertion``, without the latter being included into the match.

        :param Pregex | str match: A Pregex instance or string \
            representing the `match` pattern.
        :param Pregex | str assertion: A Pregex instance or string \
            representing the `assertion` pattern.

        :raises InvalidArgumentTypeException: At least one of the provided arguments \
            is neither a ``Pregex`` instance nor a string.
        :raises NonFixedWidthPatternException: A non-fixed-width pattern \
            is provided in place of parameter ``assertion``.

        :note: Cannot have a repeating quantifier applied to it.
        '''
        if isinstance(assertion, _pre.Pregex):
            if assertion._get_type() == _pre._Type.Quantifier \
                and (not isinstance(assertion, _Exactly)):
                raise _ex.NonFixedWidthPatternException(self, assertion)
        super().__init__(match, assertion, lambda pre1, pre2: str(pre1._preceded_by(pre2)))   


class NotPrecededBy(__NegativeLookaround):
    '''
    Matches pattern ``match`` only if it is not preceded by any one of \
    the provided ``assertion`` patterns.

    :param Pregex | str match: The pattern that is to be matched.
    :param Pregex | str \*assertions: One or more patterns, none of which must \
        come right before ``match`` in order for it to be considered a match.

    :raises NotEnoughArgumentsException: No assertion patterns were provided.
    :raises InvalidArgumentTypeException: At least one of the provided arguments \
        is neither a ``Pregex`` instance nor a string.
    :raises EmptyNegativeAssertionException: At least one of the provided assertion \
        patterns is the empty-string pattern.
    :raises NonFixedWidthPatternException: At least one of the provided assertion \
        patterns is a non-fixed-width pattern.
    '''

    def __init__(self, match: _pre.Pregex or str, *assertions: _pre.Pregex or str):
        '''
        Matches pattern ``match`` only if it is not preceded by any one of \
        the provided ``assertion`` patterns.

        :param Pregex | str match: The pattern that is to be matched.
        :param Pregex | str \*assertions: One or more patterns, none of which must \
            come right before ``match`` in order for it to be considered a match.

        :raises NotEnoughArgumentsException: No assertion patterns were provided.
        :raises InvalidArgumentTypeException: At least one of the provided arguments \
            is neither a ``Pregex`` instance nor a string.
        :raises EmptyNegativeAssertionException: At least one of the provided assertion \
            patterns is the empty-string pattern.
        :raises NonFixedWidthPatternException: At least one of the provided assertion \
            patterns is a non-fixed-width pattern.
        '''
        for pre in assertions:
            if isinstance(pre, _pre.Pregex):
                if pre._get_type() == _pre._Type.Quantifier and (not isinstance(pre, _Exactly)):
                    raise _ex.NonFixedWidthPatternException(self, pre)
        super().__init__((match, *assertions), lambda pre1, pre2: str(pre1._not_preceded_by(pre2)))


class EnclosedBy(__PositiveLookaround):
    '''
    Matches pattern ``match`` only if it is both preceded and followed \
    by pattern ``assertion``, without the latter being included into the match.

    :param Pregex | str match: A Pregex instance or string \
        representing the `match` pattern.
    :param Pregex | str assertion: A Pregex instance or string \
        representing the *assertion* pattern.

    :raises InvalidArgumentTypeException: At least one of the provided arguments \
        is neither a ``Pregex`` instance nor a string.
    :raises NonFixedWidthPatternException: Parameter ``assertion`` \
        corresponds to a non-fixed-width pattern.

    :note: Cannot have a repeating quantifier applied to it.
    '''

    def __init__(self, match: _pre.Pregex or str, assertion: _pre.Pregex or str):
        '''
        Matches pattern ``match`` only if it is both preceded and followed \
        by pattern ``assertion``, without the latter being included into the match.

        :param Pregex | str match: A Pregex instance or string \
            representing the `match` pattern.
        :param Pregex | str assertion: A Pregex instance or string \
            representing the *assertion* pattern.

        :raises InvalidArgumentTypeException: At least one of the provided arguments \
            is neither a ``Pregex`` instance nor a string.
        :raises NonFixedWidthPatternException: Parameter ``assertion`` \
            corresponds to a non-fixed-width pattern.

        :note: Cannot have a repeating quantifier applied to it.
        '''
        if isinstance(assertion, _pre.Pregex):
            if assertion._get_type() == _pre._Type.Quantifier \
                and (not isinstance(assertion, _Exactly)):
                raise _ex.NonFixedWidthPatternException(self, assertion)
        super().__init__(match, assertion, lambda pre1, pre2: str(pre1._enclosed_by(pre2)))    


class NotEnclosedBy(__NegativeLookaround):
    '''
    Matches pattern ``match`` only if it neither preceded nor followed \
    by any one of the provided ``assertion`` patterns.

    :param Pregex | str match: The pattern that is to be matched.
    :param Pregex | str \*assertions: One or more patterns, none of which must \
        come right before ``match`` in order for it to be considered a match.

    :raises NotEnoughArgumentsException: No assertion patterns were provided.
    :raises InvalidArgumentTypeException: At least one of the provided arguments \
        is neither a ``Pregex`` instance nor a string.
    :raises EmptyNegativeAssertionException: Parameter ``assertion`` \
        corresponds to the empty-string pattern.
    :raises NonFixedWidthPatternException: Parameter ``assertion`` \
        corresponds to a non-fixed-width pattern.
    '''

    def __init__(self, match: _pre.Pregex or str, *assertions: _pre.Pregex or str):
        '''
        Matches pattern ``match`` only if it neither preceded nor followed \
        by any one of the provided ``assertion`` patterns.

        :param Pregex | str match: The pattern that is to be matched.
        :param Pregex | str \*assertions: One or more patterns, none of which must \
            come right before ``match`` in order for it to be considered a match.

        :raises NotEnoughArgumentsException: No assertion patterns were provided.
        :raises InvalidArgumentTypeException: At least one of the provided arguments \
            is neither a ``Pregex`` instance nor a string.
        :raises EmptyNegativeAssertionException: Parameter ``assertion`` \
            corresponds to the empty-string pattern.
        :raises NonFixedWidthPatternException: Parameter ``assertion`` \
            corresponds to a non-fixed-width pattern.
        '''
        for pre in assertions:
            if isinstance(pre, _pre.Pregex):
                if pre._get_type() == _pre._Type.Quantifier and (not isinstance(pre, _Exactly)):
                    raise _ex.NonFixedWidthPatternException(self, pre)
        super().__init__((match, *assertions), lambda pre1, pre2: str(pre1._not_enclosed_by(pre2))) 