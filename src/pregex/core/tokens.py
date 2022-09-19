__doc__ = """
This module contains a number of classes that represent special characters.
Each token represents one and only one character. It is recommended that you
make use of these classes instead of providing their corresponding characters
as strings on your own in order to prevent any errors that relate to character
escaping from happening.

Classes & methods
-------------------------------------------

Below are listed all classes within :py:mod:`pregex.core.tokens`
along with any possible methods they may possess.
"""


import pregex.core.pre as _pre


class __Token(_pre.Pregex):
    '''
    Constitutes the base class for all classes that are part of this module.

    :param str pattern: The pattern representing the token.
    '''

    def __init__(self, pattern: str) -> '__Token':
        '''
        Constitutes the base class for all classes that are part of this module.

        :param str pattern: The pattern representing the token.
        '''
        super().__init__(pattern, escape=False)


class Backslash(__Token):
    '''
    Matches a single backslash character.
    '''

    def __init__(self) -> 'Backslash':
        '''
        Matches a single backslash character.
        '''
        super().__init__(r"\\")


class Bullet(__Token):
    '''
    Matches the bullet symbol "•".
    '''

    def __init__(self) -> 'Bullet':
        '''
         Matches the bullet symbol "•".
        '''
        super().__init__("\u2022")  


class CarriageReturn(__Token):
    '''
    Matches a single carriage return character.
    '''

    def __init__(self) -> 'CarriageReturn':
        '''
        Matches a single carriage return character.
        '''
        super().__init__("\r")


class Copyright(__Token):
    '''
    Matches the copyright symbol "©".
    '''

    def __init__(self) -> 'Copyright':
        '''
         Matches the copyright symbol "©".
        '''
        super().__init__("\u00A9")


class Division(__Token):
    '''
    Matches the division sign "÷".
    '''

    def __init__(self) -> 'Division':
        '''
         Matches the division sign "÷".
        '''
        super().__init__("\u00f7")           


class Dollar(__Token):
    '''
    Matches the dollar sign "$".
    '''

    def __init__(self) -> 'Dollar':
        '''
         Matches the dollar sign "$".
        '''
        super().__init__("\\\u0024")


class Euro(__Token):
    '''
    Matches the euro sign "€".
    '''

    def __init__(self) -> 'Euro':
        '''
         Matches the euro sign "€".
        '''
        super().__init__("\u20ac")


class FormFeed(__Token):
    '''
    Matches a single form feed character.
    '''

    def __init__(self) -> 'FormFeed':
        '''
        Matches a single form feed character.
        '''
        super().__init__("\f")


class Infinity(__Token):
    '''
    Matches the infinity symbol "∞".
    '''

    def __init__(self) -> 'Infinity':
        '''
         Matches the infinity symbol "∞".
        '''
        super().__init__("\u221e")  


class Multiplication(__Token):
    '''
    Matches the multiplication sign "×".
    '''

    def __init__(self) -> 'Multiplication':
        '''
         Matches the multiplication sign "×".
        '''
        super().__init__("\u00d7")        


class Newline(__Token):
    '''
    Matches a single newline character.
    '''

    def __init__(self) -> 'Newline':
        '''
         Matches a single newline character.
        '''
        super().__init__("\n")


class Pound(__Token):
    '''
    Matches the English pound sign "£".
    '''

    def __init__(self) -> 'Pound':
        '''
         Matches the English pound sign "£".
        '''
        super().__init__("\u00a3")


class Registered(__Token):
    '''
    Matches the registered trademark symbol "®".
    '''

    def __init__(self) -> 'Registered':
        '''
         Matches the registered trademark symbol "®".
        '''
        super().__init__("\u00ae")


class Rupee(__Token):
    '''
    Matches the Indian rupee sign "₹".
    '''

    def __init__(self) -> 'Yen':
        '''
         Matches the Indian rupee sign "₹".
        '''
        super().__init__("\u20b9") 


class Space(__Token):
    '''
    Matches a single space character.
    '''

    def __init__(self) -> 'Space':
        '''
         Matches a single space character.
        '''
        super().__init__(" ")


class Tab(__Token):
    '''
    Matches a single tab character.
    '''

    def __init__(self) -> 'Tab':
        '''
         Matches a single tab character.
        '''
        super().__init__("\t")


class Trademark(__Token):
    '''
    Matches the unregistered trademark symbol "™".
    '''

    def __init__(self) -> 'Trademark':
        '''
         Matches the unregistered trademark symbol "™".
        '''
        super().__init__("\u2122")


class VerticalTab(__Token):
    '''
    Matches a single vertical tab character.
    '''

    def __init__(self) -> 'VerticalTab':
        '''
         Matches a single vertical tab character.
        '''
        super().__init__("\v")


class WhiteBullet(__Token):
    '''
    Matches the white bullet symbol "◦".
    '''

    def __init__(self) -> 'WhiteBullet':
        '''
         Matches the white bullet symbol "◦".
        '''
        super().__init__("\u25e6") 


class Yen(__Token):
    '''
    Matches the Japanese yen sign "¥".
    '''

    def __init__(self) -> 'Yen':
        '''
         Matches the Japanese yen sign "¥".
        '''
        super().__init__("\u00a5")        