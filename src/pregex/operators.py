import pregex.pre as _pre
import pregex.exceptions as _exceptions


class __Operator(_pre.Pregex):
    '''
    Constitutes the base class for every class within "operators.py".

    :raises LessThanTwoArgumentsException: Less than two arguments are provided.
    '''

    def __init__(self, pres: tuple[_pre.Pregex or str], transform, type: _pre._Type) -> _pre.Pregex:
        if len(pres) < 2:
            raise _exceptions.LessThanTwoArgumentsException()
        result = __class__._to_pregex(pres[0])
        for pre in pres[1:]:
            result = _pre.Pregex(transform(result, __class__._to_pregex(pre)), escape=False)
            result._set_type(type)
        super().__init__(str(result), escape=False)
        self._set_type(type)


class Concat(__Operator):
    '''
    Matches the concatenation of the provided patterns.

    :param Pregex | str *pres: Two or more patterns that are to be concatenated.

    :raises LessThanTwoArgumentsException: Less than two arguments are provided.
    '''

    def __init__(self, *pres: _pre.Pregex or str) -> _pre.Pregex:
        '''
        Matches the concatenation of the provided patterns.

        :param Pregex | str *pres: Two or more patterns that are to be concatenated.

        :raises LessThanTwoArgumentsException: Less than two arguments are provided.
        '''
        super().__init__(pres, lambda pre1, pre2: pre1._concat(pre2), _pre._Type.Concat)


class Either(__Operator):
    '''
    Matches either one of the provided patterns.

    :param Pregex | str *pres: Two or more patterns that constitute the \
        operator's alternatives.

    :raises LessThanTwoArgumentsException: Less than two arguments are provided.

    :note: One should be aware that "Either" is eager, meaning that the regex engine will \
        stop the moment it matches either one of the alternatives, starting from \
        the left-most pattern and continuing on to the right until a match occurs.
    '''
    
    def __init__(self, *pres: _pre.Pregex or str):
        '''
        Matches either one of the provided patterns.

        :param Pregex | str *pres: Two or more patterns that constitute the \
            operator's alternatives.

        :raises LessThanTwoArgumentsException: Less than two arguments are provided.

        :note: One should be aware that "Either" is eager, meaning that the regex engine will \
            stop the moment it matches either one of the alternatives, starting from \
            the left-most pattern and continuing on to the right until a match occurs.
        '''
        super().__init__(pres, lambda pre1, pre2: pre1._either(pre2), _pre._Type.Alternation)