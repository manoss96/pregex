__doc__ = """
This module contains three classes, namely :class:`Concat`, :class:`Enclose`,
and :class:`Either`, the first two of which are used to concatenate two or more patterns
together, whereas the last one constitutes the alternation operator, which is used to
indicate that either one of the provided patterns constitutes a valid match.

Classes & methods
-------------------------------------------

Below are listed all classes within :py:mod:`pregex.core.operators`
along with any possible methods they may possess.
"""


import pregex.core.pre as _pre
import pregex.core.exceptions as _ex
from typing import Union as _Union


class __Operator(_pre.Pregex):
    '''
    Constitutes the base class for all classes that are part of this module.

    :param tuple[Pregex | str] pres: A tuple of strings or Pregex instances representing \
        the patterns to which the operator is to be applied.
    :param (tuple[Pregex | str] => str) transform: A `transform` function for the provided pattern.

    :raises NotEnoughArgumentsException: Less than two arguments are provided.
    :raises InvalidArgumentTypeException: At least one of the provided arguments \
        through ``pres`` is neither a ``Pregex`` instance nor a string.
    '''
    def __init__(self, pres: tuple[_Union[_pre.Pregex, str]], transform) -> _pre.Pregex:
        '''
        Constitutes the base class for all classes that are part of this module.

        :param tuple[Pregex | str] pres: A tuple of strings or Pregex instances representing \
            the patterns to which the operator is to be applied.
        :param (tuple[Pregex | str] => str) transform: A `transform` function for the provided pattern.

        :raises NotEnoughArgumentsException: Less than two arguments are provided.
        :raises InvalidArgumentTypeException: At least one of the provided arguments \
            through ``pres`` is neither a ``Pregex`` instance nor a string.
        '''
        if len(pres) < 2:
            message = "At least two arguments are required."
            raise _ex.NotEnoughArgumentsException(message)
        result = __class__._to_pregex(pres[0])
        for pre in pres[1:]:
            result = transform(result, pre)
        super().__init__(str(result), escape=False)


class Concat(__Operator):
    '''
    Matches the concatenation of the provided patterns.

    :param Pregex | str \*pres: Two or more patterns that are to be concatenated.

    :raises NotEnoughArgumentsException: Less than two arguments are provided.
    :raises InvalidArgumentTypeException: At least one of the provided arguments \
        is neither a ``Pregex`` instance nor a string.
    '''

    def __init__(self, *pres: _Union[_pre.Pregex, str]) -> _pre.Pregex:
        '''
        Matches the concatenation of the provided patterns.

        :param Pregex | str \*pres: Two or more patterns that are to be concatenated.

        :raises NotEnoughArgumentsException: Less than two arguments are provided.
        :raises InvalidArgumentTypeException: At least one of the provided arguments \
            is neither a ``Pregex`` instance nor a string.
        '''
        super().__init__(pres, lambda pre1, pre2: pre1.concat(pre2))


class Either(__Operator):
    '''
    Matches either one of the provided patterns.

    :param Pregex | str \*pres: Two or more patterns that constitute the \
        operator's alternatives.

    :raises NotEnoughArgumentsException: Less than two arguments are provided.
    :raises InvalidArgumentTypeException: At least one of the provided arguments \
        is neither a ``Pregex`` instance nor a string.

    :note: One should be aware that ``Either`` is eager, meaning that the regex engine will \
        stop the moment it matches either one of the alternatives, starting from \
        the left-most pattern and continuing on to the right until a match occurs.
    '''
    
    def __init__(self, *pres: _Union[_pre.Pregex, str]):
        '''
        Matches either one of the provided patterns.

        :param Pregex | str \*pres: Two or more patterns that constitute the \
            operator's alternatives.

        :raises NotEnoughArgumentsException: Less than two arguments are provided.
        :raises InvalidArgumentTypeException: At least one of the provided arguments \
            is neither a ``Pregex`` instance nor a string.

        :note: One should be aware that :class:`Either` is eager, meaning that the regex engine will \
            stop the moment it matches either one of the alternatives, starting from \
            the left-most pattern and continuing on to the right until a match occurs.
        '''
        super().__init__(pres, lambda pre1, pre2: pre1.either(pre2))


class Enclose(__Operator):
    '''
    Matches the pattern that results from concatenating the ``enclosing`` patterns \
    to both sides of pattern ``pre`` one by one.

    :param Pregex | str enclosed: The pattern that is to be at the center \
        of the concatenation.
    :param Pregex | str enclosing: One or more patterns that are to *enclose* \
        pattern ``pre`` one by one.

    :raises NotEnoughArgumentsException: Less than two arguments are provided.
    :raises InvalidArgumentTypeException: Either ``pre`` or at least one of the \
        ``enclosing`` patterns is neither a ``Pregex`` instance nor a string.
    '''

    def __init__(self, pre: _Union[_pre.Pregex, str], *enclosing:_Union[_pre.Pregex, str]) -> _pre.Pregex:
        '''
        Matches the pattern that results from concatenating the ``enclosing`` patterns \
        to both sides of pattern ``pre`` one by one.

        :param Pregex | str enclosed: The pattern that is to be at the center \
            of the concatenation.
        :param Pregex | str enclosing: One or more patterns that are to *enclose* \
            pattern ``pre`` one by one.

        :raises NotEnoughArgumentsException: Less than two arguments are provided.
        :raises InvalidArgumentTypeException: Either ``pre`` or at least one of the \
            ``enclosing`` patterns is neither a ``Pregex`` instance nor a string.
        '''
        super().__init__((pre, *enclosing), lambda pre1, pre2: pre1.enclose(pre2))