import pregex.core.pre as _pre
import pregex.core.tokens as _tk
import pregex.core.groups as _gr
import pregex.core.classes as _cl
import pregex.core.operators as _op
import pregex.core.exceptions as _ex
import pregex.core.assertions as _asr
import pregex.core.quantifiers as _qu


__doc__ = '''
This module contains various classes that can be used to match
all sorts of useful patterns.
'''


class Word(_pre.Pregex):
    '''
    Matches any word.

    :param int min_chars: The minimum amount of characters a word must have in order to \
        be considered a match. Defaults to ``1``.
    :param int max_chars: The maximum amount of characters a word must have in order to \
        be considered a match. If set to "None", then it is considered that there is no upper
        limit to the amount of characters a word can have. Defaults to ``None``.
    :param is_global: Determines whether to include foreign characters. Defaults to ``True``.

    :raises InvalidArgumentTypeException:
        - Parameter ``min_chars`` is not an integer.
        - Parameter ``max_chars`` is neither an integer nor ``None``.
    :raises InvalidArgumentValueException:
        - Either parameter ``min_chars`` or ``max_chars`` has a value of less than ``1``.
        - Parameter ``min_chars`` has a greater value than that of parameter ``max_chars``.
    '''
    def __init__(self, min_chars: int = 1, max_chars: int = None, is_global: bool = True) -> _pre.Pregex:
        '''
        Matches any word.

        :param int min_chars: The minimum amount of characters a word must have in order to \
            be considered a match. Defaults to ``1``.
        :param int max_chars: The maximum amount of characters a word must have in order to \
            be considered a match. If set to "None", then it is considered that there is no upper
            limit to the amount of characters a word can have. Defaults to ``None``.
        :param is_global: Determines whether to include foreign characters. Defaults to ``True``.

        :raises InvalidArgumentTypeException:
            - Parameter ``min_chars`` is not an integer.
            - Parameter ``max_chars`` is neither an integer nor ``None``.
        :raises InvalidArgumentValueException:
            - Either parameter ``min_chars`` or ``max_chars`` has a value of less than ``1``.
            - Parameter ``min_chars`` has a greater value than that of parameter ``max_chars``.
        '''
        pre = _cl.AnyWordChar(is_global=is_global)
        if not isinstance(min_chars, int):
            message = "Provided argument \"min_chars\" must be an integer."
            raise _ex.InvalidArgumentTypeException(message)
        elif min_chars < 1:
            message = "The value of parameter \"min_chars\" must be greater than zero."
            raise _ex.InvalidArgumentValueException(message)
        elif not isinstance(max_chars, int):
            if max_chars is not None:
                message = "Provided argument \"max_chars\" must be either an integer nor \"None\"."
                raise _ex.InvalidArgumentTypeException(message)
        elif max_chars < 1:
            message = "The value of parameter \"max_chars\" must be greater than zero."
            raise _ex.InvalidArgumentValueException(message)
        elif min_chars > max_chars:
            message = "The value of parameter \"max\" must be"
            message += " greater than the value of parameter \"min\"."
            raise _ex.InvalidArgumentValueException(message)
        
        pre = _qu.AtLeastAtMost(pre, min=min_chars, max=max_chars)
        pre = _op.Enclose(pre,_asr.WordBoundary())
        super().__init__(str(pre), escape=False)


class WordContains(_pre.Pregex):
    '''
    Matches any word that contains either one of the provided strings.

    :param list[str] | str infix: Either a string or a list of strings at least one of which \
        a word must contain in order to be considered a match.
    :param is_global: Determines whether to include foreign characters. Defaults to ``True``.

    :raises InvalidArgumentTypeException: At least one of the provided infixes is not a string.
    '''
    def __init__(self, infix: list[str] or str, is_global: bool = True):
        '''
        Matches any word that contains either one of the provided strings.

        :param list[str] | str infix: Either a string or a list of strings at least one of which \
            a word must contain in order to be considered a match.
        :param is_global: Determines whether to include foreign characters. Defaults to ``True``.

        :raises InvalidArgumentTypeException: At least one of the provided infixes is not a string.
        '''
        if not isinstance(infix, list):
            infix = [infix]
        for s in infix:
            if not isinstance(s, str):
                message = f"Provided infix argument \"{s}\" is not a string."
                raise _ex.InvalidArgumentTypeException(message)
        pre = _op.Either(*infix) if len(infix) > 1 else infix[0]
        pre = _qu.Indefinite(_cl.AnyWordChar(is_global=is_global)) + \
            pre + \
            _qu.Indefinite(_cl.AnyWordChar(is_global=is_global))
        pre = _op.Enclose(pre, _asr.WordBoundary())
        super().__init__(str(pre), escape=False)


class WordStartsWith(_pre.Pregex):
    '''
    Matches any word that starts with either one of the provided strings.

    :param list[str] | str prefix: Either a string or a list of strings at least one of which \
        a word must start with in order to be considered a match.
    :param is_global: Determines whether to include foreign characters. Defaults to ``True``.

    :raises InvalidArgumentTypeException: At least one of the provided prefixes is not a string.
    '''
    def __init__(self, prefix: list[str] or str, is_global: bool = True):
        '''
        Matches any word that starts with either one of the provided strings.

        :param list[str] | str prefix: Either a string or a list of strings at least one of which \
            a word must start with in order to be considered a match.
        :param is_global: Determines whether to include foreign characters. Defaults to ``True``.

        :raises InvalidArgumentTypeException: At least one of the provided prefixes is not a string.
        '''
        if not isinstance(prefix, list):
            prefix = [prefix]
        for s in prefix:
            if not isinstance(s, str):
                message = f"Provided prefix argument \"{s}\" is not a string."
                raise _ex.InvalidArgumentTypeException(message)
        pre = _op.Either(*prefix) if len(prefix) > 1 else prefix[0]
        pre = pre + _qu.Indefinite(_cl.AnyWordChar(is_global=is_global))
        pre = _asr.WordBoundary() + pre + _asr.WordBoundary()
        super().__init__(str(pre), escape=False)


class WordEndsWith(_pre.Pregex):
    '''
    Matches any word that ends with either one of the provided strings.

    :param list[str] | str suffix: Either a string or a list of strings at least one of which \
        a word must end with in order to be considered a match.
    :param is_global: Determines whether to include foreign characters. Defaults to ``True``.

    :raises InvalidArgumentTypeException: At least one of the provided suffixes is not a string.
    '''
    def __init__(self, suffix: list[str] or str, is_global: bool = True):
        '''
        Matches any word that ends with either one of the provided strings.

        :param list[str] | str suffix: Either a string or a list of strings at least one of which \
            a word must end with in order to be considered a match.
        :param is_global: Determines whether to include foreign characters. Defaults to ``True``.

        :raises InvalidArgumentTypeException: At least one of the provided suffixes is not a string.
        '''
        if not isinstance(suffix, list):
            suffix = [suffix]
        for s in suffix:
            if not isinstance(s, str):
                message = f"Provided suffix argument \"{s}\" is not a string."
                raise _ex.InvalidArgumentTypeException(message)
        pre = _op.Either(*suffix) if len(suffix) > 1 else suffix[0]
        pre = _qu.Indefinite(_cl.AnyWordChar(is_global=is_global)) + pre
        pre = _asr.WordBoundary() + pre + _asr.WordBoundary()
        super().__init__(str(pre), escape=False)


class Numeral(_pre.Pregex):
    '''
    Matches any numeral.

    :param int base: An integer through which the numeral system is specified. \
        Defaults to ``10``.
    :param int n_min: The minimum amount of digits the number may contain. \
        Defaults to ``1``.
    :param int | None n_max: The maximum amount of digits the number may contain. \
        Defaults to ``None``.

    :raises InvalidArgumentTypeException: 
        - Parameter ``base`` or ``n_min`` is not an integer.
        - Parameter ``n_max`` is neither an integer nor ``None``.
    :raises InvalidArgumentValueException: 
        - Parameter ``base`` has a value of less than ``2`` or greater than ``16``.
        - Either parameter ``n_min`` or ``n_max`` has a value of less than zero.
        - Parameter ``n_min`` has a greater value than that of parameter ``n_max``.

    :note: Setting ``n_max`` equal to ``None`` indicates that there is no upper limit to \
        the number of digits.
    '''
    def __init__(self, base: int = 10, n_min: int = 1, n_max: int = None):
        '''
        Matches any numeral.

        :param int base: An integer through which the numeral system is specified. \
            Defaults to ``10``.
        :param int n_min: The minimum amount of digits the number may contain. \
            Defaults to ``1``.
        :param int | None n_max: The maximum amount of digits the number may contain. \
            Defaults to ``None``.

        :raises InvalidArgumentTypeException: 
            - Parameter ``base`` or ``n_min`` is not an integer.
            - Parameter ``n_max`` is neither an integer nor ``None``.
        :raises InvalidArgumentValueException: 
            - Parameter ``base`` has a value of less than ``2`` or greater than ``16``.
            - Either parameter ``n_min`` or ``n_max`` has a value of less than zero.
            - Parameter ``n_min`` has a greater value than that of parameter ``n_max``.

        :note: Setting ``n_max`` equal to ``None`` indicates that there is no upper limit to \
            the number of digits.
        '''
        if not isinstance(base, int):
            message = "Provided argument \"base\" must be an integer."
            raise _ex.InvalidArgumentTypeException(message)
        if base < 2 or base > 16:
            message = "Provided argument \"base\" must be between ``2`` and ``16``."
            raise _ex.InvalidArgumentValueException(message)
        if not isinstance(n_min, int) or isinstance(n_min, bool):
            message = "Provided argument \"n_min\" must be an integer."
            raise _ex.InvalidArgumentTypeException(message)
        elif n_min < 0:
            message = "Parameter \"n_min\" must be positive."
            raise _ex.InvalidArgumentValueException(message)
        elif not isinstance(n_max, int) or isinstance(n_max, bool):
            if n_max is not None:
                message = "Provided argument \"n_max\" must be either an integer or \"None\"."
                raise _ex.InvalidArgumentTypeException(message)
        elif n_max < 0:
            message = "Parameter \"n_max\" must be positive."
            raise _ex.InvalidArgumentValueException(message)
        elif n_max < n_min:
            message = "The value of parameter \"n_max\" must be"
            message += " greater than the value of parameter \"n_min\"."
            raise _ex.InvalidArgumentValueException(message)
        if base == 2:
            pre = _op.Either("0", "1")
        else:
            pre = _cl.AnyBetween("0", "1")
            digit_map = {i : str(i-1) for i in range(11)} | \
                {11 : _cl.AnyFrom("a", "A"), 12 : _cl.AnyFrom("b", "B"), 13 : _cl.AnyFrom("c", "C"),
                14 : _cl.AnyFrom("d", "D"), 15 : _cl.AnyFrom("e", "E"), 16 : _cl.AnyFrom("f", "F")}
            for i in range(2, base + 1):
                pre = pre | digit_map[i]
        pre = _qu.AtLeastAtMost(pre, n_min, n_max)
        pre = _asr.WordBoundary() + pre + _asr.WordBoundary()
        super().__init__(str(pre), escape=False)


class __Integer(_pre.Pregex):
    '''
    Every "Integer" class inherits from this class.

    :param Pregex sign: A "Pregex" instance that is to be concatenated \
        to the left of the integer.
    :param int start: The starting value of the range.
    :param int end: The ending value of the range.

    :raises InvalidArgumentTypeException: Either parameter ``start`` \
        or parameter ``end`` is not an integer.
    :raises InvalidArgumentValueException: 
        - Parameter ``start`` has a value of less than zero.
        - Parameter ``start`` has a greater value than that of parameter ``end``.
    '''
    def __init__(self, sign: _pre.Pregex, start: int, end: int):
        '''
        Every "Integer" class inherits from this class.

        :param Pregex sign: A "Pregex" instance that is to be concatenated \
            to the left of the integer.
        :param int start: The starting value of the range.
        :param int end: The ending value of the range.

        :raises InvalidArgumentTypeException: Either parameter ``start`` \
            or parameter ``end`` is not an integer.
        :raises InvalidArgumentValueException: 
            - Parameter ``start`` has a value of less than zero.
            - Parameter ``start`` has a greater value than that of parameter ``end``.
        '''
        if not isinstance(start, int):
            message = "Provided argument \"start\" must be an integer."
            raise _ex.InvalidArgumentTypeException(message)
        elif not isinstance(end, int):
            message = "Provided argument \"end\" must be an integer."
            raise _ex.InvalidArgumentTypeException(message)
        elif start < 0:
            message = "Parameter \"start\" must be positive."
            raise _ex.InvalidArgumentValueException(message)
        if start > end:
            message = "Parameter \"end\" must have a greater value than parameter \"start\"."
            raise _ex.InvalidArgumentValueException(message)
        pre = sign + __class__.__integer(start, end)
        super().__init__(str(pre), escape=False)
        

    def __integer(start: int, end: int) -> _pre.Pregex:
        '''
        Returns a "Pregex" instance able to match integers within the \
            specified range.

        :param int start: The starting value of the range.
        :param int end: The ending value of the range.
        '''

        # Used to fill-in empty space in "start" string.
        filler = "F"

        def any_between(d_start: str, d_end: str, is_first: bool = False):
            '''
            Performs some checks and modifications before \
            returing the specified range class.

            :param str d_start: The start of the range.
            :param str d_end: The end of the range.
            :param bool is_first: Indicates whether this function is \
                called during the first iteration. Defaults to ``False``.
            '''
            if d_start == filler:
                d_start = '1' if is_first else '0'
            if d_start == d_end:
                return d_start
            return _cl.AnyBetween(d_start, d_end)
        
        start, end = str(start), str(end)
        start = f"{filler * (len(end) - len(start))}{start}"

        p_start = _asr.WordBoundary()
        p_end = _asr.WordBoundary()

        pre = _asr.WordBoundary()

        for i, (d_start, d_end) in enumerate(zip(start, end)):
            # First if will always execute for i == 0.
            if str(p_start) == str(p_end):
                digit_pre = any_between(d_start, d_end, i==0)
            else:
                digit_pre = _op.Either(
                    _asr.PrecededBy(
                        any_between(d_start, '9'),
                        p_start
                    ),
                    _asr.PrecededBy(
                        any_between('0', d_end),
                        p_end
                    ),
                    _asr.NotPrecededBy(
                        _cl.AnyDigit(),
                        p_start, p_end
                    )
                )
                if i > 1:
                    digit_pre = _asr.NotPrecededBy(
                        digit_pre,
                        *[
                            _asr.WordBoundary() + '0' 
                            + (i - 2) * _cl.AnyDigit() for i in range(2, i+1)
                        ]
                    )
                

            p_start += d_start.replace(filler, '')
            p_end += d_end
            
            if d_start == filler:
                digit_pre = _qu.Optional(digit_pre)

            pre += digit_pre

        return pre + _asr.WordBoundary()


class Integer(__Integer):
    '''
    Matches any integer within a specified range.

    :param int start: The starting value of the range. Defaults to ``0``.
    :param int end: The ending value of the range. Defaults to ``2147483647``.
    :param bool ignore_sign: Determines whether to ignore any existing \
        signs or include them into the match. Defaults to ``True``.

    :raises InvalidArgumentTypeException: Either parameter ``start`` \
        or parameter ``end`` is not an integer.
    :raises InvalidArgumentValueException: 
        - Parameter ``start`` has a value of less than zero.
        - Parameter ``start`` has a greater value than that of parameter ``end``.

    :note: Be aware that parameter ``ignore_sign`` might not only play a role in \
        deciding the content of the matches, but their number as well. For example, \
        setting ``ignore_sign`` to ``True`` will result in ``Integer`` matching both \
        ``1`` and ``2`` in ``1+2``, whereas setting it to ``False`` results in just \
        matching ``1``. That is, because in case ``ignore_sign`` is ``False``,  ``+2`` \
        is considered an integer as a whole, and as such, it cannot match when another \
        digit, namely ``1``, directly precedes it.
    '''
    def __init__(self, start: int = 0, end: int = 2147483647, ignore_sign: bool = True):
        '''
        Matches any integer within the specified range.

        :param int start: The starting value of the range. Defaults to ``0``.
        :param int end: The ending value of the range. Defaults to ``2147483647``.
        :param bool ignore_sign: Determines whether to ignore any existing \
            signs or include them into the match. Defaults to ``True``.

        :raises InvalidArgumentTypeException: Either parameter ``start`` \
            or parameter ``end`` is not an integer.
        :raises InvalidArgumentValueException: 
            - Parameter ``start`` has a value of less than zero.
            - Parameter ``start`` has a greater value than that of parameter ``end``.

        :note: Be aware that parameter ``ignore_sign`` might not only play a role in \
            deciding the content of the matches, but their number as well. For example, \
            setting ``ignore_sign`` to ``True`` will result in ``Integer`` matching both \
            ``1`` and ``2`` in ``1+2``, whereas setting it to ``False`` results in just \
            matching ``1``. That is, because in case ``ignore_sign`` is ``False``,  ``+2`` \
            is considered an integer as a whole, and as such, it cannot match when another \
            digit, namely ``1``, directly precedes it.
        '''
        if ignore_sign:
            sign = _pre.Empty()
        else:
            sign = _op.Either(
                _asr.NonWordBoundary() + _op.Either("+", "-"),
                _asr.NotPrecededBy(
                    _pre.Empty(),
                    _op.Either("+", "-")
                )
            )
        super().__init__(sign, start, end)


class PositiveInteger(__Integer):
    '''
    Matches any strictly positive integer within a specified range.

    :param int start: The starting value of the range. Defaults to ``0``.
    :param int end: The ending value of the range. Defaults to ``2147483647``.

    :raises InvalidArgumentTypeException: Either parameter ``start`` \
        or parameter ``end`` is not an integer.
    :raises InvalidArgumentValueException: 
        - Parameter ``start`` has a value of less than zero.
        - Parameter ``start`` has a greater value than that of parameter ``end``.
    '''
    def __init__(self, start: int = 0, end: int = 2147483647):
        '''
        Matches any strictly positive integer within the specified range.

        :param int start: The starting value of the range. Defaults to ``0``.
        :param int end: The ending value of the range. Defaults to ``2147483647``.

        :raises InvalidArgumentTypeException: Either parameter ``start`` \
            or parameter ``end`` is not an integer.
        :raises InvalidArgumentValueException: 
            - Parameter ``start`` has a value of less than zero.
            - Parameter ``start`` has a greater value than that of parameter ``end``.
        '''
        sign = _op.Either(
            _asr.NonWordBoundary() + "+",
            _asr.NotPrecededBy(
                _pre.Empty(),
                _op.Either("+", "-")
            )
        )
        super().__init__(sign, start, end)


class NegativeInteger(__Integer):
    '''
    Matches any strictly negative integer within a specified range.

    :param int start: The starting value of the range. Defaults to ``0``.
    :param int end: The ending value of the range. Defaults to ``2147483647``.

    :raises InvalidArgumentTypeException: Either parameter ``start`` \
        or parameter ``end`` is not an integer.
    :raises InvalidArgumentValueException: 
        - Parameter ``start`` has a value of less than zero.
        - Parameter ``start`` has a greater value than that of parameter ``end``.
    '''
    def __init__(self, start: int = 0, end: int = 2147483647):
        '''
        Matches any strictly negative integer within the specified range.

        :param int start: The starting value of the range. Defaults to ``0``.
        :param int end: The ending value of the range. Defaults to ``2147483647``.

        :raises InvalidArgumentTypeException: Either parameter ``start`` \
            or parameter ``end`` is not an integer.
        :raises InvalidArgumentValueException: 
            - Parameter ``start`` has a value of less than zero.
            - Parameter ``start`` has a greater value than that of parameter ``end``.
        '''
        sign = _asr.NonWordBoundary() + "-"
        super().__init__(sign, start, end)


class UnsignedInteger(__Integer):
    '''
    Matches any integer within a specified range, \
    provided that it is not preceded by a sign.

    :param int start: The starting value of the range. Defaults to ``0``.
    :param int end: The ending value of the range. Defaults to ``2147483647``.

    :raises InvalidArgumentTypeException: Either parameter ``start`` \
        or parameter ``end`` is not an integer.
    :raises InvalidArgumentValueException: 
        - Parameter ``start`` has a value of less than zero.
        - Parameter ``start`` has a greater value than that of parameter ``end``.
    '''
    def __init__(self, start: int = 0, end: int = 2147483647):
        '''
        Matches any integer within a specified range, \
        provided that it is not preceded by a sign.

        :param int start: The starting value of the range. Defaults to ``0``.
        :param int end: The ending value of the range. Defaults to ``2147483647``.

        :raises InvalidArgumentTypeException: Either parameter ``start`` \
            or parameter ``end`` is not an integer.
        :raises InvalidArgumentValueException: 
            - Parameter ``start`` has a value of less than zero.
            - Parameter ``start`` has a greater value than that of parameter ``end``.
        '''
        sign = _asr.NotPrecededBy(_pre.Empty(), _op.Either("+", "-"))
        super().__init__(sign, start, end)


class __Decimal(_pre.Pregex):
    '''
    Every "Decimal" class inherits from this class.

    :param Pregex integer: A ``Pregex`` instance representing the integer part.
    :param Pregex | None no_integer: A Pregex instance that, if not ``None``, \
        is added to the pattern in order to match no integer-part numbers \
        like ``.123``.
    :param int min_decimal: The minimum number of digits within the decimal part.
    :param int | None max_decimal: The maximum number of digits within the decimal part.

    :raises InvalidArgumentTypeException: Either one of parameters ``start``, \
        ``end``, ``min_decimal`` or ``max_decimal`` is not an integer.
    :raises InvalidArgumentValueException: 
        - Parameter ``start`` has a value of less than ``0``.
        - Parameter ``start`` has a greater value than that of parameter ``end``.
        - Parameter ``min_decimal`` has a value of less than ``1``.
        - Parameter ``min_decimal`` has a greater value than that of parameter ``max_decimal``.
    '''
    def __init__(self, integer: _pre.Pregex, no_integer: _pre.Pregex, min_decimal: int, max_decimal: int):
        '''
        Every "Decimal" class inherits from this class.

        :param Pregex integer: A "Pregex" instance representing the integer part.
        :param Pregex integer: A ``Pregex`` instance representing the integer part.
        :param Pregex | None no_integer: A Pregex instance that, if not ``None``, \
            is added to the pattern in order to match no integer-part numbers \
            like ``.123``.
        :param int min_decimal: The minimum number of digits within the decimal part.
        :param int | None max_decimal: The maximum number of digits within the decimal part.

        :raises InvalidArgumentTypeException: Either one of parameters ``start``, \
            ``end``, ``min_decimal`` or ``max_decimal`` is not an integer.
        :raises InvalidArgumentValueException: 
            - Parameter ``start`` has a value of less than ``0``.
            - Parameter ``start`` has a greater value than that of parameter ``end``.
            - Parameter ``min_decimal`` has a value of less than ``1``.
            - Parameter ``min_decimal`` has a greater value than that of parameter ``max_decimal``.
        '''
        if not isinstance(min_decimal, int) or isinstance(min_decimal, bool):
            message = "Provided argument \"min_decimal\" must be an integer."
            raise _ex.InvalidArgumentTypeException(message)
        elif min_decimal < 1:
            message = "Parameter \"min_decimal\" must be greater than zero."
            raise _ex.InvalidArgumentValueException(message)
        elif not isinstance(max_decimal, int) or isinstance(max_decimal, bool):
            if max_decimal is not None:
                message = "Provided argument \"max_decimal\" must be an integer."
                raise _ex.InvalidArgumentTypeException(message)
        elif min_decimal > max_decimal:
            message = "The value of parameter \"max_decimal\" must be greater"
            message += "than tha of parameter \"min_decimal\"."
            raise _ex.InvalidArgumentValueException(message)
        if no_integer is not None:
            pre = _op.Either(integer, no_integer)
        else:
            pre = integer
        pre += "." + Numeral(n_min=min_decimal, n_max=max_decimal)
        super().__init__(str(pre), escape=False)


class Decimal(__Decimal):
    '''
    Matches any decimal number within a specified range.

    :param int start: The starting value of the integer part range. \
        Defaults to ``0``.
    :param int end: The ending value of the integer part range. \
        Defaults to ``2147483647``.
    :param int min_decimal: The minimum number of digits within the decimal part. \
        Defaults to ``1``.
    :param int | None max_decimal: The maximum number of digits within the decimal part. \
        Defaults to ``None``.
    :param bool ignore_sign: Determines whether to ignore any existing \
        signs or include them into the match. Defaults to ``True``.

    :raises InvalidArgumentTypeException: Either one of parameters ``start``, \
        ``end``, ``min_decimal`` or ``max_decimal`` is not an integer.
    :raises InvalidArgumentValueException: 
        - Parameter ``start`` has a value of less than ``0``.
        - Parameter ``start`` has a greater value than that of parameter ``end``.
        - Parameter ``min_decimal`` has a value of less than ``1``.
        - Parameter ``min_decimal`` has a greater value than that of parameter ``max_decimal``.

    :note: Be aware that parameter ``ignore_sign`` might not only play a role in \
        deciding the content of the matches, but their number as well. For example, \
        setting ``ignore_sign`` to ``True`` will result in ``Integer`` matching both \
        ``1.1`` and ``2.2`` in ``1.1+2.2``, whereas setting it to ``False`` results in \
        just matching ``1.1``. That is, because in case ``ignore_sign`` is ``False``, \
        ``+2.2`` is considered an integer as a whole, and as such, it cannot match when \
        another digit, namely ``1``, directly precedes it.
    '''

    def __init__(self, start: int = 0, end: int = 2147483647,
        min_decimal: int = 1, max_decimal: int = None, ignore_sign: bool = True):
        '''
        Matches any decimal number within a specified range.

        :param int start: The starting value of the integer part range. \
            Defaults to ``0``.
        :param int end: The ending value of the integer part range. \
            Defaults to ``2147483647``.
        :param int min_decimal: The minimum number of digits within the decimal part. \
            Defaults to ``1``.
        :param int | None max_decimal: The maximum number of digits within the decimal part. \
            Defaults to ``None``.
        :param bool ignore_sign: Determines whether to ignore any existing \
            signs or include them into the match. Defaults to ``True``.

        :raises InvalidArgumentTypeException: Either one of parameters ``start``, \
            ``end``, ``min_decimal`` or ``max_decimal`` is not an integer.
        :raises InvalidArgumentValueException: 
            - Parameter ``start`` has a value of less than ``0``.
            - Parameter ``start`` has a greater value than that of parameter ``end``.
            - Parameter ``min_decimal`` has a value of less than ``1``.
            - Parameter ``min_decimal`` has a greater value than that of parameter ``max_decimal``.

        :note: Be aware that parameter ``ignore_sign`` might not only play a role in \
            deciding the content of the matches, but their number as well. For example, \
            setting ``ignore_sign`` to ``True`` will result in ``Integer`` matching both \
            ``1.1`` and ``2.2`` in ``1.1+2.2``, whereas setting it to ``False`` results in \
            just matching ``1.1``. That is, because in case ``ignore_sign`` is ``False``, \
            ``+2.2`` is considered an integer as a whole, and as such, it cannot match when \
            another digit, namely ``1``, directly precedes it.
        '''
        integer = Integer(start, end, ignore_sign)
        if start == 0:
            no_integer = _asr.NonWordBoundary()
            if not ignore_sign:
                no_integer += _qu.Optional(_op.Either("+", "-"))
        else:
            no_integer = None
        super().__init__(integer, no_integer, min_decimal, max_decimal)


class PositiveDecimal(__Decimal):
    '''
    Matches any strictly positive decimal number within a specified range.

    :param int start: The starting value of the integer part range. \
        Defaults to ``0``.
    :param int end: The ending value of the integer part range. \
        Defaults to ``2147483647``.
    :param int min_decimal: The minimum number of digits within the decimal part. \
        Defaults to ``1``.
    :param int | None max_decimal: The maximum number of digits within the decimal part. \
        Defaults to ``None``.

    :raises InvalidArgumentTypeException: Either one of parameters ``start``, \
        ``end``, ``min_decimal`` or ``max_decimal`` is not an integer.
    :raises InvalidArgumentValueException: 
        - Parameter ``start`` has a value of less than ``0``.
        - Parameter ``start`` has a greater value than that of parameter ``end``.
        - Parameter ``min_decimal`` has a value of less than ``1``.
        - Parameter ``min_decimal`` has a greater value than that of parameter ``max_decimal``.
    '''

    def __init__(self, start: int = 0, end: int = 2147483647, min_decimal: int = 1, max_decimal: int = None):
        '''
        Matches any positive decimal number within a specified range.

        :param int start: The starting value of the integer part range. \
            Defaults to ``0``.
        :param int end: The ending value of the integer part range. \
            Defaults to ``2147483647``.
        :param int min_decimal: The minimum number of digits within the decimal part. \
            Defaults to ``1``.
        :param int | None max_decimal: The maximum number of digits within the decimal part. \
            Defaults to ``None``.

        :raises InvalidArgumentTypeException: Either one of parameters ``start``, \
            ``end``, ``min_decimal`` or ``max_decimal`` is not an integer.
        :raises InvalidArgumentValueException: 
            - Parameter ``start`` has a value of less than ``0``.
            - Parameter ``start`` has a greater value than that of parameter ``end``.
            - Parameter ``min_decimal`` has a value of less than ``1``.
            - Parameter ``min_decimal`` has a greater value than that of parameter ``max_decimal``.
        '''
        integer = PositiveInteger(start, end)
        if start == 0:
            no_integer = _asr.NonWordBoundary() + _qu.Optional("+")
        else:
            no_integer = None
        super().__init__(integer, no_integer, min_decimal, max_decimal)


class NegativeDecimal(__Decimal):
    '''
    Matches any negative decimal number within a specified range.

    :param int start: The starting value of the integer part range. \
        Defaults to ``0``.
    :param int end: The ending value of the integer part range. \
        Defaults to ``2147483647``.
    :param int min_decimal: The minimum number of digits within the decimal part. \
        Defaults to ``1``.
    :param int | None max_decimal: The maximum number of digits within the decimal part. \
        Defaults to ``None``.

    :raises InvalidArgumentTypeException: Either one of parameters ``start``, \
        ``end``, ``min_decimal`` or ``max_decimal`` is not an integer.
    :raises InvalidArgumentValueException: 
        - Parameter ``start`` has a value of less than ``0``.
        - Parameter ``start`` has a greater value than that of parameter ``end``.
        - Parameter ``min_decimal`` has a value of less than ``1``.
        - Parameter ``min_decimal`` has a greater value than that of parameter ``max_decimal``.
    '''

    def __init__(self, start: int = 0, end: int = 2147483647, min_decimal: int = 1, max_decimal: int = None):
        '''
        Matches any negative decimal number within a specified range.

        :param int start: The starting value of the integer part range. \
            Defaults to ``0``.
        :param int end: The ending value of the integer part range. \
            Defaults to ``2147483647``.
        :param int min_decimal: The minimum number of digits within the decimal part. \
            Defaults to ``1``.
        :param int | None max_decimal: The maximum number of digits within the decimal part. \
            Defaults to ``None``.

        :raises InvalidArgumentTypeException: Either one of parameters ``start``, \
            ``end``, ``min_decimal`` or ``max_decimal`` is not an integer.
        :raises InvalidArgumentValueException: 
            - Parameter ``start`` has a value of less than ``0``.
            - Parameter ``start`` has a greater value than that of parameter ``end``.
            - Parameter ``min_decimal`` has a value of less than ``1``.
            - Parameter ``min_decimal`` has a greater value than that of parameter ``max_decimal``.
        '''
        integer = NegativeInteger(start, end)
        if start == 0:
            no_integer = _asr.NonWordBoundary() + "-"
        else:
            no_integer = None
        super().__init__(integer, no_integer, min_decimal, max_decimal)


class UnsignedDecimal(__Decimal):
    '''
    Matches any decimal number within a specified range, \
    provided that it is not preceded by a sign.

    :param int start: The starting value of the integer part range. \
        Defaults to ``0``.
    :param int end: The ending value of the integer part range. \
        Defaults to ``2147483647``.
    :param int min_decimal: The minimum number of decimal places. Defaults to ``1``.
    :param int | None max_decimal: The maximum number of decimal places. Defaults to ``None``.
    :param bool include_sign: Determines whether to include any existing \
        signs into the match. Defaults to ``True``.

    :raises InvalidArgumentTypeException: Either one of parameters ``start``, \
        ``end``, ``min_decimal`` or ``max_decimal`` is not an integer.
    :raises InvalidArgumentValueException: 
        - Parameter ``start`` has a value of less than ``0``.
        - Parameter ``start`` has a greater value than that of parameter ``end``.
        - Parameter ``min_decimal`` has a value of less than ``1``.
        - Parameter ``min_decimal`` has a greater value than that of parameter ``max_decimal``.
    '''

    def __init__(self, start: int = 0, end: int = 2147483647, min_decimal: int = 1, max_decimal: int = None):
        '''
        Matches any decimal number within a specified range, \
        provided that it is not preceded by a sign.

        :param int start: The starting value of the integer part range. \
            Defaults to ``0``.
        :param int end: The ending value of the integer part range. \
            Defaults to ``2147483647``.
        :param int min_decimal: The minimum number of decimal places. Defaults to ``1``.
        :param int | None max_decimal: The maximum number of decimal places. Defaults to ``None``.
        :param bool include_sign: Determines whether to include any existing \
            signs into the match. Defaults to ``True``.

        :raises InvalidArgumentTypeException: Either one of parameters ``start``, \
            ``end``, ``min_decimal`` or ``max_decimal`` is not an integer.
        :raises InvalidArgumentValueException: 
            - Parameter ``start`` has a value of less than ``0``.
            - Parameter ``start`` has a greater value than that of parameter ``end``.
            - Parameter ``min_decimal`` has a value of less than ``1``.
            - Parameter ``min_decimal`` has a greater value than that of parameter ``max_decimal``.
        '''
        integer = UnsignedInteger(start, end)
        if start == 0:
            no_integer = _asr.NotPrecededBy(_asr.FollowedBy(_asr.NonWordBoundary(), "."), "+", "-")
        else:
            no_integer = None
        super().__init__(integer, no_integer, min_decimal, max_decimal)


class Date(_pre.Pregex):
    '''
    Matches any date within a range of predefined formats.

    :param str \*formats: One or more strings through which it is determined \
        what are the exact date formats that are to be considered possible \
        matches. A valid date format can be either one of:

      - ``D<sep>M<sep>Y``
      - ``M<sep>D<sep>Y``
      - ``Y<sep>M<sep>D``

      where:

      - ``<sep>``: Either ``/``
      - ``D``: Either one of the following:

        - ``d``: one-digit day of the month for days below 10
        - ``dd``: two-digit day of the month, e.g. 02

      - ``M``: Either one of the following:

        - ``m``: one-digit month for months below 10, e.g. 3
        - ``mm``: two-digit month, e.g. 03

      - ``Y``: Either one of the following:

        - ``yy``: two-digit year, e.g. 21
        - ``yyyy``: four-digit year, e.g. 2021

      For example, ``dd/mm/yyyy`` is considered a valid date format whereas \
      ``mm/yyyy/dd`` is not. Lastly, If no arguments are provided, then all \
      possible formats are considered.

    :raises InvalidArgumentValueException: At least one of the provided arguments \
        is not a valid date format.
    '''
    __date_separators: tuple[str, str] = ("-", "/")

    __date_value_pre: dict[str, _pre.Pregex] = {
        "d": _cl.AnyDigit() - "0", 
        "dd": _op.Either("0" + (_cl.AnyDigit() - "0"), Integer(10, 31)),
        "m": _cl.AnyDigit() - "0",
        "mm": _op.Either("0" + (_cl.AnyDigit() - "0"), Integer(10, 12)),
        "yy": _cl.AnyDigit() * 2, 
        "yyyy": _cl.AnyDigit() * 4, 
    }

    def __init__(self, *formats: str):
        '''
        Matches any date within a range of predefined formats.

        :param str \*formats: One or more strings through which it is determined \
            what are the exact date formats that are to be considered possible \
            matches. A valid date format can be either one of:

          - ``D<sep>M<sep>Y``
          - ``M<sep>D<sep>Y``
          - ``Y<sep>M<sep>D``

          where:

          - ``<sep>``: Either ``/`` or ``-``
          - ``D``: Either one of the following:

              - ``d``: one-digit day of the month for days below 10
              - ``dd``: two-digit day of the month, e.g. 02

          - ``M``: Either one of the following:

              - ``m``: one-digit month for months below 10, e.g. 3
              - ``mm``: two-digit month, e.g. 03

          - ``Y``: Either one of the following:

              - ``yy``: two-digit year, e.g. 21
              - ``yyyy``: four-digit year, e.g. 2021

          For example, ``dd/mm/yyyy`` is considered a valid date format whereas \
          ``mm/yyyy/dd`` is not. Lastly, If no arguments are provided, then all \
          possible formats are considered.

        :raises InvalidArgumentValueException: At least one of the provided arguments \
            is not a valid date format.
        '''
        date_formats = __class__.__date_formats()
        formats = date_formats if not formats else formats
        
        dates: list[_pre.Pregex] = []
        for format in formats:
            if format not in date_formats:
                message = f"Provided date format \"{format}\" is not valid."
                raise _ex.InvalidArgumentValueException(message)
            dates.append(__class__.__date_pre(format))

        pre = _op.Either(*dates) if len(dates) > 1 else dates[0]
        pre = _asr.WordBoundary() + pre + _asr.WordBoundary()
        super().__init__(str(pre), escape=False)
    

    def __date_pre(format: str) -> _pre.Pregex:
        """
        Converts a date format into a ``Pregex`` instance.
        
        :param str format: The date format to be converted.
        """
        format = format.lower()

        for sep in __class__.__date_separators:
            if sep in format:
                separator = sep
                break
        
        values = format.split(separator)

        date_pre = _pre.Empty()
        for i, value in enumerate(values):
            date_pre += __class__.__date_value_pre[value]
            if i < len(values) - 1:
                date_pre += separator
                
        return date_pre


    def __date_formats() -> list[str]:
        '''
        Returns a list containing all possible date format combinations.
        '''
        day = ("dd", "d")
        month = ("mm", "m")
        year = ("yyyy", "yy")

        date_formats: list[tuple[str, str, str]] = []
        for d in day:
            for m in month:
                for y in year:
                    date_formats.append((d, m, y))
                    date_formats.append((m, d, y))
                    date_formats.append((y, m, d))

        return [sep.join(df) for df in date_formats for sep in __class__.__date_separators]


class IPv4(_pre.Pregex):
    '''
    Matches any IPv4 Address.
    '''

    def __init__(self):
        '''
        Matches any IPv4 Address.
        '''
        ip_octet = Integer(start=0, end=255)
        pre = 3 * (ip_octet + ".") + ip_octet
        pre = _asr.NotEnclosedBy(pre, _op.Either(_cl.AnyDigit(), "."))
        super().__init__(str(pre), escape=False)


class IPv6(_pre.Pregex):
    '''
    Matches any IPv6 Address.
    '''

    def __init__(self):
        '''
        Matches any IPv6 Address.
        '''
        hex_group = Numeral(base=16, n_min=1, n_max=4)
        pre = 7 * (hex_group + ":") + hex_group
        for i in range(9):
            pre = _op.Either(
                pre,
                (_qu.AtLeastAtMost(hex_group + ":", min=0, max=i-1) if i > 1 else _pre.Empty()) + \
                (hex_group if i > 0 else _pre.Empty()) + \
                "::" + \
                (_qu.AtLeastAtMost(hex_group + ":", min=0, max=7-i) if i < 7 else _pre.Empty())+ \
                (hex_group if i < 8 else _pre.Empty())
            )
        pre = _op.Either(pre, "::")
        pre = _asr.NotEnclosedBy(pre, _op.Either(_cl.AnyDigit(), ":"))
        super().__init__(str(pre), escape=False)


class Email(_pre.Pregex):
    '''
    Matches any email address.

    :note: Not guaranteed to match every possible e-mail address.
    '''

    def __init__(self):
        '''
        Matches any email address.

        :note: Not guaranteed to match every possible e-mail address.
        '''
        special = _cl.AnyFrom('!', '#', '$', '%', "'", '*', '+',
            '-', '/', '=', '?', '^', '_', '`', '{', '|', '}', '~')

        alphanum = _cl.AnyLetter() | _cl.AnyDigit()

        name_valid_char = alphanum | special

        left_most = _op.Either(
            _asr.FollowedBy(
                _asr.NonWordBoundary(),
                special
            ),
            _asr.FollowedBy(
                _asr.WordBoundary(),
                alphanum
            )  
        ) 

        name = \
            (name_valid_char - '-') + \
            _qu.AtMost(
                _op.Either(name_valid_char, _asr.NotFollowedBy('.', '.')),
                n=62) + \
            (name_valid_char - '-')

        domain_name = \
            alphanum + \
            _qu.AtMost(alphanum | "-", n=61) + \
            alphanum

        tld = "." + _qu.AtLeastAtMost(_cl.AnyLowercaseLetter(), min=2, max=6)

        pre = left_most + name + "@" + domain_name + tld + _asr.WordBoundary()
        super().__init__(str(pre), escape=False)


class HttpUrl(_pre.Pregex):
    '''
    Matches any HTTP URL.

    :param bool capture_domain: If set to ``True``, then the domain name \
        of each URL match is separately captured as well. Defaults to ``False``.

    :note: Not guaranteed to match every possible HTTP URL.
    '''

    def __init__(self, capture_domain: bool = False):
        '''
        Matches any HTTP URL.

        :param bool capture_domain: If set to ``True``, then the domain name \
            of each URL match is separately captured as well. Defaults to ``False``.

        :note: Not guaranteed to match every possible HTTP URL.
        '''
        left_most = _asr.WordBoundary()

        http_protocol = _qu.Optional("http" + _qu.Optional("s") + "://")

        www = _qu.Optional("www.")

        alphanum = _cl.AnyLetter() | _cl.AnyDigit()

        domain_name = \
            alphanum + \
            _qu.AtMost(alphanum | "-", n=61) + \
            alphanum

        subdomains = _qu.Indefinite(domain_name + ".")

        tld = "." + _qu.AtLeastAtMost(_cl.AnyLowercaseLetter(), min=2, max=6)

        optional_port = _qu.Optional(":" + _qu.AtLeastAtMost(_cl.AnyDigit(), min=1, max=4))

        directories = _qu.Indefinite(
            "/" + \
             _qu.OneOrMore(_cl.AnyWordChar(is_global=True) | (_cl.AnyPunctuation() - "/"))
        ) + _qu.Optional("/")

        right_most = _op.Either(
            _asr.PrecededBy(
                _asr.NonWordBoundary(),
                _cl.AnyPunctuation()
            ),
            _asr.PrecededBy(
                _asr.WordBoundary(),
                _cl.AnyWordChar(is_global=True)
            )  
        )  
        if capture_domain:
            domain_name = _gr.Capture(domain_name)

        pre = left_most + http_protocol + www + subdomains + \
            domain_name + tld + optional_port + directories + right_most
        super().__init__(str(pre), escape=False)

