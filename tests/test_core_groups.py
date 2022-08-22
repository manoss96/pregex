import unittest
from pregex.core.groups import *
from pregex.core.tokens import Backslash
from pregex.core.pre import Pregex, _Type
from pregex.core.exceptions import InvalidArgumentTypeException, \
    InvalidCapturingGroupNameException


TEST_STR = "test"


class TestCapture(unittest.TestCase):

    name = "NAME"

    def test_capture_on_str(self):
        self.assertEqual(str(Capture(TEST_STR)), f"({TEST_STR})")

    def test_capture_on_type(self):
        self.assertEqual(Capture("a")._get_type(), _Type.Group)

    def test_capture_on_literal(self):
        literal = Pregex(TEST_STR)
        self.assertEqual(str(Capture(literal)), f"({literal})")

    def test_capture_on_capturing_group(self):
        ''' Grouping a capturing group does nothing. '''
        group = Capture(TEST_STR)
        self.assertEqual(str(Capture(group)), f"{group}")

    def test_capture_on_concat_of_capturing_groups(self):
        pre = Capture("a") + "b" + Capture("c")
        self.assertEqual(str(Capture(pre)), f"({pre})")

    def test_capture_on_backslash_group(self):
        pre = Capture(Backslash())
        self.assertEqual(str(Capture(pre)), f"{pre}")

    def test_capture_on_concat_of_capturing_groups_starting_with_backslash_group(self):
        pre = Capture(Backslash()) + "b" + Capture("c")
        self.assertEqual(str(Capture(pre)), f"({pre})")

    def test_capture_on_concat_of_capturing_groups_ending_with_backslash_group(self):
        pre = Capture("a") + "b" + Capture(Backslash())
        self.assertEqual(str(Capture(pre)), f"({pre})")

    def test_capture_on_capturing_group_of_concat_of_capturing_groups(self):
        group = Capture(Capture("a") + "b" + Capture("c"))
        self.assertEqual(str(Capture(group)), f"{group}")

    def test_capture_on_non_capturing_group(self):
        ''' Grouping a non-capturing group converts it to a capturing group. '''
        group = Group(TEST_STR)
        self.assertEqual(str(Capture(group)), f"{str(group).replace('?:', '')}")

    def test_capture_on_concat_of_non_capturing_groups(self):
        pre = Group("a") + "b" + Group("c")
        self.assertEqual(str(Capture(pre)), f"({pre})")

    def test_capture_on_capturing_group_of_concat_of_non_capturing_groups(self):
        group = Capture(Group("a") + "b" + Group("c"))
        self.assertEqual(str(Capture(group)), f"{group}")

    def test_named_capturing_group_on_str(self):
        self.assertEqual(str(Capture(TEST_STR, self.name)), f"(?P<{self.name}>{TEST_STR})")

    def test_named_capturing_group_on_literal(self):
        literal = Pregex(TEST_STR)
        self.assertEqual(str(Capture(literal, self.name)), f"(?P<{self.name}>{literal})")

    def test_named_capturing_group_on_capturing_group(self):
        ''' Name-grouping a capturing group without a name, names the group. '''
        group = Capture(TEST_STR)
        self.assertEqual(str(Capture(group, self.name)), f"(?P<{self.name}>{str(group)[1:-1]})")

    def test_named_capturing_group_on_capturing_group(self):
        ''' Name-grouping a capturing group with name, changes the group's name. '''
        group = Capture(TEST_STR, self.name)
        new_name = "NEW_NAME"
        self.assertEqual(str(Capture(group, new_name)), str(group).replace(self.name, new_name))

    def test_named_capturing_group_on_non_capturing_group(self):
        ''' Name-Grouping a non-capturing group converts it to a named capturing group. '''
        group = Group(TEST_STR)
        self.assertEqual(str(Capture(group, self.name)), f"(?P<{self.name}>{str(group)[:-1].replace('(?:', '', 1)})")

    def test_named_capturing_group_on_invalid_argument_type_exception(self):
        invalid_type_names = [1, 1.5, True, Pregex("z")]
        for name in invalid_type_names:
            self.assertRaises(InvalidArgumentTypeException, Capture, "test", name)

    def test_named_capturing_group_on_invalid_name_exception(self):
        invalid_names = ["11zzz", "ald!!", "@%^Fl", "!flflf123", "dld-"]
        for name in invalid_names:
            self.assertRaises(InvalidCapturingGroupNameException, Capture, "test", name)


class TestGroup(unittest.TestCase):

    def test_group_on_str(self):
        self.assertEqual(str(Group(TEST_STR)), f"(?:{TEST_STR})")

    def test_group_on_type(self):
        self.assertEqual(Group("a")._get_type(), _Type.Group)
        self.assertNotEqual((Group("a") + Group("b"))._get_type(), _Type.Group)

    def test_group_on_literal(self):
        literal = Pregex(TEST_STR)
        self.assertEqual(str(Group(literal)), f"(?:{literal})")

    def test_group_on_capturing_group(self):
        ''' Applying 'Group' on a capturing group converts it into a non-capturing group. '''
        group = Capture(TEST_STR)
        self.assertEqual(str(Group(group)), f"{str(group).replace('(', '(?:')}")

    def test_group_on_concat_of_capturing_groups(self):
        pre = Capture("a") + "b" + Capture("c")
        self.assertEqual(str(Group(pre)), f"(?:{pre})")

    def test_group_on_backslash_group(self):
        group = Capture(Backslash())
        self.assertEqual(str(Group(group)),f"{str(group).replace('(', '(?:')}")

    def test_group_on_concat_of_capturing_groups_starting_with_backslash_group(self):
        pre = Capture(Backslash()) + "b" + Capture("c")
        self.assertEqual(str(Group(pre)), f"(?:{pre})")

    def test_group_on_concat_of_capturing_groups_ending_with_backslash_group(self):
        pre = Capture("a") + "b" + Capture(Backslash())
        self.assertEqual(str(Group(pre)), f"(?:{pre})")

    def test_group_on_capturing_group_of_concat_of_capturing_groups(self):
        group = Capture(Capture("a") + "b" + Capture("c"))
        self.assertEqual(str(Group(group)), f"{str(group).replace('(', '(?:', 1)}")

    def test_group_on_non_capturing_group(self):
        ''' Applying 'Group' on a non-capturing group does nothing. '''
        group = Group(TEST_STR)
        self.assertEqual(str(Group(group)), f"{group}")

    def test_group_on_concat_of_non_capturing_groups(self):
        pre = Group("a") + "b" + Group("c")
        self.assertEqual(str(Group(pre)), f"(?:{pre})")

    def test_group_on_non_capturing_group_of_concat_of_non_capturing_groups(self):
        group = Group(Group("a") + "b" + Group("c"))
        self.assertEqual(str(Group(group)), f"{group}")

    def test_group_on_named_capturing_group(self):
        ''' Applying 'Group' on a non-capturing group converts it into a non-capturing group. '''
        name = "NAME"
        group = Capture(TEST_STR, name)
        self.assertEqual(str(Group(group)), f"{str(group).replace(f'(?P<{name}>', '(?:')}")


class TestBackreference(unittest.TestCase):

    def test_backreference(self):
        name = "name"
        self.assertEqual(str(Backreference(name)), f"(?P={name})")

    def test_backreference_on_type(self):
        self.assertEqual(Backreference("a")._get_type(), _Type.Group)

    def test_backreference_on_invalid_argument_type_exception(self):
        invalid_type_names = [1, 1.5, True, Pregex("z")]
        for name in invalid_type_names:
            self.assertRaises(InvalidArgumentTypeException, Backreference, name)

    def test_backreference_on_invalid_name_exception(self):
        invalid_names = ["11zzz", "ald!!", "@%^Fl", "!flflf123", "dld-"]
        for name in invalid_names:
            with self.assertRaises(InvalidCapturingGroupNameException):
                _ = Backreference(name)

    def test_backreference_pattern(self):
        name = "name"
        pre: Pregex = Pregex(f"(?P<{name}>a|b)", escape=False) + Backreference(name)
        self.assertTrue(pre.is_exact_match("aa"))
        self.assertTrue(pre.is_exact_match("bb"))
        self.assertFalse(pre.is_exact_match("ab"))


class TestConditional(unittest.TestCase):

    name = "name"
    then_pre = Pregex("then")
    else_pre = Pregex("else")

    def test_conditional(self):
        self.assertEqual(str(Conditional(self.name, self.then_pre)), f"(?({self.name}){self.then_pre})")

    def test_conditional_on_type(self):
        self.assertEqual(Conditional("a", "b")._get_type(), _Type.Group)

    def test_conditional_with_else_pre(self):
        self.assertEqual(str(Conditional(self.name, self.then_pre, self.else_pre)),
        f"(?({self.name}){self.then_pre}|{self.else_pre})")

    def test_conditional_on_invalid_argument_type_exception(self):
        invalid_type_names = [1, 1.5, True, Pregex("z")]
        for name in invalid_type_names:
            self.assertRaises(InvalidArgumentTypeException, Conditional, name, self.then_pre)

    def test_conditional_on_invalid_name_exception(self):
        invalid_names = ["11zzz", "ald!!", "@%^Fl", "!flflf123", "dld-"]
        for name in invalid_names:
            with self.assertRaises(InvalidCapturingGroupNameException):
                _ = Conditional(name, self.then_pre)

    def test_conditional_pattern(self):
        pre: Pregex = Pregex(f"(?P<{self.name}>A)", escape=False) + Conditional(self.name, "B")
        self.assertTrue(pre.is_exact_match("AB"))

    def test_conditional_pattern_with_else(self):
        pre: Pregex = Pregex(f"(?P<{self.name}>A)?", escape=False) + Conditional(self.name, "B", "C")
        self.assertTrue(pre.is_exact_match("AB"))
        self.assertTrue(pre.is_exact_match("C"))


if __name__=="__main__":
    unittest.main()