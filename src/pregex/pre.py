import re as _re
import pregex.exceptions as _exceptions
from typing import Iterator as _Iterator

class Pregex():
    '''
    This class constitutes the basis for every other class in this package.
    '''

    '''
    The totality of active flags.
    '''
    __flags: _re.RegexFlag = _re.MULTILINE | _re.DOTALL


    def __init__(self, pattern: str, group_on_concat: bool = False, group_on_quantify: bool = False) -> 'Pregex':
        '''
        Creates a 'Pregex' instance based on the provided pattern.

        :param Pregex | str pattern: The RegEx pattern based on which the "Pregex" instance is created.
        :param bool group_on_concat: Indicates whether this expression requires getting groupped \
            whenever it is concatenated with an other expression. Defaults to 'False'.
        :param bool group_on_quantify: Indicates whether this expression requires getting groupped \
            whenever it has a quantifier applied to it. Defaults to 'False'.
        '''
        self.__pattern: str = pattern
        self.__compiled: _re.Pattern = None
        self.__group_on_concat: bool = group_on_concat
        self.__group_on_quantify: bool = group_on_quantify


    '''
    Public Methods
    '''
    def get_pattern(self, include_flags: bool = False) -> str:
        '''
        Returns the expression's pattern as its string representation.

        :param bool include_falgs: Indicates whether to display the RegEx flags \
            along with the pattern. Defaults to 'False'.

        NOTE: This method is to be preferred over str() when one needs to display \
            this instance's underlying Regex pattern.
        '''
        pattern = repr(self)
        return f"/{pattern}/gms" if include_flags else pattern

    def get_compiled_pattern(self, discard_after: bool = True) -> _re.Pattern:
        '''
        Returns the expression's compiled pattern as a 're.Pattern' instance. \
        
        :param bool discard_after: Indicates whether the compiled pattern is to be \
            discarded after this method, or to be held so that any further attempt \
            at matching a string will use the compiled pattern instead of the regular one. \
            Defaults to 'True'.
        '''
        if self.__compiled is None:
            self.compile()
        compiled = self.__compiled
        if discard_after:
            self.__compiled = None
        return compiled

    def compile(self) -> None:
        '''
        Compiles the underlying RegEx pattern. After invoking this method, any \
        further attempt at matching a string will use the compiled RegEx pattern \
        instead of the regular one.
        '''
        self.__compiled = _re.compile(self.get_pattern(), flags=self.__flags)

    def has_match(self, text: str) -> bool:
        '''
        Returns 'True' if 'text' matches this pattern at least once.

        :param str text: The piece of text that is to be matched.
        '''
        return bool(_re.search(self.__pattern, text) if self.__compiled is None \
            else self.__compiled.search(text))

    def is_exact_match(self, text: str) -> bool:
        '''
        Returns 'True' only if 'text' matches this pattern exactly.

        :param str text: The piece of text that is to be matched.
        '''
        return bool(_re.fullmatch(self.__pattern, text, flags=self.__flags) \
            if self.__compiled is None else self.__compiled.fullmatch(text))

    def iterate_matches(self, text: str) -> _Iterator[str]:
        '''
        Generates any possible matches with 'text'.

        :param str text: The piece of text that is to be matched.
        '''
        for match in self.__iterate_match_objects(text):
            yield match.group(0)

    def iterate_matches_and_pos(self, text: str) -> _Iterator[tuple[str, int, int]]:
        '''
        Generates any possible matches with 'text' along with their \
        exact position within the text.

        :param str text: The piece of text that is to be matched.
        '''
        for match in self.__iterate_match_objects(text):
            yield (match.group(0), *match.span())

    def iterate_groups(self, text: str, include_empty: bool = True) -> _Iterator[tuple[str]]:
        '''
        Generates tuples, one tuple per match, where each tuple contains \
        all of its corresponding match's captured groups. In case there exists \
        a capturing group within the pattern that has not been captured by a match, \
        then that group's corresponding value will be 'None'.

        :param str text: The piece of text that is to be matched.
        :param bool include_empty: Indicates whether to include empty groups into the results. \
            Defaults to 'True'.
        '''
        for match in self.__iterate_match_objects(text):
            yield match.groups() if include_empty else \
                tuple(group for group in match.groups() if group != '')

    def iterate_groups_and_pos(self, text: str, include_empty: bool = True, relative_to_match : bool = False) -> _Iterator[list[tuple[str, int, int]]]:
        '''
        Generates lists of tuples, one list per match, where each tuple contains one \
        of its corresponding match's captured groups along with its exact position \
        within the text. In case there exists a capturing group within the pattern that \
        has not been captured by a match, then that group's corresponding tuple will be \
        '(None, -1, -1)'.

        :param str text: The piece of text that is to be matched.
        :param bool include_empty: Indicates whether to include empty groups into the results. \
            Defaults to 'True'.
        :param bool relative_to_match: If 'True', then each group's position-indices are calculated \
            relative to the group's corresponding match, not to the whole string. Defaults to 'False'.
        '''
        for match in self.__iterate_match_objects(text):
            groups, counter = list(), 0
            for group in match.groups():
                counter += 1
                if include_empty or (group != ''):
                    start, end = match.span(counter)
                    if relative_to_match and start > -1:
                        start, end = start - match.start(0), end - match.start(0)
                    groups.append((group, start, end))
            yield groups

    def get_matches(self, text: str) -> list[str]:
        '''
        Returns a list containing any possible matches with 'text'.

        :param str text: The piece of text that is to be matched.
        '''
        return list(match for match in self.iterate_matches(text))

    def get_matches_and_pos(self, text: str) -> list[tuple[str, int, int]]:
        '''
        Returns a list containing any possible matches with 'text' \
        along with their exact position within it.

        :param str text: The piece of text that is to be matched.
        '''
        return list(match for match in self.iterate_matches_and_pos(text))

    def get_groups(self, text: str, include_empty: bool = True) -> list[tuple[str]]:
        '''
        Returns a list of tuples, one tuple per match, where each tuple contains \
        all of its corresponding match's captured groups. In case there exists \
        a capturing group within the pattern that has not been captured by a match, \
        then that group's corresponding value will be 'None'.

        :param str text: The piece of text that is to be matched.
        :param bool include_empty: Indicates whether to include empty groups into the results. \
            Defaults to 'True'.
        '''
        return list(group for group in self.iterate_groups(text, include_empty))

    def get_groups_and_pos(self, text: str, include_empty: bool = True, relative_to_match: bool = False) -> list[list[tuple[str, int, int]]]:
        '''
        Returns a list containing lists of tuples, one list per match, where each \
        tuple contains one of its corresponding match's captured groups along with \
        its exact position within the text. In case there exists a capturing group \
        within the pattern that has not been captured by a match, then that group's \
        corresponding tuple will be '(None, -1, -1)'.

        :param str text: The piece of text that is to be matched.
        :param bool include_empty: Indicates whether to include empty groups into the results. \
            Defaults to 'True'.
        :param bool relative_to_match: If 'True', then each group's position-indices are calculated \
            relative to the group's corresponding match, not to the whole string. Defaults to 'False'.
        '''
        return list(tup for tup in self.iterate_groups_and_pos(text, include_empty, relative_to_match))

    def replace(self, text: str, repl: str, count: int = 0) -> str:
        '''
        Substitutes all or some of the occuring matches with "text" for "repl" \
        and returns the resulting string. If there are no matches, returns \
        parameter "text" exactly as provided.

        :param str s: The string that is to be matched and modified.
        :param str repl: The string that is to replace any matches.
        :param int count: The number of matches that are to be replaced, \
            starting from left to right. A value of '0' indicates that \
            all matches must be replaced. Defaults to '0'.
        '''
        if count < 0:
            raise _exceptions.NegativeArgumentException(count)
        return _re.sub(str(self), repl, text, count, flags=self.__flags)

    def split_by_match(self, text: str) -> list[str]:
        '''
        Splits the provided text based on any possible matches with this \
        pattern and returns the result as a list containing each individual \
        part of the text after the split.

        :param str text: The piece of text that is to be matched and split.
        '''
        split_list, index = list(), 0
        for _, start, end in self.iterate_matches_and_pos(text):
            if index != start:
                split_list.append(text[index:start])
            index = end
        if index != len(text):
            split_list.append(text[index:])
        return split_list

    def split_by_group(self, text: str, include_empty: bool = True) -> list[str]:
        '''
        Splits the provided text based on any possible captured groups \
        that may have occured due to matches with thin pattern, and returns \
        the result as a list containing each individual part of the text after the split.

        :param str text: The piece of text that is to be matched and split.
        :param bool include_empty: Indicates whether to include empty groups into the results. \
            Defaults to 'True'.
        '''
        split_list, index = list(), 0
        for groups in self.iterate_groups_and_pos(text, include_empty):
            for group, start, end in groups:
                if group is None:
                    continue
                if index != start:
                    split_list.append(text[index:start])
                index = end
        if index != len(text):
            split_list.append(text[index:])
        return split_list


    '''
    Protected Methods
    '''
    def _get_group_on_concat(self) -> bool:
        '''
        Returns private field "__group_on_concat".
        '''
        return self.__group_on_concat

    def _get_group_on_quantify(self) -> bool:
        '''
        Returns private field "__group_on_quantify".
        '''
        return self.__group_on_quantify

    def _concat_conditional_group(self) -> 'Pregex':
        '''
        If "__group_on_concat" is "True", then returns a Pregex instance \
        containing this instance's underlying pattern wrapped within a \
        non-capturing group, else returns this instance as is.
        '''
        return self._non_capturing_group() if self.__group_on_concat else self

    def _quantify_conditional_group(self) -> 'Pregex':
        '''
        If "__group_on_quantify" is "True", then returns a Pregex instance \
        containing this instance's underlying pattern wrapped within a \
        non-capturing group, else returns this instance as is.
        '''
        return self._non_capturing_group() if self.__group_on_quantify else self

    def _to_pregex(pre: 'Pregex' or str) -> 'Pregex':
        '''
        If provided with a string, then returns it wrapped within a "Pregex" instance \
        containing an escaped form of the provided string as its underlying pattern. \
        If provided with a "Pregex" instance, then returns it as is.

        :param Pregex | str: Either a string or a "Pregex" instance.

        :raises: NeitherStringNorPregexException: If "pre" is neither a string nor a \
            "Pregex" instance.
        '''
        if isinstance(pre, str):
            return Pregex(pre)._literal()
        elif issubclass(pre.__class__, __class__):
            return pre
        else:
            raise _exceptions.NeitherStringNorPregexException()

    def _add(pre1: 'Pregex' or str, pre2: 'Pregex' or str) -> 'Pregex':
        '''
        Concatenates "pre1" and "pre2" together and returns the resulting "Pregex" instance.

        :param Pregex | str pre1: The string or a "Pregex" instance at the left side of the concatenation.
        :param Pregex | str pre2: The string or a "Pregex" instance at the right side of the concatenation.
        '''
        return __class__._to_pregex(pre1)._concat(__class__._to_pregex(pre2))


    ''' 
    Private Methods
    '''
    def __str__(self) -> str:
        '''
        Returns the string representation of this class instance.

        NOTE: Not to be used for pattern-display purposes.
        '''
        return self.__pattern

    def __repr__(self) -> str:
        '''
        Returns the string representation of this class instance in a printable format.
        '''
        # Replace any quadraple backslashes.
        s = _re.sub(r"\\\\", r"\\", repr(self.__pattern)[1:-1])
        # Replace any one-character classes with a single (possibly escaped) character
        s = _re.sub(r"\[([^\\]|\\.)\]", lambda m: str(__class__._to_pregex(m.group(1))) if len(m.group(1)) == 1 else m.group(1), s)
        # Replace negated class shorthand-notation characters with their non-class shorthand-notation.
        return _re.sub(r"\[\^(\\w|\\d|\\s)\]", lambda m: m.group(1).upper(), s)
        

    def __add__(self, pre: str or 'Pregex') -> 'Pregex':
        '''
        Calls "self._add" in order to concatenate this instance with the provided \
        string or "Pregex" instance, and returns the resulting "Pregex" instance.

        :param pre: The string or "pregex" instance that is to be concatenated with \
            this instance. 
        '''
        return __class__._add(self, pre)

    def __radd__(self, pre: str or 'Pregex') -> 'Pregex':
        '''
        Invokes "self._add" in order to concatenate the provided string or "Pregex" instance \
        with this instance, and returns the resulting "Pregex" instance.

        :param pre: The string or "pregex" instance that is to be concatenated with \
            this instance. 
        '''
        return __class__._add(pre, self)

    def __mul__(self, n: int) -> 'Pregex':
        '''
        Invokes "self._exactly" in order to apply the "{n}" quantifier \
        on this instance, and returns the resulting "Pregex" instance.

        :param int n: The parameter "n" provided to the "self.exactly" method.
        '''
        return self._exactly(n)

    def __rmul__(self, n: int) -> 'Pregex':
        '''
        Invokes "self._exactly" in order to apply the "{n}" quantifier \
        on this instance, and returns the resulting "Pregex" instance.

        :param int n: The parameter "n" provided to the "self.exactly" method.
        '''
        return self._exactly(n)

    def __is_group(self) -> bool:
        '''
        Looks at the underlying pattern of this instance, and returns either \
        "True" or "False", depending on whether this instance is a group or not.
        '''
        if self.__pattern.startswith('(') and self.__pattern.endswith(')'):
            n_open = 0
            for i in range(1, len(self.__pattern) - 1):
                prev_char, curr_char = self.__pattern[i-1], self.__pattern[i]
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

    def __iterate_match_objects(self, text: str) -> _Iterator[_re.Match]:
        '''
        Invokes "re.finditer" in order to iterate over all matches of this \
        instance's underlying pattern with the provided string "text" as \
        instances of type "re.Match".

        :param str text: The string that is to be matched.
        '''
        return _re.finditer(self.__pattern, text, flags=self.__flags) \
            if self.__compiled is None else self.__compiled.finditer(text)

    '''
    Tokens
    '''
    def _literal(self) -> 'Pregex':
        '''
        Scans this instance's underlying pattern for any characters that need to be escaped, \
        escapes them if there are any, and finally returns the resulting pattern wrapped \
        within a new "Pregex" instance.
        '''
        pattern = self.__pattern
        group_on_quantify = len(pattern.replace("\\", "")) > 1
        # Make sure that '\\' is first.
        for c in ('\\', '^', '$', '(', ')', '[', ']', '{', '}', '<', '>', '?', '+', '*', '.', '|', '-', '!', '=', ':',  '/'):
            pattern = pattern.replace(c, f"\{c}")
        return Pregex(pattern, group_on_concat=False, group_on_quantify=group_on_quantify)

    '''
    Quantifiers
    '''
    def _optional(self, is_greedy: bool = True)-> 'Pregex':
        '''
        Applies quantifier "?" on this instance's underlying pattern and \
        returns the resulting pattern wrapped within a new "Pregex" instance.

        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to 'True'.
        '''
        return Pregex(f"{self._quantify_conditional_group()}?{'' if is_greedy else '?'}", False, True)

    def _indefinite(self, is_greedy: bool = True) -> 'Pregex':
        '''
        Applies quantifier "*" on this instance's underlying pattern and \
        returns the resulting pattern wrapped within a new "Pregex" instance.

        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to 'True'.
        '''
        return Pregex(f"{self._quantify_conditional_group()}*{'' if is_greedy else '?'}", False, True)

    def _at_least_once(self, is_greedy: bool = True) -> 'Pregex':
        '''
        Applies quantifier "+" on this instance's underlying pattern and \
        returns the resulting pattern wrapped within a new "Pregex" instance.

        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to 'True'.
        '''
        return Pregex(f"{self._quantify_conditional_group()}+{'' if is_greedy else '?'}", False, True)

    def _exactly(self, n: int) -> 'Pregex':
        '''
        Applies quantifier "{n}" on this instance's underlying pattern and \
        returns the resulting pattern wrapped within a new "Pregex" instance.

        :param int n: The exact number of times that the provided pattern is to be matched.

        :raises:
            - NonIntegerArgumentException: If "n" is not an integer.
            - NonPositiveArgumentException: If "n" is either a negative integer or "0".
        '''
        if not isinstance(n, int) or isinstance(n, bool):
            raise _exceptions.NonIntegerArgumentException(n)
        if n < 1:
            raise _exceptions.NonPositiveArgumentException(n)
        elif n == 1:
            return self
        else:
            return Pregex(f"{self._quantify_conditional_group()}{{{n}}}", False, True)

    def _at_least(self, n: int, is_greedy: bool = True)-> 'Pregex':
        '''
        Applies quantifier "{n,}" on this instance's underlying pattern and \
        returns the resulting pattern wrapped within a new "Pregex" instance.

        :param int n: The minimum number of times that the provided pattern is to be matched.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to 'True'.

        :raises:
            - NonIntegerArgumentException: If "n" is not an integer.
            - NegativeArgumentException: If "n" is a negative integer.
        '''
        if not isinstance(n, int) or isinstance(n, bool):
            raise _exceptions.NonIntegerArgumentException(n)
        if n < 0:
            raise _exceptions.NegativeArgumentException(n)
        elif n == 0:
            return self._indefinite(is_greedy)
        elif n == 1:
            return self._at_least_once(is_greedy)
        else:
            return Pregex(f"{self._quantify_conditional_group()}{{{n},}}{'' if is_greedy else '?'}", False, True)

    def _at_most(self, n: int, is_greedy: bool = True) -> 'Pregex':
        '''
        Applies quantifier "{,n}" on this instance's underlying pattern and \
        returns the resulting pattern wrapped within a new "Pregex" instance.

        :param int n: The maximum number of times that the provided pattern is to be matched.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to 'True'.

        :raises:
            - NonIntegerArgumentException: If "n" is not an integer.
            - NonPositiveArgumentException: If "n" is either a negative integer or "0".
        '''
        if not isinstance(n, int) or isinstance(n, bool):
            raise _exceptions.NonIntegerArgumentException(n)
        if n < 1:
            raise _exceptions.NonPositiveArgumentException(n)
        elif n == 1:
            return self._optional(is_greedy)
        else:
            return Pregex(f"{self._quantify_conditional_group()}{{,{n}}}{'' if is_greedy else '?'}", False, True)

    def _at_least_at_most(self, min: int, max: int, is_greedy: bool = True) -> 'Pregex':
        '''
        Applies quantifier "{min,max}" on this instance's underlying pattern and \
        returns the resulting pattern wrapped within a new "Pregex" instance.

        :param int min: The minimum number of times that the provided pattern is to be matched.
        :param int max: The maximum number of times that the provided pattern is to be matched.
        :param bool is_greedy: Indicates whether to declare this quantifier as greedy. \
            When declared as such, the regex engine will try to match \
            the expression as many times as possible. Defaults to 'True'.

        :raises:
            - NonIntegerArgumentException: If either "min" or "max" is not an integer.
            - NegativeArgumentException: If either "min" or "max" is a negative integer.
            - NonPositiveArgumentException: If either "min" or "max" is either a negative \
                integer or "0".
            - MinGreaterThanMaxException: If "min" is greater than "max".
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
        elif min == max:
            return self._exactly(min)
        else:
            return Pregex(f"{self._quantify_conditional_group()}{{{min},{max}}}{'' if is_greedy else '?'}", False, True)

    '''
    Operators
    '''
    def _concat(self, pre: 'Pregex') -> 'Pregex':
        '''
        Concatenates the pattern of this instance with the provided pattern \
        and returns the resulting pattern wrapped within a new "Pregex" instance.

        :param Pregex pre: A "Pregex" instance containing he pattern on the right side \
            of the concatenation.
        '''
        return Pregex(
            f"{self._concat_conditional_group()}{pre._concat_conditional_group()}",
            group_on_concat=False,
            group_on_quantify=True)

    def _either(self, pre: 'Pregex') -> 'Pregex':
        '''
        Applies the "alternation" operator on this instance's underlying pattern and \
        the provided pattern, and returns the resulting pattern wrapped within a new \
        "Pregex" instance.

        :param Pregex pre: A "Pregex" instance containing he pattern on the right side \
            of the alternation.
        '''
        return Pregex(f"{self}|{pre}", group_on_concat=True, group_on_quantify=True)


    '''
    Groups
    '''
    def _capturing_group(self, name: str = '') -> 'Pregex':
        '''
        Applies a function on this instance's underlying pattern, that does the \
        following based on the nature of the pattern:
            - If pattern is not a group, then wraps it within a capturing group.
            - If pattern is a non-capturing group, then converts it to a capturing group.
            - If pattern is a capturing-group and "name" is the empty string, then \
                does nothing.
            - If pattern is an unnamed capturing group and "name" is not the empty string, \
                then assigns said name to the capturing group.
            - If pattern is a named capturing group and "name" is not the empty string, \
                then changes the capturing group's name to the provided name.

        Finally, returns the resulting pattern wrapped within a "Pregex" instance.

        :param name: If this parameter is not equal to the empty string, then assigns \
            it as a name to the capturing group. Defaults to the empty string.

        :raises:
            - NonStringArgumentException: If the provided "name" parameter is not a string.
            - InvalidCapturingGroupNameException: If the provided "name" parameter is not a valid \
                name for a capturing group. such a name must only contain alphanumeric characters \
                plus the character "_", and begin with a non-digit character.
        '''
        if not isinstance(name, str):
            raise _exceptions.NonStringArgumentException()
        if name != '' and _re.fullmatch("[A-Za-z_]\w*", name) is None:
            raise _exceptions.InvalidCapturingGroupNameException(name)
        if self.__is_group():
            pattern = self.__pattern.replace('?:', '', 1) if self.__pattern.startswith('(?:') else str(self)
            if name != '':
                if pattern.startswith('(?P'):
                    pattern = _re.sub('\(\?P<[^>]*>', f'(?P<{name}>', pattern)
                else:
                    pattern = f"(?P<{name}>{pattern[1:-1]})"
        else:
            pattern = f"({f'?P<{name}>' if name != '' else ''}{self})"
        return Pregex(pattern, False, False)

    def _non_capturing_group(self) -> 'Pregex':
        '''
        Applies a function on this instance's underlying pattern, that does the \
        following based on the nature of the pattern:
            - If pattern is not a group, then wraps it within a non-capturing group.
            - If pattern is a non-capturing group, then does nothing.
            - If pattern is a capturing-group, then converts it to a non-capturing group.

        Finally, returns the resulting pattern wrapped within a "Pregex" instance.
        '''
        if self.__is_group():
            if self.__pattern.startswith('(?P'):
                pattern = _re.sub('\(\?P<[^>]*>', f'(?:', str(self))
            elif not self.__pattern.startswith('(?:'):
                pattern = self.__pattern.replace('(', '(?:', 1)
            else:
                pattern = str(self)
            return Pregex(pattern, False, False)
        return Pregex(f"(?:{self})", False, False)

    '''
    Assertions
    '''
    def _match_at_start(self) -> 'Pregex':
        '''
        Applies assertion "\A" on this instance's underlying pattern and \
        returns the resulting pattern wrapped within a new "Pregex" instance.
        '''
        return Pregex(f"\\A{self}")

    def _match_at_end(self) -> 'Pregex':
        '''
        Applies assertion "\Z" on this instance's underlying pattern and \
        returns the resulting pattern wrapped within a new "Pregex" instance.
        '''
        return Pregex(f"{self}\\Z")

    def _match_at_line_start(self) -> 'Pregex':
        '''
        Applies assertion "^" on this instance's underlying pattern and \
        returns the resulting pattern wrapped within a new "Pregex" instance.
        '''
        return Pregex(f"^{self}")

    def _match_at_line_end(self) -> 'Pregex':
        '''
        Applies assertion "$" on this instance's underlying pattern and \
        returns the resulting pattern wrapped within a new "Pregex" instance.
        '''
        return Pregex(f"{self}$")

    def _match_at_word_boundary(self) -> 'Pregex':
        '''
        Applies assertion "\\b" on both sides of this instance's underlying pattern \
        and returns the resulting pattern wrapped within a new "Pregex" instance.
        '''
        return Pregex(f"\\b{self}\\b")

    def _match_at_left_word_boundary(self) -> 'Pregex':
        '''
        Applies assertion "\\b" on the left side  of this instance's underlying pattern \
        and returns the resulting pattern wrapped within a new "Pregex" instance.
        '''
        return Pregex(f"\\b{self}")

    def _match_at_right_word_boundary(self) -> 'Pregex':
        '''
        Applies assertion "\\b" on the right side  of this instance's underlying pattern \
        and returns the resulting pattern wrapped within a new "Pregex" instance.
        '''
        return Pregex(f"{self}\\b")

    def _followed_by(self, pre: 'Pregex') -> 'Pregex':
        '''
        Applies the "lookahead" assertion "(?=pre)" on this instance's underlying pattern \
        and returns the resulting pattern wrapped within a new "Pregex" instance.

        :param Pregex | str pre: The non-matching pattern of the assertion.
        '''
        return Pregex(f"{self}(?={pre})")

    def _not_followed_by(self, pre: 'Pregex') -> 'Pregex':
        '''
        Applies the "negative lookahead" assertion "(?!pre)" on this instance's underlying \
        pattern and returns the resulting pattern wrapped within a new "Pregex" instance.

        :param Pregex pre: The non-matching pattern of the assertion.
        '''
        return Pregex(f"{self}(?!{pre})")

    def _preceded_by(self, pre: 'Pregex') -> 'Pregex':
        '''
        Applies the "lookbehind" assertion "(?<=pre)" on this instance's underlying pattern \
        and returns the resulting pattern wrapped within a new "Pregex" instance.

        :param Pregex pre: The non-matching pattern of the assertion.
        '''

        return Pregex(f"(?<={pre}){self}")

    def _not_preceded_by(self, pre: 'Pregex') -> 'Pregex':
        '''
        Applies the "negative lookbehind" assertion "(?<!pre)" on this instance's underlying \
        pattern and returns the resulting pattern wrapped within a new "Pregex" instance.

        :param Pregex pre: The non-matching pattern of the assertion.
        '''
        return Pregex(f"(?<!{pre}){self}")
