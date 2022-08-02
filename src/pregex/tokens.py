import pregex.pre as _pre
import pregex.exceptions as _exceptions


class Space(_pre.Pregex):
    '''
    Matches a single space character.
    '''

    def __init__(self) -> 'Space':
        '''
         Matches a single space character.
        '''
        super().__init__(r" ", escape=False)


class Backslash(_pre.Pregex):
    '''
    Matches a single backslash character.
    '''

    def __init__(self) -> 'Backslash':
        '''
         Matches a backslash character.
        '''
        super().__init__(r"\\", escape=False)


class Newline(_pre.Pregex):
    '''
    Matches a single newline character.
    '''

    def __init__(self) -> 'Newline':
        '''
         Matches a single newline character.
        '''
        super().__init__(r"\n", escape=False)


class CarriageReturn(_pre.Pregex):
    '''
    Matches a single carriage return character.
    '''

    def __init__(self) -> 'CarriageReturn':
        '''
         Matches a carriage return character.
        '''
        super().__init__(r"\r", escape=False)


class FormFeed(_pre.Pregex):
    '''
    Matches a single form feed character.
    '''

    def __init__(self) -> 'FormFeed':
        '''
         Matches a form feed character.
        '''
        super().__init__(r"\f", escape=False)


class Tab(_pre.Pregex):
    '''
    Matches a single tab character.
    '''

    def __init__(self) -> 'Tab':
        '''
         Matches a single tab character.
        '''
        super().__init__(r"\t", escape=False)


class VerticalTab(_pre.Pregex):
    '''
    Matches a single vertical tab character.
    '''

    def __init__(self) -> 'VerticalTab':
        '''
         Matches a single vertical tab character.
        '''
        super().__init__(r"\v", escape=False)