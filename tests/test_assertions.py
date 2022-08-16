import unittest
from pregex.assertions import *
from pregex.pre import Pregex, Empty, _Type
from pregex.quantifiers import Exactly, Optional
from pregex.exceptions import NonFixedWidthPatternException, \
    NotEnoughArgumentsException, EmptyNegativeAssertionException


TEST_STR = "test"
pre1 = Pregex("PRE1")
pre2 = Pregex("PRE2")
pre3 = Pregex("PRE3")


class TestMatchAtStart(unittest.TestCase):
    
    def test_match_at_start(self):
        self.assertEqual(str(MatchAtStart(TEST_STR)), f"\A{TEST_STR}")

    def test_match_at_start_on_type(self):
        self.assertEqual(MatchAtStart("a")._get_type(), _Type.Assertion)
        self.assertEqual(MatchAtStart("abc")._get_type(), _Type.Assertion)


class TestMatchAtEnd(unittest.TestCase):
    
    def test_match_at_end(self):
        self.assertEqual(str(MatchAtEnd(TEST_STR)), f"{TEST_STR}\Z")

    def test_match_at_end_on_type(self):
        self.assertEqual(MatchAtEnd("a")._get_type(), _Type.Assertion)


class TestMatchAtLineStart(unittest.TestCase):
    
    def test_match_at_line_start(self):
        self.assertEqual(str(MatchAtLineStart(TEST_STR)), f"^{TEST_STR}")

    def test_match_at_line_start_on_type(self):
        self.assertEqual(MatchAtLineStart("a")._get_type(), _Type.Assertion)


class TestMatchAtLineEnd(unittest.TestCase):
    
    def test_match_at_line_end(self):
        self.assertEqual(str(MatchAtLineEnd(TEST_STR)), f"{TEST_STR}$")

    def test_match_at_line_end_on_type(self):
        self.assertEqual(MatchAtLineEnd("a")._get_type(), _Type.Assertion)


class TestWordBoundary(unittest.TestCase):

    left_word_boundary = WordBoundary() + TEST_STR
    right_word_boundary = TEST_STR + WordBoundary()
    left_and_right_word_boundary = WordBoundary() + TEST_STR + WordBoundary()

    def test_word_boundary_on_pattern(self):
        self.assertEqual(str(WordBoundary()), "\\b")

    def test_word_boundary_on_matches(self):
        self.assertEqual((WordBoundary() + "a").get_matches("a ba -a"), ["a", "a"])

    def test_word_boundary_on_type(self):
        self.assertEqual(WordBoundary()._get_type(), _Type.Assertion)
    
    def test_left_word_boundary(self):
        self.assertEqual(str(self.left_word_boundary), f"\\b{TEST_STR}")

    def test_left_word_boundary_on_type(self):
        self.assertEqual(self.left_word_boundary._get_type(), _Type.Assertion)

    def test_right_word_boundary(self):
        self.assertEqual(str(self.right_word_boundary), f"{TEST_STR}\\b")

    def test_right_word_boundary_on_type(self):
        self.assertEqual(self.right_word_boundary._get_type(), _Type.Assertion)

    def test_left_and_right_word_boundary(self):
        self.assertEqual(str(self.left_and_right_word_boundary), f"\\b{TEST_STR}\\b")

    def test_left_and_right_word_boundary_on_type(self):
        self.assertEqual(self.left_and_right_word_boundary._get_type(), _Type.Assertion)


class TestNonWordBoundary(unittest.TestCase):

    left_non_word_boundary = NonWordBoundary() + TEST_STR
    right_non_word_boundary = TEST_STR + NonWordBoundary()
    left_and_right_non_word_boundary = NonWordBoundary() + TEST_STR + NonWordBoundary()

    def test_non_word_boundary_on_pattern(self):
        self.assertEqual(str(NonWordBoundary()), "\\B")

    def test_non_word_boundary_on_matches(self):
        self.assertEqual((NonWordBoundary() + "a").get_matches("a ba a"), ["a"])

    def test_non_word_boundary_on_type(self):
        self.assertEqual(NonWordBoundary()._get_type(), _Type.Assertion)
    
    def test_left_non_word_boundary(self):
        self.assertEqual(str(self.left_non_word_boundary), f"\\B{TEST_STR}")

    def test_left_non_word_boundary_on_type(self):
        self.assertEqual(self.left_non_word_boundary._get_type(), _Type.Assertion)

    def test_right_non_word_boundary(self):
        self.assertEqual(str(self.right_non_word_boundary), f"{TEST_STR}\\B")

    def test_right_non_word_boundary_on_type(self):
        self.assertEqual(self.right_non_word_boundary._get_type(), _Type.Assertion)

    def test_left_and_right_non_word_boundary(self):
        self.assertEqual(str(self.left_and_right_non_word_boundary), f"\\B{TEST_STR}\\B")

    def test_left_and_right_non_word_boundary_on_type(self):
        self.assertEqual(self.left_and_right_non_word_boundary._get_type(), _Type.Assertion)


class TestFollowedBy(unittest.TestCase):
    
    def test_followed_by(self):
        self.assertEqual(str(FollowedBy(pre1, pre2)), f"{pre1}(?={pre2})")

    def test_followed_by_on_type(self):
        self.assertEqual(FollowedBy("a", "b")._get_type(), _Type.Assertion)

    def test_followed_by_on_empty_token_as_assertion_pattern(self):
        self.assertEqual(str(FollowedBy(pre1, Empty())), f"{pre1}")


class TestNotFollowedBy(unittest.TestCase):
    
    def test_not_followed_by(self):
        self.assertEqual(str(NotFollowedBy(pre1, pre2)), f"{pre1}(?!{pre2})")

    def test_not_followed_by_on_multiple_patterns(self):
        self.assertEqual(str(NotFollowedBy(pre1, pre2, pre3)), f"{pre1}(?!{pre2})(?!{pre3})")

    def test_not_followed_by_on_type(self):
        self.assertEqual(NotFollowedBy("a", "b")._get_type(), _Type.Assertion)

    def test_not_followed_by_on_not_enough_arguments_exception(self):
        self.assertRaises(NotEnoughArgumentsException, NotFollowedBy, pre1)

    def test_not_followed_by_on_empty_negative_assertion_exception(self):
        self.assertRaises(EmptyNegativeAssertionException, NotFollowedBy, pre1, Empty())

    def test_not_followed_by_on_multiple_patterns_empty_negative_assertion_exception(self):
        self.assertRaises(EmptyNegativeAssertionException, NotFollowedBy, pre1, pre2, Empty())


class TestPrecededBy(unittest.TestCase):
    
    def test_preceded_by(self):
        self.assertEqual(str(PrecededBy(pre1, pre2)), f"(?<={pre2}){pre1}")

    def test_preceded_by_on_type(self):
        self.assertEqual(PrecededBy("a", "b")._get_type(), _Type.Assertion)

    def test_preceded_by_on_quantifier(self):
        exactly = Exactly(pre2, 3)
        self.assertEqual(str(PrecededBy(pre1, exactly)), f"(?<={exactly}){pre1}")
        self.assertRaises(NonFixedWidthPatternException, PrecededBy, pre1, Optional(pre2))

    def test_preceded_by_on_empty_token_as_assertion_pattern(self):
        self.assertEqual(str(PrecededBy(pre1, Empty())), f"{pre1}")


class TestNotPrecededBy(unittest.TestCase):
    
    def test_not_preceded_by(self):
        self.assertEqual(str(NotPrecededBy(pre1, pre2)), f"(?<!{pre2}){pre1}")

    def test_not_preceded_by_on_multiple_patterns(self):
        self.assertEqual(str(NotPrecededBy(pre1, pre2, pre3)), f"(?<!{pre3})(?<!{pre2}){pre1}")

    def test_not_preceded_by_on_type(self):
        self.assertEqual(NotPrecededBy("a", "b")._get_type(), _Type.Assertion)

    def test_not_preceded_by_on_exactly_quantifier(self):
        exactly = Exactly(pre2, 3)
        self.assertEqual(str(NotPrecededBy(pre1, exactly)), f"(?<!{exactly}){pre1}")

    def test_not_preceded_by_on_not_enough_arguments_exception(self):
        self.assertRaises(NotEnoughArgumentsException, NotPrecededBy, pre1)

    def test_not_preceded_by_on_empty_negative_assertion_exception(self):
        self.assertRaises(EmptyNegativeAssertionException, NotPrecededBy, pre1, Empty())

    def test_not_preceded_by_on_multiple_patterns_empty_negative_assertion_exception(self):
        self.assertRaises(EmptyNegativeAssertionException, NotPrecededBy, pre1, pre2, Empty())

    def test_not_preceded_by_on_non_fixed_width_pattern_exception(self):
        self.assertRaises(NonFixedWidthPatternException, NotPrecededBy, pre1, Optional(pre2))

    def test_not_preceded_by_on_multiple_patterns_non_fixed_width_pattern_exception(self):
        self.assertRaises(NonFixedWidthPatternException, NotPrecededBy, pre1, pre2, Optional(pre3))


if __name__=="__main__":
    unittest.main()