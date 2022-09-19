import unittest
from pregex.meta.essentials import *
from pregex.core.pre import _Type
from itertools import permutations
from pregex.core.exceptions import InvalidArgumentTypeException, \
    InvalidArgumentValueException


TEXT = "Hey there! How are you on this fine evening?"


def get_permutations(*classes: str):
    return set(f"[{''.join(p)}]" for p in permutations(classes))


class TestWord(unittest.TestCase):

    pre = Word()

    def test_word_on_pattern(self):
        self.assertEqual(str(self.pre), "\\b\\w+\\b")

    def test_word_min_chars_on_pattern(self):
        min = 3
        self.assertEqual(str(Word(min_chars=min)), f"\\b\\w{{{min},}}\\b")

    def test_word_max_chars_on_pattern(self):
        max = 3
        self.assertEqual(str(Word(max_chars=max)), f"\\b\\w{{1,{max}}}\\b")

    def test_word_min_chars_max_chars_on_pattern(self):
        min, max = 1, 3
        self.assertEqual(str(Word(min_chars=min, max_chars=max)), f"\\b\\w{{{min},{max}}}\\b")

    def test_word_equal_min_chars_max_chars_on_pattern(self):
        min = max = 3
        self.assertEqual(str(Word(min_chars=min, max_chars=max)), f"\\b\\w{{{max}}}\\b")

    def test_word_is_global_on_pattern(self):
        self.assertTrue(str(Word(is_global=False)) in
         f"\\b\\{p}\\b" for p in get_permutations("A-Z", "a-z", "\\d", "_"))
    
    def test_word_on_matches(self):
        self.assertEqual(self.pre.get_matches(TEXT),
        ["Hey", "there", "How", "are", "you", "on", "this", "fine", "evening"])

    def test_word_min_chars_on_matches(self):
        self.assertEqual(Word(min_chars=5).get_matches(TEXT),
        ["there", "evening"])

    def test_word_max_chars_on_matches(self):
        self.assertEqual(Word(max_chars=3).get_matches(TEXT),
        ["Hey", "How", "are", "you", "on"])

    def test_word_min_chars_max_chars_on_matches(self):
        self.assertEqual(Word(min_chars=3, max_chars=4).get_matches(TEXT),
        ["Hey", "How", "are", "you", "this", "fine"])

    def test_word_is_global_on_matches(self):
        self.assertEqual(Word(is_global=False).get_matches("Γειά σου"), [])

    def test_word_on_extensibility(self):
        pre = Word(is_extensible=True) + "g"
        self.assertEqual(pre.get_matches(TEXT), ['evening'])

    def test_word_on_invalid_argument_type_exception(self):
        self.assertRaises(InvalidArgumentTypeException, Word, min_chars='1')
        self.assertRaises(InvalidArgumentTypeException, Word, min_chars=1, max_chars='1')

    def test_word_on_invalid_argument_value_exception(self):
        self.assertRaises(InvalidArgumentValueException, Word, 0)
        self.assertRaises(InvalidArgumentValueException, Word, 1, 0)
        self.assertRaises(InvalidArgumentValueException, Word, 5, 3)


class TestWordContains(unittest.TestCase):

    infixes = ['re', 'ey', 'in']

    def test_word_contains_on_pattern(self):
        infix = 'a'
        self.assertEqual(str(WordContains(infix)), f"\\b\w*{infix}\w*\\b")
        self.assertEqual(str(WordContains(self.infixes)), f"\\b\w*(?:{'|'.join(self.infixes)})\w*\\b")

    def test_word_contains_is_global_on_pattern(self):
        self.assertTrue(str(WordContains(self.infixes, is_global=False)) in
        f"\\b\{p}*(?:{'|'.join(self.infixes)})\w*\\b" for p in get_permutations("A-Z", "a-z", "\\d", "_"))
    
    def test_word_contains_on_matches(self):
        self.assertEqual(WordContains(self.infixes).get_matches(TEXT), ["Hey", "there", "are", "fine", "evening"])

    def test_word_contains_is_global_on_matches(self):
        self.assertEqual(WordContains(['ά', 'σ']).get_matches('Γειά σου!'), ["Γειά", "σου"])

    def test_word_contains_on_extensibility(self):
        pre = WordContains(self.infixes, is_extensible=True) + 'e'
        self.assertEqual(pre.get_matches(TEXT), ['fine'])

    def test_word_contains_on_invalid_argument_type_exception(self):
        self.assertRaises(InvalidArgumentTypeException, WordContains, infix=1)
        self.assertRaises(InvalidArgumentTypeException, WordContains, infix=['a', 1])


class TestWordStartsWith(unittest.TestCase):

    prefixes = ['H', 'y']

    def test_word_starts_with_on_pattern(self):
        prefix = 'a'
        self.assertEqual(str(WordStartsWith(prefix)), f"\\b{prefix}\w*\\b")
        self.assertEqual(str(WordStartsWith(self.prefixes)), f"\\b(?:{'|'.join(self.prefixes)})\w*\\b")

    def test_word_starts_with_is_global_on_pattern(self):
        self.assertTrue(str(WordStartsWith(self.prefixes, is_global=False)) in
        f"\\b(?:{'|'.join(self.prefixes)})\w*\\b" for p in get_permutations("A-Z", "a-z", "\\d", "_"))
    
    def test_word_starts_with_on_matches(self):
        self.assertEqual(WordStartsWith(self.prefixes).get_matches(TEXT), ["Hey", "How", "you"])

    def test_word_starts_with_is_global_on_matches(self):
        self.assertEqual(WordStartsWith('Γ').get_matches('Γειά σου!'), ["Γειά"])

    def test_word_starts_with_on_extensibility(self):
        pre = WordStartsWith(self.prefixes, is_extensible=True) + 'y'
        self.assertEqual(pre.get_matches(TEXT), ['Hey'])

    def test_word_starts_with_on_invalid_argument_type_exception(self):
        self.assertRaises(InvalidArgumentTypeException, WordStartsWith, prefix=1)
        self.assertRaises(InvalidArgumentTypeException, WordStartsWith, prefix=['a', 1])


class TestWordEndsWith(unittest.TestCase):

    suffixes = ['re', 'w']

    def test_word_ends_with_on_pattern(self):
        suffix = 'a'
        self.assertEqual(str(WordEndsWith(suffix)), f"\\b\w*{suffix}\\b")
        self.assertEqual(str(WordEndsWith(self.suffixes)), f"\\b\w*(?:{'|'.join(self.suffixes)})\\b")

    def test_word_ends_with_is_global_on_pattern(self):
        self.assertTrue(str(WordEndsWith(self.suffixes, is_global=False)) in
        f"\\b\w*(?:{'|'.join(self.suffixes)})\\b" for p in get_permutations("A-Z", "a-z", "\\d", "_"))
    
    def test_word_ends_with_on_matches(self):
        self.assertEqual(WordEndsWith(self.suffixes).get_matches(TEXT), ["there", "How", "are"])

    def test_word_ends_with_is_global_on_matches(self):
        self.assertEqual(WordEndsWith('ά').get_matches('Γειά σου!'), ["Γειά"])

    def test_word_ends_with_on_extensibility(self):
        pre = 'H' + WordEndsWith(self.suffixes, is_extensible=True)
        self.assertEqual(pre.get_matches(TEXT), ['How'])

    def test_word_ends_with_on_invalid_argument_type_exception(self):
        self.assertRaises(InvalidArgumentTypeException, WordEndsWith, suffix=1)
        self.assertRaises(InvalidArgumentTypeException, WordEndsWith, suffix=['a', 1])


class TestNumeral(unittest.TestCase):

    text = "0 10 123 1234 156 1901 a41 c71 ffff +999 g999"

    def test_numeral_on_base(self):
        self.assertEqual(Numeral(base=2).get_matches(self.text), ["0", "10"])
        self.assertEqual(Numeral(base=5).get_matches(self.text), ["0", "10", "123", "1234"])
        self.assertEqual(Numeral(base=10).get_matches(self.text),
        ["0", "10", "123", "1234", "156", "1901", "999"])
        self.assertEqual(Numeral(base=16).get_matches(self.text),
        ["0", "10", "123", "1234", "156", "1901", "a41", "c71", "ffff", "999"])

    def test_numeral_on_n_min(self):
        self.assertEqual(Numeral(n_min=4).get_matches(self.text), ["1234", "1901"])

    def test_numeral_on_n_max(self):
        self.assertEqual(Numeral(n_max=3).get_matches(self.text), ["0", "10", "123", "156", "999"])

    def test_numeral_on_n_min_n_max(self):
        self.assertEqual(Numeral(n_min=3, n_max=3).get_matches(self.text), ["123", "156", "999"])

    def test_numeral_on_extensibility(self):
        pre = '1' + Numeral(is_extensible=True)
        self.assertEqual(pre.get_matches(self.text), ["10", "123", "1234", "156", "1901"])

    def test_numeral_on_invalid_argument_type_exception(self):
        self.assertRaises(InvalidArgumentTypeException, Numeral, base='2')
        self.assertRaises(InvalidArgumentTypeException, Numeral, base=2, n_min='2')
        self.assertRaises(InvalidArgumentTypeException, Numeral, base=2, n_min=2, n_max='2')

    def test_numeral_on_invalid_argument_value_exception(self):
        self.assertRaises(InvalidArgumentValueException, Numeral, base=1)
        self.assertRaises(InvalidArgumentValueException, Numeral, base=17)
        self.assertRaises(InvalidArgumentValueException, Numeral, n_min=-1)
        self.assertRaises(InvalidArgumentValueException, Numeral, n_min=2, n_max=1)


class TestInteger(unittest.TestCase):

    text = "0 00 a b 01 1 cd ! 003 +3 7 000010 10 123 -128 a+141 ++142 1234069"

    def test_integer_on_matches(self):
        self.assertEqual(Integer().get_matches(self.text),
            ["0", "1", "3", "7", "10", "123", "128", "141", "142", "1234069"])
        
    def test_integer_start_on_matches(self):
        self.assertEqual(Integer(start=10).get_matches(self.text),
            ["10", "123", "128", "141", "142", "1234069"])

    def test_integer_end_on_matches(self):
        self.assertEqual(Integer(end=10).get_matches(self.text),
            ["0", "1", "3", "7", "10"])

    def test_integer_start_end_on_matches(self):
        self.assertEqual(Integer(start=3, end=10).get_matches(self.text),
            ["3", "7", "10"])

    def test_integer_include_sign_on_matches(self):
        self.assertEqual(Integer(include_sign=True).get_matches(self.text),
            ["0", "1", "+3", "7", "10", "123", "-128", "+142", "1234069"])

    def test_integer_on_extensibility(self):
        pre = 'a' + Integer(include_sign=True, is_extensible=True)
        self.assertEqual(pre.get_matches(self.text), ["a+141"])

    def test_integer_on_invalid_argument_type_exception(self):
        self.assertRaises(InvalidArgumentTypeException, Integer, start='1')
        self.assertRaises(InvalidArgumentTypeException, Integer, start=1, end='1')

    def test_integer_on_invalid_argument_value_exception(self):
        self.assertRaises(InvalidArgumentValueException, Integer, start=-1)
        self.assertRaises(InvalidArgumentValueException, Integer, start=2, end=1)


class TestPositiveInteger(unittest.TestCase):

    text = "0 00 a +b 01 +1 cd ! 003 +3 7 000010 10 123 -128 a+141 +142 1234069"

    def test_positive_integer_on_matches(self):
        self.assertEqual(PositiveInteger().get_matches(self.text),
            ["0", "+1", "+3", "7", "10", "123", "+142", "1234069"])
        
    def test_positive_integer_start_on_matches(self):
        self.assertEqual(PositiveInteger(start=10).get_matches(self.text),
            ["10", "123", "+142", "1234069"])

    def test_positive_integer_end_on_matches(self):
        self.assertEqual(PositiveInteger(end=10).get_matches(self.text),
            ["0", "+1", "+3", "7", "10"])

    def test_positive_integer_start_end_on_matches(self):
        self.assertEqual(PositiveInteger(start=3, end=10).get_matches(self.text),
            ["+3", "7", "10"])

    def test_positive_integer_on_extensibility(self):
        pre = 'a' + PositiveInteger(is_extensible=True)
        self.assertEqual(pre.get_matches(self.text), ["a+141"])

    def test_positive_integer_on_invalid_argument_type_exception(self):
        self.assertRaises(InvalidArgumentTypeException, PositiveInteger, start='1')
        self.assertRaises(InvalidArgumentTypeException, PositiveInteger, start=1, end='1')

    def test_positive_integer_on_invalid_argument_value_exception(self):
        self.assertRaises(InvalidArgumentValueException, PositiveInteger, start=-1)
        self.assertRaises(InvalidArgumentValueException, PositiveInteger, start=2, end=1)


class TestNegativeInteger(unittest.TestCase):

    text = "0 00 a -b 01 -1 cd ! 003 -3 -7 000010 -10 123 -128 a-141 +-142 -1234069"

    def test_negative_integer_on_matches(self):
        self.assertEqual(NegativeInteger().get_matches(self.text),
            ["-1", "-3", "-7", "-10", "-128", "-142", "-1234069"])
        
    def test_negative_integer_start_on_matches(self):
        self.assertEqual(NegativeInteger(start=10).get_matches(self.text),
            ["-10", "-128", "-142", "-1234069"])

    def test_negative_integer_end_on_matches(self):
        self.assertEqual(NegativeInteger(end=10).get_matches(self.text),
            ["-1", "-3", "-7", "-10"])

    def test_negative_integer_start_end_on_matches(self):
        self.assertEqual(NegativeInteger(start=3, end=7).get_matches(self.text),
            ["-3", "-7"])

    def test_negative_integer_on_extensibility(self):
        pre = 'a' + NegativeInteger(is_extensible=True)
        self.assertEqual(pre.get_matches(self.text), ["a-141"])

    def test_negative_integer_on_invalid_argument_type_exception(self):
        self.assertRaises(InvalidArgumentTypeException, NegativeInteger, start='1')
        self.assertRaises(InvalidArgumentTypeException, NegativeInteger, start=1, end='1')

    def test_negative_integer_on_invalid_argument_value_exception(self):
        self.assertRaises(InvalidArgumentValueException, NegativeInteger, start=-1)
        self.assertRaises(InvalidArgumentValueException, NegativeInteger, start=2, end=1)


class TestUnsignedInteger(unittest.TestCase):

    text = "0 00 a -b 01 -1 cd ! 003 -3 7 000010 -10 123 -128 a-141 +-142 1234069 b14"

    def test_unsigned_integer_on_matches(self):
        self.assertEqual(UnsignedInteger().get_matches(self.text),
            ["0", "7", "123", "1234069"])
        
    def test_unsigned_integer_start_on_matches(self):
        self.assertEqual(UnsignedInteger(start=3).get_matches(self.text),
            ["7", "123", "1234069"])

    def test_unsigned_integer_end_on_matches(self):
        self.assertEqual(UnsignedInteger(end=10).get_matches(self.text),
            ["0", "7"])

    def test_unsigned_integer_start_end_on_matches(self):
        self.assertEqual(UnsignedInteger(start=3, end=7).get_matches(self.text),
            ["7"])

    def test_unsigned_integer_on_extensibility(self):
        pre = 'b' + UnsignedInteger(is_extensible=True)
        self.assertEqual(pre.get_matches(self.text), ["b14"])

    def test_unsigned_integer_on_invalid_argument_type_exception(self):
        self.assertRaises(InvalidArgumentTypeException, UnsignedInteger, start='1')
        self.assertRaises(InvalidArgumentTypeException, UnsignedInteger, start=1, end='1')

    def test_unsigned_integer_on_invalid_argument_value_exception(self):
        self.assertRaises(InvalidArgumentValueException, UnsignedInteger, start=-1)
        self.assertRaises(InvalidArgumentValueException, UnsignedInteger, start=2, end=1)


class TestDecimal(unittest.TestCase):

    text = ".1 0.1 00 a b 01 1.22 cd ! 003 +3.789 7 000010 ++10.5555 123. -128.99999 a+141.1 ++142.2"

    def test_decimal_on_matches(self):
        self.assertEqual(Decimal().get_matches(self.text),
            [".1", "0.1", "1.22", "3.789", "10.5555", "128.99999", "141.1", "142.2"])
        
    def test_decimal_start_on_matches(self):
        self.assertEqual(Decimal(start=10).get_matches(self.text),
            ["10.5555", "128.99999", "141.1", "142.2"])

    def test_decimal_end_on_matches(self):
        self.assertEqual(Decimal(end=10).get_matches(self.text),
            [".1", "0.1", "1.22", "3.789", "10.5555"])

    def test_decimal_start_end_on_matches(self):
        self.assertEqual(Decimal(start=3, end=10).get_matches(self.text),
            ["3.789", "10.5555"])

    def test_decimal_min_decimal_on_matches(self):
        self.assertEqual(Decimal(min_decimal=3).get_matches(self.text),
            ["3.789", "10.5555", "128.99999"])

    def test_decimal_max_decimal_on_matches(self):
        self.assertEqual(Decimal(max_decimal=2).get_matches(self.text),
            [".1", "0.1", "1.22", "141.1", "142.2"])

    def test_decimal_min_decimal_max_decimal_on_matches(self):
        self.assertEqual(Decimal(min_decimal=2, max_decimal=4).get_matches(self.text),
            ["1.22", "3.789", "10.5555"])

    def test_decimal_start_end_min_decimal_max_decimal_on_matches(self):
        self.assertEqual(Decimal(start=3, end=10, min_decimal=2, max_decimal=4).get_matches(self.text),
            ["3.789", "10.5555"])

    def test_decimal_include_sign_on_matches(self):
        self.assertEqual(Decimal(include_sign=True).get_matches(self.text),
            [".1", "0.1", "1.22", "+3.789", "+10.5555", "-128.99999", "+142.2"])

    def test_decimal_on_extensibility(self):
        pre = 'a' + Decimal(include_sign=True, is_extensible=True)
        self.assertEqual(pre.get_matches(self.text), ["a+141.1"])

    def test_decimal_on_invalid_argument_type_exception(self):
        self.assertRaises(InvalidArgumentTypeException, Decimal, start='1')
        self.assertRaises(InvalidArgumentTypeException, Decimal, end='1')
        self.assertRaises(InvalidArgumentTypeException, Decimal, min_decimal='1')
        self.assertRaises(InvalidArgumentTypeException, Decimal, max_decimal='1')

    def test_decimal_on_invalid_argument_value_exception(self):
        self.assertRaises(InvalidArgumentValueException, Decimal, start=-1)
        self.assertRaises(InvalidArgumentValueException, Decimal, start=2, end=1)
        self.assertRaises(InvalidArgumentValueException, Decimal, min_decimal=0)
        self.assertRaises(InvalidArgumentValueException, Decimal, min_decimal=2, max_decimal=1)


class TestPositiveDecimal(unittest.TestCase):

    text = ".1 0.1 00 a b 01 1.22 cd ! 003 +3.789 7 000010 ++10.5555 123. -128.99999 a+141.1"

    def test_positive_decimal_on_matches(self):
        self.assertEqual(PositiveDecimal().get_matches(self.text),
            [".1", "0.1", "1.22", "+3.789", "+10.5555"])
        
    def test_positive_decimal_start_on_matches(self):
        self.assertEqual(PositiveDecimal(start=10).get_matches(self.text),
            ["+10.5555"])

    def test_positive_decimal_end_on_matches(self):
        self.assertEqual(PositiveDecimal(end=10).get_matches(self.text),
            [".1", "0.1", "1.22", "+3.789", "+10.5555"])

    def test_positive_decimal_start_end_on_matches(self):
        self.assertEqual(PositiveDecimal(start=3, end=10).get_matches(self.text),
            ["+3.789", "+10.5555"])

    def test_positive_decimal_min_decimal_on_matches(self):
        self.assertEqual(PositiveDecimal(min_decimal=3).get_matches(self.text),
            ["+3.789", "+10.5555"])

    def test_positive_decimal_max_decimal_on_matches(self):
        self.assertEqual(PositiveDecimal(max_decimal=2).get_matches(self.text),
            [".1", "0.1", "1.22"])

    def test_positive_decimal_min_decimal_max_decimal_on_matches(self):
        self.assertEqual(PositiveDecimal(min_decimal=2, max_decimal=4).get_matches(self.text),
            ["1.22", "+3.789", "+10.5555"])

    def test_positive_decimal_start_end_min_decimal_max_decimal_on_matches(self):
        self.assertEqual(PositiveDecimal(start=3, end=10, min_decimal=2, max_decimal=4).get_matches(self.text),
            ["+3.789", "+10.5555"])

    def test_positive_decimal_on_extensibility(self):
        pre = 'a' + PositiveDecimal(is_extensible=True)
        self.assertEqual(pre.get_matches(self.text), ["a+141.1"])

    def test_positive_decimal_on_invalid_argument_type_exception(self):
        self.assertRaises(InvalidArgumentTypeException, PositiveDecimal, start='1')
        self.assertRaises(InvalidArgumentTypeException, PositiveDecimal, end='1')
        self.assertRaises(InvalidArgumentTypeException, PositiveDecimal, min_decimal='1')
        self.assertRaises(InvalidArgumentTypeException, PositiveDecimal, max_decimal='1')

    def test_positive_decimal_on_invalid_argument_value_exception(self):
        self.assertRaises(InvalidArgumentValueException, PositiveDecimal, start=-1)
        self.assertRaises(InvalidArgumentValueException, PositiveDecimal, start=2, end=1)
        self.assertRaises(InvalidArgumentValueException, PositiveDecimal, min_decimal=0)
        self.assertRaises(InvalidArgumentValueException, PositiveDecimal, min_decimal=2, max_decimal=1)


class TestNegativeDecimal(unittest.TestCase):

    text = "-.1 -0.1 00 a b 01 -1.22 cd ! 003 -3.789 -7 000010 +-10.5555 123. +128.99999 a-141.1 +-142"

    def test_negative_decimal_on_matches(self):
        self.assertEqual(NegativeDecimal().get_matches(self.text),
            ["-.1", "-0.1", "-1.22", "-3.789", "-10.5555"])
        
    def test_negative_decimal_start_on_matches(self):
        self.assertEqual(NegativeDecimal(start=10).get_matches(self.text),
            ["-10.5555"])

    def test_negative_decimal_end_on_matches(self):
        self.assertEqual(NegativeDecimal(end=10).get_matches(self.text),
            ["-.1", "-0.1", "-1.22", "-3.789", "-10.5555"])

    def test_negative_decimal_start_end_on_matches(self):
        self.assertEqual(NegativeDecimal(start=3, end=10).get_matches(self.text),
            ["-3.789", "-10.5555"])

    def test_negative_decimal_min_decimal_on_matches(self):
        self.assertEqual(NegativeDecimal(min_decimal=3).get_matches(self.text),
            ["-3.789", "-10.5555"])

    def test_negative_decimal_max_decimal_on_matches(self):
        self.assertEqual(NegativeDecimal(max_decimal=2).get_matches(self.text),
            ["-.1", "-0.1", "-1.22"])

    def test_negative_decimal_min_decimal_max_decimal_on_matches(self):
        self.assertEqual(NegativeDecimal(min_decimal=2, max_decimal=4).get_matches(self.text),
            ["-1.22", "-3.789", "-10.5555"])

    def test_negative_decimal_start_end_min_decimal_max_decimal_on_matches(self):
        self.assertEqual(NegativeDecimal(start=3, end=10, min_decimal=2, max_decimal=4).get_matches(self.text),
            ["-3.789", "-10.5555"])

    def test_negative_decimal_on_extensibility(self):
        pre = 'a' + NegativeDecimal(is_extensible=True)
        self.assertEqual(pre.get_matches(self.text), ["a-141.1"])

    def test_negative_decimal_on_invalid_argument_type_exception(self):
        self.assertRaises(InvalidArgumentTypeException, NegativeDecimal, start='1')
        self.assertRaises(InvalidArgumentTypeException, NegativeDecimal, end='1')
        self.assertRaises(InvalidArgumentTypeException, NegativeDecimal, min_decimal='1')
        self.assertRaises(InvalidArgumentTypeException, NegativeDecimal, max_decimal='1')

    def test_negative_decimal_on_invalid_argument_value_exception(self):
        self.assertRaises(InvalidArgumentValueException, NegativeDecimal, start=-1)
        self.assertRaises(InvalidArgumentValueException, NegativeDecimal, start=2, end=1)
        self.assertRaises(InvalidArgumentValueException, NegativeDecimal, min_decimal=0)
        self.assertRaises(InvalidArgumentValueException, NegativeDecimal, min_decimal=2, max_decimal=1)


class TestUnsignedDecimal(unittest.TestCase):

    text = ".1 0.1 00 a b 01 -1.22 cd ! 003 3.789 -7 000010 10.5555 123. +128.99999 a-141 +-142 b14.1"

    def test_unsigned_decimal_on_matches(self):
        self.assertEqual(UnsignedDecimal().get_matches(self.text),
            [".1", "0.1", "3.789", "10.5555"])
        
    def test_unsigned_decimal_start_on_matches(self):
        self.assertEqual(UnsignedDecimal(start=10).get_matches(self.text),
            ["10.5555"])

    def test_unsigned_decimal_end_on_matches(self):
        self.assertEqual(UnsignedDecimal(end=10).get_matches(self.text),
            [".1", "0.1", "3.789", "10.5555"])

    def test_unsigned_decimal_start_end_on_matches(self):
        self.assertEqual(UnsignedDecimal(start=3, end=10).get_matches(self.text),
            ["3.789", "10.5555"])

    def test_unsigned_decimal_min_decimal_on_matches(self):
        self.assertEqual(UnsignedDecimal(min_decimal=3).get_matches(self.text),
            ["3.789", "10.5555"])

    def test_unsigned_decimal_max_decimal_on_matches(self):
        self.assertEqual(UnsignedDecimal(max_decimal=2).get_matches(self.text),
            [".1", "0.1"])

    def test_unsigned_decimal_min_decimal_max_decimal_on_matches(self):
        self.assertEqual(UnsignedDecimal(min_decimal=2, max_decimal=4).get_matches(self.text),
            ["3.789", "10.5555"])

    def test_unsigned_decimal_start_end_min_decimal_max_decimal_on_matches(self):
        self.assertEqual(UnsignedDecimal(start=3, end=10, min_decimal=2, max_decimal=4).get_matches(self.text),
            ["3.789", "10.5555"])

    def test_unsigned_decimal_on_extensibility(self):
        pre = 'b' + UnsignedDecimal(is_extensible=True)
        self.assertEqual(pre.get_matches(self.text), ["b14.1"])

    def test_unsigned_decimal_on_invalid_argument_type_exception(self):
        self.assertRaises(InvalidArgumentTypeException, UnsignedDecimal, start='1')
        self.assertRaises(InvalidArgumentTypeException, UnsignedDecimal, end='1')
        self.assertRaises(InvalidArgumentTypeException, UnsignedDecimal, min_decimal='1')
        self.assertRaises(InvalidArgumentTypeException, UnsignedDecimal, max_decimal='1')

    def test_unsigned_decimal_on_invalid_argument_value_exception(self):
        self.assertRaises(InvalidArgumentValueException, UnsignedDecimal, start=-1)
        self.assertRaises(InvalidArgumentValueException, UnsignedDecimal, start=2, end=1)
        self.assertRaises(InvalidArgumentValueException, UnsignedDecimal, min_decimal=0)
        self.assertRaises(InvalidArgumentValueException, UnsignedDecimal, min_decimal=2, max_decimal=1)


class TestDate(unittest.TestCase):

    text = '''
    Valid
    ------
    24/11/2001
    11-24-2001
    24/11/01
    1/3/1996
    1996/11/20
    a1998/10/21 (extensible-only)

    Invalid
    -------
    00/00/1996
    1996/24/11
    2/2/2
    24/07-1996
    1996/11/2004
    '''
    
    def test_date_on_matches(self):
        self.assertEqual(Date().get_matches(self.text), [
            "24/11/2001",
            "11-24-2001",
            "24/11/01",
            "1/3/1996",
            "1996/11/20"
        ])

    def test_date_on_specified_matches(self):
        self.assertEqual(Date(formats=["dd/mm/yyyy"]).get_matches(self.text),
            ["24/11/2001"])

    def test_date_on_extensibility(self):
        pre = 'a' + Date(is_extensible=True)
        self.assertEqual(pre.get_matches(self.text), ["a1998/10/21"])


class TestIPv4(unittest.TestCase):

    text = '''
    Valid
    -----
    192.168.1.1
    0.0.0.0
    .10.10.10.10. (extensible-only)
    
    Invalid
    -------
    1.1.1.1.1
    132.156.257.111
    1231.1.1.1
    '''

    def test_ipv4_on_matches(self):
        self.assertEqual(IPv4().get_matches(self.text), ["192.168.1.1", "0.0.0.0"])

    def test_ipv4_on_extensibility(self):
        pre = '.' + IPv4(is_extensible=True) + '.'
        self.assertEqual(pre.get_matches(self.text), [".10.10.10.10."])


class TestIPv6(unittest.TestCase):

    text = '''
    Valid
    -----
    2001:db8:1234:ffff:ffff:ffff:ffff:ffff
    f23b::fb2:8a2e:370:7334
    ::1
    ::
    :::: (extensible-only)

    Invalid
    -------
    2001:db8:1234:ffff:ffff:ffff:ffff:ffff:ffff
    2001:db8:1234:ffff:ffff:ffff:ffff:gggg
    2001:db8:1234:ffff:ffff:ffff:ffff
    1ff::234::7
    '''

    def test_ipv6_on_matches(self):
        self.assertEqual(IPv6().get_matches(self.text), [
            "2001:db8:1234:ffff:ffff:ffff:ffff:ffff",
            "f23b::fb2:8a2e:370:7334",
            "::1",
            "::"])

    def test_ipv6_on_extensibility(self):
        pre = ':' + IPv6(is_extensible=True) + ':'
        self.assertEqual(pre.get_matches(self.text), ["::::"])


class TestEmail(unittest.TestCase):

    text = '''
    Valid
    ------
    abcdef@mail.com
    abc-def@mail1.cc
    abc.def@mail-archive.com
    abc!def@mail-archive1.org
    abc^def@mail-archive2.com

    Invalid
    -------
    abc.example.com
    a@b@c@example.com
    a"b(c)d,e:f;g<h>i[j\k]l@example.com
    abc-@mail.com
    abc.def@mail.c
    abc.def@mail#archive.com
    abc.def@mail	
    abc.def@mail..com`	
    '''

    def test_email_on_matches(self):
        self.assertEqual(Email().get_matches(self.text), [
            "abcdef@mail.com",
            "abc-def@mail1.cc",
            "abc.def@mail-archive.com",
            "abc!def@mail-archive1.org",
            "abc^def@mail-archive2.com"
        ])

    def test_email_on_capture_local_part(self):
        self.assertEqual(Email(capture_local_part=True).get_captures(self.text), [
            ("abcdef",),
            ("abc-def",),
            ("abc.def",),
            ("abc!def",),
            ("abc^def",)
        ])

    def test_email_on_capture_domain(self):
        self.assertEqual(Email(capture_domain=True).get_captures(self.text), [
            ("mail",),
            ("mail1",),
            ("mail-archive",),
            ("mail-archive1",),
            ("mail-archive2",)
        ])

    def test_email_on_extensibility(self):
        pre = 'abcd' + Email(is_extensible=True)
        self.assertEqual(pre.get_matches(self.text), ["abcdef@mail.com"])


class TestHttpUrl(unittest.TestCase):

    text = '''
    Valid
    -----
    www.youtube.com
    http://wikipedia.org
    https://www.github.com
    www.subdomain.domain1.io
    www.subdomain.domain2.io:8080
    www.domain3.io/
    www.domain4.io/dir1
    www.domain5.io/dir1/
    www.subdomain.domain6.io/dir1/dir2

    Invalid
    -------
    somedomain-.com
    www.somedomain.comcomcom
    https://www.y.com
    '''

    def test_http_url_on_matches(self):
        self.assertEqual(HttpUrl().get_matches(self.text), [
            "www.youtube.com",
            "http://wikipedia.org",
            "https://www.github.com",
            "www.subdomain.domain1.io",
            "www.subdomain.domain2.io:8080",
            "www.domain3.io/",
            "www.domain4.io/dir1",
            "www.domain5.io/dir1/",
            "www.subdomain.domain6.io/dir1/dir2"
        ])

    def test_http_url_on_capture_domain(self):
        self.assertEqual(HttpUrl(capture_domain=True).get_captures(self.text), [
            ("youtube",),
            ("wikipedia",),
            ("github",),
            ("domain1",),
            ("domain2",),
            ("domain3",),
            ("domain4",),
            ("domain5",),
            ("domain6",)
        ])

    def test_http_url_on_extensibility(self):
        pre = 'www.you' + HttpUrl(is_extensible=True)
        self.assertEqual(pre.get_matches(self.text), ["www.youtube.com"])
        

if __name__=="__main__":
    unittest.main()