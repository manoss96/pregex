import unittest
from pregex.pre import Pregex
from pregex.groups import *
from pregex.tokens import Backslash, Literal
from pregex.exceptions import NonStringArgumentException, InvalidCapturingGroupNameException


TEST_STR = "test"

class TestCapturingGroup(unittest.TestCase):

    name = "NAME"

    def test_capturing_group_on_str(self):
        self.assertEqual(str(CapturingGroup(TEST_STR)), f"({TEST_STR})")

    def test_capturing_group_on_literal(self):
        literal = Literal(TEST_STR)
        self.assertEqual(str(CapturingGroup(literal)), f"({literal})")

    def test_capturing_group_on_capturing_group(self):
        ''' Grouping a capturing group does nothing. '''
        group = CapturingGroup(TEST_STR)
        self.assertEqual(str(CapturingGroup(group)), f"{group}")

    def test_capturing_group_on_concat_of_capturing_groups(self):
        pre = CapturingGroup("a") + "b" + CapturingGroup("c")
        self.assertEqual(str(CapturingGroup(pre)), f"({pre})")

    def test_capturing_group_on_backslash_group(self):
        pre = CapturingGroup(Backslash())
        self.assertEqual(str(CapturingGroup(pre)), f"{pre}")

    def test_capturing_group_on_concat_of_capturing_groups_starting_with_backslash_group(self):
        pre = CapturingGroup(Backslash()) + "b" + CapturingGroup("c")
        self.assertEqual(str(CapturingGroup(pre)), f"({pre})")

    def test_capturing_group_on_concat_of_capturing_groups_ending_with_backslash_group(self):
        pre = CapturingGroup("a") + "b" + CapturingGroup(Backslash())
        self.assertEqual(str(CapturingGroup(pre)), f"({pre})")

    def test_capturing_group_on_capturing_group_of_concat_of_capturing_groups(self):
        group = CapturingGroup(CapturingGroup("a") + "b" + CapturingGroup("c"))
        self.assertEqual(str(CapturingGroup(group)), f"{group}")

    def test_capturing_group_on_non_capturing_group(self):
        ''' Grouping a non-capturing group converts it to a capturing group. '''
        group = NonCapturingGroup(TEST_STR)
        self.assertEqual(str(CapturingGroup(group)), f"{str(group).replace('?:', '')}")

    def test_capturing_group_on_concat_of_non_capturing_groups(self):
        pre = NonCapturingGroup("a") + "b" + NonCapturingGroup("c")
        self.assertEqual(str(CapturingGroup(pre)), f"({pre})")

    def test_capturing_group_on_capturing_group_of_concat_of_non_capturing_groups(self):
        group = CapturingGroup(NonCapturingGroup("a") + "b" + NonCapturingGroup("c"))
        self.assertEqual(str(CapturingGroup(group)), f"{group}")

    def test_named_capturing_group_on_str(self):
        self.assertEqual(str(CapturingGroup(TEST_STR, self.name)), f"(?P<{self.name}>{TEST_STR})")

    def test_named_capturing_group_on_literal(self):
        literal = Literal(TEST_STR)
        self.assertEqual(str(CapturingGroup(literal, self.name)), f"(?P<{self.name}>{literal})")

    def test_named_capturing_group_on_capturing_group(self):
        ''' Name-grouping a capturing group without a name, names the group. '''
        group = CapturingGroup(TEST_STR)
        self.assertEqual(str(CapturingGroup(group, self.name)), f"(?P<{self.name}>{str(group)[1:-1]})")

    def test_named_capturing_group_on_capturing_group(self):
        ''' Name-grouping a capturing group with name, changes the group's name. '''
        group = CapturingGroup(TEST_STR, self.name)
        new_name = "NEW_NAME"
        self.assertEqual(str(CapturingGroup(group, new_name)), str(group).replace(self.name, new_name))

    def test_named_capturing_group_on_non_capturing_group(self):
        ''' Name-Grouping a non-capturing group converts it to a named capturing group. '''
        group = NonCapturingGroup(TEST_STR)
        self.assertEqual(str(CapturingGroup(group, self.name)), f"(?P<{self.name}>{str(group)[:-1].replace('(?:', '', 1)})")

    def test_named_capturing_group_on_non_string_name_exception(self):
        invalid_type_names = [1, 1.5, True, Literal("z")]
        for name in invalid_type_names:
            self.assertRaises(NonStringArgumentException, CapturingGroup, "test", name)

    def test_named_capturing_group_on_invalid_name_exception(self):
        invalid_names = ["11zzz", "ald!!", "@%^Fl", "!flflf123", "dld-"]
        for name in invalid_names:
            self.assertRaises(InvalidCapturingGroupNameException, CapturingGroup, "test", name)


class TestNonCapturingGroup(unittest.TestCase):

    def test_non_capturing_group_on_str(self):
        self.assertEqual(str(NonCapturingGroup(TEST_STR)), f"(?:{TEST_STR})")

    def test_non_capturing_group_on_literal(self):
        literal = Literal(TEST_STR)
        self.assertEqual(str(NonCapturingGroup(literal)), f"(?:{literal})")

    def test_non_capturing_group_on_capturing_group(self):
        ''' Applying 'NonCapturingGroup' on a capturing group converts it into a non-capturing group. '''
        group = CapturingGroup(TEST_STR)
        self.assertEqual(str(NonCapturingGroup(group)), f"{str(group).replace('(', '(?:')}")

    def test_non_capturing_group_on_concat_of_capturing_groups(self):
        pre = CapturingGroup("a") + "b" + CapturingGroup("c")
        self.assertEqual(str(NonCapturingGroup(pre)), f"(?:{pre})")

    def test_non_capturing_group_on_backslash_group(self):
        group = CapturingGroup(Backslash())
        self.assertEqual(str(NonCapturingGroup(group)),f"{str(group).replace('(', '(?:')}")

    def test_non_capturing_group_on_concat_of_capturing_groups_starting_with_backslash_group(self):
        pre = CapturingGroup(Backslash()) + "b" + CapturingGroup("c")
        self.assertEqual(str(NonCapturingGroup(pre)), f"(?:{pre})")

    def test_non_capturing_group_on_concat_of_capturing_groups_ending_with_backslash_group(self):
        pre = CapturingGroup("a") + "b" + CapturingGroup(Backslash())
        self.assertEqual(str(NonCapturingGroup(pre)), f"(?:{pre})")

    def test_non_capturing_group_on_capturing_group_of_concat_of_capturing_groups(self):
        group = CapturingGroup(CapturingGroup("a") + "b" + CapturingGroup("c"))
        self.assertEqual(str(NonCapturingGroup(group)), f"{str(group).replace('(', '(?:', 1)}")

    def test_non_capturing_group_on_non_capturing_group(self):
        ''' Applying 'NonCapturingGroup' on a non-capturing group does nothing. '''
        group = NonCapturingGroup(TEST_STR)
        self.assertEqual(str(NonCapturingGroup(group)), f"{group}")

    def test_non_capturing_group_on_concat_of_non_capturing_groups(self):
        pre = NonCapturingGroup("a") + "b" + NonCapturingGroup("c")
        self.assertEqual(str(NonCapturingGroup(pre)), f"(?:{pre})")

    def test_non_capturing_group_on_non_capturing_group_of_concat_of_non_capturing_groups(self):
        group = NonCapturingGroup(NonCapturingGroup("a") + "b" + NonCapturingGroup("c"))
        self.assertEqual(str(NonCapturingGroup(group)), f"{group}")

    def test_non_capturing_group_on_named_capturing_group(self):
        ''' Applying 'NonCapturingGroup' on a non-capturing group converts it into a non-capturing group. '''
        name = "NAME"
        group = CapturingGroup(TEST_STR, name)
        self.assertEqual(str(NonCapturingGroup(group)), f"{str(group).replace(f'(?P<{name}>', '(?:')}")


class TestBackreference(unittest.TestCase):

    def test_backreference(self):
        name = "name"
        self.assertEqual(str(Backreference(name)), f"(?P={name})")

    def test_backreference_on_non_string_name_exception(self):
        invalid_type_names = [1, 1.5, True, Literal("z")]
        for name in invalid_type_names:
            self.assertRaises(NonStringArgumentException, Backreference, name)

    def test_backreference_on_invalid_name_exception(self):
        invalid_names = ["11zzz", "ald!!", "@%^Fl", "!flflf123", "dld-"]
        for name in invalid_names:
            with self.assertRaises(InvalidCapturingGroupNameException):
                _ = Backreference(name)

    def test_backreference_pattern(self):
        name = "name"
        pre: Pregex = Pregex(f"(?P<{name}>a|b)", False, False) + Backreference(name)
        self.assertTrue(pre.is_exact_match("aa"))
        self.assertTrue(pre.is_exact_match("bb"))
        self.assertFalse(pre.is_exact_match("ab"))


if __name__=="__main__":
    unittest.main()