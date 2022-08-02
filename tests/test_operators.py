import unittest
from pregex.pre import Pregex
from pregex.operators import *
from pregex.quantifiers import Exactly
from pregex.classes import AnyLowercaseLetter
from pregex.assertions import FollowedBy, MatchAtStart
from pregex.exceptions import LessThanTwoArgumentsException


TEST_STR_1 = "test1"
TEST_STR_2 = "test2"
TEST_STR_3 = "test3"


class Test__Operator(unittest.TestCase):

    def test_operator_on_few_arguments(self):
        self.assertRaises(LessThanTwoArgumentsException, Concat, TEST_STR_1)


class TestConcat(unittest.TestCase):
    
    def test_concat_on_str(self):
        self.assertEqual(str(Concat(TEST_STR_1, TEST_STR_1)), f"{TEST_STR_1}{TEST_STR_1}")

    def test_concat_on_literal(self):
        self.assertEqual(str(Concat(Pregex(TEST_STR_1), TEST_STR_2)), f"{TEST_STR_1}{TEST_STR_2}")

    def test_concat_on_quantifier(self):
        quantifier = Exactly(TEST_STR_1, 2)
        self.assertEqual(str(Concat(quantifier, TEST_STR_2)), f"{quantifier}{TEST_STR_2}")

    def test_concat_on_concat(self):
        concat = Concat(TEST_STR_1, TEST_STR_2)
        self.assertEqual(str(Concat(concat, TEST_STR_3)), f"{concat}{TEST_STR_3}")

    def test_concat_on_either(self):
        either = Either(TEST_STR_1, TEST_STR_2)
        self.assertEqual(str(Concat(either, TEST_STR_3)), f"(?:{either}){TEST_STR_3}")

    def test_concat_on_class(self):
        any_ll = AnyLowercaseLetter()
        self.assertEqual(str(Concat(any_ll, TEST_STR_3)), f"{any_ll}{TEST_STR_3}")

    def test_concat_on_anchor_assertion(self):
        mat = MatchAtStart("a")
        self.assertEqual(str(Concat(mat, TEST_STR_1)), f"{mat}{TEST_STR_1}")

    def test_quantifier_on_lookaround_assertion(self):
        followed_by = FollowedBy("a", "b")
        self.assertEqual(str(Concat(followed_by, TEST_STR_1)), f"{followed_by}{TEST_STR_1}")



class TestEither(unittest.TestCase):

    def test_either_on_str(self):
        self.assertEqual(str(Either(TEST_STR_1, TEST_STR_1)), f"{TEST_STR_1}|{TEST_STR_1}")

    def test_either_on_literal(self):
        self.assertEqual(str(Either(Pregex(TEST_STR_1), TEST_STR_2)), f"{TEST_STR_1}|{TEST_STR_2}")

    def test_either_on_quantifier(self):
        quantifier = Exactly(TEST_STR_1, 2)
        self.assertEqual(str(Either(quantifier, TEST_STR_2)), f"{quantifier}|{TEST_STR_2}")

    def test_either_for_concat(self):
        concat = Concat(TEST_STR_1, TEST_STR_2)
        self.assertEqual(str(Either(concat, TEST_STR_3)), f"{concat}|{TEST_STR_3}")

    def test_either_on_either(self):
        either = Either(TEST_STR_1, TEST_STR_2)
        self.assertEqual(str(Either(either, TEST_STR_3)), f"{either}|{TEST_STR_3}")

    def test_either_on_class(self):
        any_ll = AnyLowercaseLetter()
        self.assertEqual(str(Either(any_ll, TEST_STR_3)), f"{any_ll}|{TEST_STR_3}")


if __name__=="__main__":
    unittest.main()