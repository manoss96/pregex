import unittest
from pregex.core.operators import *
from pregex.core.quantifiers import Exactly
from pregex.core.pre import Pregex, Empty, _Type
from pregex.core.classes import AnyLowercaseLetter
from pregex.core.assertions import FollowedBy, MatchAtStart
from pregex.core.exceptions import NotEnoughArgumentsException


TEST_STR_1 = "test1"
TEST_STR_2 = "test2"
TEST_STR_3 = "test3"


class TestConcat(unittest.TestCase):

    def test_concat_class_type(self):
        self.assertEqual(Concat("a", "b")._get_type(), _Type.Other)
    
    def test_concat_on_pattern(self):
        self.assertEqual(str(Concat(TEST_STR_1, TEST_STR_2)), f"{TEST_STR_1}{TEST_STR_2}")
        self.assertEqual(str(Concat(Pregex(TEST_STR_1), Pregex(TEST_STR_2))), f"{TEST_STR_1}{TEST_STR_2}")

    def test_concat_on_multiple_pattern(self):
        self.assertEqual(str(Concat(TEST_STR_1, TEST_STR_2, TEST_STR_3)),
            f"{TEST_STR_1}{TEST_STR_2}{TEST_STR_3}")

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

    def test_concat_on_lookaround_assertion(self):
        followed_by = FollowedBy("a", "b")
        self.assertEqual(str(Concat(followed_by, TEST_STR_1)), f"{followed_by}{TEST_STR_1}")

    def test_concat_on_empty_token(self):
        self.assertEqual(str(Concat(TEST_STR_1, Empty())), TEST_STR_1)

    def test_concat_on_not_enough_arguments_exception(self):
        self.assertRaises(NotEnoughArgumentsException, Concat, TEST_STR_1)


class TestEither(unittest.TestCase):

    def test_either_class_type(self):
        self.assertEqual(Either("a", "b")._get_type(), _Type.Alternation)
        self.assertEqual(Either("a", "|", "b")._get_type(), _Type.Alternation)
        self.assertNotEqual(("a" + Either("a", "b"))._get_type(), _Type.Alternation)
        self.assertNotEqual(("a|" + Either("a", "b"))._get_type(), _Type.Alternation)
        self.assertNotEqual((Either("a", "b") + "b")._get_type(), _Type.Alternation)
        self.assertNotEqual((Either("a", "b") + "|b")._get_type(), _Type.Alternation)
        self.assertNotEqual(("a" + Either("a", "b") + "b")._get_type(), _Type.Alternation)
        self.assertNotEqual(("a|" + Either("a", "b") + "|b")._get_type(), _Type.Alternation)

    def test_either_on_pattern(self):
        self.assertEqual(str(Either(TEST_STR_1, TEST_STR_2)), f"{TEST_STR_1}|{TEST_STR_2}")
        self.assertEqual(str(Either(Pregex(TEST_STR_1), Pregex(TEST_STR_2))), f"{TEST_STR_1}|{TEST_STR_2}")

    def test_either_on_multiple_pattern(self):
        self.assertEqual(str(Either(TEST_STR_1, TEST_STR_2, TEST_STR_3)),
            f"{TEST_STR_1}|{TEST_STR_2}|{TEST_STR_3}")

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

    def test_either_on_empty_token(self):
        self.assertEqual(str(Either(TEST_STR_1, Empty(), TEST_STR_2)), f"{TEST_STR_1}||{TEST_STR_2}")

    def test_either_on_not_enough_arguments_exception(self):
        self.assertRaises(NotEnoughArgumentsException, Either, TEST_STR_1)


class TestEnclose(unittest.TestCase):

    def test_enclose_class_type(self):
        self.assertEqual(Enclose("a", "b")._get_type(), _Type.Other)
    
    def test_enclose_on_pattern(self):
        self.assertEqual(str(Enclose(TEST_STR_1, TEST_STR_2)), f"{TEST_STR_2}{TEST_STR_1}{TEST_STR_2}")
        self.assertEqual(str(Enclose(Pregex(TEST_STR_1), Pregex(TEST_STR_2))), f"{TEST_STR_2}{TEST_STR_1}{TEST_STR_2}")

    def test_enclose_on_multiple_pattern(self):
        self.assertEqual(str(Enclose(TEST_STR_1, TEST_STR_2, TEST_STR_3)),
            f"{TEST_STR_3}{TEST_STR_2}{TEST_STR_1}{TEST_STR_2}{TEST_STR_3}")

    def test_enclose_on_empty_token(self):
        self.assertEqual(str(Enclose(TEST_STR_1, Empty())), f"{TEST_STR_1}")

    def test_enclose_on_not_enough_arguments_exception(self):
        self.assertRaises(NotEnoughArgumentsException, Enclose, TEST_STR_1)


if __name__=="__main__":
    unittest.main()