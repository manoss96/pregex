class InvalidArgumentValueException(Exception):
    '''
    This exception is thrown whenever an argument of invalid value is provided.

    :param str message: The message that is to be displayed \
        along with the exception.
    '''

    def __init__(self, message: str):
        '''
        This exception is thrown whenever an argument of invalid value is provided.

        :param str message: The message that is to be displayed \
            along with the exception.
        '''
        super().__init__(message)


class InvalidArgumentTypeException(Exception):
    '''
    This exception is thrown whenever an argument of invalid type is provided.

    :param str message: The message that is to be displayed \
        along with the exception.
    '''

    def __init__(self, message: str):
        '''
        This exception is thrown whenever an argument of invalid type is provided.

        :param str message: The message that is to be displayed \
            along with the exception.
        '''
        super().__init__(message)


class NotEnoughArgumentsException(Exception):
    '''
    This exception is thrown whenever an insufficient amount \
    of arguments is provided.

    :param str message: The message that is to be displayed \
        along with the exception.
    '''

    def __init__(self, message: str):
        '''
        This exception is thrown whenever an insufficient amount \
        of arguments is provided.

        :param str message: The message that is to be displayed \
            along with the exception.
        '''
        super().__init__(message)


class InvalidCapturingGroupNameException(Exception):
    '''
    This exception is thrown whenever an invalid name \
    for a capturing group was provided.

    :param str name: The string type argument because of which this exception was thrown.
    '''

    def __init__(self, name: str):
        '''
        This exception is thrown whenever an invalid name \
        for a capturing group was provided.

        :param str name: The string type argument because of which this exception was thrown.
        '''
        super().__init__(f"Name \"{name}\" is not valid. A capturing group's " +
        "name must be an alphanumeric sequence that starts with a non-digit.")


class CannotBeNegatedException(Exception):
    '''
    This exception is thrown whenever one tries to negate class ``Any``.
    '''
    def __init__(self):
        '''
        This exception is thrown whenever one tries to negate class ``Any``.
        '''
        super().__init__(f"Class \"Any\" cannot be negated.")


class CannotBeUnionedException(Exception):
    '''
    This exception is thrown whenever one tries to union a class (or negated class) \
    either with a negated class (or regular class) or an object of different type.

    :param Pregex pre: The ``Pregex`` instance because of which this exception was thrown.
    :param bool are_both_classes: Indicates whether both ``Pregex`` instances are of \ 
        type ``__Class``.
    '''

    def __init__(self, pre, are_both_classes: bool):
        '''
        This exception is thrown whenever one tries to union a class (or negated class) \
        either with a negated class (or regular class) or an object of different type.

        :param Pregex pre: The ``Pregex`` instance because of which this exception was thrown.
        :param bool are_both_classes: Indicates whether both ``Pregex`` instances are of \ 
            type ``__Class``.
        '''
        m = f"Classes and negated classes cannot be unioned together." if are_both_classes \
            else f"Instance of type \"{type(pre).__name__}\" cannot be unioned with a class."
        super().__init__(m)


class CannotBeSubtractedException(Exception):
    '''
    This exception is thrown whenever one tries to subtract a class (or negated class) \
    either from a negated class (or regular class) or an object of different type.

    :param Pregex pre: The ``Pregex`` instance because of which this exception was thrown.
    :param bool are_both_classes: Indicates whether both ``Pregex`` instances are of type ``__Class``.
    '''

    def __init__(self, pre, are_both_classes: bool):
        '''
        This exception is thrown whenever one tries to subtract a class (or negated class) \
        either from a negated class (or regular class) or an object of different type.

        :param Pregex pre: The ``Pregex`` instance because of which this exception was thrown.
        :param bool are_both_classes: Indicates whether both ``Pregex`` instances are of type ``__Class``.
        '''
        m = f"Classes and negated classes cannot be subtracted from one another." if are_both_classes \
            else f"Instance of type \"{type(pre).__name__}\" cannot be subtracted from a class."
        super().__init__(m)


class GlobalWordCharSubtractionException(Exception):
    '''
    This exception is thrown whenever one tries to subtract from an instance of \
    either one of ``AnyWordChar`` or ``AnyButWordChar`` classes, for which parameter \
    "is_global" has been set to ``True``.

    :param AnyWordChar | AnyButWordChar pre: An instance of either one of the two classes.
    '''

    def __init__(self, pre):
        '''
        This exception is thrown whenever one tries to subtract from an instance of \
        either one of ``AnyWordChar`` or ``AnyButWordChar`` classes, for which parameter \
        "is_global" has been set to ``True``.

        :param AnyWordChar | AnyButWordChar pre: An instance of either one of the two classes.
        '''
        m = f"Cannot subtract from an instance of class \"{type(pre).__name__}\"" + \
             " for which parameter \"is_global\" has been set to \"True\"."
        super().__init__(m)


class EmptyClassException(Exception):
    '''
    This exception is thrown whenever one tries to subtract a class (or negated class) \
    from a class (or negated class) which results in an empty class.

    :param Pregex pre1: The ``Pregex`` instance because of which this exception was thrown.
    :param Pregex pre2: The ``Pregex`` instance because of which this exception was thrown.
    '''

    def __init__(self, pre1, pre2):
        '''
        This exception is thrown whenever one tries to subtract a class (or negated class) \
        from a class (or negated class) which results in an empty class.

        :param Pregex pre1: The ``Pregex`` instance because of which this exception was thrown.
        :param Pregex pre2: The ``Pregex`` instance because of which this exception was thrown.
        '''
        m = f"Cannot subtract class \"{pre2}\" from class \"{pre1}\"" \
            " as this results into an empty class."
        super().__init__(m)


class InvalidRangeException(Exception):
    '''
    This exception is thrown whenever there was provided a pair \
    of values ``start`` and ``end``, where ``start`` comes after ``end``.

    :param int start: The integer because of which this exception was thrown.
    :param int end: The integer because of which this exception was thrown.
    '''

    def __init__(self, start: int, end: int):
        '''
        This exception is thrown whenever there was provided a pair \
        of values ``start`` and ``end``, where ``start`` comes after ``end``.

        :param int start: The integer because of which this exception was thrown.
        :param int end: The integer because of which this exception was thrown.
        '''
        super().__init__(f"\"[{start}-{end}]\" is not a valid range.")


class CannotBeRepeatedException(Exception):
    '''
    This exception is thrown whenever an instance of a class \
    that is part of the ``assertions`` module is being quantified.

    :param __Assertion pre: The ``__Assertion`` instance because of which this exception was thrown.
    '''

    def __init__(self, pre):
        '''
        This exception is thrown whenever there is an attempt to \
        repeat a non-repeatable pattern.

        :param __Assertion pre: The ``__Assertion`` instance because of which this exception was thrown.
        '''
        m = f"Pattern \"{pre.get_pattern()}\" is non-repeatable."
        super().__init__(m)


class NonFixedWidthPatternException(Exception):
    '''
    This exception is thrown whenever a non-fixed-width pattern is being
    provided as lookbehind-pattern to either ``PrecededBy`` or ``NotPrecededBy``.

    :param __Lookaround lookbehind: The ``__Lookaround`` instance because of which this exception was thrown.
    :param Pregex pre: The ``Pregex`` instance because of which this exception was thrown.
    '''

    def __init__(self, lookbehind, pre):
        '''
        This exception is thrown whenever a non-fixed-width pattern is being
        provided as lookbehind-pattern to either ``PrecededBy`` or ``NotPrecededBy``.

        :param __Lookaround lookbehind: The ``__Lookaround`` instance because of which this exception was thrown.
        :param Pregex pre: The ``Pregex`` instance because of which this exception was thrown.
        '''
        m = f"Instances of class \"{type(lookbehind).__name__}\" cannot receive an instance of "
        m += f"class \"{type(pre).__name__}\" in place of a lookbehind-restriction-pattern as the"
        m += " latter represents a pattern whose width is not fixed."
        super().__init__(m)


class EmptyNegativeAssertionException(Exception):
    '''
    This exception is thrown whenever the ``Empty`` pattern is provided
    as a negative assertion.
    '''

    def __init__(self):
        '''
        This exception is thrown whenever the ``Empty`` pattern is provided
        as a negative assertion.
        '''
        message = "The empty string can't be provided as a negative lookaround assertion pattern."
        super().__init__(message)