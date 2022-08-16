import pregex.pre as _pre
import pregex.exceptions as _ex


__doc__ = """
This module contains two classes, namely :class:`Concat` and :class:`Either`, the 
former of which is used to concatenate two or more patterns, whereas the latter
constitutes the alternation operator, which is used whenever either one of the
provided patterns can be matched.

Classes & methods
-------------------------------------------

Below are listed all classes within :py:mod:`pregex.operators`
along with any possible methods they may possess.
"""


class __Operator(_pre.Pregex):
    '''
    Constitutes the base class for all classes that are part of this module.

    :param tuple[Pregex | str] pres: A tuple of strings or Pregex instances representing \
        the patterns to which the operator is to be applied.
    :param (tuple[Pregex | str] => str) transform: A `transform` function for the provided pattern.

    :raises NotEnoughArgumentsException: Less than two arguments are provided.
    '''
    def __init__(self, pres: tuple[_pre.Pregex or str], transform) -> _pre.Pregex:
        '''
        Constitutes the base class for all classes that are part of this module.

        :param tuple[Pregex | str] pres: A tuple of strings or Pregex instances representing \
            the patterns to which the operator is to be applied.
        :param (tuple[Pregex | str] => str) transform: A `transform` function for the provided pattern.

        :raises NotEnoughArgumentsException: Less than two arguments are provided.
        '''
        if len(pres) < 2:
            message = "At least two requirements are required."
            raise _ex.NotEnoughArgumentsException(message)
        result =_pre.Empty()
        for pre in pres:
            result = _pre.Pregex(transform(result, __class__._to_pregex(pre)), escape=False)
        super().__init__(str(result), escape=False)


class Concat(__Operator):
    '''
    Matches the concatenation of the provided patterns.

    :param Pregex | str \*pres: Two or more patterns that are to be concatenated.

    :raises NotEnoughArgumentsException: Less than two arguments are provided.
    '''

    def __init__(self, *pres: _pre.Pregex or str) -> _pre.Pregex:
        '''
        Matches the concatenation of the provided patterns.

        :param Pregex | str \*pres: Two or more patterns that are to be concatenated.

        :raises NotEnoughArgumentsException: Less than two arguments are provided.
        '''
        super().__init__(pres, lambda pre1, pre2: pre1._concat(pre2))


class Either(__Operator):
    '''
    Matches either one of the provided patterns.

    :param Pregex | str \*pres: Two or more patterns that constitute the \
        operator's alternatives.

    :raises NotEnoughArgumentsException: Less than two arguments are provided.

    :note: One should be aware that ``Either`` is eager, meaning that the regex engine will \
        stop the moment it matches either one of the alternatives, starting from \
        the left-most pattern and continuing on to the right until a match occurs.
    '''
    
    def __init__(self, *pres: _pre.Pregex or str):
        '''
        Matches either one of the provided patterns.

        :param Pregex | str \*pres: Two or more patterns that constitute the \
            operator's alternatives.

        :raises NotEnoughArgumentsException: Less than two arguments are provided.

        :note: One should be aware that ``Either`` is eager, meaning that the regex engine will \
            stop the moment it matches either one of the alternatives, starting from \
            the left-most pattern and continuing on to the right until a match occurs.
        '''
        super().__init__(pres, lambda pre1, pre2: pre1._either(pre2))