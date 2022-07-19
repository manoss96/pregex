import unittest
from pregex.assertions import *


TEST_STR = "test"
pre1 = Pregex("PRE1")
pre2 = Pregex("PRE2")


class TestMatchAtStart(unittest.TestCase):
    
    def test_match_at_start(self):
        self.assertEqual(str(MatchAtStart(TEST_STR)), f"\A{TEST_STR}")


class TestMatchAtEnd(unittest.TestCase):
    
    def test_match_at_end(self):
        self.assertEqual(str(MatchAtEnd(TEST_STR)), f"{TEST_STR}\Z")


class TestMatchAtLineStart(unittest.TestCase):
    
    def test_match_at_line_start(self):
        self.assertEqual(str(MatchAtLineStart(TEST_STR)), f"^{TEST_STR}")


class TestMatchAtLineEnd(unittest.TestCase):
    
    def test_match_at_line_end(self):
        self.assertEqual(str(MatchAtLineEnd(TEST_STR)), f"{TEST_STR}$")


class TestMatchAtWordBoundary(unittest.TestCase):
    
    def test_match_at_word_boundary(self):
        self.assertEqual(str(MatchAtWordBoundary(TEST_STR)), f"\\b{TEST_STR}\\b")


class TestMatchAtLeftWordBoundary(unittest.TestCase):
    
    def test_match_at_left_word_boundary(self):
        self.assertEqual(str(MatchAtLeftWordBoundary(TEST_STR)), f"\\b{TEST_STR}")
        

class TestMatchAtRightWordBoundary(unittest.TestCase):
    
    def test_match_at_right_word_boundary(self):
        self.assertEqual(str(MatchAtRightWordBoundary(TEST_STR)), f"{TEST_STR}\\b")


class TestFollowedBy(unittest.TestCase):
    
    def test_followed_by(self):
        self.assertEqual(str(FollowedBy(pre1, pre2)), f"{pre1}(?={pre2})")


class TestNotFollowedBy(unittest.TestCase):
    
    def test_not_followed_by(self):
        self.assertEqual(str(NotFollowedBy(pre1, pre2)), f"{pre1}(?!{pre2})")


class TestPrecededBy(unittest.TestCase):
    
    def test_preceded_by(self):
        self.assertEqual(str(PrecededBy(pre1, pre2)), f"(?<={pre2}){pre1}")


class TestNotPrecededBy(unittest.TestCase):
    
    def test_preceded_by(self):
        self.assertEqual(str(NotPrecededBy(pre1, pre2)), f"(?<!{pre2}){pre1}")


if __name__=="__main__":
    unittest.main()