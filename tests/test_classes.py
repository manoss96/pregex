import unittest
from pregex.classes import *
from string import whitespace
from itertools import permutations
from pregex.tokens import Backslash, Literal
from pregex.exceptions import NeitherStringNorTokenException, MultiCharTokenException, \
    CannotBeCombinedException, InvalidRangeException


class Test__AnyClass(unittest.TestCase):

    def get_permutations(*classes: str):
        return set(f"[{''.join(p)}]" for p in permutations(classes))
    
    def test_any_class_bitwise_or(self):
        self.assertTrue(str(AnyLowercaseLetter() | AnyDigit()) \
            in __class__.get_permutations("a-z", "0-9"))
        self.assertTrue(str(AnyFrom("a", "b") | AnyFrom("c", "d")) \
            in __class__.get_permutations("a", "b", "c", "d"))

    def test_any_class_bitwise_or_with_subset(self):
        self.assertTrue(str(AnyLetter() | AnyLowercaseLetter()) \
            in __class__.get_permutations("a-z", "A-Z"))
        self.assertTrue(str(AnyFrom("a", "b", "c") | AnyFrom("a", "b")) \
            in __class__.get_permutations("a", "b", "c"))

    def test_any_class_bitwise_or_with_intersection(self):
        self.assertTrue(str(AnyFrom("a", "b") | AnyFrom("b", "c")) \
            in __class__.get_permutations("a", "b", "c"))

    def test_any_class_bitwise_or_on_cannot_be_combined_exception(self):
        any_letter, any_except_digit = AnyLetter(), ~AnyDigit()
        self.assertRaises(CannotBeCombinedException, any_letter.__or__, any_except_digit)
        self.assertRaises(CannotBeCombinedException, any_letter.__ror__, any_except_digit)


class Test_NegatedClass(unittest.TestCase):

    def get_permutations(*classes: str):
        return set(f"[^{''.join(p)}]" for p in permutations(classes))
    
    def test_any_except_class_bitwise_or(self):
        self.assertTrue(str(~AnyLowercaseLetter() | ~AnyDigit()) \
            in __class__.get_permutations("a-z", "0-9"))
        self.assertTrue(str(~AnyFrom("a", "b") | ~AnyFrom("c", "d")) \
            in __class__.get_permutations("a", "b", "c", "d"))

    def test_any_except_class_bitwise_or_with_subset(self):
        self.assertTrue(str(~AnyLetter() | ~AnyLowercaseLetter()) \
            in __class__.get_permutations("a-z", "A-Z"))
        self.assertTrue(str(~AnyFrom("a", "b", "c") | ~AnyFrom("a", "b")) \
            in __class__.get_permutations("a", "b", "c"))

    def test_any_except_class_bitwise_or_with_intersection(self):
        self.assertTrue(str(~AnyFrom("a", "b") | ~AnyFrom("b", "c")) \
            in __class__.get_permutations("a", "b", "c"))

    def test_any_except_class_bitwise_or_on_cannot_be_combined_exception(self):
        any_except_letter, any_digit = ~AnyLetter(), AnyDigit()
        self.assertRaises(CannotBeCombinedException, any_except_letter.__or__, any_digit)
        self.assertRaises(CannotBeCombinedException, any_except_letter.__ror__, any_digit)


class TestAny(unittest.TestCase):

    def test_any(self):
        self.assertEqual(str(Any()), ".")

    def test_any_on_or(self):
        self.assertEqual(str(Any() | AnyLetter()), ".")
        self.assertEqual(str(AnyLetter() | Any()), ".")

    def test_any_on_newline_match(self):
        self.assertTrue(Any().get_matches("\n"), ["\n"])


class TestAnyLetter(unittest.TestCase):

    def test_any_letter(self):
        self.assertEqual(str(AnyLetter()), "[a-zA-Z]")


class TestAnyLowercaseLetter(unittest.TestCase):

    def test_any_lowercase_letter(self):
        self.assertEqual(str(AnyLowercaseLetter()), "[a-z]")


class TestAnyUppercaseLetter(unittest.TestCase):

    def test_any_uppercase_letter(self):
        self.assertEqual(str(AnyUppercaseLetter()), "[A-Z]")
        

class TestAnyDigit(unittest.TestCase):

    def test_any_digit(self):
        self.assertEqual(str(AnyDigit()), "[0-9]")


class TestAnyWordChar(unittest.TestCase):

    def test_any_word_char(self):
        self.assertEqual(str(AnyWordChar()), "[a-zA-Z0-9_]")


class TestAnyPunctuationChar(unittest.TestCase):

    def test_any_punctuation_char(self):
        self.assertEqual(str(AnyPunctuationChar()), '[!"#$%&\'()*+,.\/:;<=>?@\^_`{|}~\-]')


class TestAnyWhitespace(unittest.TestCase):

    def test_any_whitespace(self):
        self.assertEqual(str(AnyWhitespace()), f"[{whitespace}]")


class TestAnyWithinRange(unittest.TestCase):

    def test_any_within_range(self):
        for start, end in [("a", "c"), (1, 5)]:
            self.assertEqual(str(AnyWithinRange(start, end)), f"[{start}-{end}]")

    def test_any_within_range_on_invalid_range_exception(self):
        for start, end in [("z", "a"), (9, 0), ("z", 0)]:
            self.assertRaises(InvalidRangeException, AnyWithinRange, start, end)


class TestAnyFrom(unittest.TestCase):

    def test_any_from(self):
        tokens = ("a", "c", Backslash(), Literal("!"))
        self.assertEqual(str(AnyFrom(*tokens)), f"[{''.join([str(t) for t in tokens])}]")

    def test_any_from_on_neither_str_or_token_exception(self):
        for t in (True, 1, 1.1, Pregex("a")):
            self.assertRaises(NeitherStringNorTokenException, AnyFrom, t)

    def test_any_from_on_multi_char_token_exception(self):
        for t in ("aa", Literal("zzen")):
            self.assertRaises(MultiCharTokenException, AnyFrom, t)


class TestNegatedAnyLetter(unittest.TestCase):

    def test_any_except_letter(self):
        self.assertEqual(str(~AnyLetter()), "[^a-zA-Z]")


class TestNegatedAnyLowercaseLetter(unittest.TestCase):

    def test_any_except_lowercase_letter(self):
        self.assertEqual(str(~AnyLowercaseLetter()), "[^a-z]")


class TestNegatedAnyUppercaseLetter(unittest.TestCase):

    def test_any_except_uppercase_letter(self):
        self.assertEqual(str(~AnyUppercaseLetter()), "[^A-Z]")
        

class TestNegatedAnyDigit(unittest.TestCase):

    def test_any_except_digit(self):
        self.assertEqual(str(~AnyDigit()), "[^0-9]")


class TestNegatedAnyWordChar(unittest.TestCase):

    def test_any_except_word_char(self):
        self.assertEqual(str(~AnyWordChar()), "[^a-zA-Z0-9_]")


class TestNegatedAnyPunctuationChar(unittest.TestCase):

    def test_any_except_punctuation_char(self):
        self.assertEqual(str(~AnyPunctuationChar()), '[^!"#$%&\'()*+,.\/:;<=>?@\^_`{|}~\-]')


class TestNegatedAnyWhitespace(unittest.TestCase):

    def test_any_except_whitespace(self):
        self.assertEqual(str(~AnyWhitespace()), f"[^{whitespace}]")


class TestNegatedAnyWithinRange(unittest.TestCase):

    def test_any_except_within_range(self):
        for start, end in [("a", "c"), (1, 5)]:
            self.assertEqual(str(~AnyWithinRange(start, end)), f"[^{start}-{end}]")

    def test_any_except_within_range_on_invalid_range_exception(self):
        for start, end in [("z", "a"), (9, 0), ("z", 0)]:
            with self.assertRaises(InvalidRangeException):
                _ = ~AnyWithinRange(start, end)


class TestNegatedAnyFrom(unittest.TestCase):

    def test_any_except_from(self):
        tokens = ("a", "c", Backslash(), Literal("!"))
        self.assertEqual(str(~AnyFrom(*tokens)), f"[^{''.join([str(t) for t in tokens])}]")

    def test_any_except_from_on_neither_str_or_token_exception(self):
        for t in (True, 1, 1.1, Pregex("a")):
            with self.assertRaises(NeitherStringNorTokenException):
                _ = ~AnyFrom(t)

    def test_any_except_from_on_multi_char_token_exception(self):
        for t in ("aa", Literal("zzen")):
            with self.assertRaises(MultiCharTokenException):
                _ = ~AnyFrom(t)



if __name__=="__main__":
    unittest.main()