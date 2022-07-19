class NeitherStringNorPregexException(Exception):
    '''
    This exception is thrown whenever an argument is neither a "Pregex" \
    instance nor a string, even though it is required to be.
    '''

    def __init__(self):
        super().__init__("The argument that was provided is neither a string nor a subtype of \"Pregex\".")



class NeitherStringNorTokenException(Exception):
    '''
    This exception is thrown whenever an argument is neither a "Token" \
    instance nor a string, even though it is required to be.
    '''

    def __init__(self):
        super().__init__("At least one of the provided arguments is neither a string nor a token.")


class NonStringArgumentException(Exception):
    '''
    This exception is thrown whenever an argument is not a string \
    even though it is required to be.
    '''

    def __init__(self):
        super().__init__("The argument that was provided is not a string.")


class MultiCharTokenException(Exception):
    '''
    This exception is thrown whenever a token argument \
    contains more than one character.
    '''

    def __init__(self, token: str):
        super().__init__(f"Token \"{token}\" must be composed from a single character.")


class NegativeArgumentException(Exception):
    '''
    This exception is thrown whenever an argument is a negative number.
    '''

    def __init__(self, n: int):
        super().__init__(f"Argument of value \"{n}\" is less than zero.")


class NonPositiveArgumentException(Exception):
    '''
    This exception is thrown whenever an argument is either \
    a negative number or the number zero.
    '''

    def __init__(self, n: int):
        super().__init__(f"Argument of value \"{n}\" is non-positive.")


class MinGreaterThanMaxException(Exception):
    '''
    This exception is thrown whenever there were provided a tuple \
    of values "min" and "max", where "min" is greater than "max".
    '''

    def __init__(self, min: int, max: int):
        super().__init__(f"Minimum value \"{min}\" is greater than maximum value \"{max}\.")


class LessThanTwoArgumentsException(Exception):
    '''
    This exception is thrown whenever a single argument \
    was provided to a method which requires at least two.
    '''

    def __init__(self):
        super().__init__("This constructor requires at least two arguments.")


class InvalidCapturingGroupNameException(Exception):
    '''
    This exception is thrown whenever an invalid name \
    for a capturing group was provided.
    '''

    def __init__(self, name: str):
        super().__init__(f"Name \"{name}\" is not valid. A capturing group's " +
        "name must be an alphanumeric sequence that starts with a non-digit.")


class NonIntegerArgumentException(Exception):
    '''
    This exception is thrown whenever the provided argument is not an integer.
    '''

    def __init__(self, arg):
        super().__init__(f"Argument \"{arg}\" is not an integer.")


class CannotBeNegatedException(Exception):
    '''
    This exception is thrown whenever one tries to negate class "Any".
    '''

    def __init__(self):
        super().__init__(f"Class \"Any\" cannot be negated.")


class CannotBeCombinedException(Exception):
    '''
    This exception is thrown whenever one tries to combine a class \
    either with a negated class or an object of different type.
    '''

    def __init__(self, pre1, pre2):
        super().__init__(f"Objects of type {type(pre1)} and {type(pre2)} cannot be combined.")


class InvalidRangeException(Exception):
    '''
    This exception is thrown whenever there were provided a tuple \
    of values "start" and "end", where "start" comes after "end".
    '''

    def __init__(self, start, end):
        super().__init__(f"Range \"[{start}-{end}]\" is not a valid range.")


class NotQuantifiableException(Exception):
    '''
    This exception is thrown whenever an instance of a class \
    that is part of the "Anchor" assertions is being quantified.
    '''

    def __init__(self, pre):
        super().__init__(f"Instance of type {type(pre)} is not quantifiable.")



