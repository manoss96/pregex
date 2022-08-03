
import re as _re
import pregex.pre as _pre
import pregex.exceptions as _exceptions
from string import whitespace as _whitespace


class __Class(_pre.Pregex):
    '''
    Constitutes the base class for every class within "classes.py".

    Operations defined for classes:
        - Union:
            AnyLowercaseLetter() | AnyDigit() => [a-z0-9]
        - Subtraction:
            AnyLetter() - AnyLowercaseLetter() => [A-Z]
        - Negation:
            ~ AnyLowercaseLetter() => [^a-z]

    NOTE: Union and subtraction can only be performed on a pair of classes of the same type, \
        that is, either a pair of regular classes or a pair of negated classes.
    '''

    def __init__(self, pattern: str, is_negated: bool) -> '__Class':
        super().__init__(__class__.__simplify(pattern, is_negated), escape=False)
        self._set_type(__class__._PatternType.Class)
        self.__is_negated = is_negated
        self.__verbose = pattern

    def get_verbose_pattern(self) -> str:
        '''
        Returns a verbose representation of this class' pattern.
        '''
        return self.__verbose

    def __simplify(pattern: str, is_negated: bool) -> str:
        '''
        Converts a verbose pattern to its simplified form.
        '''
        if pattern == ".":
            return pattern
        # Use shorthand notation for any classes that support this.
        ranges, chars = __class__.__extract_classes(pattern)
        classes = __class__.__verbose_to_shorthand(ranges.union(chars))
        pattern = ''.join(f"[{'^' if is_negated else ''}{''.join(classes)}]")
        # Replace any one-character classes with a single (possibly escaped) character
        pattern = _re.sub(r"\[([^\\]|\\.)\]", lambda m: str(__class__._to_pregex(m.group(1))) \
            if len(m.group(1)) == 1 else m.group(1), pattern)
        # Replace negated class shorthand-notation characters with their non-class shorthand-notation.
        return _re.sub(r"\[\^(\\w|\\d|\\s)\]", lambda m: m.group(1).upper(), pattern)

    def __verbose_to_shorthand(classes: set[str]) -> set[str]:
        '''
        This method searches the provided set for subsets of character classes that \
        correspond to a shorthand-notation character class, and if it finds any, it \
        replaces them with said character class, returning the resulting set at the end.

        :param set[str] classes: The set containing the classes as strings.
        '''
        word_set = {'a-z', 'A-Z', '0-9', '_'}
        digit_set = {'0-9'}
        whitespace_set = {' ', '\t', '\n', '\r', '\x0b', '\x0c'}
        if classes.issuperset(word_set):
            classes = classes.difference(word_set).union({'\w'})
        elif classes.issuperset(digit_set):
            classes = classes.difference(digit_set).union({'\d'})
        if classes.issuperset(whitespace_set):
            classes = classes.difference(whitespace_set).union({'\s'})
        return classes

    def __invert__(self) -> '__Class':
        s, rs = '' if self.__is_negated else '^', '^' if self.__is_negated else ''
        return __class__(f"[{s}{self.__verbose.lstrip('[' + rs).rstrip(']')}]", not self.__is_negated)

    def __or__(self, pre: '__Class') -> '__Class':
        if not issubclass(pre.__class__, __class__):
            raise _exceptions.CannotBeUnionedException(self, pre, False)
        return __class__.__or(self, pre)

    def __ror__(self, pre: '__Class') -> '__Class':
        if not issubclass(pre.__class__, __class__):
            raise _exceptions.CannotBeUnionedException(pre, self, False)
        return __class__.__or(pre, self)

    def __or(pre1: '__Class', pre2: '__Class') -> '__Class':
        if  pre1.__is_negated != pre2.__is_negated:
            raise _exceptions.CannotBeUnionedException(pre1, pre2, True)
        if isinstance(pre1, Any) or isinstance(pre2, Any):
            return Any()

        ranges1, chars1 = __class__.__extract_classes(pre1.__verbose)
        ranges2, chars2 = __class__.__extract_classes(pre2.__verbose)
        ranges, chars = ranges1.union(ranges2), chars1.union(chars2)

        return  __class__(
            f"[{'^' if pre1.__is_negated else ''}{''.join(__class__.__reduce(ranges, chars))}]",
            pre1.__is_negated)

    def __sub__(self, pre: '__Class') -> '__Class':
        if not issubclass(pre.__class__, __class__):
            raise _exceptions.CannotBeSubtractedException(self, pre, False)
        return __class__.__sub(self, pre)

    def __rsub__(self, pre: '__Class') -> '__Class':
        if not issubclass(pre.__class__, __class__):
            raise _exceptions.CannotBeSubtractedException(pre, self, False)
        return __class__.__sub(pre, self)

    def __sub(pre1: '__Class', pre2: '__Class') -> '__Class':
        if  pre1.__is_negated != pre2.__is_negated:
            raise _exceptions.CannotBeSubtractedException(pre1, pre2, True)
        if isinstance(pre2, Any):
            raise _exceptions.EmptyClassException(pre1, pre2)
        if isinstance(pre1, Any):
            return ~ pre2

        ranges1, chars1 = __class__.__extract_classes(pre1.__verbose)
        ranges2, chars2 = __class__.__extract_classes(pre2.__verbose)

        # Subtract any ranges found in both pre2 and pre1 from pre1.
        def subtract_ranges(ranges1: set[str], ranges2: set[str]) -> tuple[set[str], set[str]]:
            '''
            Subtracts any range found within 'ranges2' from 'ranges1' and returns \
            the resulting ranges/characters in two seperate sets.

            NOTE: This method might produce characters, for example [A-Z] - [B-Z] \
                produces the character 'A'.
            '''

            ranges1 = [rng.split('-') for rng in ranges1]
            ranges2 = [rng.split('-') for rng in ranges2]

            i = 0
            while i < len(ranges1):
                start_1, end_1 = ranges1[i]
                for start_2, end_2 in ranges2:
                    if start_1 <= end_2 and end_1 >= start_2:
                        if start_1 == start_2 and end_1 == end_2:
                            ranges1.pop(i)
                            i -= 1
                            break
                        split_rng = list()
                        if start_1 <= start_2 and end_1 <= end_2:
                            split_rng.append((start_1, chr(ord(start_2) - 1)))
                        elif start_1 >= start_2 and end_1 >= end_2:
                            split_rng.append((chr(ord(end_2) + 1), end_1))
                        else:
                            split_rng.append((start_1, chr(ord(start_2) - 1)))
                            split_rng.append((chr(ord(end_2) + 1), end_1))
                        if len(split_rng) > 0:
                            ranges1.pop(i)
                            i -= 1
                            ranges1 = ranges1 + split_rng
                            break
                i += 1
                    
            ranges, chars = set(), set()
            for start, end in ranges1:
                if start == end:
                    chars.add(start)
                else:
                    ranges.add(f"{start}-{end}")
            
            return ranges, chars


        # Subtract chars2 from chars1.
        chars1 = chars1.difference(chars2)

        # Subtract ranges2 from ranges1.
        ranges1, reduced_chars = subtract_ranges(ranges1, ranges2)
        chars1 = chars1.union(reduced_chars)

        # Subtract any characters in chars2 from ranges1.
        ranges1, reduced_chars = subtract_ranges(ranges1, set(f"{c}-{c}" for c in chars2 if len(c) == 1))
        chars1 = chars1.union(reduced_chars)

        result = ranges1.union(chars1)

        if len(result) == 0:
            raise _exceptions.EmptyClassException(pre1, pre2)

        return  __class__(
            f"[{'^' if pre1.__is_negated else ''}{''.join(result)}]",
            pre1.__is_negated)

    def __extract_classes(pattern: str) -> tuple[set[str], set[str]]:
        '''
        Extracts all classes from the provided class pattern and returns them \
        separated into two different sets based on whether they constitute a range \
        or an individual character.
        '''

        def get_start_index(pattern: str):
            if pattern.startswith('[^'):
                return 2
            elif pattern.startswith('['):
                return 1
            return 0
        
        # Remove brackets etc from string.
        start_index = get_start_index(pattern)
        classes = pattern[start_index:-1]
        
        # Return classes as a string.
        return (__class__.__extract_ranges(classes), __class__.__extract_chars(classes))


    def __extract_ranges(classes: 'str') -> set[str]:
        '''
        Extracts all ranges from the provided character class pattern and returns \
        a set containing them.

        :param str classes: One or more string character class patterns.
        '''

        return set(_re.findall("[A-Za-z0-9]-[A-Za-z0-9]", classes, flags=_re.DOTALL))


    def __extract_chars(classes: str) -> set[str]:
        '''
        Extracts all individual characters from the provided character class pattern \
        and returns a set containing them.

        :param str classes: One or more string character class patterns.
        '''
        return set(_re.findall(r"(?<!\w\-)(?:\\-|\\?[^\-])(?!\-\w)", classes, flags=_re.DOTALL))
        

    def __reduce(ranges: set[str], chars: set[str]) -> set[str]:
        '''
        Removes any characters or any sub-ranges if those are already included
        within an other specified range, and returns the set of all remaining
        ranges/characters.

        :param set[str] ranges: A set containing all specified ranges.
        :param set[str] chars: A set containing all specified chars.
        '''

        def reduce_ranges(ranges: list[str]) -> set[str]:
            '''
            Removes any sub-ranges if they are already included within an other specified range,
            and returns the set of all remaining ranges.

            :param list[str] ranges: A list containing all specified ranges.
            '''
            if len(ranges) < 2:
                return set(ranges)
            
            ranges = [rng.split('-') for rng in ranges]

            i = 0
            while i < len(ranges):
                start_i, end_i = ranges[i]
                j = 0
                while j < len(ranges):
                    if i != j:
                        start_j, end_j = ranges[j]
                        if start_i <= start_j and ord(end_i) + 1 >= ord(start_j):
                            ranges[i] = start_i, max(end_i, end_j)
                            ranges.pop(j)
                            i = -1
                            break
                    j += 1
                i += 1

            return set(f"{rng[0]}-{rng[1]}" for rng in ranges)

        lower = list(filter(lambda e: e.islower(), ranges))
        upper = list(filter(lambda e: e.isupper(), ranges.difference(lower)))
        digit = list(ranges.difference(lower).difference(upper))

        ranges = reduce_ranges(lower) \
            .union(reduce_ranges(upper)) \
            .union(reduce_ranges(digit))

        def reduce_chars(ranges: list[str], chars: list[str]):
            '''
            Removes any characters if those are already included within an other specified range,
            and returns the set of all remaining characters.

            :param list[str] ranges: A list containing all specified ranges.
            :param list[str] chars: A list containing all specified chars.
            '''

            ranges = [rng.split('-') for rng in ranges]

            i = 0
            while i < len(chars):
                for j in range(len(ranges)):
                    start, end = ranges[j]
                    if len(chars[i]) > 1:
                        continue
                    if chars[i] >= start and chars[i] <= end:
                        chars.pop(i)
                        i = -1
                    elif ord(start) == ord(chars[i]) + 1:
                        ranges[j][0] = chars[i]
                        chars.pop(i)
                        i = -1
                    elif ord(end) == ord(chars[i]) - 1:
                        ranges[j][1] = chars[i]
                        chars.pop(i)
                        i = -1
                i += 1

            return set(f"{rng[0]}-{rng[1]}" for rng in ranges), set(chars)

        ranges, chars = reduce_chars(list(ranges), list(chars))

        return ranges.union(chars)


class Any(__Class):
    '''
    Matches any possible character, including the newline character. \
    In order to match every character except for the newline character, \
    one can use "~AnyFrom('\\n')" or "AnyButFrom('\\n')".
    '''

    def __init__(self) -> 'Any':
        '''
        Matches any possible character, including the newline character. \
        In order to match every character except for the newline character, \
        one can use "~AnyFrom('\\n')" or "AnyButFrom('\\n')".
        '''
        super().__init__('.', is_negated=False)


class AnyLetter(__Class):
    '''
    Matches any alphabetic character.
    '''

    def __init__(self) -> 'AnyLetter':
        '''
        Matches any alphabetic character.
        '''
        super().__init__('[a-zA-Z]', False)


class AnyButLetter(__Class):
    '''
    Matches any character except for alphabetic characters. \
    Equivalent to "~AnyLetter()".
    '''

    def __init__(self) -> 'AnyButLetter':
        '''
        Matches any character except for alphabetic characters. \
        Equivalent to "~AnyLetter()".
        '''
        super().__init__('[^a-zA-Z]', True)


class AnyLowercaseLetter(__Class):
    '''
    Matches any lowercase alphabetic character.
    '''

    def __init__(self) -> 'AnyLowercaseLetter':
        '''
        Matches any lowercase alphabetic character.
        '''
        super().__init__('[a-z]', False)



class AnyButLowercaseLetter(__Class):
    '''
    Matches any character except for lowercase alphabetic characters. \
    Equivalent to "~AnyLowercaseLetter()".
    '''

    def __init__(self) -> 'AnyButLowercaseLetter':
        '''
        Matches any character except for lowercase alphabetic characters. \
        Equivalent to "~AnyLowercaseLetter()".
        '''
        super().__init__('[^a-z]', True)

    
class AnyUppercaseLetter(__Class):
    '''
    Matches any uppercase alphabetic character.
    '''

    def __init__(self) -> 'AnyUppercaseLetter':
        '''
        Matches any uppercase alphabetic character.
        '''
        super().__init__('[A-Z]', False)


class AnyButUppercaseLetter(__Class):
    '''
    Matches any character except for uppercase alphabetic characters. \
    Equivalent to "~AnyUppercaseLetter()".
    '''

    def __init__(self) -> 'AnyButUppercaseLetter':
        '''
        Matches any character except for uppercase alphabetic characters. \
        Equivalent to "~AnyUppercaseLetter()".
        '''
        super().__init__('[^A-Z]', True)


class AnyDigit(__Class):
    '''
    Matches any numeric character.
    '''

    def __init__(self) -> 'AnyDigit':
        '''
        Matches any numeric character.
        '''
        super().__init__('[0-9]', False)


class AnyButDigit(__Class):
    '''
    Matches any character except for numeric characters. \
    Equivalent to "~AnyDigit()".
    '''

    def __init__(self) -> 'AnyButDigit':
        '''
        Matches any character except for numeric characters. \
        Equivalent to "~AnyDigit()".
        '''
        super().__init__('[^0-9]', True)


class AnyWordChar(__Class):
    '''
    Matches any alphanumeric character plus "_".
    '''

    def __init__(self) -> 'AnyWordChar':

        '''
        Matches any alphanumeric character plus "_".
        '''
        super().__init__('[a-zA-Z0-9_]', False)


class AnyButWordChar(__Class):
    '''
    Matches any character except for alphanumeric characters plus "_". \
    Equivalent to "~AnyWordChar()".
    '''

    def __init__(self) -> 'AnyButWordChar':
        '''
        Matches any character except for alphanumeric characters plus "_".. \
        Equivalent to "~AnyWordChar()".
        '''
        super().__init__('[^a-zA-Z0-9_]', True)


class AnyPunctuation(__Class):
    '''
    Matches any puncutation character.
    '''

    def __init__(self) -> 'AnyPunctuation':
        '''
        Matches any puncutation character.
        '''
        super().__init__('[\^\-\[\]!"#$%&\'()*+,./:;<=>?@_`{|}~\\\\]', False)


class AnyButPunctuation(__Class):
    '''
    Matches any character except for punctuation characters. \
    Equivalent to "~AnyPuncutation()".
    '''

    def __init__(self) -> 'AnyButPunctuation':
        '''
        Matches any character except for punctuation characters. \
        Equivalent to "~AnyPunctuation()".
        '''
        super().__init__('[^\^\-\[\]!"#$%&\'()*+,./:;<=>?@_`{|}~\\\\]', True)


class AnyWhitespace(__Class):
    '''
    Matches any whitespace character.
    '''

    def __init__(self) -> 'AnyWhitespace':
        '''
        Matches any whitespace character.
        '''
        super().__init__(f'[{_whitespace}]', False)


class AnyButWhitespace(__Class):
    '''
    Matches any character except for whitespace characters. \
    Equivalent to "~AnyWhitespace()".
    '''

    def __init__(self) -> 'AnyButWhitespace':
        '''
        Matches any character except for whitespace characters. \
        Equivalent to "~AnyWhitespace()".
        '''
        super().__init__(f'[^{_whitespace}]', True)


class AnyWithinRange(__Class):
    '''
    Matches any character within the provided range.

    :param str | int start: The first character within the range.
    :param str | int end: The last character within the range.
    '''

    def __init__(self, start: str or int, end: str or int) -> 'AnyWithinRange':
        '''
        Matches any character within the provided range.

        :param str | int start: The first character within the range.
        :param str | int end: The last character within the range.
        '''
        start, end = str(start), str(end)
        if start >= end or (not start.isalnum()) or (not end.isalnum()):
            raise _exceptions.InvalidRangeException(start, end)
        super().__init__(f"[{start}-{end}]", False)


class AnyButWithinRange(__Class):
    '''
    Matches any character except for all characters within the provided range. \
    Equivalent to "~AnyWithinRange()".

    :param str | int start: The first character within the range.
    :param str | int end: The last character within the range.
    '''

    def __init__(self, start: str or int, end: str or int) -> 'AnyButWithinRange':
        '''
        Matches any character except for all characters within the provided range. \
         Equivalent to "~AnyWithinRange()".

        :param str | int start: The first character within the range.
        :param str | int end: The last character within the range.
        '''
        start, end = str(start), str(end)
        if start >= end or (not start.isalnum()) or (not end.isalnum()):
            raise _exceptions.InvalidRangeException(start, end)
        super().__init__(f"[^{start}-{end}]", True)      


class AnyFrom(__Class):
    '''
    Matches any one of the provided characters.

    :param Pregex | str *chars: One or more characters to match from. Each character must be \
        a string of length one, provided either as is or wrapped within a "tokens" class.
    '''

    def __init__(self, *chars: str or _pre.Pregex) -> 'AnyFrom':
        '''
        Matches any one of the provided characters.

        :param Pregex | str *chars: One or more characters to match from. Each character must be \
            a string of length one, provided either as is or wrapped within a "tokens" class.
        '''
        for c in chars:
            if not issubclass(c.__class__, (str, _pre.Pregex)):
                raise _exceptions.NeitherStringNorTokenException()
            if issubclass(c.__class__, _pre.Pregex) and c._get_type() != __class__._PatternType.Token:
                raise _exceptions.NeitherStringNorTokenException()
        to_escape = {'\\', '^', '[', ']', '-', "'"}
        chars = tuple((f"\{c}" if c in to_escape else c) if isinstance(c, str) \
             else str(c) for c in set(chars))
        super().__init__(f"[{''.join(chars)}]", False)


class AnyButFrom(__Class):
    '''
    Matches any character except for the provided characters. \
    Equivalent to "~AnyFrom()".

    :param Pregex | str *chars: One or more characters to match from. Each character must be \
        a string of length one, provided either as is or wrapped within a "tokens" class.
    '''

    def __init__(self, *chars: str or _pre.Pregex) -> 'AnyButFrom':
        '''
        Matches any character except for the provided characters. \
        Equivalent to "~AnyFrom()".

        :param Pregex | str *chars: One or more characters not to match from. Each character must be \
            a string of length one, provided either as is or wrapped within a "tokens" class.
        '''
        for c in chars:
            if not issubclass(c.__class__, (str, _pre.Pregex)):
                raise _exceptions.NeitherStringNorTokenException()
            if issubclass(c.__class__, _pre.Pregex) and c._get_type() != __class__._PatternType.Token:
                raise _exceptions.NeitherStringNorTokenException()
        to_escape = {'\\', '^', '[', ']', '-', "'"}
        chars = tuple((f"\{c}" if c in to_escape else c) if isinstance(c, str) \
             else str(c) for c in set(chars))
        super().__init__(f"[^{''.join(chars)}]", True)