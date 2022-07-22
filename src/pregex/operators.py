import pregex.pre as _pre
import pregex.exceptions as _exceptions


class __Operator(_pre.Pregex):
    '''
    Every "Operator" class must inherit from this class.
    '''

    def __init__(self, pres: tuple[str or _pre.Pregex], transform) -> _pre.Pregex:
        if len(pres) < 2:
            raise _exceptions.LessThanTwoArgumentsException()
        result = __class__._to_pregex(pres[0])
        for pre in pres[1:]:
            result = transform(result, __class__._to_pregex(pre))
        super().__init__(str(result), result._get_group_on_concat(), result._get_group_on_quantify())


class Concat(__Operator):
    '''
    Matches the concatenation of the provided patterns.
    '''

    def __init__(self, *pres: str or _pre.Pregex) -> _pre.Pregex:
        '''
        Matches the concatenation of the provided patterns.

        :param Pregex | str *pres: Two or more patterns that are to be concatenated.
        '''
        super().__init__(pres, lambda pre1, pre2: pre1._concat(pre2))


class Either(__Operator):
    '''
    Matches either one of the provided patterns.

    NOTE: One should be aware that "Either" is eager, meaning that the regex engine will \
        stop the moment it matches either one of the alternatives, starting from \
        the left-most pattern and continuing on to the right until a match occurs.
    '''
    
    def __init__(self, *pres: str or _pre.Pregex):
        '''
        Matches either one of the provided patterns.

        :param Pregex | str *pres: Two or more patterns that constitute the \
            operator's alternatives.
        '''
        super().__init__(pres, lambda pre1, pre2: pre1._either(pre2))