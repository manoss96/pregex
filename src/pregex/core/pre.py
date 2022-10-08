__doc__ = """
This module a single class, namely :class:`Pregex`, which
constitutes the base class for every other class within `pregex`.

Classes & methods
-------------------------------------------

Below are listed all classes within :py:mod:`pregex.core.pre`
along with any possible methods they may possess.
"""


import re as _re
import enum as _enum
import pregex.core.exceptions as _ex
from typing import Union as _Union
from typing import Optional as _Optional
from typing import Iterator as _Iterator


class _Type(_enum.Enum):
    '''
    This enum represents all possible types of a RegEx pattern.
    '''
    Alternation = 0
    Assertion = 1
    Class = 2
    Empty = 3
    Group = 4
    Other = 5
    Quantifier = 6
    Token = 7


class Pregex():
    '''
    Wraps the provided pattern within an instance of this class.

    :param str pattern: The pattern that is to be wrapped within an instance \
        of this class. Defaults to the empty string ``''``.
    :param bool escape: Determines whether to escape the provided pattern or not. \
        Defaults to ``True``.

    :raises InvalidArgumentTypeException: Parameter ``pattern`` is not a string.

    :note: This class constitutes the base class for every other class within the `pregex` package.
    '''

    '''
    Determines the groupping rules of each Pregex instance type:

    :schema: __groupping_rules[type] => (on_concat, on_quantify, on_assertion)
    '''
    __groupping_rules: dict[_Type, str] = {
        _Type.Alternation: (True, True, True),
        _Type.Assertion : (False, True, False),
        _Type.Class: (False, False, False),
        _Type.Empty: (False, False, False),
        _Type.Group: (False, False, False),
        _Type.Other: (False, True, False),
        _Type.Quantifier: (False, True, False),
        _Type.Token: (False, False, False),
    }


    '''
    The totality of active RegEx flags.
    '''
    __flags: _re.RegexFlag = _re.MULTILINE | _re.DOTALL


    def __init__(self, pattern: str = '', escape: bool = True) -> 'Pregex':
        '''
        Wraps the provided pattern within an instance of this class.

        :param str pattern: The pattern that is to be wrapped within an instance \
            of this class. Defaults to the empty string ``''``.
        :param bool escape: Determines whether to escape the provided pattern or not. \
            Defaults to ``True``.

        :raises InvalidArgumentTypeException: Parameter ``pattern`` is not a string.

        :note: This class constitutes the base class for every other class within the `pregex` package.
        '''
        if not isinstance(pattern, str):
            message = "Provided argument \"pattern\" is not a string."
            raise _ex.InvalidArgumentTypeException(message)
        if escape:
            self.__pattern = __class__.__escape(pattern)
        else:
            self.__pattern = pattern
        self.__type, self.__repeatable = __class__.__infer_type(self.__pattern)
        self.__compiled: _re.Pattern = None


    '''
    Public Methods
    '''
    def print_pattern(self, include_flags: bool = False) -> None:
        '''
        Prints this instance's underlying RegEx pattern.

        :param bool include_flags: Determines whether to display the \
            used RegEx flags along with the pattern. Defaults to ``False``.
        '''
        print(self.get_pattern(include_flags))


    def get_pattern(self, include_flags: bool = False) -> str:
        '''
        Returns this instance's underlying RegEx pattern as a string.

        :param bool include_flags: Determines whether to display the \
            used RegEx flags along with the pattern. Defaults to ``False``.

        :note: This method is to be preferred over str() when one needs \
            to display this instance's underlying Regex pattern.
        '''
        pattern = repr(self)
        return f"/{pattern}/gmsu" if include_flags else pattern


    def get_compiled_pattern(self, discard_after: bool = True) -> _re.Pattern:
        '''
        Returns this instance's underlying RegEx pattern as a ``re.Pattern`` instance.
        
        :param bool discard_after: Determines whether the compiled pattern is to be \
            discarded after the program has exited from this method, or to be retained \
            so that any further attempt at matching a string will use the compiled pattern \
            instead of the regular one. Defaults to ``True``.
        '''
        if self.__compiled is None:
            self.compile()
        compiled = self.__compiled
        if discard_after:
            self.__compiled = None
        return compiled


    def compile(self) -> None:
        '''
        Compiles the underlying RegEx pattern. After invoking this method, \
        any further attempt at matching a string will be making use of the \
        compiled RegEx pattern.
        '''
        self.__compiled = _re.compile(self.get_pattern(), flags=self.__flags)


    @staticmethod
    def purge() -> None:
        '''
        Clears the regular expression caches.
        '''
        _re.purge()


    def has_match(self, source: str, is_path: bool = False) -> bool:
        '''
        Returns ``True`` if at least one match is found within the provided text.

        :param str source: The text that is to be examined.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.
        '''
        if is_path:
            source = self.__extract_text(source)
        return bool(_re.search(self.__pattern, source) if self.__compiled is None \
            else self.__compiled.search(source))


    def is_exact_match(self, source: str, is_path: bool = False) -> bool:
        '''
        Returns ``True`` only if the provided text matches this pattern exactly.

        :param str source: The text that is to be examined.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.
        '''
        if is_path:
            source = self.__extract_text(source)
        return bool(_re.fullmatch(self.__pattern, source, flags=self.__flags) \
            if self.__compiled is None else self.__compiled.fullmatch(source))


    def iterate_matches(self, source: str, is_path: bool = False) -> _Iterator[str]:
        '''
        Generates any possible matches found within the provided text.

        :param str source: The text that is to be examined.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.
        '''
        for match in self.__iterate_match_objects(source, is_path):
            yield match.group(0)


    def iterate_matches_and_pos(self, source: str, is_path: bool = False) -> _Iterator[tuple[str, int, int]]:
        '''
        Generates any possible matches found within the provided text \
        along with their exact position.

        :param str source: The text that is to be examined.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.
        '''
        for match in self.__iterate_match_objects(source, is_path):
            yield (match.group(0), *match.span())


    def iterate_captures(self, source: str, include_empty: bool = True,
        is_path: bool = False) -> _Iterator[tuple[str]]:
        '''
        Generates tuples, one tuple per match, where each tuple contains \
        all of its corresponding match's captured groups.

        :param str source: The text that is to be examined.
        :param bool include_empty: Determines whether to include empty captures \
            into the results. Defaults to ``True``.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.

        :note: In case there exists an optional capturing group within the pattern, \
            that has not been captured by a match, then that capture's corresponding \
            value will be ``None``.
        '''
        for match in self.__iterate_match_objects(source, is_path):
            yield match.groups() if include_empty else \
                tuple(group for group in match.groups() if group != '')


    def iterate_captures_and_pos(self, source: str, include_empty: bool = True,
        relative_to_match : bool = False, is_path: bool = False) -> _Iterator[list[tuple[str, int, int]]]:
        '''
        Generates lists of tuples, one list per match, where each tuple contains one \
        of its corresponding match's captured groups along with its exact position \
        within the text.

        :param str source: The text that is to be examined.
        :param bool include_empty: Determines whether to include empty captures into the \
            results. Defaults to ``True``.
        :param bool relative_to_match: If ``True``, then each group's position-indices \
            are calculated relative to the group's corresponding match, not to the whole \
            string. Defaults to ``False``.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.

        :note: In case there exists an optional capturing group within the pattern, \
            that has not been captured by a match, then that capture's corresponding \
            tuple will be ``(None, -1, -1)``.
        '''
        for match in self.__iterate_match_objects(source, is_path):
            groups, counter = list(), 0
            for group in match.groups():
                counter += 1
                if include_empty or (group != ''):
                    start, end = match.span(counter)
                    if relative_to_match and start > -1:
                        start, end = start - match.start(0), end - match.start(0)
                    groups.append((group, start, end))
            yield groups


    def iterate_named_captures(self, source: str, include_empty: bool = True,
        is_path: bool = False) -> _Iterator[dict[str, str]]:
        '''
        Generates dictionaries, one dictionary per match, where each dictionary \
        contains key-value pairs of any named captured groups that belong to its \
        corresponding match, with each key being the name of the captured group, \
        whereas its corresponding value will be the actual captured text.

        :param str source: The text that is to be examined.
        :param bool include_empty: Determines whether to include empty captures \
            into the results. Defaults to ``True``.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.

        :note: In case there exists an optional capturing group within the pattern, \
            that has not been captured by a match, then that capture's corresponding \
            key-value pair will be ``name --> None``.
        '''
        for match in self.__iterate_match_objects(source, is_path):
            yield match.groupdict() if include_empty else \
                {k : v for k, v in match.groupdict().items() if v != ''}


    def iterate_named_captures_and_pos(self, source: str, include_empty: bool = True,
        relative_to_match : bool = False, is_path: bool = False) -> _Iterator[dict[str, tuple[str, int, int]]]:
        '''
        Generates dictionaries, one dictionary per match, where each dictionary \
        contains key-value pairs of any named captured groups that belong to its\
        corresponding match, with each key being the name of the captured group, \
        whereas its corresponding value will be a tuple containing the actual \
        captured group along with its exact position within the text.

        :param str source: The text that is to be examined.
        :param bool include_empty: Determines whether to include empty captures into the \
            results. Defaults to ``True``.
        :param bool relative_to_match: If ``True``, then each group's position-indices \
            are calculated relative to the group's corresponding match, not to the whole \
            string. Defaults to ``False``.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.

        :note: In case there exists an optional capturing group within the pattern, \
            that has not been captured by a match, then that capture's corresponding \
            key-value pair will be ``name --> (None, -1, -1)``.
        '''
        for match in self.__iterate_match_objects(source, is_path):
            groups, counter = dict(), 0
            for k, v in match.groupdict().items():
                counter += 1
                if include_empty or (v != ''):
                    start, end = match.span(counter)
                    if relative_to_match and start > -1:
                        start, end = start - match.start(0), end - match.start(0)
                    groups.update({k: (v, start, end)})
            yield groups


    def get_matches(self, source: str, is_path: bool = False) -> list[str]:
        '''
        Returns a list containing any possible matches found within \
        the provided text.

        :param str source: The text that is to be examined.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.
        '''
        return list(match for match in self.iterate_matches(source, is_path))


    def get_matches_and_pos(self, source: str, is_flag: bool = False) -> list[tuple[str, int, int]]:
        '''
        Returns a list containing any possible matches found within the \
        provided text along with their exact position.

        :param str source: The text that is to be examined.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.
        '''
        return list(match for match in self.iterate_matches_and_pos(source, is_flag))


    def get_captures(self, source: str, include_empty: bool = True, is_path: bool = False) -> list[tuple[str]]:
        '''
        Returns a list of tuples, one tuple per match, where each tuple contains \
        all of its corresponding match's captured groups.

        :param str source: The text that is to be examined.
        :param bool include_empty: Determines whether to include empty captures \
            into the results. Defaults to ``True``.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.

        :note: In case there exists an optional capturing group within the pattern, \
            that has not been captured by a match, then that capture's corresponding \
            value will be ``None``.
        '''
        return list(group for group in self.iterate_captures(source, include_empty, is_path))


    def get_captures_and_pos(self, source: str, include_empty: bool = True,
        relative_to_match: bool = False, is_path: bool = False) -> list[list[tuple[str, int, int]]]:
        '''
        Returns a list containing lists of tuples, one list per match, where each \
        tuple contains one of its corresponding match's captured groups along with \
        its exact position within the text.

        :param str source: The text that is to be examined.
        :param bool include_empty: Determines whether to include empty captures into the \
            results. Defaults to ``True``.
        :param bool relative_to_match: If ``True``, then each group's position-indices \
            are calculated relative to the group's corresponding match, not to the whole \
            string. Defaults to ``False``.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.

        :note: In case there exists an optional capturing group within the pattern, \
            that has not been captured by a match, then that capture's corresponding \
            tuple will be ``(None, -1, -1)``.
        '''
        return list(tup for tup in self.iterate_captures_and_pos(
            source, include_empty, relative_to_match, is_path))


    def get_named_captures(self, source: str,
        include_empty: bool = True, is_path: bool = False) -> list[dict[str, str]]:
        '''
        Returns a dictionary of tuples, one dictionary per match, where each \
        dictionary contains key-value pairs of any named captured groups that \
        belong to its corresponding match, with each key being the name of the \
        captured group, whereas its corresponding value will be the actual \
        captured text.

        :param str source: The text that is to be examined.
        :param bool include_empty: Determines whether to include empty captures \
            into the results. Defaults to ``True``.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.

        :note: In case there exists an optional capturing group within the pattern, \
            that has not been captured by a match, then that capture's corresponding \
            key-value pair will be ``name --> None``.
        '''
        return list(group for group in self.iterate_named_captures(source, include_empty, is_path))


    def get_named_captures_and_pos(self, source: str, include_empty: bool = True,
        relative_to_match: bool = False, is_path: bool = False) -> list[dict[str, tuple[str, int, int]]]:
        '''
        Returns a dictionary of tuples, one dictionary per match, where each \
        dictionary contains key-value pairs of any named captured groups that \
        belong to its corresponding match, with each key being the name of the \
        captured group, whereas its corresponding value will be a tuple containing \
        the actual captured group along with its exact position within the text.

        :param str source: The text that is to be examined.
        :param bool include_empty: Determines whether to include empty captures into the \
            results. Defaults to ``True``.
        :param bool relative_to_match: If ``True``, then each group's position-indices \
            are calculated relative to the group's corresponding match, not to the whole \
            string. Defaults to ``False``.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.

        :note: In case there exists an optional capturing group within the pattern, \
            that has not been captured by a match, then that capture's corresponding \
            key-value pair will be ``name --> (None, -1, -1)``.
        '''
        return list(group for group in self.iterate_named_captures_and_pos(
            source, include_empty, relative_to_match, is_path))


    def replace(self, source: str, repl: str, count: int = 0, is_path: bool = False) -> str:
        '''
        Replaces all or some of the occuring matches with ``repl`` and \
        returns the resulting string. If there are no matches, then this \
        method will return the provided text without modifying it.

        :param str source: The text that is to be matched and modified.
        :param str repl: The string that is to replace any matches.
        :param int count: The number of matches that are to be replaced, \
            starting from left to right. A value of ``0`` indicates that \
            all matches must be replaced. Defaults to ``0``.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.

        :raises InvalidArgumentValueException: Parameter ``count`` has a value of \
            less than zero.
        '''
        if count < 0:
            message = "Parameter \"count\" can't be negative."
            raise _ex.InvalidArgumentValueException(message)
        if is_path:
            source = self.__extract_text(source)
        return _re.sub(str(self), repl, source, count, flags=self.__flags)


    def split_by_match(self, source: str, is_path: bool = False) -> list[str]:
        '''
        Splits the provided text based on any occuring matches and returns \
        the result as a list containing each individual part of the text \
        after the split.

        :param str source: The text that is to be matched and split.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.
        '''
        if is_path:
            source = self.__extract_text(source)
        split_list, index = list(), 0
        for _, start, end in self.iterate_matches_and_pos(source):
            if index != start:
                split_list.append(source[index:start])
            index = end
        if index != len(source):
            split_list.append(source[index:])
        return split_list


    def split_by_capture(self, source: str, include_empty: bool = True, is_path: bool = False) -> list[str]:
        '''
        Splits the provided text based on any occuring captures and returns \
        the result as alist containing each individual part of the text \
        after the split.

        :param str source: The piece of text that is to be matched and split.
        :param bool include_empty: Determines whether to include empty groups into the results. \
            Defaults to ``True``.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read. Defaults to ``False``.
        '''
        if is_path:
            source = self.__extract_text(source)
        split_list, index = list(), 0
        for groups in self.iterate_captures_and_pos(source, include_empty):
            for group, start, end in groups:
                if group is None:
                    continue
                if index != start:
                    split_list.append(source[index:start])
                index = end
        if index != len(source):
            split_list.append(source[index:])
        return split_list


    '''
    Quantifiers
    '''
    def optional(self, is_greedy: bool = True)-> 'Pregex':
        '''
        Applies quantifier ``?`` to this instance's underlying pattern \
        and returns the result as a ``Pregex`` instance.

        :param bool is_greedy: Determines whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.
        '''
        if self._get_type() == _Type.Empty:
            return self
        return __class__(
            f"{self._quantify_conditional_group()}?{'' if is_greedy else '?'}",
            escape=False)


    def indefinite(self, is_greedy: bool = True) -> 'Pregex':
        '''
        Applies quantifier ``*`` to this instance's underlying pattern \
        and returns the result as a ``Pregex`` instance.

        :param bool is_greedy: Determines whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.

        :raises CannotBeRepeatedException: This instance represents a non-repeatable pattern.
        '''
        if self._get_type() == _Type.Empty:
            return self
        if not self._is_repeatable():
            raise _ex.CannotBeRepeatedException(self)
        return __class__(
            f"{self._quantify_conditional_group()}*{'' if is_greedy else '?'}",
            escape=False)


    def one_or_more(self, is_greedy: bool = True) -> 'Pregex':
        '''
        Applies quantifier ``+`` to this instance's underlying pattern \
        and returns the result as a ``Pregex`` instance.

        :param bool is_greedy: Determines whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.

        :raises CannotBeRepeatedException: This instance represents a non-repeatable pattern.
        '''
        if self._get_type() == _Type.Empty:
            return self
        if not self._is_repeatable():
            raise _ex.CannotBeRepeatedException(self)
        return __class__(
            f"{self._quantify_conditional_group()}+{'' if is_greedy else '?'}",
            escape=False)


    def exactly(self, n: int) -> 'Pregex':
        '''
        Applies quantifier ``{n}`` to this instance's underlying pattern \
        and returns the result as a ``Pregex`` instance.

        :param int n: The exact number of times that the patterns is to be matched.

        :raises InvalidArgumentTypeException: Parameter ``n`` is not an integer.
        :raises InvalidArgumentValueException: Parameter ``n`` has a value of less \
            than zero.
        :raises CannotBeRepeatedException: Parameter ``n`` has a value of greater \
            than one, while this instance represents a non-repeatable pattern.
        '''
        if not isinstance(n, int) or isinstance(n, bool):
            message = "Provided argument \"n\" is not an integer."
            raise _ex.InvalidArgumentTypeException(message)
        if n == 0:
            return Pregex()
        if n == 1:
            return self
        else:
            if n < 0:
                message = "Parameter \"n\" can't be negative."
                raise _ex.InvalidArgumentValueException(message)
            if self._get_type() == _Type.Empty:
                return self
            if not self._is_repeatable():
                raise _ex.CannotBeRepeatedException(self)
            return __class__(
                f"{self._quantify_conditional_group()}{{{n}}}",
                escape=False)


    def at_least(self, n: int, is_greedy: bool = True)-> 'Pregex':
        '''
        Applies quantifier ``{n,}`` to this instance's underlying pattern \
        and returns the result as a ``Pregex`` instance.

        :param int n: The minimum number of times that the pattern is to be matched.
        :param bool is_greedy: Determines whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.`

        :raises InvalidArgumentTypeException: Parameter ``n`` is not an integer.
        :raises InvalidArgumentValueException: Parameter ``n`` has a value of \
            less than zero.
        :raises CannotBeRepeatedException: This instance represents a \
            non-repeatable pattern.
        '''
        if not isinstance(n, int) or isinstance(n, bool):
            message = "Provided argument \"n\" is not an integer."
            raise _ex.InvalidArgumentTypeException(message)
        if n == 0:
            return self.indefinite(is_greedy)
        elif n == 1:
            return self.one_or_more(is_greedy)
        else:
            if n < 0:
                message = "Parameter \"n\" can't be negative."
                raise _ex.InvalidArgumentValueException(message)
            if self._get_type() == _Type.Empty:
                return self
            if not self._is_repeatable():
                raise _ex.CannotBeRepeatedException(self)
            return __class__(
                f"{self._quantify_conditional_group()}{{{n},}}{'' if is_greedy else '?'}",
                escape=False)


    def at_most(self, n: _Optional[int], is_greedy: bool = True) -> 'Pregex':
        '''
        Applies quantifier ``{,n}`` to this instance's underlying pattern \
        and returns the result as a ``Pregex`` instance.

        :param int n: The maximum number of times that the pattern is to be matched.
        :param bool is_greedy: Determines whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.

        :raises InvalidArgumentTypeException: Parameter ``n`` is neither an \
            integer nor ``None``.
        :raises InvalidArgumentValueException: Parameter ``n`` has a value of \
            less than zero.
        :raises CannotBeRepeatedException: Parameter ``n`` has a value of \
            greater than one, while this instance represents a non-repeatable \
            pattern.

        :note: Setting ``n`` equal to ``None`` indicates that there is no upper limit to \
            the number of times the pattern is to be repeated.
        '''
        if not isinstance(n, int) or isinstance(n, bool):
            if n == None:
                return self.indefinite(is_greedy)
            message = "Provided argument \"n\" is neither an integer nor None."
            raise _ex.InvalidArgumentTypeException(message)
        elif n == 0:
            return self.exactly(n)
        elif n == 1:
            return self.optional(is_greedy)
        else:
            if n < 0:
                message = "Parameter \"n\" can't be negative."
                raise _ex.InvalidArgumentValueException(message)
            if self._get_type() == _Type.Empty:
                return self
            if not self._is_repeatable():
                raise _ex.CannotBeRepeatedException(self)
            return __class__(
                f"{self._quantify_conditional_group()}{{,{n}}}{'' if is_greedy else '?'}",
                escape=False)


    def at_least_at_most(self, n: int, m: _Optional[int], is_greedy: bool = True) -> 'Pregex':
        '''
        Applies quantifier ``{n,m}`` to this instance's underlying pattern \
        and returns the result as a ``Pregex`` instance.

        :param int n: The minimum number of times that the pattern is to be matched.
        :param int m: The minimum number of times that the pattern is to be matched.
        :param bool is_greedy: Determines whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to ``True``.`

        :raises InvalidArgumentTypeException: 
            - Parameter ``pre`` is neither a ``Pregex`` instance nor a string.
            - Parameter ``n`` is not an integer.
            - Parameter ``m`` is neither an integer nor ``None``.
        :raises InvalidArgumentValueException:
            - Either parameter ``n`` or ``m`` has a value of less than zero.
            - Parameter ``n`` has a greater value than that of parameter ``m``.
        :raises CannotBeRepeatedException: Parameter ``m`` has a value of greater \
            than one, while this instance represents a non-repeatable pattern.

        :note: 
            - Parameter ``is_greedy`` has no effect in the case that ``n`` equals ``m``.
            - Setting ``m`` equal to ``None`` indicates that there is no upper limit to the \
                number of times the pattern is to be repeated.
        '''
        if not isinstance(n, int) or isinstance(n, bool):
            message = "Provided argument \"n\" is not an integer."
            raise _ex.InvalidArgumentTypeException(message)
        elif not isinstance(m, int) or isinstance(m, bool):
            if m is not None:
                message = "Provided argument \"m\" is neither an integer nor \"None\"."
                raise _ex.InvalidArgumentTypeException(message)
        elif n < 0:
            message = "Parameter \"n\" can't be negative."
            raise _ex.InvalidArgumentValueException(message)
        elif m < 0:
            message = "Parameter \"m\" can't be negative."
            raise _ex.InvalidArgumentValueException(message)
        elif m < n:
            message = "The value of parameter \"m\" can't be"
            message += " less than the value of parameter \"n\"."
            raise _ex.InvalidArgumentValueException(message)
        if n == m:
            return self.exactly(n)
        elif n == 0:
            return self.at_most(m, is_greedy)
        elif m is None:
            return self.at_least(n, is_greedy)
        else:
            if self._get_type() == _Type.Empty:
                return self
            if not self._is_repeatable():
                raise _ex.CannotBeRepeatedException(self)
            return __class__(
                    f"{self._quantify_conditional_group()}{{{n},{m}}}{'' if is_greedy else '?'}",
                    escape=False)


    '''
    Operators
    '''
    def concat(self, pre: _Union['Pregex', str], on_right: bool = True) -> 'Pregex':
        '''
        Concatenates the provided pattern to this instance's underlying pattern \
        and returns the resulting pattern as a ``Pregex`` instance.

        :param Pregex | str pre: Either a string or a ``Pregex`` instance \
            representing the pattern that is to take part in the concatenation.
        :param bool on_right: If ``True``, then places the provided pattern on the \
            right side of the concatenation, else on the left. Defaults to ``True``.

        :raises InvalidArgumentTypeException: Parameter ``pre`` is neither \
            a ``Pregex`` instance nor a string.
        '''
        pre = __class__._to_pregex(pre)

        if pre._get_type() == _Type.Empty:
            return self

        pattern = self._concat_conditional_group()
        pre = pre._concat_conditional_group()

        pattern = pattern + pre if on_right else pre + pattern

        return __class__(pattern, escape=False)


    def either(self, pre: _Union['Pregex', str], on_right: bool = True) -> 'Pregex':
        '''
        Applies the alternation operator ``|`` between the provided pattern \
        and this instance's underlying pattern, and returns the resulting pattern \
        as a ``Pregex`` instance.

        :param Pregex | str pre: Either a string or a ``Pregex`` instance \
            representing the pattern that is to take part in the alternation.
        :param bool on_right: If ``True``, then places the provided pattern on the \
            right side of the alternation, else on the left. Defaults to ``True``.

        :raises InvalidArgumentTypeException: Parameter ``pre`` is neither \
            a ``Pregex`` instance nor a string.
        '''
        pre = __class__._to_pregex(pre)

        if pre._get_type() == _Type.Empty:
            pattern = str(self)
        else:
            pattern = f"{self}|{pre}" if on_right else f"{pre}|{self}"

        return __class__(pattern, escape=False)


    def enclose(self, pre: _Union['Pregex', str]) -> 'Pregex':
        '''
        Concatenates the provided pattern to both sides of this instance's \
        underlying pattern, and returns the resulting pattern as a ``Pregex`` \
        instance.

        :param Pregex | str pre: Either a string or a ``Pregex`` instance \
            representing the "enclosing" pattern.

        :raises InvalidArgumentTypeException: Parameter `pre` is neither a \
            ``Pregex`` instance nor a string.
        '''
        pre = __class__._to_pregex(pre)._concat_conditional_group()
        pattern = f"{pre}{self._concat_conditional_group()}{pre}"
        return __class__(pattern, escape=False)
        

    '''
    Groups
    '''
    def capture(self, name: _Optional[str] = None) -> 'Pregex':
        '''
        Creates a capturing group out of this instance's underlying \
        pattern and returns the result as a ``Pregex`` instance.

        :param Pregex | str pre: The pattern out of which the capturing group is created.
        :param str name: The name that is assigned to the captured group for backreference \
            purposes. A value of ``None`` indicates that no name is to be assigned to the \
            group. Defaults to ``None``.

        :raises InvalidArgumentTypeException: Parameter ``name`` is neither a string \
            nor ``None``.
        :raises InvalidCapturingGroupNameException: Parameter ``name`` is not a valid \
            capturing group name. Such name must contain word characters only and start \
            with a non-digit character.

        :note:
            - Creating a capturing group out of a capturing group does nothing.
            - Creating a capturing group out of a non-capturing group converts it \
              into a capturing group, except if any flags have been applied to it, \
              in which case, the non-capturing group is wrapped within a capturing \
              group as a whole.
            - Creating a named capturing group out of an unnamed capturing group, \
              assigns a name to it.
            - Creating a named capturing group out of a named capturing group, \
              changes the group's name.
        '''
        if name is not None:
            if not isinstance(name, str):
                message = "Provided argument \"name\" is not a string."
                raise _ex.InvalidArgumentTypeException(message)
            if _re.fullmatch("[A-Za-z_]\w*", name) is None:
                raise _ex.InvalidCapturingGroupNameException(name)
        if self.__type == _Type.Empty:
            return self
        elif self.__type == _Type.Group:
            if self.__pattern.startswith('(?:'):
                # non-capturing group.
                pattern = self.__pattern.replace('?:', '', 1)
            elif _re.match('\(\?[i].+', self.__pattern):
                # non-capturing group with flag.
                pattern = f'({str(self)})'
            else:
                # capturing group.
                pattern = self.__pattern
            if name is not None:
                if pattern.startswith('(?P'):
                    pattern = _re.sub('\(\?P<[^>]*>', f'(?P<{name}>', pattern)
                else:
                    pattern = f"(?P<{name}>{pattern[1:-1]})"
        else:
            pattern = f"({f'?P<{name}>' if name != None else ''}{self})"
        return __class__(pattern, escape=False)


    def group(self, is_case_insensitive: bool = False) -> 'Pregex':
        '''
        Creates a non-capturing group out of this instance's underlying \
        pattern and returns the result as a ``Pregex`` instance.

        :param bool is_case_insensitive: If ``True``, then the "case insensitive" \
            flag is applied to the group so that the pattern within it ignores case \
            when it comes to matching. Defaults to ``False``.

        :raises InvalidArgumentTypeException: Parameter ``pre`` is neither \
            a ``Pregex`` instance nor a string.

        :note:
            - Creating a non-capturing group out of a non-capturing group does nothing, \
              except for reset its flags, e.g. ``is_case_insensitive``, if it has any.
            - Creating a non-capturing group out of a capturing group converts it into \
              a non-capturing group.
        '''
        if self.__type == _Type.Empty:
            return self
        elif self.__type == _Type.Group:
            if self.__pattern.startswith('(?P'):
                # Remove name from named capturing group.
                pattern = _re.sub('\(\?P<[^>]*>', f'(?:', str(self))
            elif self.__pattern.startswith('(?'):
                # Remove any possible flags from non-capturing group.
                pattern = _re.sub(
                    r'\(\?[i]*:', f"(?{'i' if is_case_insensitive else ''}:",
                    self.__pattern,
                    count=1)
            else:
                # Else convert capturing group to non-capturing group.
                pattern = self.__pattern.replace('(', '(?:', 1)
        else:
            pattern = f"(?{'i' if is_case_insensitive else ''}:{self})"
        return __class__(pattern, escape=False)


    '''
    Assertions
    '''
    def match_at_start(self) -> 'Pregex':
        '''
        Applies assertion ``\\A`` to this instance's underlying pattern \
        so that it only matches if it is found at the start of a string, \
        and returns the resulting pattern as a ``Pregex`` instance.

        :note: The resulting pattern cannot have a repeating quantifier \
            applied to it.
        '''
        return __class__(f"\\A{self._assert_conditional_group()}", escape=False)


    def match_at_end(self) -> 'Pregex':
        '''
        Applies assertion ``\\Z`` to this instance's underlying pattern \
        so that it only matches if it is found at the end of a string, \
        and returns the resulting pattern as a ``Pregex`` instance.

        :note: The resulting pattern cannot have a repeating quantifier \
            applied to it.
        '''
        return __class__(f"{self._assert_conditional_group()}\\Z", escape=False)


    def match_at_line_start(self) -> 'Pregex':
        '''
        Applies assertion ``^`` to this instance's underlying pattern \
        so that it only matches if it is found at the start of a line, \
        and returns the resulting pattern as a ``Pregex`` instance.

        :note:
            - The resulting pattern cannot have a repeating quantifier \
                applied to it.
            - Uses meta character ``^`` since the `MULTILINE` flag is \
                considered on.
        '''
        return __class__(f"^{self._assert_conditional_group()}", escape=False)


    def match_at_line_end(self) -> 'Pregex':
        '''
        Applies assertion ``$`` to this instance's underlying pattern \
        so that it only matches if it is found at the end of a line, \
        and returns the resulting pattern as a ``Pregex`` instance.

        :note:
            - The resulting pattern cannot have a repeating quantifier\
                applied to it.
            - Uses meta character ``$`` since the `MULTILINE` flag is \
                considered on.
        '''
        return __class__(f"{self._assert_conditional_group()}$", escape=False)


    def followed_by(self, pre: _Union['Pregex', str]) -> 'Pregex':
        '''
        Applies positive lookahead assertion ``(?=<PRE>)``, where \
        ``<PRE>`` corresponds to the provided pattern, to this \
        instance's underlying pattern and returns the resulting pattern \
        as a ``Pregex`` instance.

        :param str | Pregex pre: A Pregex instance or string \
            representing the "assertion" pattern.

        :raises InvalidArgumentTypeException: The provided argument \
            is neither a ``Pregex`` instance nor a string.

        :note: The resulting pattern cannot have a repeating quantifier \
            applied to it.
        '''
        pre = __class__._to_pregex(pre)
        if pre._get_type() == _Type.Empty:
            return self
        return __class__(
            f"{self._assert_conditional_group()}(?={pre})",
            escape=False)


    def preceded_by(self, pre: _Union['Pregex', str]) -> 'Pregex':
        '''
        Applies positive lookbehind assertion ``(?<=<PRE>)``, where \
        ``<PRE>`` corresponds to the provided pattern, to this \
        instance's underlying pattern and returns the resulting pattern \
        as a ``Pregex`` instance.

        :param str | Pregex pre: A Pregex instance or string \
            representing the "assertion" pattern.

        :raises InvalidArgumentTypeException: The provided argument \
            is neither a ``Pregex`` instance nor a string.
        :raises NonFixedWidthPatternException: A non-fixed-width pattern \
            is provided in place of parameter ``assertion``.

        :note: The resulting pattern cannot have a repeating quantifier \
            applied to it.
        '''
        pre = __class__._to_pregex(pre)
        if pre._get_type() == _Type.Empty:
            return self
        if pre._get_type() == _Type.Quantifier \
            and (_re.search("\\{\d+\\}$", str(pre)) is None):
            raise _ex.NonFixedWidthPatternException(self, pre)
        return __class__(
            f"(?<={pre}){self._assert_conditional_group()}",
            escape=False)


    def enclosed_by(self, pre: _Union['Pregex', str]) -> 'Pregex':
        '''
        Applies both positive lookahead assertion ``(?=<PRE>)`` and positive \
        lookbehind assertion ``(?<=<PRE>)``, where ``<PRE>`` corresponds to \
        the provided pattern, to this instance's underlying pattern and \
        returns the resulting pattern as a ``Pregex`` instance.

        :param str | Pregex pre: A Pregex instance or string \
            representing the "assertion" pattern.

        :raises InvalidArgumentTypeException: The provided argument \
            is neither a ``Pregex`` instance nor a string.
        :raises NonFixedWidthPatternException: A non-fixed-width pattern \
            is provided in place of parameter ``assertion``.

        :note: The resulting pattern cannot have a repeating quantifier \
            applied to it.
        '''
        pre = __class__._to_pregex(pre)
        if pre._get_type() == _Type.Empty:
            return self
        if pre._get_type() == _Type.Quantifier \
            and (_re.search("\\{\d+\\}$", str(pre)) is None):
            raise _ex.NonFixedWidthPatternException(self, pre)
        return __class__(
            f"(?<={pre}){self._assert_conditional_group()}(?={pre})",
            escape=False)


    def not_followed_by(self, pre: _Union['Pregex', str]) -> 'Pregex':
        '''
        Applies negative lookahead assertion ``(?!<PRE>)``, where ``<PRE>`` \
        corresponds to the provided pattern, to this instance's underlying \
        pattern and returns the resulting pattern as a ``Pregex`` instance.

        :param Pregex | str pre: Either a string or a ``Pregex`` instance \
            representing the "assertion" pattern.

        :raises InvalidArgumentTypeException: The provided argument is neither \
            a ``Pregex`` instance nor a string.
        :raises EmptyNegativeAssertionException: The provided assertion pattern \
            is the empty-string pattern.
        '''
        pre = __class__._to_pregex(pre)
        if pre._get_type() == _Type.Empty:
            raise _ex.EmptyNegativeAssertionException()
        pattern = f"{self._assert_conditional_group()}(?!{pre})"
        return __class__(pattern, escape=False)


    def not_preceded_by(self, pre: _Union['Pregex', str]) -> 'Pregex':
        '''
        Applies negative lookbehind assertion ``(?<!<PRE>)``, where ``<PRE>`` \
        corresponds to the provided pattern, to this instance's underlying \
        pattern and returns the resulting pattern as a ``Pregex`` instance.

        :param Pregex | str pre: Either a string or a ``Pregex`` instance \
            representing the "assertion" pattern.

        :raises InvalidArgumentTypeException: The provided argument is neither \
            a ``Pregex`` instance nor a string.
        :raises EmptyNegativeAssertionException: The provided assertion pattern \
            is the empty-string pattern.
        :raises NonFixedWidthPatternException: The provided assertion pattern \
            does not have a fixed width.
        '''
        pre = __class__._to_pregex(pre)
        if pre._get_type() == _Type.Empty:
            raise _ex.EmptyNegativeAssertionException()
        if pre._get_type() == _Type.Quantifier \
            and (_re.search("\\{\d+\\}$", str(pre)) is None):
            raise _ex.NonFixedWidthPatternException(self, pre)
        pattern = f"(?<!{pre}){self._assert_conditional_group()}"
        return __class__(pattern, escape=False)


    def not_enclosed_by(self, pre: _Union['Pregex', str]) -> 'Pregex':
        '''
        Applies both negative lookahead assertion ``(?=<PRE>)``` and \
        negative lookbehind assertion ``(?<!<PRE>)``, where ``<PRE>`` \
        corresponds to the provided pattern, to this instance's underlying \
        pattern and returns the resulting pattern as a ``Pregex`` instance.

        :param Pregex | str pre: Either a string or a ``Pregex`` instance \
            representing the "assertion" pattern.

        :raises InvalidArgumentTypeException: The provided argument is neither \
            a ``Pregex`` instance nor a string.
        :raises EmptyNegativeAssertionException: The provided assertion pattern \
            is the empty-string pattern.
        :raises NonFixedWidthPatternException: The provided assertion pattern \
            does not have a fixed width.
        '''
        pre = __class__._to_pregex(pre)
        if pre._get_type() == _Type.Empty:
            raise _ex.EmptyNegativeAssertionException()
        if pre._get_type() == _Type.Quantifier \
            and (_re.search("\\{\d+\\}$", str(pre)) is None):
            raise _ex.NonFixedWidthPatternException(self, pre)
        pattern = f"(?<!{pre}){self._assert_conditional_group()}(?!{pre})"
        return __class__(pattern, escape=False)


    '''
    Protected Methods
    '''
    def _get_type(self) -> _Type:
        '''
        Returns the type of this instance's underlying pattern.
        '''
        return self.__type


    def _is_repeatable(self) -> bool:
        '''
        Returns ``True`` if this pattern can be quantified, \
        else returns ``False``.
        '''
        return self.__repeatable


    def _concat_conditional_group(self) -> str:
        '''
        Returns this instance's underlying pattern wrapped within a \
        non-capturing group only if the instance's "group-on-concat" \
        rule is set to ``True``, else returns it as it is.
        '''
        return str(self.group()) if self.__get_group_on_concat_rule() else str(self)


    def _quantify_conditional_group(self) -> str:
        '''
        Returns this instance's underlying pattern wrapped within a \
        non-capturing group only if the instance's "group-on-quantify" \
        rule is set to ``True``, else returns it as it is.
        '''
        return str(self.group()) if self.__get_group_on_quantify_rule() else str(self)


    def _assert_conditional_group(self) -> str:
        '''
        Returns this instance's underlying pattern wrapped within a \
        non-capturing group only if the instance's "group-on-assertion" \
        rule is set to ``True``, else returns it as it is.
        '''
        return str(self.group()) if self.__get_group_on_assert_rule() else str(self)


    @staticmethod
    def _to_pregex(pre: 'Pregex' or str) -> 'Pregex':
        '''
        Returns ``pre`` exactly as provided if it is a ``Pregex`` instance, \
        else if it is a string, this method returns it wrapped within a ``Pregex`` \
        instance for which parameter ``escape`` has been set to ``True``.

        :param Pregex | str: Either a string or a ``Pregex`` instance.

        :raises InvalidArgumentTypeException: Argument ``pre`` is neither a string nor a \
            ``Pregex`` class instance.
        '''
        if isinstance(pre, str):
            return Pregex(pre, escape=True)
        elif issubclass(pre.__class__, __class__):
            return pre
        else:
            message = "Parameter \"pre\" must either be a string or an instance of \"Pregex\"."
            raise _ex.InvalidArgumentTypeException(message)


    ''' 
    Private Methods
    '''
    def __str__(self) -> str:
        '''
        Returns the string representation of this instance's \
        underlying pattern.

        :note: Not to be used for pattern-display purposes.
        '''
        return self.__pattern


    def __repr__(self) -> str:
        '''
        Returns the string representation of this instance's \
        underlying pattern in a printable format.
        '''
        # Replace any quadraple backslashes.
        return _re.sub(r"\\\\", r"\\", repr(self.__pattern)[1:-1])
        

    def __add__(self, pre: _Union['Pregex', str]) -> 'Pregex':
        '''
        Concatenates this instance's underlying pattern with the provided \
        pattern and returns the resulting ``Pregex`` instance.

        :param pre: Either a string or ``Pregex`` class instance that is to \
            be concatenated to this instance's underlying pattern. 
        '''
        return __class__(str(self.concat(__class__._to_pregex(pre))), escape=False)


    def __radd__(self, pre: _Union['Pregex', str]) -> 'Pregex':
        '''
        Concatenates this instance's underlying pattern with the provided \
        pattern and returns the resulting ``Pregex`` instance.

        :param pre: Either a string or ``Pregex`` class instance that is to \
            be concatenated to this instance's underlying pattern. 
        '''
        return __class__(str(__class__._to_pregex(pre).concat(self)), escape=False)


    def __mul__(self, n: int) -> 'Pregex':
        '''
        Applies quantifier ``{n}`` to this instance's underlying pattern \
        and returns the result as a ``Pregex`` instance.

        :param int n: The exact number of times that the patterns is to be matched.

        :raises InvalidArgumentTypeException: Parameter ``n`` is not an integer.
        :raises InvalidArgumentValueException: Parameter ``n`` has a value of less \
            than zero.
        :raises CannotBeRepeatedException: Parameter ``n`` has a value of greater \
            than one, while this instance represents a non-repeatable pattern.
        '''
        if not self._is_repeatable():
            raise _ex.CannotBeRepeatedException(self)
        if not isinstance(n, int) or isinstance(n, bool):
            message = "Provided argument \"n\" is not an integer."
            raise _ex.InvalidArgumentTypeException(message)
        if n < 0:
            message = "Using multiplication operator with a negative integer is not allowed."
            raise _ex.InvalidArgumentValueException(message)
        if self._get_type() == _Type.Empty:
            return self
        return __class__(str(self.exactly(n)), escape=False)


    def __rmul__(self, n: int) -> 'Pregex':
        '''
        Applies quantifier ``{n}`` to this instance's underlying pattern \
        and returns the result as a ``Pregex`` instance.

        :param int n: The exact number of times that the patterns is to be matched.

        :raises InvalidArgumentTypeException: Parameter ``n`` is not an integer.
        :raises InvalidArgumentValueException: Parameter ``n`` has a value of less \
            than zero.
        :raises CannotBeRepeatedException: Parameter ``n`` has a value of greater \
            than one, while this instance represents a non-repeatable pattern.
        '''
        if not self._is_repeatable():
            raise _ex.CannotBeRepeatedException(self)
        if not isinstance(n, int) or isinstance(n, bool):
            message = "Provided argument \"n\" is not an integer."
            raise _ex.InvalidArgumentTypeException(message)
        if n < 0:
            message = "Using multiplication operator with a negative integer is not allowed."
            raise _ex.InvalidArgumentValueException(message)
        if self._get_type() == _Type.Empty:
            return self
        return __class__(str(self.exactly(n)), escape=False)


    def __get_group_on_concat_rule(self) -> bool:
        '''
        Returns the value of this instance's "group-on-concat" rule.
        '''
        return __class__.__groupping_rules[self.__type][0]


    def __get_group_on_quantify_rule(self) -> bool:
        '''
        Returns the value of this instance's "group-on-quantify" rule.
        '''
        return __class__.__groupping_rules[self.__type][1]


    def __get_group_on_assert_rule(self) -> bool:
        '''
        Returns the value of this instance's "group-on-assertion" rule.
        '''
        return __class__.__groupping_rules[self.__type][2]


    def __iterate_match_objects(self, source: str, is_path: bool) -> _Iterator[_re.Match]:
        '''
        Invokes ``re.finditer`` in order to iterate over all matches of this \
        instance's underlying pattern with the provided text as instances of \
        type ``re.Match``.

        :param str source: The text that is to be examined.
        :param bool is_path: If set to ``True``, then parameter ``source`` \
            is considered to be a local path pointing to the file from which \
            the text is to be read.
        '''
        if is_path:
            source = self.__extract_text(source)
        return _re.finditer(self.__pattern, source, flags=self.__flags) \
            if self.__compiled is None else self.__compiled.finditer(source)


    @staticmethod
    def __escape(pattern: str) -> str:
        '''
        Scans this instance's underlying pattern for any characters that need to \
        be escaped, escapes them if there are any, and returns the resulting \
        pattern as a string.
        '''
        pattern = pattern.replace("\\", "\\\\")
        for c in {'^', '$', '(', ')', '[', ']', '{', '}', '?', '+', '*', '.', '|', '/'}:
            pattern = pattern.replace(c, f"\\{c}")
        return pattern   


    @staticmethod
    def __infer_type(pattern: str) -> tuple[_Type, bool]:
        '''
        Examines the provided RegEx pattern and returns its type, \
        as well as a boolean indicating whether said pattern can be \
        quantified or not.

        :param str pattern: The RegEx pattern that is to be examined.
        '''
        def remove_groups(pattern: str, repl: str = ''):
            '''
            Removes all groups from the provided pattern, and replaces them with ``repl``.

            :param str pattern: The pattern whose groups are to be removed.
            :param str repl: The string that replaces all groups within the pattern. \
                Defaults to ``''``.
            '''
            left_par, right_par = r"(?:(?<!\\)\()", r"(?:(?<!\\)\))"
            if len(_re.findall(left_par, pattern)) == 0:
                return pattern
            temp = _re.sub(pattern=left_par + r"(?:[^\(\)]|\\(?:\(|\)))+" + right_par,
                repl=repl, string=pattern)
            return temp if temp == repl else remove_groups(temp, repl)

        def __is_group(pattern: str) -> bool:
            '''
            Looks at the underlying pattern of this instance, and returns either \
            ``True`` or ``False``, depending on whether the provided RegEx pattern \
            represents a group or not.

            :param str pattern: The pattern that is to be examined.
            '''
            if pattern.startswith('(') and pattern.endswith(')'):
                n_open = 0
                for i in range(1, len(pattern) - 1):
                    prev_char, curr_char = pattern[i-1], pattern[i]
                    if prev_char != "\\": 
                        if curr_char == ')':
                            if n_open == 0:
                                return False
                            else:
                                n_open -= 1
                        if curr_char == '(':
                            n_open += 1
                return n_open == 0
            return False

        # Replace escaped backslashes with some other character.
        pattern = _re.sub(r"\\{2}", "a", pattern)

        if pattern == "":
            return _Type.Empty, True
        elif _re.fullmatch(r"\\?.", pattern, flags=__class__.__flags) is not None:
            if _re.fullmatch(r"\.|\\(?:w|d|s)", pattern,
                flags=__class__.__flags | _re.IGNORECASE) is not None:
                return _Type.Class, True
            elif _re.fullmatch(r"\\b", pattern,
                flags=__class__.__flags | _re.IGNORECASE) is not None:
                return _Type.Assertion, True
            else:
                return _Type.Token, True

        # Simplify classes by removing extra characters.
        pattern = _re.sub(r"\[.+?(?<!\\)\]", "[a]", pattern)

        if pattern == "[a]":
            return _Type.Class, True
        elif __is_group(pattern):
            return _Type.Group, True

        # Replace every group with a simple character.
        temp = remove_groups(pattern, repl="G")

        if len(_re.split(pattern=r"(?<!\\)\|", string=temp)) > 1:
                return _Type.Alternation, True
        elif _re.fullmatch(r"(?:\^|\\A|\(\?<=.+\)).+|.+(?:\$|\\Z|\(\?=.+\))",
            pattern, flags=__class__.__flags) is not None:
            return _Type.Assertion, False
        elif _re.fullmatch(r"(?:\\b|\\B|\(\?<!.+\)).+|.+(?:\\b|\\B|\(\?!.+\))",
            pattern, flags=__class__.__flags) is not None:
            return _Type.Assertion, True
        elif _re.fullmatch(r"(?:\\.|[^\\])?(?:\?|\*|\+|\{(?:\d+|\d+,|,\d+|\d+,\d+)\})",
            temp, flags=__class__.__flags) is not None:
            return _Type.Quantifier, True
        return _Type.Other, True


    @staticmethod
    def __extract_text(source: str) -> str:
        '''
        Reads and returns the text that is contained within the file \
        to which the provided path points.

        :param str source: The path pointing to the file from which the text \
            is to be extracted.
        '''
        with open(file=source, mode='r', encoding='utf-8') as f:
            text = f.read()
        return text