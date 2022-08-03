import unittest

from pregex.pre import Pregex
from pregex.quantifiers import *
from pregex.operators import Concat, Either
from pregex.classes import AnyLowercaseLetter
from pregex.assertions import FollowedBy, MatchAtStart
from pregex.exceptions import NeitherStringNorPregexException, NonPositiveArgumentException, \
    NegativeArgumentException, MinGreaterThanMaxException, NonIntegerArgumentException, \
    CannotBeQuantifiedException

TEST_STR_LEN_1 = "t"
TEST_STR_LEN_N = "test"
TEST_LITERAL_LEN_1 = Pregex(TEST_STR_LEN_1)
TEST_LITERAL_LEN_N = Pregex(TEST_STR_LEN_N)

class Test__Quantifier(unittest.TestCase):

    def test_neither_pregex_nor_str(self):
        for arg in (1, 1.56, True):
            self.assertRaises(NeitherStringNorPregexException, Indefinite, arg)

    def test_quantifier_on_str(self):
        self.assertEqual(str(Optional(TEST_STR_LEN_N)), f"(?:{TEST_STR_LEN_N})?")

    def test_quantifier_on_literal(self):
        self.assertEqual(str(Optional(TEST_LITERAL_LEN_N)), f"(?:{TEST_LITERAL_LEN_N})?")

    def test_quantifier_on_concat(self):
        concat = Concat(TEST_STR_LEN_1, TEST_STR_LEN_N)
        self.assertEqual(str(Optional(concat)), f"(?:{concat})?")

    def test_quantifier_on_either(self):
        either = Either(TEST_STR_LEN_1, TEST_STR_LEN_N)
        self.assertEqual(str(Optional(either)), f"(?:{either})?")

    def test_quantifier_on_class(self):
        any_ll = AnyLowercaseLetter()
        self.assertEqual(str(Optional(any_ll)), f"{any_ll}?")

    def test_quantifier_on_quantifier_exception(self):
        optional = Optional(TEST_STR_LEN_N)
        self.assertEqual(str(Optional(optional)), f"(?:{optional})?")

    def test_quantifier_on_anchor_assertion_exception(self):
        mat = MatchAtStart("a")
        self.assertRaises(CannotBeQuantifiedException, Optional, mat)

    def test_quantifier_on_look_around_assertion(self):
        followed_by = FollowedBy("a", "b")
        self.assertRaises(CannotBeQuantifiedException, Optional, followed_by)


class TestOptional(unittest.TestCase):
    
    def test_optional_on_len_1_str(self):
        self.assertEqual(str(Optional(TEST_STR_LEN_1)), f"{TEST_STR_LEN_1}?")

    def test_optional_on_len_n_str(self):
        self.assertEqual(str(Optional(TEST_STR_LEN_N)), f"(?:{TEST_STR_LEN_N})?")

    def test_optional_on_len_1_literal(self):
        self.assertEqual(str(Optional(TEST_LITERAL_LEN_1)), f"{TEST_STR_LEN_1}?")

    def test_optional_on_len_n_literal(self):
        self.assertEqual(str(Optional(TEST_LITERAL_LEN_N)), f"(?:{TEST_STR_LEN_N})?")

    def test_optional_on_laziness(self):
        self.assertEqual(str(Optional(TEST_LITERAL_LEN_N, is_greedy=False)), f"(?:{TEST_STR_LEN_N})??")

    def test_optional_on_match(self):
        self.assertTrue(("a" + Optional("a") + "a").get_matches("aaa") == ["aaa"])
        self.assertTrue(("a" + Optional("a") + "a").get_matches("aa") == ["aa"])

    def test_optional_on_lazy_match(self):
        self.assertTrue(("a" + Optional("a", is_greedy=False) + "a").get_matches("aaa") == ["aa"])


class TestIndefinite(unittest.TestCase):
    
    def test_indefinite_on_len_1_str(self):
        self.assertEqual(str(Indefinite(TEST_STR_LEN_1)), f"{TEST_STR_LEN_1}*")

    def test_indefinite_on_len_n_str(self):
        self.assertEqual(str(Indefinite(TEST_STR_LEN_N)), f"(?:{TEST_STR_LEN_N})*")

    def test_indefinite_on_len_1_literal(self):
        self.assertEqual(str(Indefinite(TEST_LITERAL_LEN_1)), f"{TEST_STR_LEN_1}*")

    def test_indefinite_on_len_n_literal(self):
        self.assertEqual(str(Indefinite(TEST_LITERAL_LEN_N)), f"(?:{TEST_STR_LEN_N})*")

    def test_indefinite_on_laziness(self):
        self.assertEqual(str(Indefinite(TEST_LITERAL_LEN_N, is_greedy=False)), f"(?:{TEST_STR_LEN_N})*?")


class TestOneOrMore(unittest.TestCase):
    
    def test_one_or_more_on_len_1_str(self):
        self.assertEqual(str(OneOrMore(TEST_STR_LEN_1)), f"{TEST_STR_LEN_1}+")

    def test_one_or_more_on_len_n_str(self):
        self.assertEqual(str(OneOrMore(TEST_STR_LEN_N)), f"(?:{TEST_STR_LEN_N})+")

    def test_one_or_more_on_len_1_literal(self):
        self.assertEqual(str(OneOrMore(TEST_LITERAL_LEN_1)), f"{TEST_STR_LEN_1}+")

    def test_one_or_more_on_len_n_literal(self):
        self.assertEqual(str(OneOrMore(TEST_LITERAL_LEN_N)), f"(?:{TEST_STR_LEN_N})+")

    def test_one_or_more_on_laziness(self):
        self.assertEqual(str(OneOrMore(TEST_LITERAL_LEN_N, is_greedy=False)), f"(?:{TEST_STR_LEN_N})+?")
        

class TestExactly(unittest.TestCase):

    VALID_VALUES = [2, 10]
    
    def test_exactly_on_len_1_str(self):
        for val in self.VALID_VALUES:
            self.assertEqual(str(Exactly(TEST_STR_LEN_1, val)), f"{TEST_STR_LEN_1}{{{val}}}")

    def test_exactly_on_len_n_str(self):
        for val in self.VALID_VALUES:
            self.assertEqual(str(Exactly(TEST_STR_LEN_N, val)), f"(?:{TEST_STR_LEN_N}){{{val}}}")

    def test_exactly_on_len_1_literal(self):
        for val in self.VALID_VALUES:
            self.assertEqual(str(Exactly(TEST_LITERAL_LEN_1, val)), f"{TEST_LITERAL_LEN_1}{{{val}}}")

    def test_exactly_on_len_n_literal(self):
        for val in self.VALID_VALUES:
            self.assertEqual(str(Exactly(TEST_LITERAL_LEN_N, val)), f"(?:{TEST_LITERAL_LEN_N}){{{val}}}")

    def test_exactly_on_value_1(self):
        val = 1
        self.assertEqual(str(Exactly(TEST_LITERAL_LEN_N, val)), f"{TEST_LITERAL_LEN_N}")

    def test_exactly_on_invalid_type_values(self):
        for val in ["s", 1.1, True]:
            self.assertRaises(NonIntegerArgumentException, Exactly, TEST_STR_LEN_1, val)

    def test_exactly_on_invalid_values(self):
        for val in [-10, -1, 0]:
            self.assertRaises(NonPositiveArgumentException, Exactly, TEST_STR_LEN_1, val)

class TestAtLeast(unittest.TestCase):

    VALID_VALUES = [2, 10]
    
    def test_at_least_on_len_1_str(self):
        for val in self.VALID_VALUES:
            self.assertEqual(str(AtLeast(TEST_STR_LEN_1, val)), f"{TEST_STR_LEN_1}{{{val},}}")

    def test_at_least_on_len_n_str(self):
        for val in self.VALID_VALUES:
            self.assertEqual(str(AtLeast(TEST_STR_LEN_N, val)), f"(?:{TEST_STR_LEN_N}){{{val},}}")

    def test_at_least_on_len_1_literal(self):
        for val in self.VALID_VALUES:
            self.assertEqual(str(AtLeast(TEST_LITERAL_LEN_1, val)), f"{TEST_LITERAL_LEN_1}{{{val},}}")

    def test_at_least_on_len_n_literal(self):
        for val in self.VALID_VALUES:
            self.assertEqual(str(AtLeast(TEST_LITERAL_LEN_N, val)), f"(?:{TEST_LITERAL_LEN_N}){{{val},}}") 

    def test_at_least_on_value_0(self):
        val = 0
        self.assertEqual(str(AtLeast(TEST_LITERAL_LEN_N, val)), f"(?:{TEST_LITERAL_LEN_N})*")  

    def test_at_least_on_value_1(self):
        val = 1
        self.assertEqual(str(AtLeast(TEST_LITERAL_LEN_N, val)), f"(?:{TEST_LITERAL_LEN_N})+")

    def test_at_least_on_laziness(self):
        val = 3
        self.assertEqual(str(AtLeast(TEST_LITERAL_LEN_N, val, is_greedy=False)), f"(?:{TEST_LITERAL_LEN_N}){{{val},}}?")

    def test_at_least_on_invalid_type_values(self):
        for val in ["s", 1.1, True]:
            self.assertRaises(NonIntegerArgumentException, AtLeast, TEST_STR_LEN_1, val)

    def test_at_least_on_invalid_values(self):
        for val in [-10, -1]:
            self.assertRaises(NegativeArgumentException, AtLeast, TEST_STR_LEN_1, val)

class TestAtMost(unittest.TestCase):

    VALID_VALUES = [2, 10]
    
    def test_at_most_on_len_1_str(self):
        for val in self.VALID_VALUES:
            self.assertEqual(str(AtMost(TEST_STR_LEN_1, val)), f"{TEST_STR_LEN_1}{{,{val}}}")

    def test_at_most_on_len_n_str(self):
        for val in self.VALID_VALUES:
            self.assertEqual(str(AtMost(TEST_STR_LEN_N, val)), f"(?:{TEST_STR_LEN_N}){{,{val}}}")

    def test_at_most_on_len_1_literal(self):
        for val in self.VALID_VALUES:
            self.assertEqual(str(AtMost(TEST_LITERAL_LEN_1, val)), f"{TEST_LITERAL_LEN_1}{{,{val}}}")

    def test_at_most_on_len_n_literal(self):
        for val in self.VALID_VALUES:
            self.assertEqual(str(AtMost(TEST_LITERAL_LEN_N, val)), f"(?:{TEST_LITERAL_LEN_N}){{,{val}}}") 

    def test_at_most_on_value_1(self):
        val = 1
        self.assertEqual(str(AtMost(TEST_LITERAL_LEN_N, val)), f"(?:{TEST_LITERAL_LEN_N})?")

    def test_at_most_on_laziness(self):
        val = 3
        self.assertEqual(str(AtMost(TEST_LITERAL_LEN_N, val, is_greedy=False)), f"(?:{TEST_LITERAL_LEN_N}){{,{val}}}?")

    def test_at_most_on_invalid_type_values(self):
        for val in ["s", 1.1, True]:
            self.assertRaises(NonIntegerArgumentException, AtMost, TEST_STR_LEN_1, val)

    def test_at_most_on_invalid_values(self):
        for val in [-10, -1, 0]:
            self.assertRaises(NonPositiveArgumentException, AtMost, TEST_STR_LEN_1, val)

class TestAtLeastAtMost(unittest.TestCase):

    VALID_VALUES = [(2, 3), (10, 20)]
    
    def test_at_least_at_most_on_len_1_str(self):
        for min, max in self.VALID_VALUES:
            self.assertEqual(str(AtLeastAtMost(TEST_STR_LEN_1, min, max)), f"{TEST_STR_LEN_1}{{{min},{max}}}")

    def test_at_least_at_most_on_len_n_str(self):
        for min, max in self.VALID_VALUES:
            self.assertEqual(str(AtLeastAtMost(TEST_STR_LEN_N, min, max)), f"(?:{TEST_STR_LEN_N}){{{min},{max}}}")

    def test_at_least_at_most_on_len_1_literal(self):
        for min, max in self.VALID_VALUES:
            self.assertEqual(str(AtLeastAtMost(TEST_LITERAL_LEN_1, min, max)), f"{TEST_LITERAL_LEN_1}{{{min},{max}}}")

    def test_at_least_at_most_on_len_n_literal(self):
        for min, max in self.VALID_VALUES:
            self.assertEqual(str(AtLeastAtMost(TEST_LITERAL_LEN_N, min, max)), f"(?:{TEST_LITERAL_LEN_N}){{{min},{max}}}")

    def test_at_least_at_most_on_min_equal_to_max(self):
        min, max = 4, 4
        self.assertEqual(str(AtLeastAtMost(TEST_LITERAL_LEN_N, min, max)), f"(?:{TEST_LITERAL_LEN_N}){{{min}}}")

    def test_at_least_at_most_on_laziness(self):
        min, max = 3, 5
        self.assertEqual(str(AtLeastAtMost(TEST_LITERAL_LEN_N, min, max, is_greedy=False)), f"(?:{TEST_LITERAL_LEN_N}){{{min},{max}}}?")

    def test_at_least_at_most_on_invalid_type_values(self):
        for val in ["s", 1.1, True]:
            self.assertRaises(NonIntegerArgumentException, AtLeastAtMost, TEST_STR_LEN_1, min=val, max=10)
            self.assertRaises(NonIntegerArgumentException, AtLeastAtMost, TEST_STR_LEN_1, min=2, max=val)

    def test_at_least_at_most_on_negative_min(self):
        min, max = -1, 1
        self.assertRaises(NegativeArgumentException, AtLeastAtMost, TEST_STR_LEN_1, min, max) 

    def test_at_least_at_most_on_non_positive_max(self):
        min, max = 0, 0
        self.assertRaises(NonPositiveArgumentException, AtLeastAtMost, TEST_STR_LEN_1, min, max) 

    def test_at_least_at_most_on_non_positive_max(self):
        min, max = 5, 3
        self.assertRaises(MinGreaterThanMaxException, AtLeastAtMost, TEST_STR_LEN_1, min, max)


if __name__=="__main__":
    unittest.main()