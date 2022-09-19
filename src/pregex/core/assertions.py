__doc__ = """
All classes within this module "assert" something about the provided pattern
without having to match any additional characters. For example, :class:`MatchAtStart`
ensures that the provided pattern matches only when it is found at the start of the string,
while :class:`NotFollowedBy` asserts that a match must not be followed by one or more
specified patterns. Another thing you should keep in mind is that many of these assertions
cannot be repeated, as attempting that will cause a ``CannotBeRepeatedException`` exception
to be thrown.

Classes & methods
-------------------------------------------

Below are listed all classes within :py:mod:`pregex.core.assertions`
along with any possible methods they may possess.
"""


import pregex.core.pre as _pre
import pregex.core.exceptions as _ex
from typing import Union as _Union


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
    def __init__(self, pre: _Union[_pre.Pregex, str], transform):
        '''
        Constitutes the base class for all `anchor` classes that are part of this module.

        :param Pregex | str pre: A Pregex instance or string representing the `anchor` pattern.
        :param (Pregex => str) transform: A `transform` function for the provided pattern.

        :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a ``Pregex`` instance \
            nor a string.
        '''
        super().__init__(str(transform(__class__._to_pregex(pre))))


class __Lookaround(__Assertion):
    '''
    Constitutes the base class for all "Lookaround" classes.

    :param Pregex | str pres: Two or more Pregex instances, the first of which always \
        represents the `match` pattern, while the rest constitute `assertion` patterns.
    :param (tuple[Pregex | str] => str) transform: A `transform` function for the provided patterns.

    :raises NotEnoughArgumentsException: No assertion patterns were provided.
    :raises EmptyNegativeAssertionException: The empty string is provided \
        as one of the assertion patterns.
    '''
    def __init__(self, pres: tuple[_Union[_pre.Pregex, str]], transform) -> _pre.Pregex:
        '''
        Constitutes the base class for all "Lookaround" classes.

        :param Pregex | str pres: Two or more Pregex instances, the first of which always \
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
            result = transform(result, pre)
        super().__init__(str(result))


class MatchAtStart(__Anchor):
    '''
    Matches the provided pattern only if it is at the start of the string.

    :param Pregex | str pre: The pattern that is to be matched.

    :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
        ``Pregex`` instance nor a string.

    :note: The resulting pattern cannot have a repeating quantifier applied to it.
    '''

    def __init__(self, pre: _Union[_pre.Pregex, str]):
        '''
        Matches the provided pattern only if it is at the start of the string.

        :param Pregex | str pre: The pattern that is to be matched.

        :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
            ``Pregex`` instance nor a string.

        :note: The resulting pattern cannot have a repeating quantifier applied to it.
        '''
        super().__init__(pre, lambda pre: pre.match_at_start())


class MatchAtEnd(__Anchor):
    '''
    Matches the provided pattern only if it is at the end of the string.

    :param Pregex | str pre: The pattern that is to be matched.

    :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
        ``Pregex`` instance nor a string.

    :note: The resulting pattern cannot have a repeating quantifier applied to it.
    '''

    def __init__(self, pre: _Union[_pre.Pregex, str]):
        '''
        Matches the provided pattern only if it is at the end of the string.

        :param Pregex | str pre: The pattern that is to be matched.

        :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
            ``Pregex`` instance nor a string.

        :note: The resulting pattern cannot have a repeating quantifier applied to it.
        '''
        super().__init__(pre, lambda pre: pre.match_at_end())


class MatchAtLineStart(__Anchor):
    '''
    Matches the provided pattern only if it is at the start of a line.

    :param Pregex | str pre: The pattern that is to be matched.

    :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
        ``Pregex`` instance nor a string.

    :note:
        - The resulting pattern cannot have a repeating quantifier applied to it.
        - Uses meta character ``^`` since the `MULTILINE` flag is considered on.
    '''

    def __init__(self, pre: _Union[_pre.Pregex, str]):
        '''
        Matches the provided pattern only if it is at the start of a line.

        :param Pregex | str pre: The pattern that is to be matched.

        :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
            ``Pregex`` instance nor a string.

        :note:
            - The resulting pattern cannot have a repeating quantifier applied to it.
            - Uses meta character ``^`` since the `MULTILINE` flag is considered on.
        '''
        super().__init__(pre, lambda pre: pre.match_at_line_start())


class MatchAtLineEnd(__Anchor):
    '''
    Matches the provided pattern only if it is at the end of a line.

    :param Pregex | str pre: The pattern that is to be matched.

    :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
        ``Pregex`` instance nor a string.

    :note:
        - The resulting pattern cannot have a repeating quantifier applied to it.
        - Uses meta character ``$`` since the `MULTILINE` flag is considered on.
    '''

    def __init__(self, pre: _Union[_pre.Pregex, str]):
        '''
        Matches the provided pattern only if it is at the end of a line.

        :param Pregex | str pre: The pattern that is to be matched.

        :raises InvalidArgumentTypeException: Parameter ``pre`` is neither a \
            ``Pregex`` instance nor a string.

        :note:
            - The resulting pattern cannot have a repeating quantifier applied to it.
            - Uses meta character ``$`` since the `MULTILINE` flag is considered on.
        '''
        super().__init__(pre, lambda pre: pre.match_at_line_end())


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
        super().__init__(_pre.Pregex(), lambda pre: pre.concat(_pre.Pregex("\\b", escape=False)))


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
        super().__init__(_pre.Pregex(), lambda pre: pre.concat(_pre.Pregex("\\B", escape=False)))


class FollowedBy(__Lookaround):
    '''
    Matches pattern ``match`` only if it is directly followed \
    by all of the provided ``assertion`` patterns.

    :param Pregex | str match: A Pregex instance or string \
        representing the `match` pattern.
    :param Pregex | str \*assertions: One or more patterns, all of which must \
        come right after pattern ``match`` in order for it to be considered a match.

    :raises NotEnoughArgumentsException: No assertion patterns were provided.
    :raises InvalidArgumentTypeException: At least one of the provided arguments \
        is neither a ``Pregex`` instance nor a string.

    :note: The resulting pattern cannot have a repeating quantifier applied to it.
    '''

    def __init__(self, match: _Union[_pre.Pregex, str], *assertions: _Union[_pre.Pregex, str]):
        '''
        Matches pattern ``match`` only if it is directly followed \
        by all of the provided ``assertion`` patterns.

        :param Pregex | str match: A Pregex instance or string \
            representing the `match` pattern.
        :param Pregex | str \*assertions: One or more patterns, all of which must \
            come right after pattern ``match`` in order for it to be considered a match.

        :raises NotEnoughArgumentsException: No assertion patterns were provided.
        :raises InvalidArgumentTypeException: At least one of the provided arguments \
            is neither a ``Pregex`` instance nor a string.

        :note: The resulting pattern cannot have a repeating quantifier applied to it.
        '''
        super().__init__((match, *assertions), lambda pre1, pre2: pre1.followed_by(pre2))


class PrecededBy(__Lookaround):
    '''
    Matches pattern ``match`` only if it is directly preceded \
    by all of the provided ``assertion`` patterns.

    :param Pregex | str match: A Pregex instance or string \
        representing the `match` pattern.
    :param Pregex | str \*assertions: One or more patterns, all of which must \
        come right before pattern ``match`` in order for it to be considered a match.

    :raises NotEnoughArgumentsException: No assertion patterns were provided.
    :raises InvalidArgumentTypeException: At least one of the provided arguments \
        is neither a ``Pregex`` instance nor a string.
    :raises NonFixedWidthPatternException: Parameter ``assertion`` \
        corresponds to a pattern that does not have a fixed width.

    :note: The resulting pattern cannot have a repeating quantifier applied to it.
    '''

    def __init__(self, match: _Union[_pre.Pregex, str], *assertions: _Union[_pre.Pregex, str]):
        '''
        Matches pattern ``match`` only if it is directly preceded \
        by all of the provided ``assertion`` patterns.

        :param Pregex | str match: A Pregex instance or string \
            representing the `match` pattern.
        :param Pregex | str \*assertions: One or more patterns, all of which must \
            come right before pattern ``match`` in order for it to be considered a match.

        :raises NotEnoughArgumentsException: No assertion patterns were provided.
        :raises InvalidArgumentTypeException: At least one of the provided arguments \
            is neither a ``Pregex`` instance nor a string.
        :raises NonFixedWidthPatternException: Parameter ``assertion`` \
            corresponds to a pattern that does not have a fixed width.

        :note: The resulting pattern cannot have a repeating quantifier applied to it.
        '''
        super().__init__((match, *assertions), lambda pre1, pre2: pre1.preceded_by(pre2))


class EnclosedBy(__Lookaround):
    '''
    Matches pattern ``match`` only if it is both directly preceded \
    and followed by all of the provided ``assertion`` patterns.

    :param Pregex | str match: A Pregex instance or string \
        representing the `match` pattern.
    :param Pregex | str \*assertions: One or more patterns, all of which must \
        come both right before and right after pattern ``match`` in order for \
        it to be considered a match.

    :raises NotEnoughArgumentsException: No assertion patterns were provided.
    :raises InvalidArgumentTypeException: At least one of the provided arguments \
        is neither a ``Pregex`` instance nor a string.
    :raises NonFixedWidthPatternException: Parameter ``assertion`` \
        corresponds to a pattern that does not have a fixed width.

    :note: The resulting pattern cannot have a repeating quantifier applied to it.
    '''

    def __init__(self, match: _Union[_pre.Pregex, str], *assertions: _Union[_pre.Pregex, str]):
        '''
        Matches pattern ``match`` only if it is both directly preceded \
        and followed by all of the provided ``assertion`` patterns.

        :param Pregex | str match: A Pregex instance or string \
            representing the `match` pattern.
        :param Pregex | str \*assertions: One or more patterns, all of which must \
            come both right before and right after pattern ``match`` in order for \
            it to be considered a match.

        :raises NotEnoughArgumentsException: No assertion patterns were provided.
        :raises InvalidArgumentTypeException: At least one of the provided arguments \
            is neither a ``Pregex`` instance nor a string.
        :raises NonFixedWidthPatternException: Parameter ``assertion`` \
            corresponds to a pattern that does not have a fixed width.

        :note: The resulting pattern cannot have a repeating quantifier applied to it.
        '''
        super().__init__((match, *assertions), lambda pre1, pre2: pre1.enclosed_by(pre2))


class NotFollowedBy(__Lookaround):
    '''
    Matches pattern ``match`` only if it is not directly followed by \
    any one of the provided ``assertions`` patterns.

    :param Pregex | str match: The pattern that is to be matched.
    :param Pregex | str \*assertions: One or more patterns, none of which must \
        come right after pattern ``match`` in order for it to be considered a match.

    :raises NotEnoughArgumentsException: No assertion patterns were provided.
    :raises InvalidArgumentTypeException: At least one of the provided arguments \
        is neither a ``Pregex`` instance nor a string.
    :raises EmptyNegativeAssertionException: At least one of the provided assertion \
        patterns is the empty-string pattern.
    '''

    def __init__(self, match: _Union[_pre.Pregex, str], *assertions: _Union[_pre.Pregex, str]):
        '''
        Matches pattern ``match`` only if it is not directly followed by \
        any one of the provided ``assertions`` patterns.

        :param Pregex | str match: The pattern that is to be matched.
        :param Pregex | str \*assertions: One or more patterns, none of which must \
            come right after pattern ``match`` in order for it to be considered a match.

        :raises NotEnoughArgumentsException: No assertion patterns were provided.
        :raises InvalidArgumentTypeException: At least one of the provided arguments \
            is neither a ``Pregex`` instance nor a string.
        :raises EmptyNegativeAssertionException: At least one of the provided assertion \
            patterns is the empty-string pattern.
        '''
        super().__init__((match, *assertions),
            lambda pre1, pre2: pre1.not_followed_by(pre2))


class NotPrecededBy(__Lookaround):
    '''
    Matches pattern ``match`` only if it is not directly preceded by \
    any one of the provided ``assertions`` patterns.

    :param Pregex | str match: The pattern that is to be matched.
    :param Pregex | str \*assertions: One or more patterns, none of which must \
        come right before pattern ``match`` in order for it to be considered a match.

    :raises NotEnoughArgumentsException: No assertion patterns were provided.
    :raises InvalidArgumentTypeException: At least one of the provided arguments \
        is neither a ``Pregex`` instance nor a string.
    :raises EmptyNegativeAssertionException: At least one of the provided assertion \
        patterns is the empty-string pattern.
    :raises NonFixedWidthPatternException: At least one of the provided assertion \
        patterns does not have a fixed width.
    '''

    def __init__(self, match: _Union[_pre.Pregex, str], *assertions: _Union[_pre.Pregex, str]):
        '''
        Matches pattern ``match`` only if it is not directly preceded by \
        any one of the provided ``assertions`` patterns.

        :param Pregex | str match: The pattern that is to be matched.
        :param Pregex | str \*assertions: One or more patterns, none of which must \
            come right before pattern ``match`` in order for it to be considered a match.

        :raises NotEnoughArgumentsException: No assertion patterns were provided.
        :raises InvalidArgumentTypeException: At least one of the provided arguments \
            is neither a ``Pregex`` instance nor a string.
        :raises EmptyNegativeAssertionException: At least one of the provided assertion \
            patterns is the empty-string pattern.
        :raises NonFixedWidthPatternException: At least one of the provided assertion \
            patterns does not have a fixed width.
        '''
        super().__init__((match, *assertions),
            lambda pre1, pre2: pre1.not_preceded_by(pre2))


class NotEnclosedBy(__Lookaround):
    '''
    Matches pattern ``match`` only if it is neither directly preceded \
    nor followed by any one of the provided ``assertions`` patterns.

    :param Pregex | str match: The pattern that is to be matched.
    :param Pregex | str \*assertions: One or more patterns, none of which must \
        come either right before or right after pattern ``match`` in order for \
        it to be considered a match.

    :raises NotEnoughArgumentsException: No assertion patterns were provided.
    :raises InvalidArgumentTypeException: At least one of the provided arguments \
        is neither a ``Pregex`` instance nor a string.
    :raises EmptyNegativeAssertionException: At least one of the provided assertion \
        patterns is the empty-string pattern.
    :raises NonFixedWidthPatternException: At least one of the provided assertion \
        patterns does not have a fixed width.
    '''

    def __init__(self, match: _Union[_pre.Pregex, str], *assertions: _Union[_pre.Pregex, str]):
        '''
        Matches pattern ``match`` only if it is neither directly preceded \
        nor followed by any one of the provided ``assertions`` patterns.

        :param Pregex | str match: The pattern that is to be matched.
        :param Pregex | str \*assertions: One or more patterns, none of which must \
            come either right before or right after pattern ``match`` in order for \
            it to be considered a match.

        :raises NotEnoughArgumentsException: No assertion patterns were provided.
        :raises InvalidArgumentTypeException: At least one of the provided arguments \
            is neither a ``Pregex`` instance nor a string.
        :raises EmptyNegativeAssertionException: At least one of the provided assertion \
            patterns is the empty-string pattern.
        :raises NonFixedWidthPatternException: At least one of the provided assertion \
            patterns does not have a fixed width.
        '''
        super().__init__((match, *assertions),
            lambda pre1, pre2: pre1.not_enclosed_by(pre2))