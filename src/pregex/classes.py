import re
from string import whitespace
from pregex.pre import Pregex
from pregex.tokens import Token
from pregex.exceptions import InvalidRangeException, NeitherStringNorTokenException, \
    MultiCharTokenException, CannotBeNegatedException, CannotBeCombinedException


class __Class(Pregex):
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
    def __init__(self, pattern: str) -> '__Class':
        super().__init__(pattern, group_on_concat=False, group_on_quantify=False)

    def __invert__(self) -> '_NegatedClass':
        return _NegatedClass(f"[^{str(self).lstrip('[').rstrip(']')}]")

    def __or__(self, pre: '__Class') -> '__Class':
        if (not issubclass(pre.__class__, __class__)) or isinstance(pre, _NegatedClass):
            raise CannotBeCombinedException(self, pre)
        return __class__.__or(self, pre)

    def __ror__(self, pre: '__Class') -> '__Class':
        if (not issubclass(pre.__class__, __class__)) or isinstance(pre, _NegatedClass):
            raise CannotBeCombinedException(pre, self)
        return __class__.__or(pre, self)

    def __or(pre1: '__Class', pre2: '__Class') -> '__Class':
        # Create pattern for matching possible classes.
        pattern = r".\-.|\\?[^\[\]]"
        classes = set(re.findall(pattern, str(pre1)))\
            .union(set(re.findall(pattern, str(pre2))))
        return Any() if isinstance(pre1, Any) or isinstance(pre2, Any) \
            else __class__(f"[{''.join(classes)}]")


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
            raise CannotBeCombinedException(self, pre)
        return __class__.__or(self, pre)

    def __ror__(self, pre: '_NegatedClass') -> '_NegatedClass':
        if (not issubclass(pre.__class__, __class__)) or isinstance(pre, super().__class__):
            raise CannotBeCombinedException(self, pre)
        return __class__.__or(pre, self)

    def __or(pre1: '_NegatedClass', pre2: '_NegatedClass') -> '_NegatedClass':
        # Create pattern for matching possible classes.
        pattern = r".\-.|\\?[^\^\[\]]"
        classes = set(re.findall(pattern, str(pre1)))\
            .union(set(re.findall(pattern, str(pre2))))
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
        raise CannotBeNegatedException()

    def __or__(self, pre: '__Class') -> 'Any':
        if (not issubclass(pre.__class__, __class__.__base__)) or isinstance(pre, _NegatedClass):
            raise CannotBeCombinedException(self, pre)
        return Any()

    def __ror__(self, pre: '__Class') -> 'Any':
        if (not issubclass(pre.__class__, __class__.__base__)) or isinstance(pre, _NegatedClass):
            raise CannotBeCombinedException(self, pre)
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
        super().__init__('[0-9]')


class AnyWordChar(__Class):
    '''
    Matches any alphanumeric character plus "_".
    '''

    def __init__(self) -> 'AnyWordChar':

        '''
        Matches any alphanumeric character plus "_".
        '''
        super().__init__('[a-zA-Z0-9_]')


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
        super().__init__(f'[{whitespace}]')


class AnyWithinRange(__Class):
    '''
    Matches any character within the provided range.
    '''

    def __init__(self, start, end) -> 'AnyWithinRange':
        if (type(start) != type(end)) or start >= end:
            raise InvalidRangeException(start, end)
        super().__init__(f"[{start}-{end}]")


class AnyFrom(__Class):
    '''
    Matches any one of the provided characters.
    '''

    def __init__(self, *chars: str or Token) -> 'AnyFrom':
        '''
        Matches any one of the provided characters.

        :param Pregex | str *chars: One or more characters to match from. Each character must be \
            a string of length one, provided either as is or wrapped within an instance of type \
            "Token".
        '''
        for c in chars:
            if not issubclass(c.__class__, (str, Token)):
                raise NeitherStringNorTokenException()
            if len(str(c).replace("\\", "")) > 1:
                raise MultiCharTokenException(str(c))
        chars = tuple(str(Pregex(pre)._literal()) if isinstance(pre, str) else str(pre) for pre in chars)
        super().__init__(f"[{''.join(chars)}]")