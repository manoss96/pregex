import re as _re
from xmlrpc.client import Boolean
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

    :note: Union and subtraction can only be performed on a pair of classes of the same type, \
        that is, either a pair of regular classes or a pair of negated classes.
    '''

    '''
    A set containing characters that must be escaped when used within a class.
    '''
    _to_escape = ('\\', '^', '[', ']', '-', '/')


    def __init__(self, pattern: str, is_negated: bool, simplify_word: bool = False) -> '__Class':

        super().__init__(__class__.__simplify(pattern, is_negated, simplify_word), escape=False)
        self._set_type(_pre._Type.Class)
        self.__is_negated = is_negated
        self.__verbose = pattern


    def _get_verbose_pattern(self) -> str:
        '''
        Returns a verbose representation of this class's pattern.
        '''
        return self.__verbose


    def __simplify(pattern: str, is_negated: bool, simplify_word: bool) -> str:
        '''
        Converts a verbose pattern to its simplified form.

        :param str pattern: The pattern that is to be simplified.
        :param bool is_negated: Indicates whether the patterns belongs \
            to a negated class or a regular one.
        :param bool simplify_word: Indicates whether '[A-Za-z0-9_]' should be simplified \
            to '[\w]' or not.
        '''
        if pattern == ".":
            return pattern
        # Use shorthand notation for any classes that support this.
        ranges, chars = __class__.__extract_classes(pattern)
        classes = __class__.__verbose_to_shorthand(ranges.union(chars), simplify_word)
        pattern = ''.join(f"[{'^' if is_negated else ''}{''.join(classes)}]")
        # Replace any one-character classes with a single (possibly escaped) character
        pattern = _re.sub(r"\[([^\\]|\\.)\]", lambda m: str(__class__._to_pregex(m.group(1))) \
            if len(m.group(1)) == 1 else m.group(1), pattern)
        # Replace negated class shorthand-notation characters with their non-class shorthand-notation.
        return _re.sub(r"\[\^(\\w|\\d|\\s)\]", lambda m: m.group(1).upper(), pattern)


    def __verbose_to_shorthand(classes: set[str], simplify_word: bool) -> set[str]:
        '''
        This method searches the provided set for subsets of character classes that \
        correspond to a shorthand-notation character class, and if it finds any, it \
        replaces them with said character class, returning the resulting set at the end.

        :param set[str] classes: The set containing the classes as strings.
        :param bool simplify_word: Indicates whether '[A-Za-z0-9_]' should be simplified \
            to '[\w]' or not.
        '''
        word_set = {'a-z', 'A-Z', '0-9', '_'}
        digit_set = {'0-9'}
        whitespace_set = {' ', '\t', '\n', '\r', '\x0b', '\x0c'}
        if classes.issuperset(word_set) and simplify_word:
            classes = classes.difference(word_set).union({'\w'})
        elif classes.issuperset(digit_set):
            classes = classes.difference(digit_set).union({'\d'})
        if classes.issuperset(whitespace_set):
            classes = classes.difference(whitespace_set).union({'\s'})
        return classes


    def __invert__(self) -> '__Class':
        '''
        If this instance is a regular class, then converts it to its negated counterpart. \
        If this instance is a negated class, then converts it to its regular counterpart.
        '''
        s, rs = '' if self.__is_negated else '^', '^' if self.__is_negated else ''
        return __class__(f"[{s}{self.__verbose.lstrip('[' + rs).rstrip(']')}]", not self.__is_negated)


    def __or__(self, pre: '__Class' or str) -> '__Class':
        '''
        Returns a "__Class" instance representing the union of the provided classes.

        :param __Class | str pre: The class that is to be unioned with this instance.

        :raises CannotBeUnionedException: 'pre' is neither a "__Class" instance nor a token.
        '''
        if not self.__is_negated:
            if isinstance(pre, str) and (len(pre) == 1):
                pre = AnyFrom(pre)
            elif isinstance(pre, _pre.Pregex) and pre._get_type() == _pre._Type.Token:
                pre = AnyFrom(pre)
        if not issubclass(pre.__class__, __class__):
            raise _exceptions.CannotBeUnionedException(self, pre, False)
        return __class__.__or(self, pre)


    def __ror__(self, pre: '__Class' or str) -> '__Class':
        '''
        Returns a "__Class" instance representing the union of the provided classes.

        :param __Class | str pre: The class that is to be unioned with this instance.

        :raises CannotBeUnionedException: 'pre' is neither a "__Class" instance nor a token.
        '''
        if not self.__is_negated:
            if isinstance(pre, str) and (len(pre) == 1):
                pre = AnyFrom(pre)
            elif isinstance(pre, _pre.Pregex) and pre._get_type() == _pre._Type.Token:
                pre = AnyFrom(pre)
        if not issubclass(pre.__class__, __class__):
            raise _exceptions.CannotBeUnionedException(pre, self, False)
        return __class__.__or(pre, self)


    def __or(pre1: '__Class', pre2: '__Class') -> '__Class':
        '''
        Returns a "__Class" instance representing the union of the provided classes.

        :param __Class pre: The class that is to be unioned with this instance.

        :raises CannotBeUnionedException: 'pre1' is a different type of class than 'pre2'.
        '''
        if  pre1.__is_negated != pre2.__is_negated:
            raise _exceptions.CannotBeUnionedException(pre1, pre2, True)
        if isinstance(pre1, Any) or isinstance(pre2, Any):
            return Any()

        simplify_word = False
        if isinstance(pre1, (AnyWordChar, AnyButWordChar)):
            simplify_word = simplify_word or pre1._is_global()
        if isinstance(pre2, (AnyWordChar, AnyButWordChar)):
            simplify_word = simplify_word or pre2._is_global()
            
        ranges1, chars1 = __class__.__extract_classes(pre1.__verbose, unescape=True)
        ranges2, chars2 = __class__.__extract_classes(pre2.__verbose, unescape=True)

        ranges, chars = ranges1.union(ranges2), chars1.union(chars2)

        def reduce_ranges(ranges: list[str]) -> set[str]:
            '''
            Removes any sub-ranges if they are already included within an other specified range,
            and returns the set of all remaining ranges.

            :param list[str] ranges: A list containing all specified ranges.
            '''
            if len(ranges) < 2:
                return set(ranges)
            
            ranges = [__class__.__split_range(rng) for rng in ranges]

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

        def reduce_chars(ranges: list[str], chars: list[str]):
            '''
            Removes any characters if those are already included within an other specified range,
            and returns the set of all remaining characters.

            :param list[str] ranges: A list containing all specified ranges.
            :param list[str] chars: A list containing all specified chars.
            '''

            ranges = [__class__.__split_range(rng) for rng in ranges]

            i = 0
            while i < len(chars):
                for j in range(len(ranges)):
                    start, end = ranges[j]
                    if chars[i] >= start and chars[i] <= end:
                        chars.pop(i)
                        i = -1
                        break
                    elif ord(start) == ord(chars[i]) + 1:
                        ranges[j][0] = chars[i]
                        chars.pop(i)
                        i = -1
                        break
                    elif ord(end) == ord(chars[i]) - 1:
                        ranges[j][1] = chars[i]
                        chars.pop(i)
                        i = -1
                        break
                i += 1

            return set(f"{rng[0]}-{rng[1]}" for rng in ranges), set(chars)        

        ranges = reduce_ranges(ranges)
        ranges, chars = reduce_chars(list(ranges), list(chars))

        result =  __class__.__modify_classes(ranges.union(chars), escape=True)

        return  __class__(
            f"[{'^' if pre1.__is_negated else ''}{''.join(result)}]",
            pre1.__is_negated, simplify_word)


    def __sub__(self, pre: '__Class' or str) -> '__Class':
        '''
        Returns a "__Class" instance representing the difference of the provided classes.

        :param __Class | str pre: The class that is to be subtracted from this instance.

        :raises CannotBeSubtractedException: 'pre' is neither a "__Class" instance nor a token.
        '''
        if not self.__is_negated:
            if isinstance(pre, str) and (len(pre) == 1):
                pre = AnyFrom(pre)
            elif isinstance(pre, _pre.Pregex) and pre._get_type() == _pre._Type.Token:
                pre = AnyFrom(pre)
        if not issubclass(pre.__class__, __class__):
            raise _exceptions.CannotBeSubtractedException(self, pre, False)
        return __class__.__sub(self, pre)


    def __rsub__(self, pre: '__Class' or str) -> '__Class':
        '''
        Returns a "__Class" instance representing the difference of the provided classes.

        :param __Class | str pre: The class that is to be subtracted from this instance.

        :raises CannotBeSubtractedException: 'pre' is neither a "__Class" instance nor a token.
        '''
        if not self.__is_negated:
            if isinstance(pre, str) and (len(pre) == 1):
                pre = AnyFrom(pre)
            elif isinstance(pre, _pre.Pregex) and pre._get_type() == _pre._Type.Token:
                pre = AnyFrom(pre)
        if not issubclass(pre.__class__, __class__):
            raise _exceptions.CannotBeSubtractedException(pre, self, False)
        return __class__.__sub(pre, self)


    def __sub(pre1: '__Class', pre2: '__Class') -> '__Class':
        '''
        Returns a "__Class" instance representing the difference of the provided classes.

        :param __Class  pre: The class that is to be subtracted from this instance.

        :raises CannotBeSubtractedException: 'pre' is neither a "__Class" instance nor a token.
        :raises EmptyClassException: 'pre2' is an instance of class "Any".
        '''
        if  pre1.__is_negated != pre2.__is_negated:
            raise _exceptions.CannotBeSubtractedException(pre1, pre2, True)
        if isinstance(pre2, Any):
            raise _exceptions.EmptyClassException(pre1, pre2)
        if isinstance(pre1, Any):
            return ~ pre2
        if isinstance(pre1, (AnyWordChar, AnyButWordChar)) and pre1._is_global():
            raise _exceptions.GlobalWordCharSubtractionException(pre1)

        # Subtract any ranges found in both pre2 and pre1 from pre1.
        def subtract_ranges(ranges1: set[str], ranges2: set[str]) -> tuple[set[str], set[str]]:
            '''
            Subtracts any range found within 'ranges2' from 'ranges1' and returns \
            the resulting ranges/characters in two seperate sets.

            :note: This method might also produce characters, for example \
                [A-Z] - [B-Z] produces the character 'A'.
            '''
            ranges1 = [__class__.__split_range(rng) for rng in ranges1]
            ranges2 = [__class__.__split_range(rng) for rng in ranges2]

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

        # 1. Extract classes while unescaping them
        ranges1, chars1 = __class__.__extract_classes(pre1.__verbose, unescape=True)
        ranges2, chars2 = __class__.__extract_classes(pre2.__verbose, unescape=True)

        # 2.a. Subtract ranges2 from chars1.
        splt_ranges2 = [__class__.__split_range(rng) for rng in ranges2]
        lst_chars1 = list(chars1)

        for start, end in splt_ranges2:
            i = 0
            while i < len(lst_chars1):
                c = lst_chars1[i]
                if c.isalnum and c >= start and c <= end:
                    lst_chars1.pop(i)
                    i = -1
                i += 1
        chars1 = set(lst_chars1)

        # 2.b Subtract chars2 from chars1.
        chars1 = chars1.difference(chars2)

        # 2.c. Subtract ranges2 from ranges1.
        ranges1, reduced_chars = subtract_ranges(ranges1, ranges2)
        chars1 = chars1.union(reduced_chars)

        # 2.d. Subtract any characters in chars2 from ranges1.
        ranges1, reduced_chars = subtract_ranges(ranges1, set(f"{c}-{c}" for c in chars2))
        chars1 = chars1.union(reduced_chars)

        # 3. Union ranges and chars together while escaping them.
        result = __class__.__modify_classes(ranges1.union(chars1), escape=True)
        
        if len(result) == 0:
            raise _exceptions.EmptyClassException(pre1, pre2)

        return  __class__(
            f"[{'^' if pre1.__is_negated else ''}{''.join(result)}]",
            pre1.__is_negated)


    def __extract_classes(pattern: str, unescape: bool = False) -> tuple[set[str], set[str]]:
        '''
        Extracts all classes from the provided class pattern and returns them \
        separated into two different sets based on whether they constitute a range \
        or an individual character.

        :param str pattern: The pattern from which classes are to be extracted.
        :param bool unespace: If 'True' then unescapes all escaped characters. \
            Defaults to 'False'.
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

        # Extract classes separately.
        ranges, chars = __class__.__extract_ranges(classes), __class__.__extract_chars(classes)

        # Escape their characters if you must.
        if unescape:
            ranges, chars = __class__.__modify_classes(ranges, escape=False), \
                __class__.__modify_classes(chars, escape=False)
        # Return classes.
        return ranges, chars


    def __extract_ranges(classes: 'str') -> set[str]:
        '''
        Extracts all ranges from the provided character class pattern and returns \
        a set containing them.

        :param str classes: One or more string character class patterns.
        '''
        return set(_re.findall(
            r"(?:\\(?:\[|\]|\^|\$|\-|\/|\\)|[^\[\]\^\$\-\/\\])-(?:\\(?:\[|\]|\^|\$|\-|\/|\\)|[^\[\]\^\$\-\/\\])",
            classes, flags=_re.DOTALL))


    def __extract_chars(classes: str) -> set[str]:
        '''
        Extracts all individual characters from the provided character class pattern \
        and returns a set containing them.

        :param str classes: One or more string character class patterns.
        '''
        return set(_re.findall(r"(?<!.\-)(?:\\(?:\[|\]|\^|\$|\-|\/|\\)|[^\[\]\^\$\-\/\\])(?!\-.)",
            classes, flags=_re.DOTALL))

    
    def __modify_classes(classes: set[str], escape: bool) -> set[str]:
        '''
        Either escapes or unescapes any character within the provided classes that \
        needs to be escaped.

        :param bool escape: Indicates whether to "escape" or "unescape" characters.
        '''

        def escape_char(c):
            return "\\" + c if c in __class__._to_escape else c
        def unescape_char(c):
            return c.replace("\\", "", 1) if len(c) > 1 and c[1] in __class__._to_escape else c

        fun = escape_char if escape else unescape_char
        modified_classes = set()

        for c in classes:
            if len(c) >= 3: # classes: [.-.], [\.-.], [\.-\.]
                start, end = tuple(map(fun, __class__.__split_range(c)))
                modified_c = start + "-" + end
            else: # characters: [.]
                modified_c = fun(c)
            modified_classes.add(modified_c)

        return modified_classes


    def __split_range(pattern: str) -> tuple[str, str]:
        '''
        Splits the provided range pattern and returns result as a tuple \
        containing the range's beginning and end.

        :param str pattern: The pattern that is to be split.

        :note: Provided characters within the range MUST NOT be escaped.
        '''

        count = pattern.count("-")

        if count == 1:
            return pattern.split("-")
        elif count== 2:
            split_fun = pattern.split if pattern[-1] == "-" else pattern.rsplit
            return split_fun("-", 1)
        else:
            return ("-", "-")


class Any(__Class):
    '''
    Matches any possible character, including the newline character.
    '''

    def __init__(self) -> 'Any':
        '''
        Matches any possible character, including the newline character.
        '''
        super().__init__('.', is_negated=False)


class AnyLetter(__Class):
    '''
    Matches any character from the Latin alphabet.
    '''

    def __init__(self) -> 'AnyLetter':
        '''
        Matches any character from the Latin alphabet.
        '''
        super().__init__('[a-zA-Z]', is_negated=False)


class AnyButLetter(__Class):
    '''
    Matches any character except for characters in the Latin alphabet.
    '''

    def __init__(self) -> 'AnyButLetter':
        '''
        Matches any character except for characters in the Latin alphabet.
        '''
        super().__init__('[^a-zA-Z]', is_negated=True)


class AnyLowercaseLetter(__Class):
    '''
    Matches any lowercase character from the Latin alphabet.
    '''

    def __init__(self) -> 'AnyLowercaseLetter':
        '''
        Matches any lowercase character from the Latin alphabet.
        '''
        super().__init__('[a-z]', is_negated=False)


class AnyButLowercaseLetter(__Class):
    '''
    Matches any character except for lowercase characters in the Latin alphabet.
    '''

    def __init__(self) -> 'AnyButLowercaseLetter':
        '''
        Matches any character except for lowercase characters in the Latin alphabet.
        '''
        super().__init__('[^a-z]', is_negated=True)

    
class AnyUppercaseLetter(__Class):
    '''
    Matches any uppercase character from the Latin alphabet.
    '''

    def __init__(self) -> 'AnyUppercaseLetter':
        '''
        Matches any uppercase character from the Latin alphabet.
        '''
        super().__init__('[A-Z]', is_negated=False)


class AnyButUppercaseLetter(__Class):
    '''
    Matches any character except for uppercase characters in the Latin alphabet.
    '''

    def __init__(self) -> 'AnyButUppercaseLetter':
        '''
        Matches any character except for uppercase characters in the Latin alphabet.
        '''
        super().__init__('[^A-Z]', is_negated=True)


class AnyDigit(__Class):
    '''
    Matches any numeric character.
    '''

    def __init__(self) -> 'AnyDigit':
        '''
        Matches any numeric character.
        '''
        super().__init__('[0-9]', is_negated=False)


class AnyButDigit(__Class):
    '''
    Matches any character except for numeric characters.
    '''

    def __init__(self) -> 'AnyButDigit':
        '''
        Matches any character except for numeric characters.
        '''
        super().__init__('[^0-9]', is_negated=True)


class AnyWordChar(__Class):
    '''
    Matches any alphanumeric character plus "_".

    :param bool is_global: Indicates whether to include foreign alphabetic \
        characters or not. Defaults to 'False'.

    :note: Attempting to subtract a regular class instance from an instance of this \
        class for which parameter "is_global" has been set to "True" will \
        cause a "GlobalWordCharSubtractionException" exception to be thrown.
    '''

    def __init__(self, is_global: bool = False) -> 'AnyWordChar':
        '''
        Matches any alphanumeric character plus "_".

        :param bool is_global: Indicates whether to include foreign alphabetic \
            characters or not. Defaults to 'False'.

        :note: Attempting to subtract a regular class instance from an instance of this \
            class for which parameter "is_global" has been set to "True" will \
            cause a "GlobalWordCharSubtractionException" exception to be thrown.
        '''
        super().__init__('[a-zA-Z0-9_]', is_negated=False, simplify_word=is_global)
        self.__is_global = is_global


    def _is_global(self) -> Boolean:
        '''
        Returns "True" if this instance supports matching foreign alphabetic \
        characters, else returns "False".
        '''
        return self.__is_global 


class AnyButWordChar(__Class):
    '''
    Matches any character except for alphanumeric characters and "_".

    :param bool is_global: Indicates whether to include foreign alphabetic \
        characters or not. Defaults to 'False'.

    :note: Attempting to subtract a negated class instance from an instance of this \
        class for which parameter "is_global" has been set to "True" will \
        cause a "GlobalWordCharSubtractionException" exception to be thrown.
    '''

    def __init__(self, is_global: bool = False) -> 'AnyButWordChar':
        '''
        Matches any character except for alphanumeric characters and "_".

        :param bool is_global: Indicates whether to include foreign alphabetic \
            characters or not. Defaults to 'False'.

        :note: Attempting to subtract a negated class instance from an instance of this \
            class for which parameter "is_global" has been set to "True" will \
            cause a "GlobalWordCharSubtractionException" exception to be thrown.
        '''
        super().__init__('[^a-zA-Z0-9_]', is_negated=True, simplify_word=is_global)
        self.__is_global = is_global


    def _is_global(self) -> Boolean:
        '''
        Returns "True" if this instance also excludes foreign alphabetic \
        characters from matching, else returns "False".
        '''
        return self.__is_global 


class AnyPunctuation(__Class):
    '''
    Matches any puncutation character as defined within the ASCII table.
    '''

    def __init__(self) -> 'AnyPunctuation':
        '''
        Matches any puncutation character as defined within the ASCII table.
        '''
        super().__init__('[!-\/:-@\[-`{-~]', is_negated=False)


class AnyButPunctuation(__Class):
    '''
    Matches any character except for punctuation characters \
    as defined within the ASCII table.
    '''

    def __init__(self) -> 'AnyButPunctuation':
        '''
        Matches any character except for punctuation characters \
        as defined within the ASCII table.
        '''
        super().__init__('[^!-\/:-@\[-`{-~]', is_negated=True)


class AnyWhitespace(__Class):
    '''
    Matches any whitespace character.
    '''

    def __init__(self) -> 'AnyWhitespace':
        '''
        Matches any whitespace character.
        '''
        super().__init__(f'[{_whitespace}]', is_negated=False)


class AnyButWhitespace(__Class):
    '''
    Matches any character except for whitespace characters.
    '''

    def __init__(self) -> 'AnyButWhitespace':
        '''
        Matches any character except for whitespace characters.
        '''
        super().__init__(f'[^{_whitespace}]', is_negated=True)


class AnyBetween(__Class):
    '''
    Matches any character within the provided range.

    :param str start: The first character of the range.
    :param str end: The last character of the range.

    :raises NeitherCharNorTokenException: At least one of the provided characters \
        is neither a "token" class instance nor a single-character string.
    :raises InvalidRangeException: A non-valid range is provided.

    :note: Any pair of characters "start", "end" constitutes a valid range, \
        provided that the integer code point of "end" is greater than the \
        integer code point of "start", as defined by the Unicode Standard.
    '''

    def __init__(self, start: str, end: str) -> 'AnyBetween':
        '''
        Matches any character within the provided range.

        :param str start: The first character of the range.
        :param str end: The last character of the range.

        :raises NeitherCharNorTokenException: At least one of the provided characters \
            is neither a "token" class instance nor a single-character string.
        :raises InvalidRangeException: A non-valid range is provided.

        :note: Any pair of characters "start", "end" constitutes a valid range, \
            provided that the integer code point of "end" is greater than the \
            integer code point of "start", as defined by the Unicode Standard.
        '''
        for c in (start, end):
            if isinstance(c, (str, _pre.Pregex)):
                if len(str(c).replace("\\", "", 1)) > 1: 
                    raise _exceptions.NeitherCharNorTokenException()
            else:
                raise _exceptions.NeitherCharNorTokenException() 
        start, end = str(start), str(end)
        if ord(start) >= ord(end):
            raise _exceptions.InvalidRangeException(start, end)
        start = f"\\{start}" if start in __class__._to_escape else start
        end = f"\\{end}" if end in __class__._to_escape else end
        super().__init__(f"[{start}-{end}]", is_negated=False)


class AnyButBetween(__Class):
    '''
    Matches any character except for all characters within the provided range.

    :param str start: The first character of the range.
    :param str end: The last character of the range.

    :raises NeitherCharNorTokenException: At least one of the provided characters \
        is neither a "token" class instance nor a single-character string.
    :raises InvalidRangeException: A non-valid range is provided.

    :note: Any pair of characters "start", "end" constitutes a valid range, \
        provided that the integer code point of "end" is greater than the \
        integer code point of "start", as defined by the Unicode Standard.
    '''

    def __init__(self, start: str, end: str) -> 'AnyButBetween':
        '''
        Matches any character except for all characters within the provided range.

        :param str start: The first character of the range.
        :param str end: The last character of the range.

        :raises NeitherCharNorTokenException: At least one of the provided characters \
            is neither a "token" class instance nor a single-character string.
        :raises InvalidRangeException: A non-valid range is provided.

        :note: Any pair of characters "start", "end" constitutes a valid range, \
            provided that the integer code point of "end" is greater than the \
            integer code point of "start", as defined by the Unicode Standard.
        '''
        for c in (start, end):
            if isinstance(c, (str, _pre.Pregex)):
                if len(str(c).replace("\\", "", 1)) > 1: 
                    raise _exceptions.NeitherCharNorTokenException()
            else:
                raise _exceptions.NeitherCharNorTokenException() 
        start, end = str(start), str(end)
        if ord(start) >= ord(end):
            raise _exceptions.InvalidRangeException(start, end)
        start = f"\\{start}" if start in __class__._to_escape else start
        end = f"\\{end}" if end in __class__._to_escape else end
        super().__init__(f"[^{start}-{end}]", is_negated=True)      


class AnyFrom(__Class):
    '''
    Matches any one of the provided characters.

    :param Pregex | str *chars: One or more characters to match from. Each character must be \
        a string of length one, provided either as is or wrapped within a "tokens" class.

    :raises NeitherCharNorTokenException: At least one of the provided characters is \
        neither a "token" class instance nor a single-character string.
    '''

    def __init__(self, *chars: str or _pre.Pregex) -> 'AnyFrom':
        '''
        Matches any one of the provided characters.

        :param Pregex | str *chars: One or more characters to match from. Each character must be \
            a string of length one, provided either as is or wrapped within a "tokens" class.

        :raises NeitherCharNorTokenException: At least one of the provided characters is \
            neither a "token" class instance nor a single-character string.
        '''
        for c in chars:
            if isinstance(c, (str, _pre.Pregex)):
                if len(str(c).replace("\\", "", 1)) > 1: 
                    raise _exceptions.NeitherCharNorTokenException()
            else:
                raise _exceptions.NeitherCharNorTokenException()
        chars = tuple((f"\\{c}" if c in __class__._to_escape else c) \
            if isinstance(c, str) else str(c) for c in chars)
        super().__init__(f"[{''.join(chars)}]", is_negated=False)


class AnyButFrom(__Class):
    '''
    Matches any character except for the provided characters.

    :param Pregex | str *chars: One or more characters not to match from. Each character must be \
        a string of length one, provided either as is or wrapped within a "tokens" class.

    :raises NeitherCharNorTokenException: At least one of the provided characters is \
        neither a "token" class instance nor a single-character string.
    '''

    def __init__(self, *chars: str or _pre.Pregex) -> 'AnyButFrom':
        '''
        Matches any character except for the provided characters.

        :param Pregex | str *chars: One or more characters not to match from. Each character must be \
            a string of length one, provided either as is or wrapped within a "tokens" class.

        :raises NeitherCharNorTokenException: At least one of the provided characters is \
            neither a "token" class instance nor a single-character string.
        '''
        for c in chars:
            if isinstance(c, (str, _pre.Pregex)):
                if len(str(c).replace("\\", "", 1)) > 1: 
                    raise _exceptions.NeitherCharNorTokenException()
            else:
                raise _exceptions.NeitherCharNorTokenException() 
        chars = tuple((f"\{c}" if c in __class__._to_escape else c)
            if isinstance(c, str) else str(c) for c in chars)
        super().__init__(f"[^{''.join(chars)}]", is_negated=True)


class AnyGermanLetter(__Class):
    '''
    Matches any character from the German alphabet.
    '''

    def __init__(self) -> 'AnyGermanLetter':
        '''
        Matches any character from the German alphabet.
        '''
        super().__init__('[a-zA-ZäöüßÄÖÜẞ]', is_negated=False)


class AnyButGermanLetter(__Class):
    '''
    Matches any character except for characters in the German alphabet.
    '''

    def __init__(self) -> 'AnyButGermanLetter':
        '''
        Matches any character except for characters in the German alphabet.
        '''
        super().__init__('[^a-zA-ZäöüßÄÖÜẞ]', is_negated=True)


class AnyGreekLetter(__Class):
    '''
    Matches any character from the Greek alphabet.
    '''

    def __init__(self) -> 'AnyGreekLetter':
        '''
        Matches any character from the Greek alphabet.
        '''
        # Start from 'Έ' and include "Ά" separately so that
        # Ano Teleia '·' is not included.
        super().__init__('[ΆΈ-ώ]', is_negated=False)


class AnyButGreekLetter(__Class):
    '''
    Matches any character except for characters in the Greek alphabet.
    '''

    def __init__(self) -> 'AnyGreekLetter':
        '''
        Matches any character except for characters in the Greek alphabet.
        '''
        # Start from 'Έ' and include "Ά" separately so that
        # Ano Teleia '·' is not included.
        super().__init__('[^ΆΈ-ώ]', is_negated=True)


class AnyCyrillicLetter(__Class):
    '''
    Matches any character from the Cyrillic alphabet.
    '''

    def __init__(self) -> 'AnyCyrillicLetter':
        '''
        Matches any character from the Cyrillic alphabet.
        '''
        super().__init__('[Ѐ-ӿ]', is_negated=False)

    
class AnyButCyrillicLetter(__Class):
    '''
    Matches any character except for characters in the Cyrillic alphabet.
    '''

    def __init__(self) -> 'AnyButCyrillicLetter':
        '''
        Matches any character except for characters in the Cyrillic alphabet.
        '''
        super().__init__('[^Ѐ-ӿ]', is_negated=True)