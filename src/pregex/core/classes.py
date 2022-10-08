__doc__ = """
All classes within this module represent the so-called RegΕx *character classes*,
which can be used in order to define a set or "class" of characters that can be matched.

Class types
-------------------------------------------
A character class can be either one of the following two types:

	1. **Regular class**: This type of class represents the `[...]` pattern, 
	   which can be translated as "match every character defined within the
	   brackets". You can tell regular classes by their name, which follows
	   the `Any*` pattern.


	2. **Negated class**: This type of class represents the `[^...]` pattern, 
	   which can be translated as "match every character except for those 
	   defined within the brackets". You can tell negated classes by their name, 
	   which follows the `AnyBut*` pattern.

Here is an example containing a regular class as well as its negated counterpart.

.. code-block:: python
   
   from pregex.core.classes import AnyLetter, AnyButLetter

   regular = AnyLetter()
   negated = AnyButLetter()

   regular.print_pattern() # This prints "[A-Za-z]"
   negated.print_pattern() # This prints "[^A-Za-z]"

Class unions
-------------------------------------------
Classes of the same type can be combined together in order to get the union of
the sets of characters they represent. This can be easily done though the use 
of the bitwise OR operator ``|``, as depicted within the code snippet below:

.. code-block:: python
   
   from pregex.core.classes import AnyDigit, AnyLowercaseLetter

   pre = AnyDigit() | AnyLowercaseLetter()
   pre.print_pattern() # This prints "[\da-z]"

The same goes for negated classes as well:

.. code-block:: python

   from pregex.core.classes import AnyButDigit, AnyButLowercaseLetter

   pre = AnyButDigit() | AnyButLowercaseLetter()
   pre.print_pattern() # This prints "[^\da-z]"

However, attempting to get the union of a regular class and a negated class
causes a ``CannotBeUnionedException`` to be thrown.

.. code-block:: python

   from pregex.core.classes import AnyDigit, AnyButLowercaseLetter

   pre = AnyDigit() | AnyButLowercaseLetter() # This is not OK!

Lastly, it is also possible to union a regular class with a token, that is,
any string of length one or any instance of a class that is part of the
:py:mod:`pregex.core.tokens` module:

.. code-block:: python

   from pregex.core.classes import AnyDigit
   from pregex.core.tokens import Newline

   pre = AnyDigit() | "a" | Newline()
   
   pre.print_pattern() # This prints "[\da\\n]"

However, in the case of negated classes one is forced to wrap any tokens
within an :class:`AnyButFrom` class instance in order to achieve the same
result:

.. code-block:: python

   from pregex.core.classes import AnyButDigit
   from pregex.core.tokens import Newline

   pre = AnyButDigit() | AnyButFrom("a", Newline())
   
   pre.print_pattern() # This prints "[^\da\\n]"

Subtracting classes
-------------------------------------------
Subtraction is another operation that is exclusive to classes and it is made possible
via the overloaded subtraction operator ``-``. This feature comes in handy when one
wishes to construct a class that would be tiresome to create otherwise. Consider
for example the class of all word characters except for all characters in the
set `{C, c, G, g, 3}`. Constructing said class via subtraction
is extremely easy:

.. code-block:: python

   from pregex.core.classes import AnyWordChar, AnyFrom

   pre = AnyWordChar() - AnyFrom('C', 'c', 'G', 'g', '3')

Below we are able to see this operation's resulting pattern, from which it
becomes evident that building said pattern through multiple class unions would
be more time consuming, and more importantly, prone to errors.

.. code-block:: python

	[A-BD-FH-Za-bd-fh-z0-24-9_]

It should be noted that just like in the case of class unions, one is only 
allowed to subtract a regular class from a regular class or a negated class
from a negated class, as any other attempt will cause a 
``CannotBeSubtractedException`` to be thrown.

.. code-block:: python

   from pregex.core.classes import AnyWordChar, AnyButLowercaseLetter

   pre = AnyWordChar() - AnyButLowercaseLetter() # This is not OK!

Furthermore, applying the subtraction operation between a class and a token
is also possible, but just like in the case of class unions, this only works
with regular classes:

.. code-block:: python

   from pregex.core.classes import AnyWhitespace
   from pregex.core.tokens import Newline

   pre = AnyWhitespace() - Newline()
   
   pre.print_pattern() # This prints "[\\t \\x0b-\\r]"

Negating classes
-------------------------------------------
Finally, it is useful to know that every regular class can be negated through
the use of the bitwise NOT operator ``~``:

.. code-block:: python

   from pregex.core.classes import AnyDigit

   pre = ~ AnyDigit()
   pre.print_pattern() # This prints "[^0-9]"

Negated classes can be negated as well, however you should probably avoid
this as it doesn't help much in making the code any easier to read.

.. code-block:: python

   from pregex.core.classes import AnyButDigit

   pre = ~ AnyButDigit()
   pre.print_pattern() # This prints "[0-9]"

Therefore, in order to create a negated class one can either negate a regular `Any*`
class or use its `AnyBut*` negated class equivalent. The result is entirely the same
and which one you'll use is just a matter of choice.

Classes & methods
-------------------------------------------

Below are listed all classes within :py:mod:`pregex.core.classes`
along with any possible methods they may possess.
"""


import re as _re
import pregex.core.pre as _pre
import pregex.core.exceptions as _ex
from string import whitespace as _whitespace


class __Class(_pre.Pregex):
    '''
    Constitutes the base class for every class within "classes.py".

    Operations defined for classes:
        - Union:
            AnyLowercaseLetter() | AnyDigit() => [a-z0-9]
        - Subtraction:
            AnyLetter() - AnyLowercaseLetter() => [A-Z]
        - Negation:
            ~ AnyLowercaseLetter() => [^a-z]

    :param str pattern: The RegEx class pattern.
    :param bool is_negated: Indicates whether this class instance represents \
        a regular or a negated class.
    :param bool simplify_word: In case class instance represents the `word` \
        character class, this parameter indicates whether this character class \
        should be simplified to `\\w` or not.

    :note: Union and subtraction can only be performed on a pair of classes of the same type, \
        that is, either a pair of regular classes or a pair of negated classes.
    '''


    '''
    A set containing characters that must be escaped when used within a class.
    '''
    _to_escape = ('\\', '^', '[', ']', '-', '/')


    def __init__(self, pattern: str, is_negated: bool, simplify_word: bool = False) -> '__Class':
        '''
        Constitutes the base class for every class within "classes.py".

        Operations defined for classes:
            - Union:
                AnyLowercaseLetter() | AnyDigit() => [a-z0-9]
            - Subtraction:
                AnyLetter() - AnyLowercaseLetter() => [A-Z]
            - Negation:
                ~ AnyLowercaseLetter() => [^a-z]

        :param str pattern: The RegEx class pattern.
        :param bool is_negated: Indicates whether this class instance represents \
            a regular or a negated class.
        :param bool simplify_word: In case class instance represents the `word` \
            character class, this parameter indicates whether this character class \
            should be simplified to `\\w` or not.

        :note: Union and subtraction can only be performed on a pair of classes of the same type, \
            that is, either a pair of regular classes or a pair of negated classes.
        '''
        self.__is_negated = is_negated
        self.__verbose, pattern = __class__.__process(pattern, is_negated, simplify_word)
        super().__init__(pattern, escape=False)


    def _get_verbose_pattern(self) -> str:
        '''
        Returns a verbose representation of this class's pattern.
        '''
        return self.__verbose


    @staticmethod
    def __process(pattern: str, is_negated: bool, simplify_word: bool) -> tuple[str, str]:
        '''
        Performs some modifications to the provided pattern and returns \
        it in both a verbose and a simplified form.

        :param str pattern: The pattern that is to be processed.
        :param bool is_negated: Determines whether the patterns \
            belongs to a negated class or a regular one.
        :param bool simplify_word: Indicates whether `[A-Za-z0-9_]` \
            should be simplified to `[\w]` or not.
        '''
        if pattern == '.':
            return pattern, pattern
        # Separate ranges from chars.
        ranges, chars = __class__.__extract_classes(pattern)
        # Reduce chars to any possible ranges.
        ranges, chars = __class__.__chars_to_ranges(ranges, chars)
        # Combine classes back together.
        verbose_classes = ranges.union(chars)
        verbose_pattern = ''.join(f"[{'^' if is_negated else ''}{''.join(verbose_classes)}]")
        # Use shorthand notation for any classes that support this.
        simplified_classes = __class__.__verbose_to_shorthand(verbose_classes, simplify_word)
        simplified_pattern = ''.join(f"[{'^' if is_negated else ''}{''.join(simplified_classes)}]")
        # Replace any one-character classes with a single (possibly escaped) character
        simplified_pattern = _re.sub(r"\[([^\\]|\\.)\]", lambda m: str(__class__._to_pregex(m.group(1))) \
            if len(m.group(1)) == 1 else m.group(1), simplified_pattern)
        # Replace negated class shorthand-notation characters with their non-class shorthand-notation.
        return verbose_pattern, _re.sub(r"\[\^(\\w|\\d|\\s)\]", lambda m: m.group(1).upper(), simplified_pattern)


    @staticmethod    
    def __chars_to_ranges(ranges: set[str], chars: set[str]) -> tuple[set[str], set[str]]:
        '''
        Checks whether the provided characters can be incorporated within ranges.
        Returns the newly constructed ranges and characters as sets.

        :param set[str] ranges: A set containing all ranges.
        :param set[str] chars: A set containing all characters.
        '''
        # 1. Un-escape any escaped characters and convert to list.
        chars: list[str] = list(__class__.__modify_classes(chars, escape=False))
        ranges: list[list[str]] = list(__class__.__split_range(rng) for rng in 
            __class__.__modify_classes(ranges, escape=False))

        # 2. Check whether ranges can be constructed from chars.
        i = 0
        while i < len(chars):
            for j in range(len(chars)):
                if i != j and len(chars[j]) == 1:
                    c_i, c_j = chars[i], chars[j]
                    if len(chars[i]) > 1:
                        start, end = c_i[0], c_i[-1]
                    else:
                        start, end = c_i, c_i
                    if ord(start) == ord(c_j) + 1:
                        chars[i] = c_j + end
                        chars.pop(j)
                        i = -1
                        break
                    elif ord(end) == ord(c_j) - 1:
                        chars[i] = start + c_j
                        chars.pop(j)
                        i = -1
                        break
            i += 1

        # Check whether these character-ranges can be incorporated into
        # any existing ranges. If two characters are next to each other
        # then keep them as characters.
        ranges_set = set(f"{rng[0]}-{rng[1]}" for rng in ranges)
        chars_set = set()
        for c in chars:
            if len(c) == 1:
                chars_set.add(c)
            else:
                if ord(c[1]) == ord(c[0]) + 1:
                    chars_set.add(c[0])
                    chars_set.add(c[1])
                else:
                    ranges_set.add(f"{c[0]}-{c[1]}")

        ranges = __class__.__modify_classes(ranges_set, escape=True)
        chars = __class__.__modify_classes(chars_set, escape=True)

        return ranges, chars


    @staticmethod
    def __verbose_to_shorthand(classes: set[str], simplify_word: bool) -> set[str]:
        '''
        This method searches the provided set for subsets of character classes that \
        correspond to a shorthand-notation character class, and if it finds any, it \
        replaces them with said character class, returning the resulting set at the end.

        :param set[str] classes: The set containing the classes as strings.
        :param bool simplify_word: Indicates whether `[A-Za-z0-9_]` should be simplified \
            to `[\w]` or not.
        '''
        
        word_set = {'a-z', 'A-Z', '0-9', '_'}
        digit_set = {'0-9'}
        whitespace_set = {' ', '\t-\r'}
        if classes.issuperset(word_set) and simplify_word:
            classes = classes.difference(word_set).union({'\w'})
        elif classes.issuperset(digit_set):
            classes = classes.difference(digit_set).union({'\d'})
        if classes.issuperset(whitespace_set):
            classes = classes.difference(whitespace_set).union({'\s'})
        return classes


    def __invert__(self) -> '__Class':
        '''
        If this instance is a regular class, then converts it to its negated counterpart. \
        If this instance is a negated class, then converts it to its regular counterpart.
        '''
        s, rs = '' if self.__is_negated else '^', '^' if self.__is_negated else ''
        return __class__(f"[{s}{self.__verbose.lstrip('[' + rs).rstrip(']')}]", not self.__is_negated)


    def __or__(self, pre: '__Class' or str) -> '__Class':
        '''
        Returns a `__Class` instance representing the union of the provided classes.

        :param __Class | str pre: The class that is to be unioned with this instance.

        :raises CannotBeUnionedException: `pre` is neither a `__Class` instance nor a token.
        '''
        if not self.__is_negated:
            if isinstance(pre, str) and (len(pre) == 1):
                pre = AnyFrom(pre)
            elif isinstance(pre, _pre.Pregex) and pre._get_type() == _pre._Type.Token:
                pre = AnyFrom(pre)
        if not issubclass(pre.__class__, __class__):
            raise _ex.CannotBeUnionedException(pre, False)
        return __class__.__or(self, pre)


    def __ror__(self, pre: '__Class' or str) -> '__Class':
        '''
        Returns a `__Class` instance representing the union of the provided classes.

        :param __Class | str pre: The class that is to be unioned with this instance.

        :raises CannotBeUnionedException: `pre` is neither a `__Class` instance nor a token.
        '''
        if not self.__is_negated:
            if isinstance(pre, str) and (len(pre) == 1):
                pre = AnyFrom(pre)
            elif isinstance(pre, _pre.Pregex) and pre._get_type() == _pre._Type.Token:
                pre = AnyFrom(pre)
        if not issubclass(pre.__class__, __class__):
            raise _ex.CannotBeUnionedException(pre, False)
        return __class__.__or(pre, self)


    def __or(pre1: '__Class', pre2: '__Class') -> '__Class':
        '''
        Returns a `__Class` instance representing the union of the provided classes.

        :param __Class pre: The class that is to be unioned with this instance.

        :raises CannotBeUnionedException: `pre1` is a different type of class than `pre2`.
        '''
        if  pre1.__is_negated != pre2.__is_negated:
            raise _ex.CannotBeUnionedException(pre2, True)
        if isinstance(pre1, Any) or isinstance(pre2, Any):
            return Any()

        simplify_word = False
        if isinstance(pre1, (AnyWordChar, AnyButWordChar)):
            simplify_word = simplify_word or pre1._is_global()
        if isinstance(pre2, (AnyWordChar, AnyButWordChar)):
            simplify_word = simplify_word or pre2._is_global()
            
        ranges1, chars1 = __class__.__extract_classes(pre1.__verbose, unescape=True)
        ranges2, chars2 = __class__.__extract_classes(pre2.__verbose, unescape=True)

        ranges, chars = ranges1.union(ranges2), chars1.union(chars2)

        def reduce_ranges(ranges: list[str]) -> set[str]:
            '''
            Removes any sub-ranges if they are already included within an other specified range,
            and returns the set of all remaining ranges.

            :param list[str] ranges: A list containing all specified ranges.
            '''
            if len(ranges) < 2:
                return set(ranges)
            
            ranges = [__class__.__split_range(rng) for rng in ranges]

            i = 0
            while i < len(ranges):
                start_i, end_i = ranges[i]
                j = 0
                while j < len(ranges):
                    if i != j:
                        start_j, end_j = ranges[j]
                        if start_i <= start_j and ord(end_i) + 1 >= ord(start_j):
                            ranges[i] = start_i, max(end_i, end_j)
                            ranges.pop(j)
                            i = -1
                            break
                    j += 1
                i += 1

            return set(f"{rng[0]}-{rng[1]}" for rng in ranges)

        def reduce_chars(ranges: list[str], chars: list[str]):
            '''
            Removes any characters if those are already included within an other specified range,
            and returns the set of all remaining characters.

            :param list[str] ranges: A list containing all specified ranges.
            :param list[str] chars: A list containing all specified chars.
            '''

            ranges = [__class__.__split_range(rng) for rng in ranges]

            i = 0
            while i < len(chars):
                for j in range(len(ranges)):
                    start, end = ranges[j]
                    if chars[i] >= start and chars[i] <= end:
                        chars.pop(i)
                        i = -1
                        break
                    elif ord(start) == ord(chars[i]) + 1:
                        ranges[j][0] = chars[i]
                        chars.pop(i)
                        i = -1
                        break
                    elif ord(end) == ord(chars[i]) - 1:
                        ranges[j][1] = chars[i]
                        chars.pop(i)
                        i = -1
                        break
                i += 1

            return set(f"{rng[0]}-{rng[1]}" for rng in ranges), set(chars)        

        ranges = reduce_ranges(ranges)

        ranges, chars = reduce_chars(list(ranges), list(chars))

        result =  __class__.__modify_classes(ranges.union(chars), escape=True)

        return  __class__(
            f"[{'^' if pre1.__is_negated else ''}{''.join(result)}]",
            pre1.__is_negated, simplify_word)


    def __sub__(self, pre: '__Class' or str) -> '__Class':
        '''
        Returns a `__Class` instance representing the difference of the provided classes.

        :param __Class | str pre: The class that is to be subtracted from this instance.

        :raises CannotBeSubtractedException: `pre` is neither a `__Class` instance nor a token.
        '''
        if not self.__is_negated:
            if isinstance(pre, str) and (len(pre) == 1):
                pre = AnyFrom(pre)
            elif isinstance(pre, _pre.Pregex) and pre._get_type() == _pre._Type.Token:
                pre = AnyFrom(pre)
        if not issubclass(pre.__class__, __class__):
            raise _ex.CannotBeSubtractedException(pre, False)
        return __class__.__sub(self, pre)


    def __rsub__(self, pre: '__Class' or str) -> '__Class':
        '''
        Returns a `__Class` instance representing the difference of the provided classes.

        :param __Class | str pre: The class that is to be subtracted from this instance.

        :raises CannotBeSubtractedException: `pre` is neither a `__Class` instance nor a token.
        '''
        if not self.__is_negated:
            if isinstance(pre, str) and (len(pre) == 1):
                pre = AnyFrom(pre)
            elif isinstance(pre, _pre.Pregex) and pre._get_type() == _pre._Type.Token:
                pre = AnyFrom(pre)
        if not issubclass(pre.__class__, __class__):
            raise _ex.CannotBeSubtractedException(pre, False)
        return __class__.__sub(pre, self)


    def __sub(pre1: '__Class', pre2: '__Class') -> '__Class':
        '''
        Returns a `__Class` instance representing the difference of the provided classes.

        :param __Class  pre: The class that is to be subtracted from this instance.

        :raises CannotBeSubtractedException: `pre` is neither a `__Class` instance nor a token.
        :raises EmptyClassException: `pre2` is an instance of class "Any".
        '''
        if  pre1.__is_negated != pre2.__is_negated:
            raise _ex.CannotBeSubtractedException(pre2, True)
        if isinstance(pre2, Any):
            raise _ex.EmptyClassException(pre1, pre2)
        if isinstance(pre1, Any):
            return ~ pre2
        if isinstance(pre1, (AnyWordChar, AnyButWordChar)) and pre1._is_global():
            raise _ex.GlobalWordCharSubtractionException(pre1)

        # Subtract any ranges found in both pre2 and pre1 from pre1.
        def subtract_ranges(ranges1: set[str], ranges2: set[str]) -> tuple[set[str], set[str]]:
            '''
            Subtracts any range found within `ranges2` from `ranges1` and returns \
            the resulting ranges/characters in two seperate sets.

            :note: This method might also produce characters, for example \
                [A-Z] - [B-Z] produces the character 'A'.
            '''
            ranges1 = [__class__.__split_range(rng) for rng in ranges1]
            ranges2 = [__class__.__split_range(rng) for rng in ranges2]

            i = 0
            while i < len(ranges1):
                start_1, end_1 = ranges1[i]
                for start_2, end_2 in ranges2:
                    if start_1 <= end_2 and end_1 >= start_2:
                        if start_1 == start_2 and end_1 == end_2:
                            ranges1.pop(i)
                            i -= 1
                            break
                        split_rng = list()
                        if start_1 <= start_2 and end_1 <= end_2:
                            split_rng.append((start_1, chr(ord(start_2) - 1)))
                        elif start_1 >= start_2 and end_1 >= end_2:
                            split_rng.append((chr(ord(end_2) + 1), end_1))
                        else:
                            split_rng.append((start_1, chr(ord(start_2) - 1)))
                            split_rng.append((chr(ord(end_2) + 1), end_1))
                        if len(split_rng) > 0:
                            ranges1.pop(i)
                            i -= 1
                            ranges1 = ranges1 + split_rng
                            break
                i += 1

            ranges, chars = set(), set()
            for start, end in ranges1:
                if start == end:
                    chars.add(start)
                else:
                    if ord(end) == ord(start) + 1:
                        chars.add(start)
                        chars.add(end)
                    else:
                        ranges.add(f"{start}-{end}")

            return ranges, chars

        # 1. Extract classes while unescaping them
        ranges1, chars1 = __class__.__extract_classes(pre1.__verbose, unescape=True)
        ranges2, chars2 = __class__.__extract_classes(pre2.__verbose, unescape=True)

        # 2.a. Subtract ranges2 from chars1.
        splt_ranges2 = [__class__.__split_range(rng) for rng in ranges2]
        lst_chars1 = list(chars1)

        for start, end in splt_ranges2:
            i = 0
            while i < len(lst_chars1):
                c = lst_chars1[i]
                if c.isalnum and c >= start and c <= end:
                    lst_chars1.pop(i)
                    i = -1
                i += 1
        chars1 = set(lst_chars1)

        # 2.b Subtract chars2 from chars1.
        chars1 = chars1.difference(chars2)

        # 2.c. Subtract any characters in chars2 from ranges1.
        ranges1, reduced_chars = subtract_ranges(ranges1, set(f"{c}-{c}" for c in chars2))
        chars1 = chars1.union(reduced_chars)

        # 2.d. Subtract ranges2 from ranges1.
        ranges1, reduced_chars = subtract_ranges(ranges1, ranges2)
        chars1 = chars1.union(reduced_chars)

        # 3. Union ranges and chars together while escaping them.
        result = __class__.__modify_classes(ranges1.union(chars1), escape=True)
        
        if len(result) == 0:
            raise _ex.EmptyClassException(pre1, pre2)

        return  __class__(
            f"[{'^' if pre1.__is_negated else ''}{''.join(result)}]",
            pre1.__is_negated)


    @staticmethod
    def __extract_classes(pattern: str, unescape: bool = False) -> tuple[set[str], set[str]]:
        '''
        Extracts all classes from the provided class pattern and returns them \
        separated into two different sets based on whether they constitute a range \
        or an individual character.

        :param str pattern: The pattern from which classes are to be extracted.
        :param bool unespace: If `True` then unescapes all escaped characters. \
            Defaults to `False`.
        '''

        def get_start_index(pattern: str):
            if pattern.startswith('[^'):
                return 2
            else:
                return 1
        
        # Remove brackets etc from string.
        start_index = get_start_index(pattern)
        classes = pattern[start_index:-1]

        # Extract classes separately.
        ranges, chars = __class__.__separate_classes(classes)

        # Unescape any escaped characters if you must.
        if unescape:
            ranges = __class__.__modify_classes(ranges, escape=False)
            chars = __class__.__modify_classes(chars, escape=False)
        # Return classes.
        return ranges, chars


    @staticmethod
    def __separate_classes(classes: 'str') -> tuple[set[str], set[str]]:
        '''
        Extracts all classes from the provided character class pattern and \
        returns them separated into ranges and characters.

        :param str classes: One or more string character class patterns.
        '''
        range_pattern = \
            r"(?:\\(?:\[|\]|\^|\$|\-|\/|[a-z]|\\)|[^\[\]\^\$\-\/\\])" + \
            r"-(?:\\(?:\[|\]|\^|\$|\-|\/|[a-z]|\\)|[^\[\]\^\$\-\/\\])"
        ranges = set(_re.findall(range_pattern, classes))
        classes = _re.sub(pattern=range_pattern, repl="", string=classes)
        return (ranges, set(_re.findall(r"\\?.", classes, flags=_re.DOTALL)))

    
    @staticmethod
    def __modify_classes(classes: set[str], escape: bool) -> set[str]:
        '''
        Either escapes or unescapes any character within the provided classes that \
        needs to be escaped.

        :param bool escape: Determines whether to "escape" or "unescape" characters.
        '''

        def escape_char(c):
            return "\\" + c if c in __class__._to_escape else c
        def unescape_char(c):
            return c.replace("\\", "", 1) if len(c) > 1 and c[1] in __class__._to_escape else c

        fun = escape_char if escape else unescape_char
        modified_classes = set()

        for c in classes:
            if len(c) >= 3: # classes: [.-.], [\.-.], [\.-\.]
                start, end = tuple(map(fun, __class__.__split_range(c)))
                modified_c = start + "-" + end
            else: # characters: [.]
                modified_c = fun(c)
            modified_classes.add(modified_c)

        return modified_classes


    @staticmethod
    def __split_range(pattern: str) -> tuple[str, str]:
        '''
        Splits the provided range pattern and returns result as a tuple \
        containing the range's beginning and end.

        :param str pattern: The pattern that is to be split.

        :note: Provided characters within the range MUST NOT be escaped.
        '''

        count = pattern.count("-")

        if count == 1:
            return pattern.split("-")
        elif count == 2:
            split_fun = pattern.split if pattern[-1] == "-" else pattern.rsplit
            return split_fun("-", 1)
        else:
            return ("-", "-")


class Any(__Class):
    '''
    Matches any possible character, including the newline character.
    '''

    def __init__(self) -> 'Any':
        '''
        Matches any possible character, including the newline character.
        '''
        super().__init__('.', is_negated=False)

    def __invert__(self) -> None:
        '''
        Raises a "CannotBeNegatedException".
        '''
        raise _ex.CannotBeNegatedException()


class AnyLetter(__Class):
    '''
    Matches any character from the Latin alphabet.
    '''

    def __init__(self) -> 'AnyLetter':
        '''
        Matches any character from the Latin alphabet.
        '''
        super().__init__('[a-zA-Z]', is_negated=False)


class AnyButLetter(__Class):
    '''
    Matches any character except for characters in the Latin alphabet.
    '''

    def __init__(self) -> 'AnyButLetter':
        '''
        Matches any character except for characters in the Latin alphabet.
        '''
        super().__init__('[^a-zA-Z]', is_negated=True)


class AnyLowercaseLetter(__Class):
    '''
    Matches any lowercase character from the Latin alphabet.
    '''

    def __init__(self) -> 'AnyLowercaseLetter':
        '''
        Matches any lowercase character from the Latin alphabet.
        '''
        super().__init__('[a-z]', is_negated=False)


class AnyButLowercaseLetter(__Class):
    '''
    Matches any character except for lowercase characters in the Latin alphabet.
    '''

    def __init__(self) -> 'AnyButLowercaseLetter':
        '''
        Matches any character except for lowercase characters in the Latin alphabet.
        '''
        super().__init__('[^a-z]', is_negated=True)

    
class AnyUppercaseLetter(__Class):
    '''
    Matches any uppercase character from the Latin alphabet.
    '''

    def __init__(self) -> 'AnyUppercaseLetter':
        '''
        Matches any uppercase character from the Latin alphabet.
        '''
        super().__init__('[A-Z]', is_negated=False)


class AnyButUppercaseLetter(__Class):
    '''
    Matches any character except for uppercase characters in the Latin alphabet.
    '''

    def __init__(self) -> 'AnyButUppercaseLetter':
        '''
        Matches any character except for uppercase characters in the Latin alphabet.
        '''
        super().__init__('[^A-Z]', is_negated=True)


class AnyDigit(__Class):
    '''
    Matches any numeric character.
    '''

    def __init__(self) -> 'AnyDigit':
        '''
        Matches any numeric character.
        '''
        super().__init__('[0-9]', is_negated=False)


class AnyButDigit(__Class):
    '''
    Matches any character except for numeric characters.
    '''

    def __init__(self) -> 'AnyButDigit':
        '''
        Matches any character except for numeric characters.
        '''
        super().__init__('[^0-9]', is_negated=True)


class AnyWordChar(__Class):
    '''
    Matches any alphanumeric character as well as the underscore character ``_``.

    :param bool is_global: Indicates whether to include foreign alphabetic \
        characters or not. Defaults to ``False``.

    :raises GlobalWordCharSubtractionException: There is an attempt to subtract \
        a regular character class from an instance of this class for which \
        parameter ``is_global`` has been set to ``True``.
    '''

    def __init__(self, is_global: bool = False) -> 'AnyWordChar':
        '''
        Matches any alphanumeric character as well as the underscore character ``_``.

        :param bool is_global: Indicates whether to include foreign alphabetic \
            characters or not. Defaults to ``False``.

        :raises GlobalWordCharSubtractionException: There is an attempt to subtract \
            a regular character class from an instance of this class for which \
            parameter ``is_global`` has been set to ``True``.
        '''
        super().__init__('[a-zA-Z0-9_]', is_negated=False, simplify_word=is_global)
        self.__is_global = is_global


    def _is_global(self) -> bool:
        '''
        Returns ``True`` if this instance supports matching foreign alphabetic \
        characters, else returns ``False``.
        '''
        return self.__is_global


    def __invert__(self) -> '__Class':
        '''
        Returns an instance of class "AnyButWordChar" where parameter "is_global" \
        is set according to the value of this instance's "is_global" parameter.
        '''
        return AnyButWordChar(is_global=self._is_global())


class AnyButWordChar(__Class):
    '''
    Matches any character except for alphanumeric characters \
    and the underscore character  "_".

    :param bool is_global: Indicates whether to include foreign alphabetic \
        characters or not. Defaults to ``False``.

    :raises GlobalWordCharSubtractionException: There is an attempt to subtract \
        a negated character class from an instance of this class for which \
        parameter ``is_global`` has been set to ``True``.
    '''

    def __init__(self, is_global: bool = False) -> 'AnyButWordChar':
        '''
        Matches any character except for alphanumeric characters \
        and the underscore character "_".

        :param bool is_global: Indicates whether to include foreign alphabetic \
            characters or not. Defaults to ``False``.

        :raises GlobalWordCharSubtractionException: There is an attempt to subtract \
            a negated character class from an instance of this class for which \
            parameter ``is_global`` has been set to ``True``.
        '''
        super().__init__('[^a-zA-Z0-9_]', is_negated=True, simplify_word=is_global)
        self.__is_global = is_global


    def _is_global(self) -> bool:
        '''
        Returns ``True`` if this instance also excludes foreign alphabetic \
        characters from matching, else returns ``False``.
        '''
        return self.__is_global


    def __invert__(self) -> '__Class':
        '''
        Returns an instance of class "AnyWordChar" where parameter "is_global" \
        is set according to the value of this instance's "is_global" parameter.
        '''
        return AnyWordChar(is_global=self._is_global())


class AnyPunctuation(__Class):
    '''
    Matches any puncutation character as defined within the ASCII table.
    '''

    def __init__(self) -> 'AnyPunctuation':
        '''
        Matches any puncutation character as defined within the ASCII table.
        '''
        super().__init__('[!-\/:-@\[-`{-~]', is_negated=False)


class AnyButPunctuation(__Class):
    '''
    Matches any character except for punctuation characters \
    as defined within the ASCII table.
    '''

    def __init__(self) -> 'AnyButPunctuation':
        '''
        Matches any character except for punctuation characters \
        as defined within the ASCII table.
        '''
        super().__init__('[^!-\/:-@\[-`{-~]', is_negated=True)


class AnyWhitespace(__Class):
    '''
    Matches any whitespace character.
    '''

    def __init__(self) -> 'AnyWhitespace':
        '''
        Matches any whitespace character.
        '''
        super().__init__(f'[{_whitespace}]', is_negated=False)


class AnyButWhitespace(__Class):
    '''
    Matches any character except for whitespace characters.
    '''

    def __init__(self) -> 'AnyButWhitespace':
        '''
        Matches any character except for whitespace characters.
        '''
        super().__init__(f'[^{_whitespace}]', is_negated=True)


class AnyBetween(__Class):
    '''
    Matches any character within the provided range.

    :param str start: The first character of the range.
    :param str end: The last character of the range.

    :raises InvalidArgumentTypeException: At least one of the provided characters \
        is neither a *Token* class instance nor a single-character string.
    :raises InvalidRangeException: A non-valid range is provided.

    :note: Any pair of characters ``start``, ``end`` constitutes a valid range \
        as long as the code point of character ``end`` is greater than the code \
        point of character ``start``, as defined by the Unicode Standard.
    '''

    def __init__(self, start: str, end: str) -> 'AnyBetween':
        '''
        Matches any character within the provided range.

        :param str start: The first character of the range.
        :param str end: The last character of the range.

        :raises InvalidArgumentTypeException: At least one of the provided characters \
            is neither a *Token* class instance nor a single-character string.
        :raises InvalidRangeException: A non-valid range is provided.

        :note: Any pair of characters ``start``, ``end`` constitutes a valid range \
            as long as the code point of character ``end`` is greater than the code \
            point of character ``start``, as defined by the Unicode Standard.
        '''
        for c in (start, end):
            if isinstance(c, (str, _pre.Pregex)):
                if len(str(c).replace("\\", "", 1)) > 1:
                    message = f"Argument \"{c}\" is neither a string nor a token."
                    raise _ex.InvalidArgumentTypeException(message)
            else:
                message = f"Argument \"{c}\" is neither a string nor a token."
                raise _ex.InvalidArgumentTypeException(message)
        start, end = str(start), str(end)
        if ord(start) >= ord(end):
            raise _ex.InvalidRangeException(start, end)
        start = f"\\{start}" if start in __class__._to_escape else start
        end = f"\\{end}" if end in __class__._to_escape else end
        super().__init__(f"[{start}-{end}]", is_negated=False)


class AnyButBetween(__Class):
    '''
    Matches any character except for those within the provided range.

    :param str start: The first character of the range.
    :param str end: The last character of the range.

    :raises InvalidArgumentTypeException: At least one of the provided characters \
        is neither a *Token* class instance nor a single-character string.
    :raises InvalidRangeException: A non-valid range is provided.

    :note: Any pair of characters ``start``, ``end`` constitutes a valid range \
        as long as the code point of character ``end`` is greater than the code \
        point of character ``start``, as defined by the Unicode Standard.
    '''

    def __init__(self, start: str, end: str) -> 'AnyButBetween':
        '''
        Matches any character except for those within the provided range.

        :param str start: The first character of the range.
        :param str end: The last character of the range.

        :raises InvalidArgumentTypeException: At least one of the provided characters \
            is neither a *Token* class instance nor a single-character string.
        :raises InvalidRangeException: A non-valid range is provided.

        :note: Any pair of characters ``start``, ``end`` constitutes a valid range \
            as long as the code point of character ``end`` is greater than the code \
            point of character ``start``, as defined by the Unicode Standard.
        '''
        for c in (start, end):
            if isinstance(c, (str, _pre.Pregex)):
                if len(str(c).replace("\\", "", 1)) > 1: 
                    message = f"Argument \"{c}\" is neither a string nor a token."
                    raise _ex.InvalidArgumentTypeException(message)
            else:
                message = f"Argument \"{c}\" is neither a string nor a token."
                raise _ex.InvalidArgumentTypeException(message)
        start, end = str(start), str(end)
        if ord(start) >= ord(end):
            raise _ex.InvalidRangeException(start, end)
        start = f"\\{start}" if start in __class__._to_escape else start
        end = f"\\{end}" if end in __class__._to_escape else end
        super().__init__(f"[^{start}-{end}]", is_negated=True)      


class AnyFrom(__Class):
    '''
    Matches any one of the provided characters.

    :param str | Pregex \*chars: One or more characters to match from. \
        Each character must be either a string of length one or an instance \
        of a class defined within the :py:mod:`pregex.core.tokens` module.

    :raises NotEnoughArgumentsExceptions: No arguments are provided.
    :raises InvalidArgumentTypeException: At least one of the provided \
        arguments is neither a string of length one nor an instance of \
        a class defined within :py:mod:`pregex.core.tokens`.
    '''

    def __init__(self, *chars: str or _pre.Pregex) -> 'AnyFrom':
        '''
        Matches any one of the provided characters.

        :param str | Pregex \*chars: One or more characters to match from. \
            Each character must be either a string of length one or an instance \
            of a class defined within the :py:mod:`pregex.core.tokens` module.

        :raises NotEnoughArgumentsExceptions: No arguments are provided.
        :raises InvalidArgumentTypeException: At least one of the provided \
            arguments is neither a string of length one nor an instance of \
            a class defined within :py:mod:`pregex.core.tokens`.
        '''
        if len(chars) == 0:
            message = f"No characters were provided to \"{__class__.__name__}\"."
            raise _ex.NotEnoughArgumentsException(message)
        for c in chars:
            if isinstance(c, (str, _pre.Pregex)):
                if len(str(c).replace("\\", "", 1)) > 1: 
                    message = f"Argument \"{c}\" is neither a string nor a token."
                    raise _ex.InvalidArgumentTypeException(message)
            else:
                message = f"Argument \"{c}\" is neither a string nor a token."
                raise _ex.InvalidArgumentTypeException(message)
        chars = tuple((f"\\{c}" if c in __class__._to_escape else c) \
            if isinstance(c, str) else str(c) for c in chars)
        super().__init__(f"[{''.join(chars)}]", is_negated=False)


class AnyButFrom(__Class):
    '''
    Matches any character except for the provided characters.

    :param str | Pregex \*chars: One or more characters not to match from.
        Each character must be either a string of length one or an instance \
        of a class defined within the :py:mod:`pregex.core.tokens` module.

    :raises NotEnoughArgumentsExceptions: No arguments are provided.
    :raises InvalidArgumentTypeException: At least one of the provided \
        arguments is neither a string of length one nor an instance of \
        a class defined within :py:mod:`pregex.core.tokens`.
    '''

    def __init__(self, *chars: str or _pre.Pregex) -> 'AnyButFrom':
        '''
        Matches any character except for the provided characters.

        :param str | Pregex \*chars: One or more characters not to match from.
            Each character must be either a string of length one or an instance \
            of a class defined within the :py:mod:`pregex.core.tokens` module.

        :raises NotEnoughArgumentsExceptions: No arguments are provided.
        :raises InvalidArgumentTypeException: At least one of the provided \
            arguments is neither a string of length one nor an instance of \
            a class defined within :py:mod:`pregex.core.tokens`.
        '''
        if len(chars) == 0:
            message = f"No characters were provided to \"{__class__.__name__}\"."
            raise _ex.NotEnoughArgumentsException(message)
        for c in chars:
            if isinstance(c, (str, _pre.Pregex)):
                if len(str(c).replace("\\", "", 1)) > 1: 
                    message = f"Argument \"{c}\" is neither a string nor a token."
                    raise _ex.InvalidArgumentTypeException(message)
            else:
                message = f"Argument \"{c}\" is neither a string nor a token."
                raise _ex.InvalidArgumentTypeException(message)
        chars = tuple((f"\{c}" if c in __class__._to_escape else c)
            if isinstance(c, str) else str(c) for c in chars)
        super().__init__(f"[^{''.join(chars)}]", is_negated=True)


class AnyGermanLetter(__Class):
    '''
    Matches any character from the German alphabet.
    '''

    def __init__(self) -> 'AnyGermanLetter':
        '''
        Matches any character from the German alphabet.
        '''
        super().__init__('[a-zA-ZäöüßÄÖÜẞ]', is_negated=False)


class AnyButGermanLetter(__Class):
    '''
    Matches any character except for characters in the German alphabet.
    '''

    def __init__(self) -> 'AnyButGermanLetter':
        '''
        Matches any character except for characters in the German alphabet.
        '''
        super().__init__('[^a-zA-ZäöüßÄÖÜẞ]', is_negated=True)


class AnyGreekLetter(__Class):
    '''
    Matches any character from the Greek alphabet.
    '''

    def __init__(self) -> 'AnyGreekLetter':
        '''
        Matches any character from the Greek alphabet.
        '''
        # Start from 'Έ' and include "Ά" separately so that
        # Ano Teleia '·' is not included.
        super().__init__('[ΆΈ-ώ]', is_negated=False)


class AnyButGreekLetter(__Class):
    '''
    Matches any character except for characters in the Greek alphabet.
    '''

    def __init__(self) -> 'AnyGreekLetter':
        '''
        Matches any character except for characters in the Greek alphabet.
        '''
        # Start from 'Έ' and include "Ά" separately so that
        # Ano Teleia '·' is not included.
        super().__init__('[^ΆΈ-ώ]', is_negated=True)


class AnyCyrillicLetter(__Class):
    '''
    Matches any character from the Cyrillic alphabet.
    '''

    def __init__(self) -> 'AnyCyrillicLetter':
        '''
        Matches any character from the Cyrillic alphabet.
        '''
        super().__init__('[Ѐ-ӿ]', is_negated=False)

    
class AnyButCyrillicLetter(__Class):
    '''
    Matches any character except for characters in the Cyrillic alphabet.
    '''

    def __init__(self) -> 'AnyButCyrillicLetter':
        '''
        Matches any character except for characters in the Cyrillic alphabet.
        '''
        super().__init__('[^Ѐ-ӿ]', is_negated=True)


class AnyCJK(__Class):
    '''
    Matches any character that is defined within the \
    `CJK Unified Ideographs <https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)>`_ \
    Unicode block.
    '''
    def __init__(self) -> 'AnyCJK':
        '''
        Matches any character that is defined within the \
        `CJK Unified Ideographs <https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)>`_ \
        Unicode block.
        '''
        super().__init__('[\u4e00-\u9fd5]', is_negated=False)

    
class AnyButCJK(__Class):
    '''
    Matches any character except for those defined within the \
    `CJK Unified Ideographs <https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)>`_ \
    Unicode block.
    '''
    def __init__(self) -> 'AnyButCJK':
        '''
        Matches any character except for those defined within the \
        `CJK Unified Ideographs <https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)>`_ \
        Unicode block.
        '''
        super().__init__('[^\u4e00-\u9fd5]', is_negated=True)


class AnyKoreanLetter(__Class):
    '''
    Matches any character from the Korean alphabet.
    '''
    def __init__(self) -> 'AnyKoreanLetter':
        '''
        Matches any character from the Korean alphabet.
        '''
        super().__init__('[\u3131-\u314e\uac00-\ud7a3]', is_negated=False)


class AnyButKoreanLetter(__Class):
    '''
    Matches any character except for characters in the Korean alphabet.
    '''
    def __init__(self) -> 'AnyButKoreanLetter':
        '''
        Matches any character except for characters in the Korean alphabet.
        '''
        super().__init__('[^\u3131-\u314e\uac00-\ud7a3]', is_negated=True)