import unittest
from pregex.core.quantifiers import *
from pregex.core.pre import Pregex, _Type
from pregex.core.operators import Concat, Either
from pregex.core.classes import AnyLowercaseLetter
from pregex.core.assertions import MatchAtStart
from pregex.core.exceptions import InvalidArgumentTypeException, \
    InvalidArgumentValueException, CannotBeQuantifiedException


TEST_STR_LEN_1 = "t"
TEST_STR_LEN_N = "test"
TEST_LITERAL_LEN_1 = Pregex(TEST_STR_LEN_1)
TEST_LITERAL_LEN_N = Pregex(TEST_STR_LEN_N)


class Test__Quantifier(unittest.TestCase):

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

    def test_quantifier_on_assertion_exception(self):
        mat = MatchAtStart("a")
        self.assertRaises(CannotBeQuantifiedException, Indefinite, mat)
        try:
            _ = Optional(mat)
        except CannotBeQuantifiedException:
            self.fail("Applying \"Optional\" on an assertion raised an exception!")


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

    def test_optional_on_type(self):
        self.assertEqual(Optional("a")._get_type(), _Type.Quantifier)
        self.assertEqual(Optional("abc")._get_type(), _Type.Quantifier)
        self.assertNotEqual(Pregex("abc?", escape=False)._get_type(), _Type.Quantifier)

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

    def test_indefinite_on_type(self):
        self.assertEqual(Indefinite("a")._get_type(), _Type.Quantifier)
        self.assertEqual(Indefinite("abc")._get_type(), _Type.Quantifier)
        self.assertNotEqual(Pregex("abc*", escape=False)._get_type(), _Type.Quantifier)


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

    def test_one_or_more_on_type(self):
        self.assertEqual(OneOrMore("a")._get_type(), _Type.Quantifier)
        self.assertEqual(OneOrMore("abc")._get_type(), _Type.Quantifier)
        self.assertNotEqual(Pregex("abc+", escape=False)._get_type(), _Type.Quantifier)
        

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
        self.assertEqual(str(Exactly(TEST_LITERAL_LEN_N, 1)), f"{TEST_LITERAL_LEN_N}")

    def test_exactly_on_value_0(self):
        self.assertEqual(str(Exactly(TEST_LITERAL_LEN_N, 0)), "")

    def test_exactly_on_type(self):
        self.assertEqual(Exactly("a", n=2)._get_type(), _Type.Quantifier)
        self.assertEqual(Exactly("abc", n=2)._get_type(), _Type.Quantifier)
        self.assertNotEqual(Pregex("abc{2}", escape=False)._get_type(), _Type.Quantifier)

    def test_exactly_on_invalid_argument_type_exception(self):
        for val in ["s", 1.1, True]:
            self.assertRaises(InvalidArgumentTypeException, Exactly, TEST_STR_LEN_1, val)

    def test_exactly_on_invalid_argument_value_exception(self):
        for val in [-10, -1]:
            self.assertRaises(InvalidArgumentValueException, Exactly, TEST_STR_LEN_1, val)

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

    def test_at_least_on_value_0(self):
        val = 0
        self.assertEqual(str(AtLeast(TEST_LITERAL_LEN_N, val, is_greedy=False)), f"(?:{TEST_LITERAL_LEN_N})*?")  

    def test_at_least_on_lazy_value_1(self):
        val = 1
        self.assertEqual(str(AtLeast(TEST_LITERAL_LEN_N, val, is_greedy=False)), f"(?:{TEST_LITERAL_LEN_N})+?")

    def test_at_least_on_type(self):
        self.assertEqual(AtLeast("a", n=2)._get_type(), _Type.Quantifier)
        self.assertEqual(AtLeast("abc", n=2)._get_type(), _Type.Quantifier)
        self.assertNotEqual(Pregex("abc{2,}", escape=False)._get_type(), _Type.Quantifier)

    def test_at_least_on_invalid_argument_type_exception(self):
        for val in ["s", 1.1, True]:
            self.assertRaises(InvalidArgumentTypeException, AtLeast, TEST_STR_LEN_1, val)

    def test_at_least_on_invalid_argument_value_exception(self):
        for val in [-10, -1]:
            self.assertRaises(InvalidArgumentValueException, AtLeast, TEST_STR_LEN_1, val)


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

    def test_at_most_on_value_0(self):
        val = 0
        self.assertEqual(str(AtMost(TEST_LITERAL_LEN_N, val)), "")

    def test_at_most_on_value_1(self):
        val = 1
        self.assertEqual(str(AtMost(TEST_LITERAL_LEN_N, val)), f"(?:{TEST_LITERAL_LEN_N})?")

    def test_at_most_on_value_None(self):
        val = None
        self.assertEqual(str(AtMost(TEST_LITERAL_LEN_N, val)), f"(?:{TEST_LITERAL_LEN_N})*")

    def test_at_most_on_laziness(self):
        val = 3
        self.assertEqual(str(AtMost(TEST_LITERAL_LEN_N, val, is_greedy=False)), f"(?:{TEST_LITERAL_LEN_N}){{,{val}}}?")

    def test_at_most_on_lazy_value_1(self):
        val = 1
        self.assertEqual(str(AtMost(TEST_LITERAL_LEN_N, val, is_greedy=False)), f"(?:{TEST_LITERAL_LEN_N})??")

    def test_at_most_on_lazy_value_None(self):
        val = None
        self.assertEqual(str(AtMost(TEST_LITERAL_LEN_N, val, is_greedy=False)), f"(?:{TEST_LITERAL_LEN_N})*?")

    def test_at_most_on_type(self):
        self.assertEqual(AtMost("a", n=2)._get_type(), _Type.Quantifier)
        self.assertEqual(AtMost("abc", n=2)._get_type(), _Type.Quantifier)
        self.assertNotEqual(Pregex("abc{,2}", escape=False)._get_type(), _Type.Quantifier)

    def test_at_most_on_invalid_argument_type_exception(self):
        for val in ["s", 1.1, True]:
            self.assertRaises(InvalidArgumentTypeException, AtMost, TEST_STR_LEN_1, val)

    def test_at_most_on_invalid_argument_value_exception(self):
        for val in [-10, -1]:
            self.assertRaises(InvalidArgumentValueException, AtMost, TEST_STR_LEN_1, val)

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

    def test_at_least_at_most_on_min_equal_to_max_equal_to_zero(self):
        min, max = 0, 0
        self.assertEqual(str(AtLeastAtMost(TEST_LITERAL_LEN_N, min, max)), "")

    def test_at_least_at_most_on_min_equal_to_zero_max_equal_to_1(self):
        min, max = 0, 1
        self.assertEqual(str(AtLeastAtMost(TEST_LITERAL_LEN_N, min, max)), f"(?:{TEST_LITERAL_LEN_N})?")

    def test_at_least_at_most_on_min_equal_to_zero_max_greater_than_1(self):
        min, max = 0, 2
        self.assertEqual(str(AtLeastAtMost(TEST_LITERAL_LEN_N, min, max)), f"(?:{TEST_LITERAL_LEN_N}){{,{max}}}")

    def test_at_least_at_most_on_min_equal_to_zero_max_equal_to_None(self):
        min, max = 0, None
        self.assertEqual(str(AtLeastAtMost(TEST_LITERAL_LEN_N, min, max)), f"(?:{TEST_LITERAL_LEN_N})*")

    def test_at_least_at_most_on_min_equal_to_max_equal_to_one(self):
        min, max = 1, 1
        self.assertEqual(str(AtLeastAtMost(TEST_LITERAL_LEN_N, min, max)), str(TEST_LITERAL_LEN_N))

    def test_at_least_at_most_on_min_equal_to_one_max_equal_to_None(self):
        min, max = 1, None
        self.assertEqual(str(AtLeastAtMost(TEST_LITERAL_LEN_N, min, max)), f"(?:{TEST_LITERAL_LEN_N})+")

    def test_at_least_at_most_on_min_equal_to_max(self):
        min, max = 2, 2
        self.assertEqual(str(AtLeastAtMost(TEST_LITERAL_LEN_N, min, max)), f"(?:{TEST_LITERAL_LEN_N}){{{min}}}")

    def test_at_least_at_most_on_min_equal_to_two_max_equal_to_None(self):
        min, max = 2, None
        self.assertEqual(str(AtLeastAtMost(TEST_LITERAL_LEN_N, min, max)), f"(?:{TEST_LITERAL_LEN_N}){{{min},}}")

    def test_at_least_at_most_on_laziness(self):
        min, max = 3, 5
        self.assertEqual(str(AtLeastAtMost(TEST_LITERAL_LEN_N, min, max, is_greedy=False)),
            f"(?:{TEST_LITERAL_LEN_N}){{{min},{max}}}?")

    def test_at_least_at_most_on_lazy_min_equal_to_zero_max_equal_to_1(self):
        min, max = 0, 1
        self.assertEqual(str(AtLeastAtMost(TEST_LITERAL_LEN_N, min, max, is_greedy=False)), f"(?:{TEST_LITERAL_LEN_N})??")

    def test_at_least_at_most_on_lazy_min_equal_to_zero_max_greater_than_1(self):
        min, max = 0, 2
        self.assertEqual(str(AtLeastAtMost(TEST_LITERAL_LEN_N, min, max, is_greedy=False)), f"(?:{TEST_LITERAL_LEN_N}){{,{max}}}?")

    def test_at_least_at_most_on_lazy_min_equal_to_zero_max_equal_to_None(self):
        min, max = 0, None
        self.assertEqual(str(AtLeastAtMost(TEST_LITERAL_LEN_N, min, max, is_greedy=False)),
            f"(?:{TEST_LITERAL_LEN_N})*?")

    def test_at_least_at_most_on_lazy_min_equal_to_one_max_equal_to_None(self):
        min, max = 1, None
        self.assertEqual(str(AtLeastAtMost(TEST_LITERAL_LEN_N, min, max, is_greedy=False)),
        f"(?:{TEST_LITERAL_LEN_N})+?")

    def test_at_least_at_most_on_lazy_min_equal_to_two_max_equal_to_None(self):
        min, max = 2, None
        self.assertEqual(str(AtLeastAtMost(TEST_LITERAL_LEN_N, min, max, is_greedy=False)),
            f"(?:{TEST_LITERAL_LEN_N}){{{min},}}?")

    def test_at_least_at_most_on_lazy_min_equal_to_max(self):
        min, max = 2, 2
        self.assertEqual(str(AtLeastAtMost(TEST_LITERAL_LEN_N, min, max, is_greedy=False)), f"(?:{TEST_LITERAL_LEN_N}){{{min}}}")

    def test_at_least_at_most_on_type(self):
        self.assertEqual(AtLeastAtMost("a", min=1, max=2)._get_type(), _Type.Quantifier)
        self.assertEqual(AtLeastAtMost("abc", min=1, max=2)._get_type(), _Type.Quantifier)
        self.assertNotEqual(Pregex("abc{1,2}", escape=False)._get_type(), _Type.Quantifier)

    def test_at_least_at_most_on_invalid_argument_type_exception(self):
        for val in ["s", 1.1, True]:
            self.assertRaises(InvalidArgumentTypeException, AtLeastAtMost, TEST_STR_LEN_1, min=val, max=10)
            self.assertRaises(InvalidArgumentTypeException, AtLeastAtMost, TEST_STR_LEN_1, min=2, max=val)

    def test_at_least_at_most_on_invalid_argument_value_exception(self):
        self.assertRaises(InvalidArgumentValueException, AtLeastAtMost, TEST_STR_LEN_1, min=-1, max=1)
        self.assertRaises(InvalidArgumentValueException, AtLeastAtMost, TEST_STR_LEN_1, min=1, max=-1)
        self.assertRaises(InvalidArgumentValueException, AtLeastAtMost, TEST_STR_LEN_1, min=5, max=3)


if __name__=="__main__":
    unittest.main()