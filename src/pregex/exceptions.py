

class NeitherStringNorPregexException(Exception):
    '''
    This exception is thrown whenever an argument is neither a "Pregex" \
    instance nor a string, even though it is required to be.
    '''

    def __init__(self):
        '''
        The class's constructor.
        '''
        super().__init__("The argument that was provided is neither a string nor a subtype of \"Pregex\".")


class NeitherCharNorTokenException(Exception):
    '''
    This exception is thrown whenever an argument is neither an instance \
    belonging in module "tokens" nor a single character string.
    '''

    def __init__(self):
        '''
        The class's constructor.
        '''
        super().__init__("At least one of the provided arguments is neither a string nor a token.")


class NonStringArgumentException(Exception):
    '''
    This exception is thrown whenever an argument is not a string \
    even though it is required to be.
    '''

    def __init__(self):
        '''
        The class's constructor.
        '''
        super().__init__("The argument that was provided is not a string.")


class NegativeArgumentException(Exception):
    '''
    This exception is thrown whenever an argument is a negative number.
    '''

    def __init__(self, n: int):
        '''
        The class's constructor.

        :param int n: The integer because of which this exception was thrown.
        '''
        super().__init__(f"Argument of value \"{n}\" is less than zero.")


class NonPositiveArgumentException(Exception):
    '''
    This exception is thrown whenever an argument is either \
    a negative number or the number zero.
    '''

    def __init__(self, n: int):
        '''
        The class's constructor.

        :param int n: The integer because of which this exception was thrown.
        '''
        super().__init__(f"Argument of value \"{n}\" is non-positive.")


class MinGreaterThanMaxException(Exception):
    '''
    This exception is thrown whenever there were provided a tuple \
    of values "min" and "max", where "min" is greater than "max".
    '''

    def __init__(self, min: int, max: int):
        '''
        The class's constructor.

        :param int min: The integer because of which this exception was thrown.
        :param int max: The integer because of which this exception was thrown.
        '''
        super().__init__(f"Minimum value \"{min}\" is greater than maximum value \"{max}\.")


class LessThanTwoArgumentsException(Exception):
    '''
    This exception is thrown whenever a single argument \
    was provided to a method which requires at least two.
    '''

    def __init__(self):
        '''
        The class's constructor.
        '''
        super().__init__("This constructor requires at least two arguments.")


class InvalidCapturingGroupNameException(Exception):
    '''
    This exception is thrown whenever an invalid name \
    for a capturing group was provided.
    '''

    def __init__(self, name: str):
        '''
        The class's constructor.

        :param str name: The string type argument because of which this exception was thrown.
        '''
        super().__init__(f"Name \"{name}\" is not valid. A capturing group's " +
        "name must be an alphanumeric sequence that starts with a non-digit.")


class NonIntegerArgumentException(Exception):
    '''
    This exception is thrown whenever the provided argument is not an integer.
    '''

    def __init__(self, arg):
        '''
        The class's constructor.

        :param Any arg: The unknown type argument because of which this exception was thrown.
        '''
        super().__init__(f"Argument \"{arg}\" is not an integer.")


class CannotBeNegatedException(Exception):
    '''
    This exception is thrown whenever one tries to negate class "Any".
    '''

    def __init__(self):
        super().__init__(f"Class \"Any\" cannot be negated.")


class CannotBeUnionedException(Exception):
    '''
    This exception is thrown whenever one tries to union a class (or negated class) \
    either with a negated class (or regular class) or an object of different type.
    '''

    def __init__(self, pre1, pre2, are_both_classes: bool):
        '''
        The class's constructor.

        :param Pregex pre1: The "Pregex" instance because of which this exception was thrown.
        :param Pregex pre2: The "Pregex" instance because of which this exception was thrown.
        :param bool are_both_classes: Indicates whether both "Pregex" instances are of type "__Class".
        '''
        m = f"Classes and negated classes cannot be unioned together." if are_both_classes \
            else f"Objects of type \"{type(pre1).__name__}\" and \"{type(pre2).__name__}\" cannot be combined."
        super().__init__(m)


class CannotBeSubtractedException(Exception):
    '''
    This exception is thrown whenever one tries to subtract a class (or negated class) \
    either from a negated class (or regular class) or an object of different type.
    '''

    def __init__(self, pre1, pre2, are_both_classes: bool):
        '''
        The class's constructor.

        :param Pregex pre1: The "Pregex" instance because of which this exception was thrown.
        :param Pregex pre2: The "Pregex" instance because of which this exception was thrown.
        :param bool are_both_classes: Indicates whether both "Pregex" instances are of type "__Class".
        '''
        m = f"Classes and negated classes cannot be subtracted from one another" if are_both_classes \
            else f"Objects of type {type(pre1)} and {type(pre2)} cannot be subtracted from one another."
        super().__init__(m)


class GlobalWordCharSubtractionException(Exception):
    '''
    This exception is thrown whenever one tries to subtract from an instance of \
    either one of "AnyWordChar" or "AnyButWordChar" classes, for which parameter \
    "is_global" has been set to "true".
    '''

    def __init__(self, pre):
        '''
        The class's constructor.

        :param AnyWordChar | AnyButWordChar pre: An instance of either one of the two classes.
        '''
        m = f"Cannot subtract from an instance of class \"{type(pre).__name__}\"" + \
             " for which parameter \"is_global\" has been set to \"True\"."
        super().__init__(m)


class EmptyClassException(Exception):
    '''
    This exception is thrown whenever one tries to subtract a class (or negated class) \
    from a class (or negated class) which results in an empty class.
    '''

    def __init__(self, pre1, pre2):
        '''
        The class's constructor.

        :param Pregex pre1: The "Pregex" instance because of which this exception was thrown.
        :param Pregex pre2: The "Pregex" instance because of which this exception was thrown.
        '''
        m = f"Cannot subtract class \"{pre2}\" from class \"{pre1}\"" \
            " as this results into an empty class."
        super().__init__(m)


class InvalidRangeException(Exception):
    '''
    This exception is thrown whenever there were provided a tuple \
    of values "start" and "end", where "start" comes after "end".
    '''

    def __init__(self, start, end):
        '''
        The class's constructor.

        :param int start: The integer because of which this exception was thrown.
        :param int end: The integer because of which this exception was thrown.
        '''
        super().__init__(f"\"[{start}-{end}]\" is not a valid range.")


class CannotBeQuantifiedException(Exception):
    '''
    This exception is thrown whenever an instance of a class \
    that is part of the "assertions" module is being quantified.
    '''

    def __init__(self, pre):
        '''
        The class's constructor.

        :param __Assertion pre: The "__Assertion" instance because of which this exception was thrown.
        '''
        super().__init__(f"Instance of type {type(pre)} is not quantifiable.")


class NonFixedWidthPatternException(Exception):
    '''
    This exception is thrown whenever an non-fixed-width pattern
    is being provided as parameter "pre2" to either "PrecededBy"
    or "NotPrecededBy".
    '''

    def __init__(self, lookbehind, pre):
        '''
        The class's constructor.

        :param __Lookaround lookbehind: The "__Lookaround" instance because of which this exception was thrown.
        :param Pregex pre: The "Pregex" instance because of which this exception was thrown.
        '''
        super().__init__(f"Instance of type {type(lookbehind)} cannot receive an instance of type {type(pre)} in "
            "place of parameter \"pre2\" as the latter represents a pattern whose width is not fixed.")



