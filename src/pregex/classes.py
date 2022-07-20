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
        word_set, digit_set = {'a-z', 'A-Z', '0-9', '_'}, {'0-9'}
        whitespace_set = {' ', '\t', '\n', '\r', '\x0b', '\x0c'}
        if classes.issuperset(word_set):
            classes = classes.difference(word_set).union({'\w'})
        elif classes.issuperset(digit_set):
            classes = classes.difference(digit_set).union({'\d'})
        if classes.issuperset(whitespace_set):
            classes = classes.difference(whitespace_set).union({'\s'})
        return classes

    def __init__(self, pattern: str) -> '__Class':
        super().__init__(pattern, group_on_concat=False, group_on_quantify=False)

    def __invert__(self) -> '_NegatedClass':
        return _NegatedClass(f"[^{str(self).lstrip('[').rstrip(']')}]")

    def __or__(self, pre: '__Class') -> '__Class':
        if (not issubclass(pre.__class__, __class__)) or isinstance(pre, _NegatedClass):
            raise _exceptions.CannotBeCombinedException(self, pre)
        return __class__.__or(self, pre)

    def __ror__(self, pre: '__Class') -> '__Class':
        if (not issubclass(pre.__class__, __class__)) or isinstance(pre, _NegatedClass):
            raise _exceptions.CannotBeCombinedException(pre, self)
        return __class__.__or(pre, self)

    def __or(pre1: '__Class', pre2: '__Class') -> '__Class':
        if isinstance(pre1, Any) or isinstance(pre2, Any):
            return Any()
        p1, p2 = str(pre1), str(pre2)
        s_map = pre1.__shorthand_map
        for s_key in s_map:
            p1, p2 = p1.replace(s_key, s_map[s_key]), p2.replace(s_key, s_map[s_key])
        # Create pattern for matching possible classes.
        pattern = r".\-.|\\?[^\[\]]"
        classes = set(_re.findall(pattern, p1)).union(set(_re.findall(pattern, p2)))
        return  __class__(f"[{''.join(__class__.__inverse_shorthand_map(classes))}]")


class _NegatedClass(__Class):
    '''
    Any direct "__Class" instance that is negated though the use of  \
    the overloaded bitwise NOT operator "~" is of this type.
    '''
    def __init__(self, pattern: str) -> '_NegatedClass':
        super().__init__(pattern)

    def __invert__(self) -> '__Class':
        return super().__init__(f"[{str(self).lstrip('[^').rstrip(']')}]")

    def __or__(self, pre: '_NegatedClass') -> '_NegatedClass':
        if (not issubclass(pre.__class__, __class__)) or isinstance(pre, super().__class__):
            raise _exceptions.CannotBeCombinedException(self, pre)
        return __class__.__or(self, pre)

    def __ror__(self, pre: '_NegatedClass') -> '_NegatedClass':
        if (not issubclass(pre.__class__, __class__)) or isinstance(pre, super().__class__):
            raise _exceptions.CannotBeCombinedException(self, pre)
        return __class__.__or(pre, self)

    def __or(pre1: '_NegatedClass', pre2: '_NegatedClass') -> '_NegatedClass':
        # Create pattern for matching possible classes.
        pattern = r".\-.|\\?[^\^\[\]]"
        classes = set(_re.findall(pattern, str(pre1)))\
            .union(set(_re.findall(pattern, str(pre2))))
        return __class__(f"[^{''.join(classes)}]")


class Any(__Class):
    '''
    Matches any possible character, including the newline character. \
    In order to match every character except for the newline character,
    one can use "~AnyFrom(pregex.tokens.Newline())".
    '''

    def __init__(self) -> 'Any':
        '''
        Matches any possible character, including the newline character. \
        In order to match every character except for the newline character,
        one can use "~AnyFrom(pregex.tokens.Newline())".
        '''
        super().__init__('.')

    def __invert__(self) -> None:
        raise _exceptions.CannotBeNegatedException()

    def __or__(self, pre: '__Class') -> 'Any':
        if (not issubclass(pre.__class__, __class__.__base__)) or isinstance(pre, _NegatedClass):
            raise _exceptions.CannotBeCombinedException(self, pre)
        return Any()

    def __ror__(self, pre: '__Class') -> 'Any':
        if (not issubclass(pre.__class__, __class__.__base__)) or isinstance(pre, _NegatedClass):
            raise _exceptions.CannotBeCombinedException(self, pre)
        return Any()


class AnyLetter(__Class):
    '''
    Matches any alphabetic character.
    '''

    def __init__(self) -> 'AnyLetter':
        '''
        Matches any alphabetic character.
        '''
        super().__init__('[a-zA-Z]')


class AnyLowercaseLetter(__Class):
    '''
    Matches any lowercase alphabetic character.
    '''

    def __init__(self) -> 'AnyLowercaseLetter':
        '''
        Matches any lowercase alphabetic character.
        '''
        super().__init__('[a-z]')

    
class AnyUppercaseLetter(__Class):
    '''
    Matches any uppercase alphabetic character.
    '''

    def __init__(self) -> 'AnyUppercaseLetter':
        '''
        Matches any uppercase alphabetic character.
        '''
        super().__init__('[A-Z]')


class AnyDigit(__Class):
    '''
    Matches any numeric character.
    '''

    def __init__(self) -> 'AnyDigit':
        '''
        Matches any numeric character.
        '''
        super().__init__(r'[\d]')


class AnyWordChar(__Class):
    '''
    Matches any alphanumeric character plus "_".
    '''

    def __init__(self) -> 'AnyWordChar':

        '''
        Matches any alphanumeric character plus "_".
        '''
        super().__init__(r'[\w]')


class AnyPunctuationChar(__Class):
    '''
    Matches any puncutation character.
    '''

    def __init__(self) -> 'AnyPunctuationChar':
        '''
        Matches any puncutation character.
        '''
        super().__init__('[!"#$%&\'()*+,.\/:;<=>?@\^_`{|}~\-]')


class AnyWhitespace(__Class):
    '''
    Matches any whitespace character.
    '''

    def __init__(self) -> 'AnyWhitespace':
        '''
        Matches any whitespace character.
        '''
        super().__init__(fr'[\s]')


class AnyWithinRange(__Class):
    '''
    Matches any character within the provided range.
    '''

    def __init__(self, start, end) -> 'AnyWithinRange':
        if (type(start) != type(end)) or start >= end:
            raise _exceptions.InvalidRangeException(start, end)
        super().__init__(f"[{start}-{end}]")


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
        super().__init__(f"[{''.join(chars)}]")