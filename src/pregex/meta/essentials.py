__doc__ = '''
This module contains various classes that can be used to match
all sorts of commonly-search-for patterns.

Classes & methods
-------------------------------------------

Below are listed all classes within :py:mod:`pregex.meta.essentials`
along with any possible methods they may possess.
'''

import pregex.core.pre as _pre
import pregex.core.groups as _gr
import pregex.core.classes as _cl
import pregex.core.operators as _op
import pregex.core.exceptions as _ex
import pregex.core.assertions as _asr
import pregex.core.quantifiers as _qu
from typing import Union as _Union
from typing import Optional as _Optional


class Text(_pre.Pregex):
    '''
    Matches any string of text of arbitrary length.

    :param bool is_optional: Determines whether this pattern is optional \
        or not. Defaults to ``False``.
    '''

    def __init__(self, is_optional: bool = False) -> _pre.Pregex:
        '''
        Matches any string of text of arbitrary length.

        :param bool is_optional: Determines whether this pattern is optional \
            or not. Defaults to ``False``.
        '''
        if is_optional:
            pre = _qu.Indefinite(_cl.Any())
        else:
            pre = _qu.OneOrMore(_cl.Any())
        super().__init__(str(pre), escape=False)


class NonWhitespace(_pre.Pregex):
    '''
    Matches any string of text of arbitrary length that does not contain \
    any whitespace characters.

    :param bool is_optional: Determines whether this pattern is optional \
        or not. Defaults to ``False``.
    '''

    def __init__(self, is_optional: bool = False) -> _pre.Pregex:
        '''
        Matches any string of text of arbitrary length that does not contain \
        any whitespace characters.

        :param bool is_optional: Determines whether this pattern is optional \
            or not. Defaults to ``False``.
        '''
        if is_optional:
            pre = _qu.Indefinite(_cl.AnyButWhitespace())
        else:
            pre = _qu.OneOrMore(_cl.AnyButWhitespace())
        super().__init__(str(pre), escape=False)


class Whitespace(_pre.Pregex):
    '''
    Matches any string of whitespace characters of arbitrary length.

    :param bool is_optional: Determines whether this pattern is optional \
        or not. Defaults to ``False``.
    '''

    def __init__(self, is_optional: bool = False) -> _pre.Pregex:
        '''
        Matches any string of whitespace characters of arbitrary length.

        :param bool is_optional: Determines whether this pattern is optional \
            or not. Defaults to ``False``.
        '''
        if is_optional:
            pre = _qu.Indefinite(_cl.AnyWhitespace())
        else:
            pre = _qu.OneOrMore(_cl.AnyWhitespace())
        super().__init__(str(pre), escape=False)


class __Word(_pre.Pregex):
    '''
    This is the base class for every "Word" as well as the "Numeral" class.

    :param Pregex pre: A Pregex instance representing the word pattern.
    :param bool is_extensible: If ``True``, then no additional assertions \
        are imposed upon the underlying pattern, other than any necessary ones, \
        which in turn prevents certain complications from arising whenever it \
        serves as a building block to a larger pattern. As a general rule of thumb, \
        set this parameter to ``True`` if you wish to extend the resulting instance's \
        underlying pattern, or to ``False`` if you are only using it for matching purposes.
    '''

    def __init__(self, pre: _pre.Pregex, is_extensible: bool) -> _pre.Pregex:
        '''
        This is the base class for every "Word" class.

        :param Pregex pre: A Pregex instance representing the word pattern.
        :param bool is_extensible: If ``True``, then no additional assertions \
            are imposed upon the underlying pattern, other than any necessary ones, \
            which in turn prevents certain complications from arising whenever it \
            serves as a building block to a larger pattern. As a general rule of thumb, \
            set this parameter to ``True`` if you wish to extend the resulting instance's \
            underlying pattern, or to ``False`` if you are only using it for matching purposes.
        '''
        if not is_extensible:
            pre = pre.enclose(_asr.WordBoundary())
        super().__init__(str(pre), escape=False)



class Word(__Word):
    '''
    Matches any word.

    :param int min_chars: The minimum amount of characters a word must have in order to \
        be considered a match. Defaults to ``1``.
    :param int max_chars: The maximum amount of characters a word must have in order to \
        be considered a match. If set to "None", then it is considered that there is no upper
        limit to the amount of characters a word can have. Defaults to ``None``.
    :param is_global: Determines whether to include foreign characters. Defaults to ``True``.
    :param bool is_extensible: If ``True``, then no additional assertions \
        are imposed upon the underlying pattern, other than any necessary ones, \
        which in turn prevents certain complications from arising whenever it \
        serves as a building block to a larger pattern. As a general rule of thumb, \
        set this parameter to ``True`` if you wish to extend the resulting instance's \
        underlying pattern, or to ``False`` if you are only using it for matching purposes. \
        Defaults to ``False``.

    :raises InvalidArgumentTypeException:
        - Parameter ``min_chars`` is not an integer.
        - Parameter ``max_chars`` is neither an integer nor ``None``.
    :raises InvalidArgumentValueException:
        - Either parameter ``min_chars`` or ``max_chars`` has a value of less than ``1``.
        - Parameter ``min_chars`` has a greater value than that of parameter ``max_chars``.
    '''
    def __init__(self, min_chars: int = 1, max_chars: _Optional[int] = None,
        is_global: bool = True, is_extensible: bool = False) -> _pre.Pregex:
        '''
        Matches any word.

        :param int min_chars: The minimum amount of characters a word must have in order to \
            be considered a match. Defaults to ``1``.
        :param int max_chars: The maximum amount of characters a word must have in order to \
            be considered a match. If set to "None", then it is considered that there is no upper
            limit to the amount of characters a word can have. Defaults to ``None``.
        :param is_global: Determines whether to include foreign characters. Defaults to ``True``.
        :param bool is_extensible: If ``True``, then no additional assertions \
            are imposed upon the underlying pattern, other than any necessary ones, \
            which in turn prevents certain complications from arising whenever it \
            serves as a building block to a larger pattern. As a general rule of thumb, \
            set this parameter to ``True`` if you wish to extend the resulting instance's \
            underlying pattern, or to ``False`` if you are only using it for matching purposes. \
            Defaults to ``False``.

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
        
        pre = pre.at_least_at_most(n=min_chars, m=max_chars)
        super().__init__(pre, is_extensible)


class WordContains(__Word):
    '''
    Matches any word that contains either one of the provided strings.

    :param str | list[str] infix: Either a string or a list of strings at \
        least one of which a word must contain in order to be considered a match.
    :param is_global: Determines whether to include foreign characters. \
        Defaults to ``True``.
    :param bool is_extensible: If ``True``, then no additional assertions \
        are imposed upon the underlying pattern, other than any necessary ones, \
        which in turn prevents certain complications from arising whenever it \
        serves as a building block to a larger pattern. As a general rule of thumb, \
        set this parameter to ``True`` if you wish to extend the resulting instance's \
        underlying pattern, or to ``False`` if you are only using it for matching purposes. \
        Defaults to ``False``.

    :raises InvalidArgumentTypeException: At least one of the provided infixes is not a string.
    '''
    def __init__(self, infix: _Union[str, list[str]],
        is_global: bool = True, is_extensible: bool = False) -> _pre.Pregex:
        '''
        Matches any word that contains either one of the provided strings.

        :param str | list[str] infix: Either a string or a list of strings at \
            least one of which a word must contain in order to be considered a match.
        :param is_global: Determines whether to include foreign characters. \
            Defaults to ``True``.
        :param bool is_extensible: If ``True``, then no additional assertions \
            are imposed upon the underlying pattern, other than any necessary ones, \
            which in turn prevents certain complications from arising whenever it \
            serves as a building block to a larger pattern. As a general rule of thumb, \
            set this parameter to ``True`` if you wish to extend the resulting instance's \
            underlying pattern, or to ``False`` if you are only using it for matching purposes. \
            Defaults to ``False``.

        :raises InvalidArgumentTypeException: At least one of the provided infixes is not a string.
        '''
        if not isinstance(infix, list):
            infix = [infix]
        for s in infix:
            if not isinstance(s, str):
                message = f"Provided infix argument \"{s}\" is not a string."
                raise _ex.InvalidArgumentTypeException(message)
        pre = _op.Enclose(
            _op.Either(*infix),
            _qu.Indefinite(_cl.AnyWordChar(is_global=is_global))
        )
        super().__init__(pre, is_extensible)


class WordStartsWith(__Word):
    '''
    Matches any word that starts with either one of the provided strings.

    :param str | list[str] prefix: Either a string or a list of strings with \
        any of which a word must start in order to be considered a match.
    :param is_global: Determines whether to include foreign characters. \
        Defaults to ``True``.
    :param bool is_extensible: If ``True``, then no additional assertions \
        are imposed upon the underlying pattern, other than any necessary ones, \
        which in turn prevents certain complications from arising whenever it \
        serves as a building block to a larger pattern. As a general rule of thumb, \
        set this parameter to ``True`` if you wish to extend the resulting instance's \
        underlying pattern, or to ``False`` if you are only using it for matching purposes. \
        Defaults to ``False``.

    :raises InvalidArgumentTypeException: At least one of the provided prefixes is not a string.
    '''
    def __init__(self, prefix: _Union[str, list[str]],
        is_global: bool = True, is_extensible: bool = False) -> _pre.Pregex:
        '''
        Matches any word that starts with either one of the provided strings.

        :param str | list[str] prefix: Either a string or a list of strings with \
            any of which a word must start in order to be considered a match.
        :param is_global: Determines whether to include foreign characters. \
            Defaults to ``True``.
        :param bool is_extensible: If ``True``, then no additional assertions \
            are imposed upon the underlying pattern, other than any necessary ones, \
            which in turn prevents certain complications from arising whenever it \
            serves as a building block to a larger pattern. As a general rule of thumb, \
            set this parameter to ``True`` if you wish to extend the resulting instance's \
            underlying pattern, or to ``False`` if you are only using it for matching purposes. \
            Defaults to ``False``.

        :raises InvalidArgumentTypeException: At least one of the provided prefixes is not a string.
        '''
        if not isinstance(prefix, list):
            prefix = [prefix]
        for s in prefix:
            if not isinstance(s, str):
                message = f"Provided prefix argument \"{s}\" is not a string."
                raise _ex.InvalidArgumentTypeException(message)
        pre = _op.Either(*prefix)
        pre = pre + _qu.Indefinite(_cl.AnyWordChar(is_global=is_global))
        super().__init__(pre, is_extensible)


class WordEndsWith(__Word):
    '''
    Matches any word that ends with either one of the provided strings.

    :param str | list[str] suffix: Either a string or a list of strings with \
        any of which a word must end in order to be considered a match.
    :param is_global: Determines whether to include foreign characters. \
        Defaults to ``True``.
    :param bool is_extensible: If ``True``, then no additional assertions \
        are imposed upon the underlying pattern, other than any necessary ones, \
        which in turn prevents certain complications from arising whenever it \
        serves as a building block to a larger pattern. As a general rule of thumb, \
        set this parameter to ``True`` if you wish to extend the resulting instance's \
        underlying pattern, or to ``False`` if you are only using it for matching purposes. \
        Defaults to ``False``.


    :raises InvalidArgumentTypeException: At least one of the provided suffixes is not a string.
    '''
    def __init__(self, suffix: _Union[str, list[str]],
        is_global: bool = True, is_extensible: bool = False) -> _pre.Pregex:
        '''
        Matches any word that ends with either one of the provided strings.

        :param str | list[str] suffix: Either a string or a list of strings with \
            any of which a word must end in order to be considered a match.
        :param is_global: Determines whether to include foreign characters. \
            Defaults to ``True``.
        :param bool is_extensible: If ``True``, then no additional assertions \
            are imposed upon the underlying pattern, other than any necessary ones, \
            which in turn prevents certain complications from arising whenever it \
            serves as a building block to a larger pattern. As a general rule of thumb, \
            set this parameter to ``True`` if you wish to extend the resulting instance's \
            underlying pattern, or to ``False`` if you are only using it for matching purposes. \
            Defaults to ``False``.

        :raises InvalidArgumentTypeException: At least one of the provided suffixes is not a string.
        '''
        if not isinstance(suffix, list):
            suffix = [suffix]
        for s in suffix:
            if not isinstance(s, str):
                message = f"Provided suffix argument \"{s}\" is not a string."
                raise _ex.InvalidArgumentTypeException(message)
        pre = _op.Either(*suffix)
        pre = _qu.Indefinite(_cl.AnyWordChar(is_global=is_global)) + pre
        super().__init__(pre, is_extensible)


class Numeral(__Word):
    '''
    Matches any numeral.

    :param int base: An integer through which the numeral system is specified. \
        Defaults to ``10``.
    :param int n_min: The minimum amount of digits the number may contain. \
        Defaults to ``1``.
    :param int n_max: The maximum amount of digits the number may contain. \
        Defaults to ``None``.
    :param bool is_extensible: If ``True``, then no additional assertions \
        are imposed upon the underlying pattern, other than any necessary ones, \
        which in turn prevents certain complications from arising whenever it \
        serves as a building block to a larger pattern. As a general rule of thumb, \
        set this parameter to ``True`` if you wish to extend the resulting instance's \
        underlying pattern, or to ``False`` if you are only using it for matching purposes. \
        Defaults to ``False``.

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
    def __init__(self, base: int = 10, n_min: int = 1,
        n_max: _Optional[int] = None, is_extensible: bool = False) -> _pre.Pregex:
        '''
        Matches any numeral.

        :param int base: An integer through which the numeral system is specified. \
            Defaults to ``10``.
        :param int n_min: The minimum amount of digits the number may contain. \
            Defaults to ``1``.
        :param int n_max: The maximum amount of digits the number may contain. \
            Defaults to ``None``.
        :param bool is_extensible: If ``True``, then no additional assertions \
            are imposed upon the underlying pattern, other than any necessary ones, \
            which in turn prevents certain complications from arising whenever it \
            serves as a building block to a larger pattern. As a general rule of thumb, \
            set this parameter to ``True`` if you wish to extend the resulting instance's \
            underlying pattern, or to ``False`` if you are only using it for matching purposes. \
            Defaults to ``False``.

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
        pre = pre.at_least_at_most(n=n_min, m=n_max)
        super().__init__(pre, is_extensible)


class __Integer(_pre.Pregex):
    '''
    Every "Integer" class inherits from this class.

    :param Pregex sign: A "Pregex" instance that is to be concatenated \
        to the left of the integer.
    :param int start: The starting value of the range.
    :param int end: The ending value of the range.
    :param bool is_extensible: If ``True``, then no additional assertions \
        are imposed upon the underlying pattern, other than any necessary ones, \
        which in turn prevents certain complications from arising whenever it \
        serves as a building block to a larger pattern. As a general rule of thumb, \
        set this parameter to ``True`` if you wish to extend the resulting instance's \
        underlying pattern, or to ``False`` if you are only using it for matching purposes. \
        Defaults to ``False``.

    :raises InvalidArgumentTypeException: Either parameter ``start`` \
        or parameter ``end`` is not an integer.
    :raises InvalidArgumentValueException: 
        - Parameter ``start`` has a value of less than zero.
        - Parameter ``start`` has a greater value than that of parameter ``end``.
    '''
    def __init__(self, sign: _pre.Pregex, start: int,
        end: int, is_extensible: bool) -> _pre.Pregex:
        '''
        Every "Integer" class inherits from this class.

        :param Pregex sign: A "Pregex" instance that is to be concatenated \
            to the left of the integer.
        :param int start: The starting value of the range.
        :param int end: The ending value of the range.
        :param bool is_extensible: If ``True``, then no additional assertions \
            are imposed upon the underlying pattern, other than any necessary ones, \
            which in turn prevents certain complications from arising whenever it \
            serves as a building block to a larger pattern. As a general rule of thumb, \
            set this parameter to ``True`` if you wish to extend the resulting instance's \
            underlying pattern, or to ``False`` if you are only using it for matching purposes. \
            Defaults to ``False``.

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
        pre = sign + __class__.__integer(start, end, is_extensible)
        super().__init__(str(pre), escape=False)
        

    def __integer(start: int, end: int, is_extensible: bool) -> _pre.Pregex:
        '''
        Returns a ``Pregex`` instance able to match integers \
        within the specified range.

        :param int start: The starting value of the range.
        :param int end: The ending value of the range.
        :param bool is_extensible: If ``True``, then no additional assertions \
            are imposed upon the underlying pattern, other than any necessary ones, \
            which in turn prevents certain complications from arising whenever it \
            serves as a building block to a larger pattern. As a general rule of thumb, \
            set this parameter to ``True`` if you wish to extend the resulting instance's \
            underlying pattern, or to ``False`` if you are only using it for matching purposes. \
            Defaults to ``False``.
        '''

        # Used to fill-in empty space in "start" string.
        filler = "F"

        def any_between(d_start: str, d_end: str, is_first: bool = False) -> _pre.Pregex:
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
                return _pre.Pregex(d_start)
            return _cl.AnyBetween(d_start, d_end)
        
        start, end = str(start), str(end)
        start = f"{filler * (len(end) - len(start))}{start}"

        integer_start = _pre.Pregex().preceded_by(_cl.AnyButDigit()) \
            if is_extensible else _asr.WordBoundary()

        p_start = integer_start
        p_end = integer_start

        pre = integer_start

        for i, (d_start, d_end) in enumerate(zip(start, end)):
            # "if" block will always execute for i == 0.
            if str(p_start) == str(p_end):
                digit_pre = any_between(d_start, d_end, i==0)
            else:
                digit_pre = _op.Either(
                    any_between(d_start, '9').preceded_by(p_start),
                    any_between('0', d_end).preceded_by(p_end),
                    _asr.NotPrecededBy(
                        _cl.AnyDigit(),
                        *[p for p in (p_start, p_end) if p._get_type() != _pre._Type.Empty]
                    )
                )
                if i > 1:
                    digit_pre = \
                        _asr.NotPrecededBy(
                            digit_pre,
                            *[_cl.AnyButDigit() + '0' + (i - 2) * _cl.AnyDigit() for i in range(2, i+1)]
                        )
                
            p_start += d_start.replace(filler, '')
            p_end += d_end
            
            if d_start == filler:
                digit_pre = _qu.Optional(digit_pre)

            pre += digit_pre

        if not is_extensible:
            pre += _asr.WordBoundary()

        return pre


class Integer(__Integer):
    '''
    Matches any integer within a specified range.

    :param int start: The starting value of the range. Defaults to ``0``.
    :param int end: The ending value of the range. Defaults to ``2147483647``.
    :param bool include_sign: Determines whether to include any existing \
        signs into the match, or just ignore them. Defaults to ``False``.
    :param bool is_extensible: If ``True``, then no additional assertions \
        are imposed upon the underlying pattern, other than any necessary ones, \
        which in turn prevents certain complications from arising whenever it \
        serves as a building block to a larger pattern. As a general rule of thumb, \
        set this parameter to ``True`` if you wish to extend the resulting instance's \
        underlying pattern, or to ``False`` if you are only using it for matching purposes. \
        Defaults to ``False``.

    :raises InvalidArgumentTypeException: Either parameter ``start`` \
        or parameter ``end`` is not an integer.
    :raises InvalidArgumentValueException: 
        - Parameter ``start`` has a value of less than zero.
        - Parameter ``start`` has a greater value than that of parameter ``end``.

    :note: 
        - Be aware that parameter ``include_sign`` might not only play a role in \
          deciding the content of the matches, but their number as well. For example, \
          setting ``include_sign`` to ``False`` will result in ``Integer`` matching both \
          ``1`` and ``2`` in ``1+2``, whereas setting it to ``True`` results in just \
          matching ``1``. That is, because in case ``include_sign`` is ``True``,  ``+2`` \
          is considered an integer as a whole, and as such, it cannot match when another \
          digit, namely ``1``, directly precedes it.
        - Even by setting parameter ``is_extensible`` to ``True``, there still persists \
          an assertion that is essential to the pattern, which dictates that this pattern \
          must not be preceded by any numeric characters. For that reason, one should avoid \
          concatenating an instance of this class to the right of a pattern that ends in \
          such a character.


    '''
    def __init__(self, start: int = 0, end: int = 2147483647,
        include_sign: bool = False, is_extensible: bool = False) -> _pre.Pregex:
        '''
        Matches any integer within the specified range.

        :param int start: The starting value of the range. Defaults to ``0``.
        :param int end: The ending value of the range. Defaults to ``2147483647``.
        :param bool include_sign: Determines whether to include any existing \
            signs into the match, or just ignore them. Defaults to ``False``.
        :param bool is_extensible: If ``True``, then no additional assertions \
            are imposed upon the underlying pattern, other than any necessary ones, \
            which in turn prevents certain complications from arising whenever it \
            serves as a building block to a larger pattern. As a general rule of thumb, \
            set this parameter to ``True`` if you wish to extend the resulting instance's \
            underlying pattern, or to ``False`` if you are only using it for matching purposes. \
            Defaults to ``False``.

        :raises InvalidArgumentTypeException: Either parameter ``start`` \
            or parameter ``end`` is not an integer.
        :raises InvalidArgumentValueException: 
            - Parameter ``start`` has a value of less than zero.
            - Parameter ``start`` has a greater value than that of parameter ``end``.

        :note: 
            - Be aware that parameter ``include_sign`` might not only play a role in \
              deciding the content of the matches, but their number as well. For example, \
              setting ``include_sign`` to ``False`` will result in ``Integer`` matching both \
              ``1`` and ``2`` in ``1+2``, whereas setting it to ``True`` results in just \
              matching ``1``. That is, because in case ``include_sign`` is ``True``,  ``+2`` \
              is considered an integer as a whole, and as such, it cannot match when another \
              digit, namely ``1``, directly precedes it.
            - Even by setting parameter ``is_extensible`` to ``True``, there still persists \
              an assertion that is essential to the pattern, which dictates that this pattern \
              must not be preceded by any numeric characters. For that reason, one should avoid \
              concatenating an instance of this class to the right of a pattern that ends in \
              such a character.
        '''

        empty = _pre.Pregex()

        either_sign = _op.Either('+', '-')

        if include_sign:
            if is_extensible:
                left_most = either_sign
            else:
                left_most = _op.Either(
                    _asr.NonWordBoundary() + either_sign,
                    empty.not_preceded_by(either_sign)
                )
        else:
            left_most = empty

        super().__init__(left_most, start, end, is_extensible)


class PositiveInteger(__Integer):
    '''
    Matches any strictly positive integer within a specified range.

    :param int start: The starting value of the range. Defaults to ``0``.
    :param int end: The ending value of the range. Defaults to ``2147483647``.
    :param bool is_extensible: If ``True``, then no additional assertions \
        are imposed upon the underlying pattern, other than any necessary ones, \
        which in turn prevents certain complications from arising whenever it \
        serves as a building block to a larger pattern. As a general rule of thumb, \
        set this parameter to ``True`` if you wish to extend the resulting instance's \
        underlying pattern, or to ``False`` if you are only using it for matching purposes. \
        Defaults to ``False``.

    :raises InvalidArgumentTypeException: Either parameter ``start`` \
        or parameter ``end`` is not an integer.
    :raises InvalidArgumentValueException: 
        - Parameter ``start`` has a value of less than zero.
        - Parameter ``start`` has a greater value than that of parameter ``end``.

    :note: Even by setting parameter ``is_extensible`` to ``True``, there still persists \
        an assertion that is essential to the pattern, which dictates that this pattern \
        must not be preceded by any numeric characters. For that reason, one should avoid \
        concatenating an instance of this class to the right of a pattern that ends in such \
        a character.
    '''
    def __init__(self, start: int = 0,
        end: int = 2147483647, is_extensible: bool = False) -> _pre.Pregex:
        '''
        Matches any strictly positive integer within the specified range.

        :param int start: The starting value of the range. Defaults to ``0``.
        :param int end: The ending value of the range. Defaults to ``2147483647``.
        :param bool is_extensible: If ``True``, then no additional assertions \
            are imposed upon the underlying pattern, other than any necessary ones, \
            which in turn prevents certain complications from arising whenever it \
            serves as a building block to a larger pattern. As a general rule of thumb, \
            set this parameter to ``True`` if you wish to extend the resulting instance's \
            underlying pattern, or to ``False`` if you are only using it for matching purposes. \
            Defaults to ``False``.

        :raises InvalidArgumentTypeException: Either parameter ``start`` \
            or parameter ``end`` is not an integer.
        :raises InvalidArgumentValueException: 
            - Parameter ``start`` has a value of less than zero.
            - Parameter ``start`` has a greater value than that of parameter ``end``.

        :note: Even by setting parameter ``is_extensible`` to ``True``, there still persists \
            an assertion that is essential to the pattern, which dictates that this pattern \
            must not be preceded by any numeric characters. For that reason, one should avoid \
            concatenating an instance of this class to the right of a pattern that ends in such \
            a character.
        '''
        if is_extensible:
            sign = _pre.Pregex('+')
        else:
            sign = _op.Either(
                _asr.NonWordBoundary() + '+',
                _pre.Pregex().not_preceded_by(_op.Either('+', '-'))
            )
        super().__init__(sign, start, end, is_extensible)


class NegativeInteger(__Integer):
    '''
    Matches any strictly negative integer within a specified range.

    :param int start: The starting value of the range. Defaults to ``0``.
    :param int end: The ending value of the range. Defaults to ``2147483647``.
    :param bool is_extensible: If ``True``, then no additional assertions \
        are imposed upon the underlying pattern, other than any necessary ones, \
        which in turn prevents certain complications from arising whenever it \
        serves as a building block to a larger pattern. As a general rule of thumb, \
        set this parameter to ``True`` if you wish to extend the resulting instance's \
        underlying pattern, or to ``False`` if you are only using it for matching purposes. \
        Defaults to ``False``.

    :raises InvalidArgumentTypeException: Either parameter ``start`` \
        or parameter ``end`` is not an integer.
    :raises InvalidArgumentValueException: 
        - Parameter ``start`` has a value of less than zero.
        - Parameter ``start`` has a greater value than that of parameter ``end``.

    :note: Even by setting parameter ``is_extensible`` to ``True``, there still persists \
        an assertion that is essential to the pattern, which dictates that this pattern \
        must not be preceded by any numeric characters. For that reason, one should avoid \
        concatenating an instance of this class to the right of a pattern that ends in such \
        a character.
    '''
    def __init__(self, start: int = 0,
        end: int = 2147483647, is_extensible: bool = False) -> _pre.Pregex:
        '''
        Matches any strictly negative integer within the specified range.

        :param int start: The starting value of the range. Defaults to ``0``.
        :param int end: The ending value of the range. Defaults to ``2147483647``.
        :param bool is_extensible: If ``True``, then no additional assertions \
            are imposed upon the underlying pattern, other than any necessary ones, \
            which in turn prevents certain complications from arising whenever it \
            serves as a building block to a larger pattern. As a general rule of thumb, \
            set this parameter to ``True`` if you wish to extend the resulting instance's \
            underlying pattern, or to ``False`` if you are only using it for matching purposes. \
            Defaults to ``False``.

        :raises InvalidArgumentTypeException: Either parameter ``start`` \
            or parameter ``end`` is not an integer.
        :raises InvalidArgumentValueException: 
            - Parameter ``start`` has a value of less than zero.
            - Parameter ``start`` has a greater value than that of parameter ``end``.
        '''
        sign = (_pre.Pregex() if is_extensible else _asr.NonWordBoundary()) + "-"
        super().__init__(sign, start, end, is_extensible)


class UnsignedInteger(__Integer):
    '''
    Matches any integer within a specified range, \
    provided that it is not preceded by a sign.

    :param int start: The starting value of the range. Defaults to ``0``.
    :param int end: The ending value of the range. Defaults to ``2147483647``.
    :param bool is_extensible: If ``True``, then no additional assertions \
        are imposed upon the underlying pattern, other than any necessary ones, \
        which in turn prevents certain complications from arising whenever it \
        serves as a building block to a larger pattern. As a general rule of thumb, \
        set this parameter to ``True`` if you wish to extend the resulting instance's \
        underlying pattern, or to ``False`` if you are only using it for matching purposes. \
        Defaults to ``False``.

    :raises InvalidArgumentTypeException: Either parameter ``start`` \
        or parameter ``end`` is not an integer.
    :raises InvalidArgumentValueException: 
        - Parameter ``start`` has a value of less than zero.
        - Parameter ``start`` has a greater value than that of parameter ``end``.

    :note: Even by setting parameter ``is_extensible`` to ``True``, there still persists \
        an assertion that is essential to the pattern, which dictates that this pattern \
        must not be preceded by any numeric characters. For that reason, one should avoid \
        concatenating an instance of this class to the right of a pattern that ends in such \
        a character.
    '''
    def __init__(self, start: int = 0,
        end: int = 2147483647, is_extensible: bool = False) -> _pre.Pregex:
        '''
        Matches any integer within a specified range, \
        provided that it is not preceded by a sign.

        :param int start: The starting value of the range. Defaults to ``0``.
        :param int end: The ending value of the range. Defaults to ``2147483647``.
        :param bool is_extensible: If ``True``, then no additional assertions \
            are imposed upon the underlying pattern, other than any necessary ones, \
            which in turn prevents certain complications from arising whenever it \
            serves as a building block to a larger pattern. As a general rule of thumb, \
            set this parameter to ``True`` if you wish to extend the resulting instance's \
            underlying pattern, or to ``False`` if you are only using it for matching purposes. \
            Defaults to ``False``.

        :raises InvalidArgumentTypeException: Either parameter ``start`` \
            or parameter ``end`` is not an integer.
        :raises InvalidArgumentValueException: 
            - Parameter ``start`` has a value of less than zero.
            - Parameter ``start`` has a greater value than that of parameter ``end``.
        '''
        sign = _pre.Pregex().not_preceded_by(_op.Either('+', '-'))
        super().__init__(sign, start, end, is_extensible)


class __Decimal(_pre.Pregex):
    '''
    Every "Decimal" class inherits from this class.

    :param Pregex integer_part: A ``Pregex`` instance representing the integer part.
    :param Pregex no_integer_part: A Pregex instance that, if not ``None``, \
        is added to the pattern in order to match no integer-part numbers \
        like ``.123``.
    :param int min_decimal: The minimum number of digits within the decimal part.
    :param int max_decimal: The maximum number of digits within the decimal part.
    :param bool is_extensible: If ``True``, then no additional assertions \
        are imposed upon the underlying pattern, other than any necessary ones, \
        which in turn prevents certain complications from arising whenever it \
        serves as a building block to a larger pattern. As a general rule of thumb, \
        set this parameter to ``True`` if you wish to extend the resulting instance's \
        underlying pattern, or to ``False`` if you are only using it for matching purposes.

    :raises InvalidArgumentTypeException: Either one of parameters ``start``, \
        ``end``, ``min_decimal`` or ``max_decimal`` is not an integer.
    :raises InvalidArgumentValueException: 
        - Parameter ``start`` has a value of less than ``0``.
        - Parameter ``start`` has a greater value than that of parameter ``end``.
        - Parameter ``min_decimal`` has a value of less than ``1``.
        - Parameter ``min_decimal`` has a greater value than that of parameter ``max_decimal``.
    '''
    def __init__(self, integer_part: _pre.Pregex, no_integer_part: _Optional[_pre.Pregex],
        min_decimal: int, max_decimal: _Optional[int], is_extensible: bool) -> _pre.Pregex:
        '''
        Every "Decimal" class inherits from this class.

        :param Pregex integer_part: A ``Pregex`` instance representing the integer part.
        :param Pregex no_integer_part: A Pregex instance that, if not ``None``, \
            is added to the pattern in order to match no integer-part numbers \
            like ``.123``.
        :param int min_decimal: The minimum number of digits within the decimal part.
        :param int max_decimal: The maximum number of digits within the decimal part.
        :param bool is_extensible: If ``True``, then no additional assertions \
            are imposed upon the underlying pattern, other than any necessary ones, \
            which in turn prevents certain complications from arising whenever it \
            serves as a building block to a larger pattern. As a general rule of thumb, \
            set this parameter to ``True`` if you wish to extend the resulting instance's \
            underlying pattern, or to ``False`` if you are only using it for matching purposes.

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
        if no_integer_part is not None:
            pre = _op.Either(integer_part, no_integer_part)
        else:
            pre = integer_part
        pre += "." + Numeral(n_min=min_decimal, n_max=max_decimal, is_extensible=is_extensible)
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
    :param int max_decimal: The maximum number of digits within the decimal part. \
        Defaults to ``None``.
    :param bool include_sign: Determines whether to include any existing \
        signs into the match. Defaults to ``False``.
    :param bool is_extensible: If ``True``, then no additional assertions \
        are imposed upon the underlying pattern, other than any necessary ones, \
        which in turn prevents certain complications from arising whenever it \
        serves as a building block to a larger pattern. As a general rule of thumb, \
        set this parameter to ``True`` if you wish to extend the resulting instance's \
        underlying pattern, or to ``False`` if you are only using it for matching purposes. \
        Defaults to ``False``.

    :raises InvalidArgumentTypeException: Either one of parameters ``start``, \
        ``end``, ``min_decimal`` or ``max_decimal`` is not an integer.
    :raises InvalidArgumentValueException: 
        - Parameter ``start`` has a value of less than ``0``.
        - Parameter ``start`` has a greater value than that of parameter ``end``.
        - Parameter ``min_decimal`` has a value of less than ``1``.
        - Parameter ``min_decimal`` has a greater value than that of parameter ``max_decimal``.

    :note: 
        - Be aware that parameter ``include_sign`` might not only play a role in \
          deciding the content of the matches, but their number as well. For example, \
          setting ``include_sign`` to ``False`` will result in ``Integer`` matching both \
          ``1.1`` and ``2.2`` in ``1.1+2.2``, whereas setting it to ``True`` results in \
          just matching ``1.1``. That is, because in case ``include_sign`` is ``True``, \
          ``+2.2`` is considered a decimal number as a whole, and as such, it cannot match \
          when another digit, namely ``1``, directly precedes it.
        - Even by setting parameter ``is_extensible`` to ``True``, there still persists \
          an assertion that is essential to the pattern, which dictates that this pattern \
          must not be preceded by any numeric characters. For that reason, one should avoid \
          concatenating an instance of this class to the right of a pattern that ends in such \
          a character.
    '''

    def __init__(self, start: int = 0, end: int = 2147483647, min_decimal: int = 1,
        max_decimal: _Optional[int] = None, include_sign: bool = False, is_extensible: bool = False) \
        -> _pre.Pregex:
        '''
        Matches any decimal number within a specified range.

        :param int start: The starting value of the integer part range. \
            Defaults to ``0``.
        :param int end: The ending value of the integer part range. \
            Defaults to ``2147483647``.
        :param int min_decimal: The minimum number of digits within the decimal part. \
            Defaults to ``1``.
        :param int max_decimal: The maximum number of digits within the decimal part. \
            Defaults to ``None``.
        :param bool include_sign: Determines whether to include any existing \
            signs into the match. Defaults to ``False`.
        :param bool is_extensible: If ``True``, then no additional assertions \
            are imposed upon the underlying pattern, other than any necessary ones, \
            which in turn prevents certain complications from arising whenever it \
            serves as a building block to a larger pattern. As a general rule of thumb, \
            set this parameter to ``True`` if you wish to extend the resulting instance's \
            underlying pattern, or to ``False`` if you are only using it for matching purposes. \
            Defaults to ``False``.

        :raises InvalidArgumentTypeException: Either one of parameters ``start``, \
            ``end``, ``min_decimal`` or ``max_decimal`` is not an integer.
        :raises InvalidArgumentValueException: 
            - Parameter ``start`` has a value of less than ``0``.
            - Parameter ``start`` has a greater value than that of parameter ``end``.
            - Parameter ``min_decimal`` has a value of less than ``1``.
            - Parameter ``min_decimal`` has a greater value than that of parameter ``max_decimal``.

        :note: 
            - Be aware that parameter ``include_sign`` might not only play a role in \
              deciding the content of the matches, but their number as well. For example, \
              setting ``include_sign`` to ``False`` will result in ``Integer`` matching both \
              ``1.1`` and ``2.2`` in ``1.1+2.2``, whereas setting it to ``True`` results in \
              just matching ``1.1``. That is, because in case ``include_sign`` is ``True``, \
              ``+2.2`` is considered a decimal number as a whole, and as such, it cannot match \
              when another digit, namely ``1``, directly precedes it.
            - Even by setting parameter ``is_extensible`` to ``True``, there still persists \
              an assertion that is essential to the pattern, which dictates that this pattern \
              must not be preceded by any numeric characters. For that reason, one should avoid \
              concatenating an instance of this class to the right of a pattern that ends in such \
              a character.
        '''
        integer_part = Integer(start, end, include_sign, is_extensible)

        if start == 0:
            no_integer_part = _pre.Pregex().not_preceded_by(_cl.AnyDigit())
            if include_sign:
                no_integer_part += _qu.Optional(_op.Either("+", "-"))
        else:
            no_integer_part = None

        super().__init__(integer_part, no_integer_part, min_decimal, max_decimal, is_extensible)


class PositiveDecimal(__Decimal):
    '''
    Matches any strictly positive decimal number within a specified range.

    :param int start: The starting value of the integer part range. \
        Defaults to ``0``.
    :param int end: The ending value of the integer part range. \
        Defaults to ``2147483647``.
    :param int min_decimal: The minimum number of digits within the decimal part. \
        Defaults to ``1``.
    :param int max_decimal: The maximum number of digits within the decimal part. \
        Defaults to ``None``.
    :param bool is_extensible: If ``True``, then no additional assertions \
        are imposed upon the underlying pattern, other than any necessary ones, \
        which in turn prevents certain complications from arising whenever it \
        serves as a building block to a larger pattern. As a general rule of thumb, \
        set this parameter to ``True`` if you wish to extend the resulting instance's \
        underlying pattern, or to ``False`` if you are only using it for matching purposes. \
        Defaults to ``False``.

    :raises InvalidArgumentTypeException: Either one of parameters ``start``, \
        ``end``, ``min_decimal`` or ``max_decimal`` is not an integer.
    :raises InvalidArgumentValueException: 
        - Parameter ``start`` has a value of less than ``0``.
        - Parameter ``start`` has a greater value than that of parameter ``end``.
        - Parameter ``min_decimal`` has a value of less than ``1``.
        - Parameter ``min_decimal`` has a greater value than that of parameter ``max_decimal``.

    :note: Even by setting parameter ``is_extensible`` to ``True``, there still persists \
        an assertion that is essential to the pattern, which dictates that this pattern \
        must not be preceded by any numeric characters. For that reason, one should avoid \
        concatenating an instance of this class to the right of a pattern that ends in such \
        a character.
    '''

    def __init__(self, start: int = 0, end: int = 2147483647, min_decimal: int = 1,
        max_decimal: _Optional[int] = None, is_extensible: bool = False) -> _pre.Pregex:
        '''
        Matches any positive decimal number within a specified range.

        :param int start: The starting value of the integer part range. \
            Defaults to ``0``.
        :param int end: The ending value of the integer part range. \
            Defaults to ``2147483647``.
        :param int min_decimal: The minimum number of digits within the decimal part. \
            Defaults to ``1``.
        :param int max_decimal: The maximum number of digits within the decimal part. \
            Defaults to ``None``.
        :param bool is_extensible: If ``True``, then no additional assertions \
            are imposed upon the underlying pattern, other than any necessary ones, \
            which in turn prevents certain complications from arising whenever it \
            serves as a building block to a larger pattern. As a general rule of thumb, \
            set this parameter to ``True`` if you wish to extend the resulting instance's \
            underlying pattern, or to ``False`` if you are only using it for matching purposes. \
            Defaults to ``False``.

        :raises InvalidArgumentTypeException: Either one of parameters ``start``, \
            ``end``, ``min_decimal`` or ``max_decimal`` is not an integer.
        :raises InvalidArgumentValueException: 
            - Parameter ``start`` has a value of less than ``0``.
            - Parameter ``start`` has a greater value than that of parameter ``end``.
            - Parameter ``min_decimal`` has a value of less than ``1``.
            - Parameter ``min_decimal`` has a greater value than that of parameter ``max_decimal``.

        :note: Even by setting parameter ``is_extensible`` to ``True``, there still persists \
            an assertion that is essential to the pattern, which dictates that this pattern \
            must not be preceded by any numeric characters. For that reason, one should avoid \
            concatenating an instance of this class to the right of a pattern that ends in such \
            a character.
        '''
        integer_part = PositiveInteger(start, end, is_extensible)
        if start == 0:
            if is_extensible:
                no_integer_part = _pre.Pregex().not_preceded_by(_cl.AnyDigit())
            else:
                no_integer_part = _asr.NonWordBoundary()
            no_integer_part += _qu.Optional("+")
        else:
            no_integer_part = None
        super().__init__(integer_part, no_integer_part, min_decimal, max_decimal, is_extensible)


class NegativeDecimal(__Decimal):
    '''
    Matches any negative decimal number within a specified range.

    :param int start: The starting value of the integer part range. \
        Defaults to ``0``.
    :param int end: The ending value of the integer part range. \
        Defaults to ``2147483647``.
    :param int min_decimal: The minimum number of digits within the decimal part. \
        Defaults to ``1``.
    :param int max_decimal: The maximum number of digits within the decimal part. \
        Defaults to ``None``.
    :param bool is_extensible: If ``True``, then no additional assertions \
        are imposed upon the underlying pattern, other than any necessary ones, \
        which in turn prevents certain complications from arising whenever it \
        serves as a building block to a larger pattern. As a general rule of thumb, \
        set this parameter to ``True`` if you wish to extend the resulting instance's \
        underlying pattern, or to ``False`` if you are only using it for matching purposes. \
        Defaults to ``False``.

    :raises InvalidArgumentTypeException: Either one of parameters ``start``, \
        ``end``, ``min_decimal`` or ``max_decimal`` is not an integer.
    :raises InvalidArgumentValueException: 
        - Parameter ``start`` has a value of less than ``0``.
        - Parameter ``start`` has a greater value than that of parameter ``end``.
        - Parameter ``min_decimal`` has a value of less than ``1``.
        - Parameter ``min_decimal`` has a greater value than that of parameter ``max_decimal``.

    :note: Even by setting parameter ``is_extensible`` to ``True``, there still persists \
        an assertion that is essential to the pattern, which dictates that this pattern \
        must not be preceded by any numeric characters. For that reason, one should avoid \
        concatenating an instance of this class to the right of a pattern that ends in such \
        a character.
    '''

    def __init__(self, start: int = 0, end: int = 2147483647, min_decimal: int = 1,
        max_decimal: _Optional[int] = None, is_extensible: bool = False) -> _pre.Pregex:
        '''
        Matches any negative decimal number within a specified range.

        :param int start: The starting value of the integer part range. \
            Defaults to ``0``.
        :param int end: The ending value of the integer part range. \
            Defaults to ``2147483647``.
        :param int min_decimal: The minimum number of digits within the decimal part. \
            Defaults to ``1``.
        :param int max_decimal: The maximum number of digits within the decimal part. \
            Defaults to ``None``.
        :param bool is_extensible: If ``True``, then no additional assertions \
            are imposed upon the underlying pattern, other than any necessary ones, \
            which in turn prevents certain complications from arising whenever it \
            serves as a building block to a larger pattern. As a general rule of thumb, \
            set this parameter to ``True`` if you wish to extend the resulting instance's \
            underlying pattern, or to ``False`` if you are only using it for matching purposes. \
            Defaults to ``False``.

        :raises InvalidArgumentTypeException: Either one of parameters ``start``, \
            ``end``, ``min_decimal`` or ``max_decimal`` is not an integer.
        :raises InvalidArgumentValueException: 
            - Parameter ``start`` has a value of less than ``0``.
            - Parameter ``start`` has a greater value than that of parameter ``end``.
            - Parameter ``min_decimal`` has a value of less than ``1``.
            - Parameter ``min_decimal`` has a greater value than that of parameter ``max_decimal``.

        :note: Even by setting parameter ``is_extensible`` to ``True``, there still persists \
            an assertion that is essential to the pattern, which dictates that this pattern \
            must not be preceded by any numeric characters. For that reason, one should avoid \
            concatenating an instance of this class to the right of a pattern that ends in such \
            a character.
        '''
        integer_part = NegativeInteger(start, end, is_extensible)
        if start == 0:
            if is_extensible:
                no_integer_part = _pre.Pregex().not_preceded_by(_cl.AnyDigit())
            else:
                no_integer_part = _asr.NonWordBoundary()
            no_integer_part += '-'
        else:
            no_integer_part = None
        super().__init__(integer_part, no_integer_part, min_decimal, max_decimal, is_extensible)


class UnsignedDecimal(__Decimal):
    '''
    Matches any decimal number within a specified range, \
    provided that it is not preceded by a sign.

    :param int start: The starting value of the integer part range. \
        Defaults to ``0``.
    :param int end: The ending value of the integer part range. \
        Defaults to ``2147483647``.
    :param int min_decimal: The minimum number of decimal places. \
        Defaults to ``1``.
    :param int max_decimal: The maximum number of decimal places. \
        Defaults to ``None``.
    :param bool is_extensible: If ``True``, then no additional assertions \
        are imposed upon the underlying pattern, other than any necessary ones, \
        which in turn prevents certain complications from arising whenever it \
        serves as a building block to a larger pattern. As a general rule of thumb, \
        set this parameter to ``True`` if you wish to extend the resulting instance's \
        underlying pattern, or to ``False`` if you are only using it for matching purposes. \
        Defaults to ``False``.

    :raises InvalidArgumentTypeException: Either one of parameters ``start``, \
        ``end``, ``min_decimal`` or ``max_decimal`` is not an integer.
    :raises InvalidArgumentValueException: 
        - Parameter ``start`` has a value of less than ``0``.
        - Parameter ``start`` has a greater value than that of parameter ``end``.
        - Parameter ``min_decimal`` has a value of less than ``1``.
        - Parameter ``min_decimal`` has a greater value than that of parameter ``max_decimal``.

    :note: Even by setting parameter ``is_extensible`` to ``True``, there still persists \
        an assertion that is essential to the pattern, which dictates that this pattern \
        must not be preceded by any numeric characters. For that reason, one should avoid \
        concatenating an instance of this class to the right of a pattern that ends in such \
        a character.
    '''

    def __init__(self, start: int = 0, end: int = 2147483647, min_decimal: int = 1,
        max_decimal: _Optional[int] = None, is_extensible: bool = False) -> _pre.Pregex:
        '''
        Matches any decimal number within a specified range, \
        provided that it is not preceded by a sign.

        :param int start: The starting value of the integer part range. \
            Defaults to ``0``.
        :param int end: The ending value of the integer part range. \
            Defaults to ``2147483647``.
        :param int min_decimal: The minimum number of decimal places. \
            Defaults to ``1``.
        :param int max_decimal: The maximum number of decimal places. \
            Defaults to ``None``.
        :param bool is_extensible: If ``True``, then no additional assertions \
            are imposed upon the underlying pattern, other than any necessary ones, \
            which in turn prevents certain complications from arising whenever it \
            serves as a building block to a larger pattern. As a general rule of thumb, \
            set this parameter to ``True`` if you wish to extend the resulting instance's \
            underlying pattern, or to ``False`` if you are only using it for matching purposes. \
            Defaults to ``False``.

        :raises InvalidArgumentTypeException: Either one of parameters ``start``, \
            ``end``, ``min_decimal`` or ``max_decimal`` is not an integer.
        :raises InvalidArgumentValueException: 
            - Parameter ``start`` has a value of less than ``0``.
            - Parameter ``start`` has a greater value than that of parameter ``end``.
            - Parameter ``min_decimal`` has a value of less than ``1``.
            - Parameter ``min_decimal`` has a greater value than that of parameter ``max_decimal``.

        :note: Even by setting parameter ``is_extensible`` to ``True``, there still persists \
            an assertion that is essential to the pattern, which dictates that this pattern \
            must not be preceded by any numeric characters. For that reason, one should avoid \
            concatenating an instance of this class to the right of a pattern that ends in such \
            a character.
        '''
        integer_part = UnsignedInteger(start, end, is_extensible)
        if start == 0:
            if is_extensible:
                no_integer_part = _pre.Pregex().not_preceded_by(
                    _op.Either('+', '-', _cl.AnyDigit()))
            else:
                no_integer_part = _asr.NonWordBoundary().not_preceded_by(_op.Either('+', '-'))
        else:
            no_integer_part = None
        super().__init__(integer_part, no_integer_part, min_decimal, max_decimal, is_extensible)


class Date(_pre.Pregex):
    '''
    Matches any date within a range of predefined formats.

    :param str | list[str] formats: Either a string or a list of strings \
        through which it is determined what are the exact date formats that \
        are to be considered possible matches. A valid date format can be \
        either one of:

        - ``D<sep>M<sep>Y``
        - ``M<sep>D<sep>Y``
        - ``Y<sep>M<sep>D``

        where:

        - ``<sep>``: Either ``/`` or ``-``
        - ``D``: Either one of the following:

            - ``d``: one-digit day of the month for days below 10, e.g. 2
            - ``dd``: two-digit day of the month, e.g. 02

        - ``M``: Either one of the following:

            - ``m``: one-digit month for months below 10, e.g. 3
            - ``mm``: two-digit month, e.g. 03

        - ``Y``: Either one of the following:

            - ``yy``: two-digit year, e.g. 21
            - ``yyyy``: four-digit year, e.g. 2021

        For example, ``dd/mm/yyyy`` is considered a valid date format whereas \
        ``mm/yyyy/dd`` is not. Lastly, If ``None`` is provided in place of this \
        list, then all possible formats are considered. Defaults to ``None``.
    :param bool is_extensible: If ``True``, then no additional assertions \
        are imposed upon the underlying pattern, other than any necessary ones, \
        which in turn prevents certain complications from arising whenever it \
        serves as a building block to a larger pattern. As a general rule of thumb, \
        set this parameter to ``True`` if you wish to extend the resulting instance's \
        underlying pattern, or to ``False`` if you are only using it for matching purposes. \
        Defaults to ``False``.

    :raises InvalidArgumentValueException: At least one of the provided arguments \
        is not a valid date format.
    '''

    __date_separators: tuple[str, str] = ("-", "/")

    def __init__(self, formats: _Optional[_Union[str, list[str]]] = None, is_extensible: bool = False) -> _pre.Pregex:
        '''
        Matches any date within a range of predefined formats.

        :param str | list[str] formats: Either a string or a list of strings \
            through which it is determined what are the exact date formats that \
            are to be considered possible matches. A valid date format can be \
            either one of:

            - ``D<sep>M<sep>Y``
            - ``M<sep>D<sep>Y``
            - ``Y<sep>M<sep>D``

            where:

            - ``<sep>``: Either ``/`` or ``-``
            - ``D``: Either one of the following:

                - ``d``: one-digit day of the month for days below 10, e.g. 2
                - ``dd``: two-digit day of the month, e.g. 02

            - ``M``: Either one of the following:

                - ``m``: one-digit month for months below 10, e.g. 3
                - ``mm``: two-digit month, e.g. 03

            - ``Y``: Either one of the following:

                - ``yy``: two-digit year, e.g. 21
                - ``yyyy``: four-digit year, e.g. 2021

            For example, ``dd/mm/yyyy`` is considered a valid date format whereas \
            ``mm/yyyy/dd`` is not. Lastly, If ``None`` is provided in place of this \
            list, then all possible formats are considered. Defaults to ``None``.
        :param bool is_extensible: If ``True``, then no additional assertions \
            are imposed upon the underlying pattern, other than any necessary ones, \
            which in turn prevents certain complications from arising whenever it \
            serves as a building block to a larger pattern. As a general rule of thumb, \
            set this parameter to ``True`` if you wish to extend the resulting instance's \
            underlying pattern, or to ``False`` if you are only using it for matching purposes. \
            Defaults to ``False``.

        :raises InvalidArgumentValueException: At least one of the provided arguments \
            is not a valid date format.
        '''
        date_formats = __class__.__date_formats()
        formats = date_formats if formats is None else formats

        if isinstance(formats, str):
            formats = [formats]
        
        dates: list[_pre.Pregex] = []
        for format in formats:
            if format not in date_formats:
                message = f"Provided date format \"{format}\" is not valid."
                raise _ex.InvalidArgumentValueException(message)
            dates.append(__class__.__date_pre(format))

        pre = _op.Either(*dates)

        if not is_extensible:
            pre = pre.enclose(_asr.WordBoundary())

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

        any_digit_but_zero = _cl.AnyDigit() - '0'
        either_zero_or_one = _op.Either('0', '1')
        either_one_or_two = _op.Either('1', '2')

        date_to_pre: dict[str, _pre.Pregex] = {
            'd': any_digit_but_zero, 
            'dd': _op.Either(
                '0' + any_digit_but_zero,
                either_one_or_two.either('3') + \
                _op.Either(
                    _cl.AnyDigit().preceded_by(either_one_or_two),
                    either_zero_or_one.preceded_by('3')
            )),
            'm': any_digit_but_zero,
            'mm': _op.Either(
                '0' + any_digit_but_zero,
                '1' + either_zero_or_one.either('2')),
            'yy': _cl.AnyDigit() * 2, 
            'yyyy': _cl.AnyDigit() * 4, 
        }

        pre = _pre.Pregex()
        for i, value in enumerate(values):
            pre += date_to_pre[value]
            if i < len(values) - 1:
                pre += separator
                
        return pre


    @staticmethod
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

    :param bool is_extensible: If ``True``, then no additional assertions \
        are imposed upon the underlying pattern, other than any necessary ones, \
        which in turn prevents certain complications from arising whenever it \
        serves as a building block to a larger pattern. As a general rule of thumb, \
        set this parameter to ``True`` if you wish to extend the resulting instance's \
        underlying pattern, or to ``False`` if you are only using it for matching purposes. \
        Defaults to ``False``.
    '''

    def __init__(self, is_extensible: bool = False) -> _pre.Pregex:
        '''
        Matches any IPv4 Address.

        :param bool is_extensible: If ``True``, then no additional assertions \
            are imposed upon the underlying pattern, other than any necessary ones, \
            which in turn prevents certain complications from arising whenever it \
            serves as a building block to a larger pattern. As a general rule of thumb, \
            set this parameter to ``True`` if you wish to extend the resulting instance's \
            underlying pattern, or to ``False`` if you are only using it for matching purposes. \
            Defaults to ``False``.
        '''

        any_digit_but_zero = _cl.AnyDigit() - '0'
        any_digit_up_to_four = _cl.AnyBetween('0', '4')

        ip_octet = _op.Either(
            _cl.AnyDigit(),
            any_digit_but_zero + _cl.AnyDigit(),
            '1' + 2 * _cl.AnyDigit(),
            '2' + _op.Either(
                any_digit_up_to_four + _cl.AnyDigit(),
                '5' + (any_digit_up_to_four | '5')
            )
        )

        pre = 3 * (ip_octet + ".") + ip_octet

        if not is_extensible:
            pre = pre.not_enclosed_by(_op.Either(_cl.AnyDigit(), "."))

        super().__init__(str(pre), escape=False)


class IPv6(_pre.Pregex):
    '''
    Matches any IPv6 Address.

    :param bool is_extensible: If ``True``, then no additional assertions \
        are imposed upon the underlying pattern, other than any necessary ones, \
        which in turn prevents certain complications from arising whenever it \
        serves as a building block to a larger pattern. As a general rule of thumb, \
        set this parameter to ``True`` if you wish to extend the resulting instance's \
        underlying pattern, or to ``False`` if you are only using it for matching purposes. \
        Defaults to ``False``.
    '''

    def __init__(self, is_extensible: bool = False) -> _pre.Pregex:
        '''
        Matches any IPv6 Address.

        :param bool is_extensible: If ``True``, then no additional assertions \
            are imposed upon the underlying pattern, other than any necessary ones, \
            which in turn prevents certain complications from arising whenever it \
            serves as a building block to a larger pattern. As a general rule of thumb, \
            set this parameter to ``True`` if you wish to extend the resulting instance's \
            underlying pattern, or to ``False`` if you are only using it for matching purposes. \
            Defaults to ``False``.
        '''
        hex_group = Numeral(base=16, n_min=1, n_max=4, is_extensible=is_extensible)

        pre = 7 * (hex_group + ":") + hex_group

        empty = _pre.Pregex()

        for i in range(9):
            pre = _op.Either(
                pre,
                (_qu.AtLeastAtMost(hex_group + ":", n=0, m=i-1) if i > 1 else empty) + \
                (hex_group if i > 0 else empty) + \
                "::" + \
                (_qu.AtLeastAtMost(hex_group + ":", n=0, m=7-i) if i < 7 else empty)+ \
                (hex_group if i < 8 else empty)
            )

        pre = _op.Either(pre, "::")

        if not is_extensible:
            pre = pre.not_enclosed_by(_op.Either(_cl.AnyDigit(), ":"))

        super().__init__(str(pre), escape=False)


class Email(_pre.Pregex):
    '''
    Matches any email address.

    :param bool capture_local_part: If set to ``True``, then the local-part \
        of each email address match is separately captured as well. Defaults \
        to ``False``.
    :param bool capture_domain: If set to ``True``, then the domain name \
        of each email address match is separately captured as well. \
        Defaults to ``False``.
    :param bool is_extensible: If ``True``, then no additional assertions \
        are imposed upon the underlying pattern, other than any necessary ones, \
        which in turn prevents certain complications from arising whenever it \
        serves as a building block to a larger pattern. As a general rule of thumb, \
        set this parameter to ``True`` if you wish to extend the resulting instance's \
        underlying pattern, or to ``False`` if you are only using it for matching purposes. \
        Defaults to ``False``.

    :note: Not guaranteed to match every possible email address.
    '''

    def __init__(self, capture_local_part: bool = False,
        capture_domain: bool = False, is_extensible: bool = False) -> _pre.Pregex:
        '''
        Matches any email address.

        :param bool capture_local_part: If set to ``True``, then the local-part \
            of each Email address match is separately captured as well. Defaults \
            to ``False``.
        :param bool capture_domain: If set to ``True``, then the domain name \
            of each Email address match is separately captured as well. \
            Defaults to ``False``.
        :param bool is_extensible: If ``True``, then no additional assertions \
            are imposed upon the underlying pattern, other than any necessary ones, \
            which in turn prevents certain complications from arising whenever it \
            serves as a building block to a larger pattern. As a general rule of thumb, \
            set this parameter to ``True`` if you wish to extend the resulting instance's \
            underlying pattern, or to ``False`` if you are only using it for matching purposes. \
            Defaults to ``False``.

        :note: Not guaranteed to match every possible e-mail address.
        '''
        potential_word_boundary = _pre.Pregex() if is_extensible else _asr.WordBoundary()
        potential_non_word_boundary = _pre.Pregex() if is_extensible else _asr.NonWordBoundary()

        special = _cl.AnyFrom('!', '#', '$', '%', "'", '*', '+',
            '-', '/', '=', '?', '^', '_', '`', '{', '|', '}', '~')

        alphanum = _cl.AnyLetter() | _cl.AnyDigit()

        local_part_valid_char = alphanum | special

        left_most = _op.Either(
            potential_non_word_boundary.followed_by(special),
            potential_word_boundary.followed_by(alphanum)
        ) 

        local_part = \
            (local_part_valid_char - '-') + \
            _qu.AtMost(
                _op.Either(local_part_valid_char, _asr.NotFollowedBy('.', '.')),
                n=62
            ) + \
            (local_part_valid_char - '-')

        if capture_local_part:
            local_part = _gr.Capture(local_part)

        domain_name = \
            alphanum + \
            _qu.AtMost(alphanum | "-", n=61) + \
            alphanum

        if capture_domain:
            domain_name = _gr.Capture(domain_name)

        tld = "." + _qu.AtLeastAtMost(_cl.AnyLowercaseLetter(), n=2, m=6)

        pre = left_most + local_part + "@" + domain_name + tld + potential_word_boundary
        super().__init__(str(pre), escape=False)


class HttpUrl(_pre.Pregex):
    '''
    Matches any HTTP URL.

    :param bool capture_domain: If set to ``True``, then the domain name \
        of each URL match is separately captured as well. Defaults to ``False``.
    :param bool is_extensible: If ``True``, then no additional assertions \
        are imposed upon the underlying pattern, other than any necessary ones, \
        which in turn prevents certain complications from arising whenever it \
        serves as a building block to a larger pattern. As a general rule of thumb, \
        set this parameter to ``True`` if you wish to extend the resulting instance's \
        underlying pattern, or to ``False`` if you are only using it for matching purposes. \
        Defaults to ``False``.

    :note: Not guaranteed to match every possible HTTP URL.
    '''

    def __init__(self, capture_domain: bool = False, is_extensible: bool = False) -> _pre.Pregex:
        '''
        Matches any HTTP URL.

        :param bool capture_domain: If set to ``True``, then the domain name \
            of each URL match is separately captured as well. Defaults to ``False``.
        :param bool is_extensible: If ``True``, then no additional assertions \
            are imposed upon the underlying pattern, other than any necessary ones, \
            which in turn prevents certain complications from arising whenever it \
            serves as a building block to a larger pattern. As a general rule of thumb, \
            set this parameter to ``True`` if you wish to extend the resulting instance's \
            underlying pattern, or to ``False`` if you are only using it for matching purposes. \
            Defaults to ``False``.

        :note: Not guaranteed to match every possible HTTP URL.
        '''

        potential_word_boundary = _pre.Pregex() if is_extensible else _asr.WordBoundary()
        potential_non_word_boundary = _pre.Pregex() if is_extensible else _asr.NonWordBoundary()

        left_most = potential_word_boundary

        http_protocol = _qu.Optional("http" + _qu.Optional('s') + "://")

        www = _qu.Optional("www.")

        alphanum = _cl.AnyLetter() | _cl.AnyDigit()

        domain_name = \
            alphanum + \
            _qu.AtMost(alphanum | "-", n=61) + \
            alphanum

        subdomains = _qu.Indefinite(domain_name + ".")

        tld = "." + _cl.AnyLowercaseLetter().at_least_at_most(n=2, m=6)

        optional_port = _qu.Optional(":" + _cl.AnyDigit().at_least_at_most(n=1, m=4))

        directories = _qu.Indefinite(
            "/" + \
             _qu.OneOrMore(_cl.AnyWordChar(is_global=True) | (_cl.AnyPunctuation() - "/"))
        ) + _qu.Optional("/")

        right_most = _op.Either(
            potential_non_word_boundary.preceded_by(_cl.AnyPunctuation()),
            potential_word_boundary.preceded_by(_cl.AnyWordChar(is_global=True))
        )

        if capture_domain:
            domain_name = _gr.Capture(domain_name)

        pre = left_most + http_protocol + www + subdomains + \
            domain_name + tld + optional_port + directories + right_most
        super().__init__(str(pre), escape=False)

