import re as _re
import pregex.pre as _pre
import pregex.tokens as _tokens
import pregex.exceptions as _exceptions
from string import whitespace as _whitespace


class __Class(_pre.Pregex):
    '''
    Any "Class" class must inherit from this class.

    This type of objects are used to  construct character classes. \
    For example, the "AnyLetter" class represents character class "[a-zA-Z]". \
    This modules contains a number of classes in order for various character \
    classes to be easily constructed.
    
    Besides these pre-defined character classes, one is also able to create their own \
    by combining other character classes together through the use of the overloaded Bitwise \
    OR operator "|". For instance, one can construct character class "[a-z0-9]" as such:
        - AnyLowercaseLetter() | AnyDigit()

    Furthermore, one is also able to negate character classes by using the overloaded \
    Bitwise NOT operator "~". For instance, one can construct character class "[^a-z]" \
    by negating "AnyLowercaseLetter()":
        - ~ AnyLowercaseLetter()
    '''

    '''
    This map is used to transform shorthand character classes \
    into their more verbose form, in order to effectively \
    combine this type of classes.
    '''
    __shorthand_map: dict[str, str] = {
        "\w" : "a-zA-Z0-9_",
        "\d" : "0-9",
        "\s" : _whitespace
    }

    '''
    This method searches the provided set for subsets of character classes that \
    correspond to a shorthand charater class, and if it finds any, it replaces \
    them with said character class, returning the resulting set at the end.

    :param set[str] classes: The set containing the classes as strings.
    '''
    def __inverse_shorthand_map(classes: set[str]) -> set[str]:
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

    def __init__(self, pattern: str, is_negated: bool) -> '__Class':
        super().__init__(pattern, group_on_concat=False, group_on_quantify=False)
        self.__is_negated = is_negated

    def __invert__(self) -> '__Class':
        s, rs = '' if self.__is_negated else '^', '^' if self.__is_negated else ''
        return __class__(f"[{s}{str(self).lstrip('[' + rs).rstrip(']')}]", not self.__is_negated)

    def __or__(self, pre: '__Class') -> '__Class':
        if not issubclass(pre.__class__, __class__):
            raise _exceptions.CannotBeCombinedException(self, pre, False)
        return __class__.__or(self, pre)

    def __ror__(self, pre: '__Class') -> '__Class':
        if not issubclass(pre.__class__, __class__):
            raise _exceptions.CannotBeCombinedException(pre, self, False)
        return __class__.__or(pre, self)

    def __or(pre1: '__Class', pre2: '__Class') -> '__Class':
        if  pre1.__is_negated != pre2.__is_negated:
            raise _exceptions.CannotBeCombinedException(pre1, pre2, True)
        if isinstance(pre1, Any) or isinstance(pre2, Any):
            return Any()
        start_1, start_2 = 2 if pre1.__is_negated else 1, 2 if pre2.__is_negated else 1
        p1, p2 = str(pre1)[start_1:-1], str(pre2)[start_2:-1]
        s_map = pre1.__shorthand_map
        for s_key in s_map:
            p1, p2 = p1.replace(s_key, s_map[s_key]), p2.replace(s_key, s_map[s_key])
        # Create pattern for matching possible classes.
        pattern = "[A-Za-z0-9]-[A-Za-z0-9]|\\\\?."
        classes = set(_re.findall(pattern, p1, flags=_re.DOTALL)) \
            .union(set(_re.findall(pattern, p2, flags=_re.DOTALL)))
        return  __class__(
            f"[{'^' if pre1.__is_negated else ''}{''.join(__class__.__inverse_shorthand_map(classes))}]",
            pre1.__is_negated)


class Any(__Class):
    '''
    Matches any possible character, including the newline character. \
    In order to match every character except for the newline character, \
    one can use "~AnyFrom(pregex.tokens.Newline())".
    '''

    def __init__(self) -> 'Any':
        '''
        Matches any possible character, including the newline character. \
        In order to match every character except for the newline character, \
        one can use "AnyButFrom(pregex.tokens.Newline())" or \
        "~AnyFrom(pregex.tokens.Newline())".
        '''
        super().__init__('.', False)


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
    Matches any character except for alphabetic characters.
    '''

    def __init__(self) -> 'AnyButLetter':
        '''
        Matches any character except for alphabetic characters.
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
    Matches any character except for lowercase alphabetic characters.
    '''

    def __init__(self) -> 'AnyButLowercaseLetter':
        '''
        Matches any character except for lowercase alphabetic characters.
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
    Matches any character except for uppercase alphabetic characters.
    '''

    def __init__(self) -> 'AnyButUppercaseLetter':
        '''
        Matches any character except for uppercase alphabetic characters.
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
        super().__init__('[\d]', False)


class AnyButDigit(__Class):
    '''
    Matches any character except for numeric characters.
    '''

    def __init__(self) -> 'AnyButDigit':
        '''
        Matches any character except for numeric characters.
        '''
        super().__init__('[^\d]', True)


class AnyWordChar(__Class):
    '''
    Matches any alphanumeric character plus "_".
    '''

    def __init__(self) -> 'AnyWordChar':

        '''
        Matches any alphanumeric character plus "_".
        '''
        super().__init__('[\w]', False)


class AnyButWordChar(__Class):
    '''
    Matches any character except for alphanumeric characters plus "_".
    '''

    def __init__(self) -> 'AnyButWordChar':
        '''
        Matches any character except for alphanumeric characters plus "_".
        '''
        super().__init__('[^\w]', True)


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
    Matches any character except for punctuation characters.
    '''

    def __init__(self) -> 'AnyButPunctuation':
        '''
        Matches any character except for punctuation characters.
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
        super().__init__('[\s]', False)


class AnyButWhitespace(__Class):
    '''
    Matches any character except for whitespace characters.
    '''

    def __init__(self) -> 'AnyButWhitespace':
        '''
        Matches any character except for whitespace characters.
        '''
        super().__init__('[^\s]', True)


class AnyWithinRange(__Class):
    '''
    Matches any character within the provided range.
    '''

    def __init__(self, start: str or int, end: str or int) -> 'AnyWithinRange':
        '''
        Matches any character within the provided range.

        :param str | int start: The first character within the range.
        :param str | int end: The last character within the range.
        '''
        if (type(start) != type(end)) or start >= end:
            raise _exceptions.InvalidRangeException(start, end)
        super().__init__(f"[{start}-{end}]", False)


class AnyButWithinRange(__Class):
    '''
    Matches any character except for all characters within the provided range.
    '''

    def __init__(self, start: str or int, end: str or int) -> 'AnyButWithinRange':
        '''
        Matches any character except for all characters within the provided range.

        :param str | int start: The first character within the range.
        :param str | int end: The last character within the range.
        '''
        if (type(start) != type(end)) or start >= end:
            raise _exceptions.InvalidRangeException(start, end)
        super().__init__(f"[^{start}-{end}]", True)      


class AnyFrom(__Class):
    '''
    Matches any one of the provided characters.
    '''

    def __init__(self, *chars: str or _tokens.Token) -> 'AnyFrom':
        '''
        Matches any one of the provided characters.

        :param Pregex | str *chars: One or more characters to match from. Each character must be \
            a string of length one, provided either as is or wrapped within an instance of type \
            "Token".
        '''
        for c in chars:
            if not issubclass(c.__class__, (str, _tokens.Token)):
                raise _exceptions.NeitherStringNorTokenException()
            if len(str(c).replace("\\", "")) > 1:
                raise _exceptions.MultiCharTokenException(str(c))
        chars = tuple(str(_pre.Pregex(pre)._literal()) if isinstance(pre, str) else str(pre) for pre in chars)
        super().__init__(f"[{''.join(chars)}]", False)


class AnyButFrom(__Class):
    '''
    Matches any character except for the provided characters.
    '''

    def __init__(self, *chars: str or _tokens.Token) -> 'AnyButFrom':
        '''
        Matches any character except for the provided characters.

        :param Pregex | str *chars: One or more characters to match from. Each character must be \
            a string of length one, provided either as is or wrapped within an instance of type \
            "Token".
        '''
        for c in chars:
            if not issubclass(c.__class__, (str, _tokens.Token)):
                raise _exceptions.NeitherStringNorTokenException()
            if len(str(c).replace("\\", "")) > 1:
                raise _exceptions.MultiCharTokenException(str(c))
        chars = tuple(str(_pre.Pregex(pre)._literal()) if isinstance(pre, str) else str(pre) for pre in chars)
        super().__init__(f"[^{''.join(chars)}]", True)