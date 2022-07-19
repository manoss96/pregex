from abc import ABC
from pregex.pre import Pregex
from pregex.exceptions import NonStringArgumentException


class Token(Pregex, ABC):
    '''
    All tokens must inherit from this class.
    '''

    def __init__(self, pattern, group_on_concat, group_on_quantify) -> 'Token':
        super().__init__(pattern, group_on_concat, group_on_quantify)


class Literal(Token):
    '''
    Matches the provided string as it is.
    '''

    def __init__(self, s: str) -> 'Literal':
        '''
        Matches the provided string as it is.

        :param str s: The string that is to be matched.
        '''
        if not isinstance(s, str):
            raise NonStringArgumentException()
        literal = __class__._to_pregex(s)
        super().__init__(
            str(literal),
            group_on_concat=literal._get_group_on_concat(),
            group_on_quantify=literal._get_group_on_quantify())


class Space(Token):
    '''
    Matches a single space character.
    '''

    def __init__(self) -> 'Space':
        '''
         Matches a single space character.
        '''
        super().__init__(r" ", group_on_concat=False, group_on_quantify=False)


class Backslash(Token):
    '''
    Matches a single backslash character.
    '''

    def __init__(self) -> 'Backslash':
        '''
         Matches a backslash character.
        '''
        super().__init__(r"\\", group_on_concat=False, group_on_quantify=False)


class Newline(Token):
    '''
    Matches a single newline character.
    '''

    def __init__(self) -> 'Newline':
        '''
         Matches a single newline character.
        '''
        super().__init__(r"\n", group_on_concat=False, group_on_quantify=False)


class CarriageReturn(Token):
    '''
    Matches a single carriage return character.
    '''

    def __init__(self) -> 'CarriageReturn':
        '''
         Matches a carriage return character.
        '''
        super().__init__(r"\r", group_on_concat=False, group_on_quantify=False)


class FormFeed(Token):
    '''
    Matches a single form feed character.
    '''

    def __init__(self) -> 'FormFeed':
        '''
         Matches a form feed character.
        '''
        super().__init__(r"\f", group_on_concat=False, group_on_quantify=False)


class Tab(Token):
    '''
    Matches a single tab character.
    '''

    def __init__(self) -> 'Tab':
        '''
         Matches a single tab character.
        '''
        super().__init__(r"\t", group_on_concat=False, group_on_quantify=False)


class VerticalTab(Token):
    '''
    Matches a single vertical tab character.
    '''

    def __init__(self) -> 'VerticalTab':
        '''
         Matches a single vertical tab character.
        '''
        super().__init__(r"\v", group_on_concat=False, group_on_quantify=False)