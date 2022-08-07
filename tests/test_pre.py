import re
import unittest
from pregex.pre import Pregex
from pregex.assertions import MatchAtStart
from pregex.exceptions import CannotBeQuantifiedException, NegativeArgumentException, \
    NonStringArgumentException, NonIntegerArgumentException, NonPositiveArgumentException


class TestPregex(unittest.TestCase):

    TEXT = "A0z aaa _9 z9z 99a B0c"
    PATTERN = "([A-Za-z_])[0-9]+([a-z]?)"

    pre1 = Pregex(PATTERN, escape=False)
    pre2 = Pregex(PATTERN, escape=False)
    # pre2 is compiled.
    pre2.compile()

    MATCHES = ["A0z", "_9", "z9z", "B0c"]
    MATCHES_AND_POS = [("A0z", 0, 3), ("_9", 8, 10), ("z9z", 11, 14), ("B0c", 19, 22)]

    GROUPS = [("A", "z"), ("_", ""), ("z", "z"), ("B", "c")]
    GROUPS_AND_POS = [
        [("A", 0, 1), ("z", 2, 3)],
        [("_", 8, 9), ('', 10, 10)],
        [("z", 11, 12), ("z", 13, 14)],
        [("B", 19, 20), ("c", 21, 22)]
    ]
    GROUPS_AND_RELATIVE_POS = [
        [("A", 0, 1), ("z", 2, 3)],
        [("_", 0, 1), ('', 2, 2)],
        [("z", 0, 1), ("z", 2, 3)],
        [("B", 0, 1), ("c", 2, 3)]
    ]

    GROUPS_WITHOUT_EMPTY = [("A", "z"), tuple("_"), ("z", "z"), ("B", "c")]
    GROUPS_AND_POS_WITHOUT_EMPTY = [
        [("A", 0, 1), ("z", 2, 3)],
        [("_", 8, 9)],
        [("z", 11, 12), ("z", 13, 14)],
        [("B", 19, 20), ("c", 21, 22)]
    ]
    GROUPS_AND_RELATIVE_POS_WITHOUT_EMPTY = [
        [("A", 0, 1), ("z", 2, 3)],
        [("_", 0, 1)],
        [("z", 0, 1), ("z", 2, 3)],
        [("B", 0, 1), ("c", 2, 3)]
    ]
    
    SPLIT_BY_MATCH = [" aaa ", " ", " 99a "]
    SPLIT_BY_GROUP = ['0', ' aaa ', '9', ' ', '9', ' 99a ', '0']
    SPLIT_BY_GROUP_WITHOUT_EMPTY = ['0', ' aaa ', '9 ', '9', ' 99a ', '0']


    '''
    Test Pregex Constructor.
    '''    
    def test_pregex_on_len_1_str(self):
        s = "s"
        self.assertEqual(str(Pregex(s)), s)

    def test_pregex_on_len_n_str(self):
        s = "test"
        self.assertEqual(str(Pregex(s)), s)

    def test_pregex_on_escape(self):
        for c in {'\\', '^', '$', '(', ')', '[', ']', '{', '}', '?', '+', '*', '.', '|', '/'}:
            self.assertEqual(str(Pregex(c)), f"\{c}")

    def test_pregex_on_non_string_argument(self):
        for val in [1, 1.3, True, Pregex("z")]:
            self.assertRaises(NonStringArgumentException, Pregex, val)

    def test_pregex_on_match(self):
        text = ":\z^l"
        self.assertTrue(Pregex(text).get_matches(f"text{text}text") == [text])


    '''
    Test Public Methods
    '''
    def test_pregex_on_get_pattern(self):
        self.assertEqual(self.pre1.get_pattern(include_flags=False), self.PATTERN)
        self.assertEqual(self.pre1.get_pattern(include_flags=True), f"/{self.PATTERN}/gmsu")

    def test_pregex_on_get_compiled_pattern(self):
        flags = re.MULTILINE | re.DOTALL
        self.assertEqual(self.pre1.get_compiled_pattern(), re.compile(self.PATTERN, flags))

    def test_pregex_on_has_match(self):
        self.assertEqual(self.pre1.has_match(self.TEXT), True)
        self.assertEqual(self.pre1.has_match("ab"), False)
        self.assertEqual(self.pre2.has_match(self.TEXT), True)

    def test_pregex_on_is_exact_match(self):
        self.assertEqual(self.pre1.is_exact_match("A0a"), True)
        self.assertEqual(self.pre1.is_exact_match("A0ab"), False)
        self.assertEqual(self.pre1.is_exact_match("aA0a"), False)
        self.assertEqual(self.pre2.is_exact_match("A0a"), True)
    
    def test_pregex_on_iterate_matches(self):
        self.assertEqual([match for match in self.pre1.iterate_matches(self.TEXT)], self.MATCHES)
        self.assertEqual([match for match in self.pre2.iterate_matches(self.TEXT)], self.MATCHES)

    def test_pregex_on_iterate_matches_and_pos(self):
        self.assertEqual([tup for tup in self.pre1.iterate_matches_and_pos(self.TEXT)], self.MATCHES_AND_POS)
        self.assertEqual([tup for tup in self.pre2.iterate_matches_and_pos(self.TEXT)], self.MATCHES_AND_POS)

    def test_pregex_on_iterate_captures(self):
        self.assertEqual([group_tup for group_tup in self.pre1.iterate_captures(self.TEXT)], self.GROUPS)
        self.assertEqual([group_tup for group_tup in self.pre1.iterate_captures(self.TEXT, include_empty=False)],
            self.GROUPS_WITHOUT_EMPTY)
        self.assertEqual([group_tup for group_tup in self.pre2.iterate_captures(self.TEXT)], self.GROUPS)

    def test_pregex_on_iterate_captures_and_pos(self):
        self.assertEqual([group_list for group_list in self.pre1.iterate_captures_and_pos(self.TEXT)], self.GROUPS_AND_POS)
        self.assertEqual([group_list for group_list in self.pre1.iterate_captures_and_pos(self.TEXT, include_empty=False)],
            self.GROUPS_AND_POS_WITHOUT_EMPTY)
        self.assertEqual([group_list for group_list in self.pre2.iterate_captures_and_pos(self.TEXT)], self.GROUPS_AND_POS)

    def test_pregex_on_iterate_captures_and_pos_relative_to_match(self):
        self.assertEqual([group_list for group_list in self.pre1.iterate_captures_and_pos(self.TEXT, relative_to_match=True)],
            self.GROUPS_AND_RELATIVE_POS)
        self.assertEqual([group_list for group_list in self.pre1.iterate_captures_and_pos(self.TEXT,
            include_empty=False, relative_to_match=True)], self.GROUPS_AND_RELATIVE_POS_WITHOUT_EMPTY)
        self.assertEqual([group_list for group_list in self.pre2.iterate_captures_and_pos(self.TEXT, relative_to_match=True)],
            self.GROUPS_AND_RELATIVE_POS)

    def test_pregex_on_get_matches(self):
        self.assertEqual(self.pre1.get_matches(self.TEXT), self.MATCHES)
        self.assertEqual(self.pre2.get_matches(self.TEXT), self.MATCHES)

    def test_pregex_on_get_matches_and_pos(self):
        self.assertEqual(self.pre1.get_matches_and_pos(self.TEXT), self.MATCHES_AND_POS)
        self.assertEqual(self.pre2.get_matches_and_pos(self.TEXT), self.MATCHES_AND_POS)

    def test_pregex_on_get_captures(self):
        self.assertEqual(self.pre1.get_captures(self.TEXT), self.GROUPS)
        self.assertEqual(self.pre1.get_captures(self.TEXT, include_empty=False), self.GROUPS_WITHOUT_EMPTY)
        self.assertEqual(self.pre2.get_captures(self.TEXT, include_empty=False), self.GROUPS_WITHOUT_EMPTY)

    def test_pregex_on_get_captures_and_pos(self):
        self.assertEqual(self.pre1.get_captures_and_pos(self.TEXT), self.GROUPS_AND_POS)
        self.assertEqual(self.pre1.get_captures_and_pos(self.TEXT, include_empty=False), self.GROUPS_AND_POS_WITHOUT_EMPTY)
        self.assertEqual(self.pre2.get_captures_and_pos(self.TEXT, include_empty=False), self.GROUPS_AND_POS_WITHOUT_EMPTY)

    def test_pregex_on_get_captures_and_relative_pos(self):
        self.assertEqual(self.pre1.get_captures_and_pos(self.TEXT, relative_to_match=True), self.GROUPS_AND_RELATIVE_POS)
        self.assertEqual(self.pre1.get_captures_and_pos(self.TEXT, include_empty=False, relative_to_match=True),
            self.GROUPS_AND_RELATIVE_POS_WITHOUT_EMPTY)
        self.assertEqual(self.pre2.get_captures_and_pos(self.TEXT, include_empty=False, relative_to_match=True),
            self.GROUPS_AND_RELATIVE_POS_WITHOUT_EMPTY)

    def test_pregex_on_replace(self):
        repl = "bb"
        self.assertEqual(self.pre1.replace(self.TEXT, repl), "bb aaa bb bb 99a bb")
        self.assertEqual(self.pre1.replace(self.TEXT, repl, count=1), "bb aaa _9 z9z 99a B0c")
        self.assertEqual(self.pre2.replace(self.TEXT, repl, count=1), "bb aaa _9 z9z 99a B0c")
        self.assertRaises(NegativeArgumentException, self.pre1.replace, self.TEXT, repl, -1)

    def test_pregex_on_split_by_match(self):
        self.assertEqual(self.pre1.split_by_match(self.TEXT), self.SPLIT_BY_MATCH)

    def test_pregex_on_split_by_capture(self):
        self.assertEqual(self.pre1.split_by_capture(self.TEXT, include_empty=True), self.SPLIT_BY_GROUP)
        self.assertEqual(self.pre1.split_by_capture(self.TEXT, include_empty=False), self.SPLIT_BY_GROUP_WITHOUT_EMPTY)


    '''
    Test Protected Methods
    '''
    def test_pregex_on__concat_conditional_group(self):
        self.assertEqual(self.pre1._concat_conditional_group(), f"{self.pre1}")

    def test_pregex_on__quantify_conditional_group(self):
        self.assertEqual(self.pre1._quantify_conditional_group(), f"(?:{self.pre1})")

    def test_pregex_on_addition_operator(self):
        self.assertEqual(str(self.pre1 + self.pre2), f"{self.pre1}{self.pre2}")
        l1, l2 = "a", "b"
        self.assertEqual(str(Pregex(l1) + Pregex(l2)), l1 + l2)
        l1, l2 = "|", "?"
        self.assertEqual(str(Pregex(l1) + Pregex(l2)), f"\\{l1}\\{l2}")


    '''
    Test Overloaded Operators
    '''
    def test_pregex_on_pregex_str_addition(self):
        s = "TEST"
        self.assertEqual(str(self.pre1 + s), f"{self.PATTERN}{s}")
        self.assertEqual(str(s + self.pre1), f"{s}{self.PATTERN}")

    def test_pregex_on_pregex_pregex_addition(self):
        self.assertEqual(str(self.pre1 + self.pre2), f"{self.PATTERN}{self.PATTERN}")
        self.assertEqual(str(self.pre2 + self.pre1), f"{self.PATTERN}{self.PATTERN}")

    def test_pregex_on_multiplication(self):
        self.assertEqual(str(self.pre1.__mul__(1)), self.PATTERN)
        self.assertEqual(str(self.pre1.__mul__(2)), f"(?:{self.PATTERN}){{2}}")
        self.assertRaises(NonPositiveArgumentException, self.pre1.__mul__, 0)
        for val in ["s", 1.1, True]:
            self.assertRaises(NonIntegerArgumentException, self.pre1.__mul__, val)
        self.assertRaises(CannotBeQuantifiedException, MatchAtStart("x").__mul__, 2)

    def test_pregex_on_right_side_multiplication(self):
        self.assertEqual(str(self.pre1.__rmul__(1)), self.PATTERN)
        self.assertEqual(str(self.pre1.__rmul__(2)), f"(?:{self.PATTERN}){{2}}")
        self.assertRaises(NonPositiveArgumentException, self.pre1.__rmul__, 0)
        for val in ["s", 1.1, True]:
            self.assertRaises(NonIntegerArgumentException, self.pre1.__rmul__, val)
        self.assertRaises(CannotBeQuantifiedException, MatchAtStart("x").__rmul__, 2)

if __name__=="__main__":
    unittest.main()