import unittest
from pregex.pre import Pregex
from pregex.classes import *
from string import whitespace
from itertools import permutations
from pregex.tokens import Backslash, Literal
from pregex.exceptions import NeitherStringNorTokenException, MultiCharTokenException, \
    CannotBeCombinedException, InvalidRangeException


def get_permutations(*classes: str):
    return set(f"[{''.join(p)}]" for p in permutations(classes))

def get_negated_permutations(*classes: str):
    return set(f"[^{''.join(p)}]" for p in permutations(classes))


class Test__Class(unittest.TestCase):

    def test_any_class_bitwise_or(self):
        self.assertTrue(str(AnyLowercaseLetter() | AnyDigit()) \
            in get_permutations("a-z", "\d"))
        self.assertTrue(str(AnyFrom("a", "b") | AnyFrom("c", "d")) \
            in get_permutations("a", "b", "c", "d"))

    def test_any_class_bitwise_or_with_subset(self):
        self.assertTrue(str(AnyLetter() | AnyLowercaseLetter()) \
            in get_permutations("a-z", "A-Z"))
        self.assertTrue(str(AnyFrom("a", "b", "c") | AnyFrom("a", "b")) \
            in get_permutations("a", "b", "c"))

    def test_any_class_bitwise_or_with_intersection(self):
        self.assertTrue(str(AnyFrom("a", "b") | AnyFrom("b", "c")) \
            in get_permutations("a", "b", "c"))

    def test_any_class_bitwise_or_with_overlapping_ranges(self):
        self.assertTrue(str(AnyWithinRange("a", "d") | AnyWithinRange("b", "k")) == "[a-k]")
        self.assertTrue(str(AnyWithinRange("a", "d") | AnyWithinRange("e", "k")) == "[a-k]")
        self.assertTrue(str(AnyWithinRange("A", "D") | AnyWithinRange("B", "K")) == "[A-K]")
        self.assertTrue(str(AnyWithinRange("A", "D") | AnyWithinRange("E", "K")) == "[A-K]")
        self.assertTrue(str(AnyWithinRange("0", "3") | AnyWithinRange("2", "7")) == "[0-7]")
        self.assertTrue(str(AnyWithinRange("0", "3") | AnyWithinRange("4", "7")) == "[0-7]")

    def test_any_class_bitwise_or_on_cannot_be_combined_exception(self):
        any_letter, any_but_digit = AnyLetter(), ~AnyDigit()
        self.assertRaises(CannotBeCombinedException, any_letter.__or__, any_but_digit)
        self.assertRaises(CannotBeCombinedException, any_letter.__ror__, any_but_digit)


class TestNegated__Class(unittest.TestCase):
    
    def test_any_but_class_bitwise_or(self):
        self.assertTrue(str(~AnyLowercaseLetter() | ~AnyDigit()) \
            in get_negated_permutations("a-z", "\d"))
        self.assertTrue(str(~AnyFrom("a", "b") | ~AnyFrom("c", "d")) \
            in get_negated_permutations("a", "b", "c", "d"))

    def test_any_but_class_bitwise_or_with_subset(self):
        self.assertTrue(str(~AnyLetter() | ~AnyLowercaseLetter()) \
            in get_negated_permutations("a-z", "A-Z"))
        self.assertTrue(str(~AnyFrom("a", "b", "c") | ~AnyFrom("a", "b")) \
            in get_negated_permutations("a", "b", "c"))

    def test_any_but_class_bitwise_or_with_intersection(self):
        self.assertTrue(str(~AnyFrom("a", "b") | ~AnyFrom("b", "c")) \
            in get_negated_permutations("a", "b", "c"))

    def test_any_but_class_bitwise_or_with_overlapping_ranges(self):
        self.assertTrue(str(AnyButWithinRange("a", "d") | AnyButWithinRange("b", "k")) == "[^a-k]")
        self.assertTrue(str(AnyButWithinRange("a", "d") | AnyButWithinRange("d", "k")) == "[^a-k]")
        self.assertTrue(str(AnyButWithinRange("A", "D") | AnyButWithinRange("B", "K")) == "[^A-K]")
        self.assertTrue(str(AnyButWithinRange("A", "D") | AnyButWithinRange("E", "K")) == "[^A-K]")
        self.assertTrue(str(AnyButWithinRange("0", "3") | AnyButWithinRange("2", "7")) == "[^0-7]")
        self.assertTrue(str(AnyButWithinRange("0", "3") | AnyButWithinRange("4", "7")) == "[^0-7]")

    def test_any_but_class_bitwise_or_on_cannot_be_combined_exception(self):
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
        self.assertEqual(str(AnyDigit()), "[\d]")


class TestAnyWordChar(unittest.TestCase):

    def test_any_word_char(self):
        self.assertEqual(str(AnyWordChar()), "[\w]")

    def test_any_word_char_combine_with_subsets(self):
        self.assertEqual(str(AnyWordChar() | (AnyLetter() | AnyDigit())), "[\w]")
        self.assertEqual(str(AnyWordChar() | AnyLetter()), "[\w]")
        self.assertEqual(str(AnyWordChar() | AnyLowercaseLetter()), "[\w]")
        self.assertEqual(str(AnyWordChar() | AnyUppercaseLetter()), "[\w]")
        self.assertEqual(str(AnyWordChar() | AnyDigit()), "[\w]")

    def test_any_word_char_result_from_subsets(self):
        self.assertEqual(str(AnyLetter() | (AnyDigit() | AnyFrom("_"))), "[\w]")


class TestAnyPunctuation(unittest.TestCase):

    def test_any_punctuation(self):
        self.assertEqual(str(AnyPunctuation()), '[\^\-\[\]!"#$%&\'()*+,./:;<=>?@_`{|}~\\\\]')


class TestAnyWhitespace(unittest.TestCase):

    def test_any_whitespace(self):
        self.assertEqual(str(AnyWhitespace()), "[\s]")

    def test_any_whitespace_combine_with_subsets(self):
        self.assertEqual(str(AnyWhitespace() | AnyFrom(" ", "\r")), "[\s]")

    def test_any_whitespace_result_from_subsets(self):
        self.assertEqual(str(AnyFrom(' ', '\t', '\n', '\r', '\x0b') | AnyFrom('\x0c')), "[\s]")


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

    def test_any_but_letter(self):
        pattern = "[^a-zA-Z]"
        self.assertEqual(str(~AnyLetter()), pattern)
        self.assertEqual(str(AnyButLetter()), pattern)


class TestNegatedAnyLowercaseLetter(unittest.TestCase):

    def test_any_but_lowercase_letter(self):
        pattern = "[^a-z]"
        self.assertEqual(str(~AnyLowercaseLetter()), pattern)
        self.assertEqual(str(AnyButLowercaseLetter()), pattern)


class TestNegatedAnyUppercaseLetter(unittest.TestCase):

    def test_any_but_uppercase_letter(self):
        pattern = "[^A-Z]"
        self.assertEqual(str(~AnyUppercaseLetter()), pattern)
        self.assertEqual(str(AnyButUppercaseLetter()), pattern)
        

class TestNegatedAnyDigit(unittest.TestCase):

    def test_any_but_digit(self):
        pattern = "[^\d]"
        self.assertEqual(str(~AnyDigit()), pattern)
        self.assertEqual(str(AnyButDigit()), pattern)


class TestNegatedAnyWordChar(unittest.TestCase):

    def test_any_but_word_char(self):
        pattern = "[^\w]"
        self.assertEqual(str(~AnyWordChar()), pattern)
        self.assertEqual(str(AnyButWordChar()), pattern)


class TestNegatedAnyPunctuation(unittest.TestCase):

    def test_any_but_punctuation_char(self):
        pattern = '[^\^\-\[\]!"#$%&\'()*+,./:;<=>?@_`{|}~\\\\]'
        self.assertEqual(str(~AnyPunctuation()), pattern)
        self.assertEqual(str(AnyButPunctuation()), pattern)


class TestNegatedAnyWhitespace(unittest.TestCase):

    def test_any_but_whitespace(self):
        pattern = "[^\s]"
        self.assertEqual(str(~AnyWhitespace()), pattern)
        self.assertEqual(str(AnyButWhitespace()), pattern)


class TestNegatedAnyWithinRange(unittest.TestCase):

    def test_any_but_within_range(self):
        for start, end in [("a", "c"), (1, 5)]:
            self.assertEqual(str(~AnyWithinRange(start, end)), f"[^{start}-{end}]")
            self.assertEqual(str(AnyButWithinRange(start, end)), f"[^{start}-{end}]")

    def test_any_but_within_range_on_invalid_range_exception(self):
        for start, end in [("z", "a"), (9, 0), ("z", 0)]:
            with self.assertRaises(InvalidRangeException):
                _ = ~AnyWithinRange(start, end)
            self.assertRaises(InvalidRangeException, AnyButWithinRange, start, end)


class TestNegatedAnyFrom(unittest.TestCase):

    def test_any_but_from(self):
        tokens = ("a", "c", Backslash(), Literal("!"))
        self.assertEqual(str(~AnyFrom(*tokens)), f"[^{''.join([str(t) for t in tokens])}]")
        self.assertEqual(str(AnyButFrom(*tokens)), f"[^{''.join([str(t) for t in tokens])}]")

    def test_any_but_from_on_neither_str_or_token_exception(self):
        for t in (True, 1, 1.1, Pregex("a")):
            with self.assertRaises(NeitherStringNorTokenException):
                _ = ~AnyFrom(t)
            self.assertRaises(NeitherStringNorTokenException, AnyButFrom, t)

    def test_any_but_from_on_multi_char_token_exception(self):
        for t in ("aa", Literal("zzen")):
            with self.assertRaises(MultiCharTokenException):
                _ = ~AnyFrom(t)
            self.assertRaises(MultiCharTokenException, AnyButFrom, t)



if __name__=="__main__":
    unittest.main()