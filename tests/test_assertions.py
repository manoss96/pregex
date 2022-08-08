import unittest
from pregex.assertions import *
from pregex.pre import Pregex, _Type
from pregex.quantifiers import Exactly, Optional
from pregex.exceptions import NonFixedWidthPatternException


TEST_STR = "test"
pre1 = Pregex("PRE1")
pre2 = Pregex("PRE2")


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


class TestMatchAtWordBoundary(unittest.TestCase):
    
    def test_match_at_word_boundary(self):
        self.assertEqual(str(MatchAtWordBoundary(TEST_STR)), f"\\b{TEST_STR}\\b")

    def test_match_at_word_boundary_on_type(self):
        self.assertEqual(MatchAtWordBoundary("a")._get_type(), _Type.Assertion)


class TestMatchAtLeftWordBoundary(unittest.TestCase):
    
    def test_match_at_left_word_boundary(self):
        self.assertEqual(str(MatchAtLeftWordBoundary(TEST_STR)), f"\\b{TEST_STR}")

    def test_match_at_left_word_boundary_on_type(self):
        self.assertEqual(MatchAtLeftWordBoundary("a")._get_type(), _Type.Assertion)
        

class TestMatchAtRightWordBoundary(unittest.TestCase):
    
    def test_match_at_right_word_boundary(self):
        self.assertEqual(str(MatchAtRightWordBoundary(TEST_STR)), f"{TEST_STR}\\b")

    def test_match_at_word_boundary_on_type(self):
        self.assertEqual(MatchAtRightWordBoundary("a")._get_type(), _Type.Assertion)


class TestFollowedBy(unittest.TestCase):
    
    def test_followed_by(self):
        self.assertEqual(str(FollowedBy(pre1, pre2)), f"{pre1}(?={pre2})")

    def test_followed_by_on_type(self):
        self.assertEqual(FollowedBy("a", "b")._get_type(), _Type.Assertion)


class TestNotFollowedBy(unittest.TestCase):
    
    def test_not_followed_by(self):
        self.assertEqual(str(NotFollowedBy(pre1, pre2)), f"{pre1}(?!{pre2})")

    def test_not_followed_by_on_type(self):
        self.assertEqual(NotFollowedBy("a", "b")._get_type(), _Type.Assertion)


class TestPrecededBy(unittest.TestCase):
    
    def test_preceded_by(self):
        self.assertEqual(str(PrecededBy(pre1, pre2)), f"(?<={pre2}){pre1}")

    def test_preceded_by_on_type(self):
        self.assertEqual(PrecededBy("a", "b")._get_type(), _Type.Assertion)

    def test_preceded_by_on_quantifier(self):
        exactly = Exactly(pre2, 3)
        self.assertEqual(str(PrecededBy(pre1, exactly)), f"(?<={exactly}){pre1}")
        self.assertRaises(NonFixedWidthPatternException, PrecededBy, pre1, Optional(pre2))


class TestNotPrecededBy(unittest.TestCase):
    
    def test_not_preceded_by(self):
        self.assertEqual(str(NotPrecededBy(pre1, pre2)), f"(?<!{pre2}){pre1}")

    def test_not_preceded_by_on_type(self):
        self.assertEqual(NotPrecededBy("a", "b")._get_type(), _Type.Assertion)

    def test_not_preceded_by_on_quantifier(self):
        exactly = Exactly(pre2, 3)
        self.assertEqual(str(NotPrecededBy(pre1, exactly)), f"(?<!{exactly}){pre1}")
        self.assertRaises(NonFixedWidthPatternException, NotPrecededBy, pre1, Optional(pre2))


if __name__=="__main__":
    unittest.main()