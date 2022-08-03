import unittest
from pregex.tokens import *
from pregex.exceptions import NonStringArgumentException


class TestWhitespace(unittest.TestCase):

    def test_space(self):
        self.assertEqual(str(Space()), r" ")

    def test_space_on_match(self):
        self.assertTrue(Space().get_matches(r"text ext") == [" "])


class TestBackslash(unittest.TestCase):

    def test_backslash(self):
        self.assertEqual(str(Backslash()), r"\\")

    def test_backslash_on_match(self):
        self.assertTrue(Backslash().get_matches(r"text\text") == ["\\"])


class TestNewline(unittest.TestCase):

    def test_newline(self):
        self.assertEqual(str(Newline()), "\n")

    def test_newline_on_match(self):
        self.assertTrue(Newline().get_matches("text\ntext") == ["\n"])


class TestCarriageReturn(unittest.TestCase):

    def test_carriage_return(self):
        self.assertEqual(str(CarriageReturn()), "\r")

    def test_carriage_return_on_match(self):
        self.assertTrue(CarriageReturn().get_matches("text\rtext") == ["\r"])


class TestFormFeed(unittest.TestCase):

    def test_form_feed(self):
        self.assertEqual(str(FormFeed()), "\f")

    def test_form_feed_on_match(self):
        self.assertTrue(FormFeed().get_matches("text\ftext") == ["\f"])


class TestTab(unittest.TestCase):

    def test_tab(self):
        self.assertEqual(str(Tab()), "\t")

    def test_tab_on_match(self):
        self.assertTrue(Tab().get_matches("text\ttext") == ["\t"])


class TestVerticalTab(unittest.TestCase):

    def test_vertical_tab(self):
        self.assertEqual(str(VerticalTab()), "\v")

    def test_vertical_tab_on_match(self):
        self.assertTrue(VerticalTab().get_matches("text\vtext") == ["\v"])


if __name__=="__main__":
    unittest.main()