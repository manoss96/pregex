import unittest
from pregex.tokens import *
from pregex.pre import _Type


class Test__Token(unittest.TestCase):

    def test_token_class_type(self):
        self.assertEqual(Backslash()._get_type(), _Type.Token)

class TestBackslash(unittest.TestCase):

    def test_backslash(self):
        self.assertEqual(str(Backslash()), r"\\")

    def test_backslash_on_match(self):
        self.assertTrue(Backslash().get_matches(r"text\ttext") == ["\\"])


class TestBullet(unittest.TestCase):

    def test_bullet(self):
        self.assertEqual(str(Bullet()), "\u2022")

    def test_bullet_on_match(self):
        self.assertTrue(Bullet().get_matches("text•text") == ["•"])


class TestCarriageReturn(unittest.TestCase):

    def test_carriage_return(self):
        self.assertEqual(str(CarriageReturn()), "\r")

    def test_carriage_return_on_match(self):
        self.assertTrue(CarriageReturn().get_matches("text\rtext") == ["\r"])        


class TestCopyright(unittest.TestCase):

    def test_copyright(self):
        self.assertEqual(str(Copyright()), "\u00A9")

    def test_copyright_on_match(self):
        self.assertTrue(Copyright().get_matches("text©text") == ["©"])


class TestDivision(unittest.TestCase):

    def test_division(self):
        self.assertEqual(str(Division()), "\u00f7")

    def test_division_on_match(self):
        self.assertTrue(Division().get_matches("text÷text") == ["÷"])         


class TestDollar(unittest.TestCase):

    def test_dollar(self):
        self.assertEqual(str(Dollar()), "\\\u0024")

    def test_dollar_on_match(self):
        self.assertTrue(Dollar().get_matches("text$text") == ["$"])


class TestEuro(unittest.TestCase):

    def test_euro(self):
        self.assertEqual(str(Euro()), "\u20ac")

    def test_euro_on_match(self):
        self.assertTrue(Euro().get_matches("text€text") == ["€"])   


class TestFormFeed(unittest.TestCase):

    def test_form_feed(self):
        self.assertEqual(str(FormFeed()), "\f")

    def test_form_feed_on_match(self):
        self.assertTrue(FormFeed().get_matches("text\ftext") == ["\f"])


class TestInfinity(unittest.TestCase):

    def test_infinity(self):
        self.assertEqual(str(Infinity()), "\u221e")

    def test_infinity_on_match(self):
        self.assertTrue(Infinity().get_matches("text∞text") == ["∞"])


class TestMultiplication(unittest.TestCase):

    def test_multiplication(self):
        self.assertEqual(str(Multiplication()), "\u00d7")

    def test_multiplication_on_match(self):
        self.assertTrue(Multiplication().get_matches("text×text") == ["×"])        


class TestNewline(unittest.TestCase):

    def test_newline(self):
        self.assertEqual(str(Newline()), "\n")

    def test_newline_on_match(self):
        self.assertTrue(Newline().get_matches("text\ntext") == ["\n"])


class TestPound(unittest.TestCase):

    def test_pound(self):
        self.assertEqual(str(Pound()), "\u00a3")

    def test_pound_on_match(self):
        self.assertTrue(Pound().get_matches("text£text") == ["£"]) 


class TestRegistered(unittest.TestCase):

    def test_registered(self):
        self.assertEqual(str(Registered()), "\u00ae")

    def test_registered_on_match(self):
        self.assertTrue(Registered().get_matches("text®text") == ["®"])


class TestRupee(unittest.TestCase):

    def test_rupee(self):
        self.assertEqual(str(Rupee()), "\u20b9")

    def test_rupee_on_match(self):
        self.assertTrue(Rupee().get_matches("text₹text") == ["₹"])         


class TestSpace(unittest.TestCase):

    def test_space(self):
        self.assertEqual(str(Space()), r" ")

    def test_space_on_match(self):
        self.assertTrue(Space().get_matches(r"text ext") == [" "])


class TestTab(unittest.TestCase):

    def test_tab(self):
        self.assertEqual(str(Tab()), "\t")

    def test_tab_on_match(self):
        self.assertTrue(Tab().get_matches("text\ttext") == ["\t"])


class TestTrademark(unittest.TestCase):

    def test_trademark(self):
        self.assertEqual(str(Trademark()), "\u2122")

    def test_trademark_on_match(self):
        self.assertTrue(Trademark().get_matches("text™text") == ["™"])


class TestVerticalTab(unittest.TestCase):

    def test_vertical_tab(self):
        self.assertEqual(str(VerticalTab()), "\v")

    def test_vertical_tab_on_match(self):
        self.assertTrue(VerticalTab().get_matches("text\vtext") == ["\v"])


class TestWhiteBullet(unittest.TestCase):

    def test_white_bullet(self):
        self.assertEqual(str(WhiteBullet()), "\u25e6")

    def test_white_bullet_on_match(self):
        self.assertTrue(WhiteBullet().get_matches("text◦text") == ["◦"])        


class TestYen(unittest.TestCase):

    def test_yen(self):
        self.assertEqual(str(Yen()), "\u00a5")

    def test_yen_on_match(self):
        self.assertTrue(Yen().get_matches("text¥text") == ["¥"]) 


if __name__=="__main__":
    unittest.main()