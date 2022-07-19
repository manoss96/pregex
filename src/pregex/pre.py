import re as _re
import pregex.exceptions as _exceptions
from typing import Iterator as _Iterator

class Pregex():
    
    '''
    This class constitutes the basis for every other "Pregex" subclass.
    '''

    '''
    The totality of active flags.
    '''
    __flags: _re.RegexFlag = _re.MULTILINE | _re.DOTALL


    def __init__(self, pattern: str, group_on_concat=False, group_on_quantify=False) -> 'Pregex':
        '''
        Creates a 'Pregex' instance based on the provided pattern.

        :param Pregex | str pattern: The RegEx pattern based on which the "Pregex" instance is created.
        :param bool group_on_concat: Indicates whether this expression requires getting groupped \
            whenever it is concatenated with an other expression.
        :param bool group_on_quantify: Indicates whether this expression requires getting groupped \
            whenever it has a quantifier applied to it.
        '''
        self.__pattern: str = pattern
        self.__group_on_concat: bool = group_on_concat
        self.__group_on_quantify: bool = group_on_quantify
        self.__compiled: _re.Pattern = None


    '''
    Public Methods
    '''
    def get_pattern(self, include_flags=False) -> str:
        '''
        Returns the expression's pattern as its string representation.

        :param bool include_falgs: Indicates whether to display the RegEx flags along with the pattern.

        NOTE: This method is to be preferred over str() when one needs to display the pattern.
        '''
        pattern = repr(self)
        return f"/{pattern}/gms" if include_flags else pattern

    def compile(self) -> None:
        '''
        Compiles the underlying RegEx pattern. After invoking this method, \
        any attempt at matching a string will use the compiled RegEx pattern.
        '''
        self.__compiled = _re.compile(self.__pattern, flags=self.__flags)

    def has_match(self, text: str) -> bool:
        '''
        Returns 'True' if 'text' matches this pattern at least once.

        :param str text: The piece of text that is to be matched.
        '''
        return bool(_re.search(self.__pattern, text) if self.__compiled is None \
            else self.__compiled.search(text, flags=self.__flags))

    def is_exact_match(self, text: str) -> bool:
        '''
        Returns 'True' only if 'text' matches this pattern exactly.

        :param str text: The piece of text that is to be matched.
        '''
        return bool(_re.fullmatch(self.__pattern, text, flags=self.__flags) \
            if self.__compiled is None else self.__compiled.fullmatch(text))

    def iterate_matches(self, text: str) -> _Iterator[str]:
        '''
        Generates any possible matches with 'text' one by one.

        :param str text: The piece of text that is to be matched.
        '''
        for match in self.__iterate_match_objects(text):
            yield match.group(0)

    def iterate_matches_and_pos(self, text: str) -> _Iterator[tuple[str, int, int]]:
        '''
        Generates any possible matches with 'text' one by one, \
        along with their exact position within the text.

        :param str text: The piece of text that is to be matched.
        '''
        for match in self.__iterate_match_objects(text):
            yield (match.group(0), *match.span())

    def iterate_groups(self, text: str, include_empty: bool = True) -> _Iterator[tuple[str]]:
        '''
        Generates any tuples of captured groups that may have occured \
        due to this pattern matching with 'text' one by one.

        :param str text: The piece of text that is to be matched.
        :param bool include_empty: Indicates whether to include empty groups into the results.
        '''
        for match in self.__iterate_match_objects(text):
            yield match.groups() if include_empty else \
                tuple(group for group in match.groups() if group != '')

    def iterate_groups_and_pos(self, text: str, include_empty: bool = True) -> _Iterator[list[tuple[str, int, int]]]:
        '''
        Generates any tuples of captured groups that may have occured \
        due to this pattern matching with 'text' one by one, along with \
        their exact position within the text.

        :param str text: The piece of text that is to be matched.
        :param bool include_empty: Indicates whether to include empty groups into the results.
        '''
        for match in self.__iterate_match_objects(text):
            groups, counter = list(), 0
            for group in match.groups():
                counter += 1
                if include_empty or (group != ''):
                    groups.append((group, *match.span(counter)))
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
        Returns a list containing tuples of any captured groups that may \
        have occured due to this pattern matching with 'text'.

        :param str text: The piece of text that is to be matched.
        :param bool include_empty: Indicates whether to include empty groups into the results.
        '''
        return list(group for group in self.iterate_groups(text, include_empty))

    def get_groups_and_pos(self, text: str, include_empty: bool = True) -> list[list[tuple[str, int, int]]]:
        '''
        Returns a list containing tuples of any captured groups that may \
        have occured due to this pattern matching with 'text', along with \
        their exact position within the text.

        :param str text: The piece of text that is to be matched.
        :param bool include_empty: Indicates whether to include empty groups into the results.
        '''
        return list(tup for tup in self.iterate_groups_and_pos(text, include_empty))

    def replace(self, text: str, repl: str, count: int = 0) -> str:
        '''
        Substitutes all or some of the matches within "text" for "repl" \
        and returns the resulting string. If there are no matches, returns \
        string "text" exactly as provided.

        :param str s: The string that is to be matched and modified.
        :param str repl: The string that is to replace any matches.
        :param int count: The number of matches that are to be replaced, \
            starting from left to right. The default value '0' indicates \
            that all matches must be replaced.
        '''
        if count < 0:
            raise _exceptions.NegativeArgumentException(count)
        return _re.sub(str(self), repl, text, count, flags=self.__flags)

    def split_by_match(self, text: str) -> list[str]:
        '''
        Splits the provided text based on any possible matches \
        and returns it as a list containing each individual part \
        of the text after the split.

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
        and returns it as a list containing each individual part \
        of the text after the split.

        :param str text: The piece of text that is to be matched and split.
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
        return self.__group_on_concat

    def _get_group_on_quantify(self) -> bool:
        return self.__group_on_quantify

    def _concat_conditional_group(self) -> 'Pregex':
        return self._non_capturing_group() if self.__group_on_concat else self

    def _quantify_conditional_group(self) -> 'Pregex':
        return self._non_capturing_group() if self.__group_on_quantify else self

    def _to_pregex(pre: str or 'Pregex') -> 'Pregex':
        if isinstance(pre, str):
            return Pregex(pre)._literal()
        elif issubclass(pre.__class__, __class__):
            return pre
        else:
            raise _exceptions.NeitherStringNorPregexException()

    def _add(pre1: str or 'Pregex', pre2: str or 'Pregex') -> 'Pregex':
        return __class__._to_pregex(pre1)._concat(__class__._to_pregex(pre2))


    ''' 
    Private Methods
    '''
    def __str__(self) -> str:
        '''
        Returns the string representation of this class instance.
        '''
        return self.__pattern

    def __repr__(self) -> str:
        '''
        Returns the string representation of this class instance in a printable format.
        '''
        return _re.sub(r"\\\\", r"\\", repr(self.__pattern)[1:-1])

    def __add__(self, pre: str or 'Pregex') -> 'Pregex':
        return __class__._add(self, pre)

    def __radd__(self, pre: str or 'Pregex') -> 'Pregex':
        return __class__._add(pre, self)

    def __mul__(self, n) -> 'Pregex':
        return self._exactly(n)

    def __rmul__(self, n) -> 'Pregex':
        return self._exactly(n)

    def __is_group(self) -> bool:
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
        Iterates over all matches as objects of type '_re.Match'
        '''
        return _re.finditer(self.__pattern, text, flags=self.__flags) \
            if self.__compiled is None else self.__compiled.finditer(text)

    '''
    Tokens
    '''
    def _literal(self) -> 'Pregex':
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
        return Pregex(f"{self._quantify_conditional_group()}?{'' if is_greedy else '?'}", False, True)

    def _indefinite(self, is_greedy: bool = True) -> 'Pregex':
        return Pregex(f"{self._quantify_conditional_group()}*{'' if is_greedy else '?'}", False, True)

    def _enforced(self, is_greedy: bool = True) -> 'Pregex':
        return Pregex(f"{self._quantify_conditional_group()}+{'' if is_greedy else '?'}", False, True)

    def _exactly(self, n: int) -> 'Pregex':
        if not isinstance(n, int) or isinstance(n, bool):
            raise _exceptions.NonIntegerArgumentException(n)
        if n < 1:
            raise _exceptions.NonPositiveArgumentException(n)
        elif n == 1:
            return self
        else:
            return Pregex(f"{self._quantify_conditional_group()}{{{n}}}", False, True)

    def _at_least(self, n: int, is_greedy: bool = True)-> 'Pregex':
        if not isinstance(n, int) or isinstance(n, bool):
            raise _exceptions.NonIntegerArgumentException(n)
        if n < 0:
            raise _exceptions.NegativeArgumentException(n)
        elif n == 0:
            return self._indefinite(is_greedy)
        elif n == 1:
            return self._enforced(is_greedy)
        else:
            return Pregex(f"{self._quantify_conditional_group()}{{{n},}}{'' if is_greedy else '?'}", False, True)

    def _at_most(self, n: int, is_greedy: bool = True) -> 'Pregex':
        if not isinstance(n, int) or isinstance(n, bool):
            raise _exceptions.NonIntegerArgumentException(n)
        if n < 1:
            raise _exceptions.NonPositiveArgumentException(n)
        elif n == 1:
            return self._optional(is_greedy)
        else:
            return Pregex(f"{self._quantify_conditional_group()}{{,{n}}}{'' if is_greedy else '?'}", False, True)

    def _at_least_at_most(self, min: int, max: int, is_greedy: bool = True) -> 'Pregex':
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
    def _concat(self, pre: str or 'Pregex') -> 'Pregex':
        pre = __class__._to_pregex(pre)
        return Pregex(
            f"{self._concat_conditional_group()}{pre._concat_conditional_group()}",
            group_on_concat=False,
            group_on_quantify=True)

    def _either(self, pre: str or 'Pregex') -> 'Pregex':
        pre = __class__._to_pregex(pre)
        return Pregex(f"{self}|{pre}", group_on_concat=True, group_on_quantify=True)


    '''
    Groups
    '''
    def _capturing_group(self, name: str) -> 'Pregex':
        if not isinstance(name, str):
            raise _exceptions.NonStringArgumentException()
        if name != '' and _re.fullmatch("[A-Za-z_][A-Za-z_0-9]*", name) is None:
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
        return Pregex(f"\\A{self}")

    def _match_at_end(self) -> 'Pregex':
        return Pregex(f"{self}\\Z")

    def _match_at_line_start(self) -> 'Pregex':
        return Pregex(f"^{self}")

    def _match_at_line_end(self) -> 'Pregex':
        return Pregex(f"{self}$")

    def _match_at_word_boundary(self) -> 'Pregex':
        return Pregex(f"\\b{self}\\b")

    def _match_at_left_word_boundary(self) -> 'Pregex':
        return Pregex(f"\\b{self}")

    def _match_at_right_word_boundary(self) -> 'Pregex':
        return Pregex(f"{self}\\b")

    def _followed_by(self, pre: str or 'Pregex') -> 'Pregex':
        pre = __class__._to_pregex(pre)
        return Pregex(f"{self}(?={pre})")

    def _not_followed_by(self, pre: str or 'Pregex') -> 'Pregex':
        pre = __class__._to_pregex(pre)
        return Pregex(f"{self}(?!{pre})")

    def _preceded_by(self, pre: str or 'Pregex') -> 'Pregex':
        pre = __class__._to_pregex(pre)
        return Pregex(f"(?<={pre}){self}")

    def _not_preceded_by(self, pre: str or 'Pregex') -> 'Pregex':
        pre = __class__._to_pregex(pre)
        return Pregex(f"(?<!{pre}){self}")
