import re
import io
import sys
import unittest
from pregex.core.pre import Pregex, _Type
from unittest.mock import mock_open, patch
from pregex.core.assertions import MatchAtStart, WordBoundary, NonWordBoundary
from pregex.core.exceptions import CannotBeRepeatedException, \
    InvalidArgumentValueException, InvalidArgumentTypeException


class TestPregex(unittest.TestCase):

    TEXT = "A0z aaa _9 z9z 99a B0cDDDD "
    PATTERN = "(?P<group_1>[A-Za-z_])[0-9]+(?P<group_2>[a-z]?)(?P<group_3>DDDD)?"

    pre1 = Pregex(PATTERN, escape=False)
    pre2 = Pregex(PATTERN, escape=False)
    # pre2 is compiled.
    pre2.compile()

    MATCHES = ["A0z", "_9", "z9z", "B0cDDDD"]
    MATCHES_AND_POS = [("A0z", 0, 3), ("_9", 8, 10), ("z9z", 11, 14), ("B0cDDDD", 19, 26)]
    MATCHES_WITH_CONTEXT = ["A0z ", " _9 ", " z9z ", " B0cDDDD "]

    GROUPS = [("A", "z", None), ("_", "", None), ("z", "z", None), ("B", "c", 'DDDD')]
    GROUPS_AND_POS = [
        [('A', 0, 1), ('z', 2, 3), (None, -1, -1)],
        [('_', 8, 9), ('', 10, 10), (None, -1, -1)],
        [('z', 11, 12), ('z', 13, 14), (None, -1, -1)],
        [('B', 19, 20), ('c', 21, 22), ('DDDD', 22, 26)]
    ]
    GROUPS_AND_RELATIVE_POS = [
        [('A', 0, 1), ('z', 2, 3), (None, -1, -1)],
        [('_', 0, 1), ('', 2, 2), (None, -1, -1)],
        [('z', 0, 1), ('z', 2, 3), (None, -1, -1)],
        [('B', 0, 1), ('c', 2, 3), ('DDDD', 3, 7)]
    ]

    GROUPS_WITHOUT_EMPTY = [("A", "z", None), ("_", None), ("z", "z", None), ("B", "c", 'DDDD')]
    GROUPS_AND_POS_WITHOUT_EMPTY = [
        [("A", 0, 1), ("z", 2, 3), (None, -1, -1)],
        [("_", 8, 9), (None, -1, -1)],
        [("z", 11, 12), ("z", 13, 14), (None, -1, -1)],
        [("B", 19, 20), ("c", 21, 22), ('DDDD', 22, 26)]
    ]
    GROUPS_AND_RELATIVE_POS_WITHOUT_EMPTY = [
        [("A", 0, 1), ("z", 2, 3), (None, -1, -1)],
        [("_", 0, 1), (None, -1, -1)],
        [("z", 0, 1), ("z", 2, 3), (None, -1, -1)],
        [("B", 0, 1), ("c", 2, 3), ('DDDD', 3, 7)]
    ]

    GROUPS_AS_DICTS =  [
        {'group_1': 'A', 'group_2': 'z', 'group_3': None},
        {'group_1': '_', 'group_2': '', 'group_3': None},
        {'group_1': 'z', 'group_2': 'z', 'group_3': None},
        {'group_1': 'B', 'group_2': 'c', 'group_3': 'DDDD'},
    ]
    GROUPS_AND_POS_AS_DICTS =  [
        {'group_1': ('A', 0, 1), 'group_2': ('z', 2, 3), 'group_3': (None, -1, -1)},
        {'group_1': ('_', 8, 9), 'group_2': ('', 10, 10), 'group_3': (None, -1, -1)},
        {'group_1': ('z', 11, 12), 'group_2': ('z', 13, 14), 'group_3': (None, -1, -1)},
        {'group_1': ('B', 19, 20), 'group_2': ('c', 21, 22), 'group_3': ('DDDD', 22, 26)},
    ]
    GROUPS_AND_RELATIVE_POS_AS_DICTS =  [
        {'group_1': ('A', 0, 1), 'group_2': ('z', 2, 3), 'group_3': (None, -1, -1)},
        {'group_1': ('_', 0, 1), 'group_2': ('', 2, 2), 'group_3': (None, -1, -1)},
        {'group_1': ('z', 0, 1), 'group_2': ('z', 2, 3), 'group_3': (None, -1, -1)},
        {'group_1': ('B', 0, 1), 'group_2': ('c', 2, 3), 'group_3': ('DDDD', 3, 7)},
    ]

    GROUPS_AS_DICTS_WITHOUT_EMPTY =  [
        {'group_1': 'A', 'group_2': 'z', 'group_3': None},
        {'group_1': '_', 'group_3': None},
        {'group_1': 'z', 'group_2': 'z', 'group_3': None},
        {'group_1': 'B', 'group_2': 'c', 'group_3': 'DDDD'},
    ]
    GROUPS_AND_POS_AS_DICTS_WITHOUT_EMPTY =  [
        {'group_1': ('A', 0, 1), 'group_2': ('z', 2, 3), 'group_3': (None, -1, -1)},
        {'group_1': ('_', 8, 9), 'group_3': (None, -1, -1)},
        {'group_1': ('z', 11, 12), 'group_2': ('z', 13, 14), 'group_3': (None, -1, -1)},
        {'group_1': ('B', 19, 20), 'group_2': ('c', 21, 22), 'group_3': ('DDDD', 22, 26)},
    ]
    GROUPS_AND_RELATIVE_POS_AS_DICTS_WITHOUT_EMPTY =  [
        {'group_1': ('A', 0, 1), 'group_2': ('z', 2, 3), 'group_3': (None, -1, -1)},
        {'group_1': ('_', 0, 1), 'group_3': (None, -1, -1)},
        {'group_1': ('z', 0, 1), 'group_2': ('z', 2, 3), 'group_3': (None, -1, -1)},
        {'group_1': ('B', 0, 1), 'group_2': ('c', 2, 3), 'group_3': ('DDDD', 3, 7)},
    ]
    
    SPLIT_BY_MATCH = [" aaa ", " ", " 99a ", ' ']
    SPLIT_BY_GROUP = ['0', ' aaa ', '9', ' ', '9', ' 99a ', '0', ' ']
    SPLIT_BY_GROUP_WITHOUT_EMPTY = ['0', ' aaa ', '9 ', '9', ' 99a ', '0', ' ']


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

    def test_pregex_on_invalid_argument_type_exception(self):
        for val in [1, 1.3, True, Pregex("z")]:
            self.assertRaises(InvalidArgumentTypeException, Pregex, val)

    def test_pregex_on_match(self):
        text = ":\z^l"
        self.assertTrue(Pregex(text).get_matches(f"text{text}text") == [text])


    '''
    Test Public Methods
    '''
    def test_pregex_on_print_pattern(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        self.pre1.print_pattern(include_flags=False)
        sys.stdout = sys.__stdout__
        self.assertEqual(capturedOutput.getvalue(), f"{self.PATTERN}\n")

    def test_pregex_on_get_pattern(self):
        self.assertEqual(self.pre1.get_pattern(include_flags=False), self.PATTERN)
        self.assertEqual(self.pre1.get_pattern(include_flags=True), f"/{self.PATTERN}/gmsu")

    def test_pregex_on_get_compiled_pattern(self):
        flags = re.MULTILINE | re.DOTALL
        self.assertEqual(self.pre1.get_compiled_pattern(), re.compile(self.PATTERN, flags))

    def test_pregex_on_purge(self):
        self.assertEqual(Pregex.purge(), None)

    def test_pregex_on_has_match(self):
        self.assertEqual(self.pre1.has_match(self.TEXT), True)
        self.assertEqual(self.pre1.has_match("ab"), False)

    def test_pregex_on_compiled_has_match(self):
        self.assertEqual(self.pre2.has_match(self.TEXT), True)
        self.assertEqual(self.pre2.has_match("ab"), False)

    @patch("builtins.open", mock_open(read_data=TEXT))
    def test_pregex_on_has_match_is_path(self):
        self.assertEqual(self.pre1.has_match(None, is_path=True), True)

    def test_pregex_on_is_exact_match(self):
        self.assertEqual(self.pre1.is_exact_match("A0a"), True)
        self.assertEqual(self.pre1.is_exact_match("A0ab"), False)
        self.assertEqual(self.pre1.is_exact_match("aA0a"), False)

    def test_pregex_on_compiled_is_exact_match(self):
        self.assertEqual(self.pre2.is_exact_match("A0a"), True)
        self.assertEqual(self.pre2.is_exact_match("A0ab"), False)
        self.assertEqual(self.pre2.is_exact_match("aA0a"), False)

    @patch("builtins.open", mock_open(read_data="A0a"))
    def test_pregex_on_is_exact_match_is_path(self):
        self.assertEqual(self.pre1.is_exact_match(None, is_path=True), True)
    
    def test_pregex_on_iterate_matches(self):
        self.assertEqual([match for match in self.pre1.iterate_matches(self.TEXT)], self.MATCHES)

    def test_pregex_on_compiled_iterate_matches(self):
        self.assertEqual([match for match in self.pre2.iterate_matches(self.TEXT)], self.MATCHES)

    @patch("builtins.open", mock_open(read_data=TEXT))
    def test_pregex_on_iterate_matches_is_path(self):
        self.assertEqual([match for match in self.pre1.iterate_matches(None, is_path=True)], self.MATCHES)

    def test_pregex_on_iterate_matches_and_pos(self):
        self.assertEqual([tup for tup in self.pre1.iterate_matches_and_pos(self.TEXT)], self.MATCHES_AND_POS)

    def test_pregex_on_compiled_iterated_matches_and_pos(self):
        self.assertEqual([tup for tup in self.pre2.iterate_matches_and_pos(self.TEXT)], self.MATCHES_AND_POS)

    @patch("builtins.open", mock_open(read_data=TEXT))
    def test_pregex_on_iterate_matches_and_pos_is_path(self):
        self.assertEqual([tup for tup in self.pre1.iterate_matches_and_pos(None, is_path=True)], self.MATCHES_AND_POS)

    def test_pregex_on_iterate_matches_with_context(self):
        self.assertEqual([match for match in self.pre1.iterate_matches_with_context(self.TEXT, n_left=1, n_right=1)],
            self.MATCHES_WITH_CONTEXT)

    def test_pregex_on_iterate_captures(self):
        self.assertEqual([group_tup for group_tup in self.pre1.iterate_captures(self.TEXT)], self.GROUPS)

    def test_pregex_on_compiled_iterate_captures(self):
        self.assertEqual([group_tup for group_tup in self.pre2.iterate_captures(self.TEXT)], self.GROUPS)

    def test_pregex_on_iterate_captures_without_empty(self):
        self.assertEqual([group_tup for group_tup in self.pre1.iterate_captures(self.TEXT, include_empty=False)],
            self.GROUPS_WITHOUT_EMPTY)

    @patch("builtins.open", mock_open(read_data=TEXT))
    def test_pregex_on_iterate_captures_is_path(self):
        self.assertEqual([group_tup for group_tup in self.pre1.iterate_captures(None, is_path=True)], self.GROUPS)

    def test_pregex_on_iterate_captures_and_pos(self):
        self.assertEqual([group_list for group_list in self.pre1.iterate_captures_and_pos(self.TEXT)], self.GROUPS_AND_POS)

    def test_pregex_on_compiled_iterate_captures_and_pos(self):
        self.assertEqual([group_list for group_list in self.pre2.iterate_captures_and_pos(self.TEXT)], self.GROUPS_AND_POS)

    def test_pregex_on_iterate_captures_and_pos_without_empty(self):
        self.assertEqual([group_list for group_list in self.pre1.iterate_captures_and_pos(self.TEXT, include_empty=False)],
            self.GROUPS_AND_POS_WITHOUT_EMPTY)

    def test_pregex_on_iterate_captures_and_pos_relative_to_match(self):
        self.assertEqual([group_list for group_list in self.pre1.iterate_captures_and_pos(self.TEXT, relative_to_match=True)],
            self.GROUPS_AND_RELATIVE_POS)
    
    def test_pregex_on_iterate_captures_and_pos_relative_to_match_without_empty(self):
        self.assertEqual([group_list for group_list in self.pre1.iterate_captures_and_pos(self.TEXT,
            include_empty=False, relative_to_match=True)], self.GROUPS_AND_RELATIVE_POS_WITHOUT_EMPTY)

    @patch("builtins.open", mock_open(read_data=TEXT))
    def test_pregex_on_iterate_captures_and_pos_is_path(self):
        self.assertEqual([group_tup for group_tup in self.pre1.iterate_captures_and_pos(None, is_path=True)],
            self.GROUPS_AND_POS)

    def test_pregex_on_iterate_named_captures(self):
        self.assertEqual([group_dict for group_dict in self.pre1.iterate_named_captures(self.TEXT)], self.GROUPS_AS_DICTS)

    def test_pregex_on_compiled_iterate_named_captures(self):
        self.assertEqual([group_dict for group_dict in self.pre2.iterate_named_captures(self.TEXT)], self.GROUPS_AS_DICTS)

    def test_pregex_on_iterate_named_captures_without_empty(self):
        self.assertEqual([group_dict for group_dict in self.pre1.iterate_named_captures(self.TEXT, include_empty=False)],
            self.GROUPS_AS_DICTS_WITHOUT_EMPTY)

    @patch("builtins.open", mock_open(read_data=TEXT))
    def test_pregex_on_iterate_named_captures_is_path(self):
        self.assertEqual([group_dict for group_dict in self.pre1.iterate_named_captures(None, is_path=True)],
            self.GROUPS_AS_DICTS)

    def test_pregex_on_iterate_named_captures_and_pos(self):
        self.assertEqual([group_dict for group_dict in self.pre1.iterate_named_captures_and_pos(self.TEXT)],
            self.GROUPS_AND_POS_AS_DICTS)

    def test_pregex_on_compiled_iterate_named_captures_and_pos(self):
        self.assertEqual([group_dict for group_dict in self.pre2.iterate_named_captures_and_pos(self.TEXT)],
            self.GROUPS_AND_POS_AS_DICTS)

    def test_pregex_on_iterate_named_captures_and_pos_without_empty(self):
        self.assertEqual([group_dict for group_dict in self.pre1.iterate_named_captures_and_pos(self.TEXT, include_empty=False)],
            self.GROUPS_AND_POS_AS_DICTS_WITHOUT_EMPTY)

    def test_pregex_on_iterate_named_captures_and_relative_pos(self):
        self.assertEqual([group_dict for group_dict in self.pre1.iterate_named_captures_and_pos(self.TEXT, relative_to_match=True)],
            self.GROUPS_AND_RELATIVE_POS_AS_DICTS)

    def test_pregex_on_iterate_named_captures_and_relative_pos_without_empty(self):
        self.assertEqual([group_dict for group_dict in self.pre1.iterate_named_captures_and_pos(
            self.TEXT, include_empty=False, relative_to_match=True)],
            self.GROUPS_AND_RELATIVE_POS_AS_DICTS_WITHOUT_EMPTY)

    @patch("builtins.open", mock_open(read_data=TEXT))
    def test_pregex_on_iterate_named_captures_and_pos_is_path(self):
        self.assertEqual([group_dict for group_dict in self.pre1.iterate_named_captures_and_pos(None, is_path=True)],
            self.GROUPS_AND_POS_AS_DICTS)

    def test_pregex_on_get_matches(self):
        self.assertEqual(self.pre1.get_matches(self.TEXT), self.MATCHES)

    def test_pregex_on_compiled_get_matches(self):
        self.assertEqual(self.pre2.get_matches(self.TEXT), self.MATCHES)

    def test_pregex_on_get_matches_and_pos(self):
        self.assertEqual(self.pre1.get_matches_and_pos(self.TEXT), self.MATCHES_AND_POS)

    def test_pregex_on_compiled_get_matches_and_pos(self):    
        self.assertEqual(self.pre2.get_matches_and_pos(self.TEXT), self.MATCHES_AND_POS)

    def test_pregex_on_get_matches_with_context(self):
        self.assertEqual([match for match in self.pre1.get_matches_with_context(self.TEXT, n_left=1, n_right=1)],
            self.MATCHES_WITH_CONTEXT)

    def test_pregex_on_get_matches_with_context_invalid_argument_type_exception(self):
        self.assertRaises(InvalidArgumentTypeException, self.pre1.get_matches_with_context, self.TEXT, '1')
        self.assertRaises(InvalidArgumentTypeException, self.pre1.get_matches_with_context, source=self.TEXT, n_right='1')

    def test_pregex_on_get_matches_with_context_invalid_argument_value_exception(self):
        self.assertRaises(InvalidArgumentValueException, self.pre1.get_matches_with_context, source=self.TEXT, n_left=-1)
        self.assertRaises(InvalidArgumentValueException, self.pre1.get_matches_with_context, source=self.TEXT, n_right=-1)

    def test_pregex_on_get_captures(self):
        self.assertEqual(self.pre1.get_captures(self.TEXT), self.GROUPS)
    
    def test_pregex_on_compiled_get_captures(self):
        self.assertEqual(self.pre2.get_captures(self.TEXT), self.GROUPS)

    def test_pregex_on_get_captures_without_empty(self):
        self.assertEqual(self.pre1.get_captures(self.TEXT, include_empty=False), self.GROUPS_WITHOUT_EMPTY)

    def test_pregex_on_get_captures_and_pos(self):
        self.assertEqual(self.pre1.get_captures_and_pos(self.TEXT), self.GROUPS_AND_POS)

    def test_pregex_on_compiled_get_captures_and_pos(self):
        self.assertEqual(self.pre2.get_captures_and_pos(self.TEXT), self.GROUPS_AND_POS)

    def test_pregex_on_get_captures_and_pos_without_empty(self):
        self.assertEqual(self.pre1.get_captures_and_pos(self.TEXT, include_empty=False), self.GROUPS_AND_POS_WITHOUT_EMPTY)

    def test_pregex_on_get_captures_and_relative_pos(self):
        self.assertEqual(self.pre1.get_captures_and_pos(self.TEXT, relative_to_match=True), self.GROUPS_AND_RELATIVE_POS)

    def test_pregex_on_get_captures_and_relative_pos_without_empty(self):
        self.assertEqual(self.pre1.get_captures_and_pos(self.TEXT, include_empty=False, relative_to_match=True),
            self.GROUPS_AND_RELATIVE_POS_WITHOUT_EMPTY)

    def test_pregex_on_get_named_captures(self):
        self.assertEqual(self.pre1.get_named_captures(self.TEXT), self.GROUPS_AS_DICTS)
    
    def test_pregex_on_compiled_get_named_captures(self):
        self.assertEqual(self.pre2.get_named_captures(self.TEXT), self.GROUPS_AS_DICTS)

    def test_pregex_on_get_named_captures_without_empty(self):
        self.assertEqual(self.pre1.get_named_captures(self.TEXT, include_empty=False),
            self.GROUPS_AS_DICTS_WITHOUT_EMPTY)

    def test_pregex_on_get_named_captures_and_pos(self):
        self.assertEqual(self.pre1.get_named_captures_and_pos(self.TEXT), self.GROUPS_AND_POS_AS_DICTS)

    def test_pregex_on_compiled_get_named_captures_and_pos(self):
        self.assertEqual(self.pre2.get_named_captures_and_pos(self.TEXT), self.GROUPS_AND_POS_AS_DICTS)

    def test_pregex_on_get_named_captures_and_pos_without_empty(self):
        self.assertEqual(self.pre1.get_named_captures_and_pos(self.TEXT, include_empty=False),
            self.GROUPS_AND_POS_AS_DICTS_WITHOUT_EMPTY)

    def test_pregex_on_get_named_captures_and_relative_pos(self):
        self.assertEqual(self.pre1.get_named_captures_and_pos(self.TEXT, relative_to_match=True),
            self.GROUPS_AND_RELATIVE_POS_AS_DICTS)

    def test_pregex_on_get_named_captures_and_relative_pos_without_empty(self):
        self.assertEqual(self.pre1.get_named_captures_and_pos(self.TEXT, include_empty=False,
            relative_to_match=True), self.GROUPS_AND_RELATIVE_POS_AS_DICTS_WITHOUT_EMPTY)

    def test_pregex_on_replace(self):
        repl = "bb"
        self.assertEqual(self.pre1.replace(self.TEXT, repl), "bb aaa bb bb 99a bb ")
        self.assertEqual(self.pre1.replace(self.TEXT, repl, count=1), "bb aaa _9 z9z 99a B0cDDDD ")

    def test_pregex_on_compiled_replace(self):
        repl = "bb"
        self.assertEqual(self.pre2.replace(self.TEXT, repl), "bb aaa bb bb 99a bb ")
        self.assertEqual(self.pre1.replace(self.TEXT, repl, count=1), "bb aaa _9 z9z 99a B0cDDDD ")

    @patch("builtins.open", mock_open(read_data=TEXT))
    def test_pregex_on_replace_is_path(self):
        repl = "bb"
        self.assertEqual(self.pre1.replace(None, repl, is_path=True), "bb aaa bb bb 99a bb ")

    def test_pregex_on_replace_invalid_argument_value_exception(self):
        repl = "bb"
        self.assertRaises(InvalidArgumentValueException, self.pre1.replace, self.TEXT, repl, -1)

    def test_pregex_on_split_by_match(self):
        self.assertEqual(self.pre1.split_by_match(self.TEXT), self.SPLIT_BY_MATCH)

    def test_pregex_on_compiled_split_by_match(self):
        self.assertEqual(self.pre2.split_by_match(self.TEXT), self.SPLIT_BY_MATCH)

    @patch("builtins.open", mock_open(read_data=TEXT))
    def test_pregex_on_split_by_match_is_path(self):
        self.assertEqual(self.pre1.split_by_match(None, is_path=True), self.SPLIT_BY_MATCH)

    def test_pregex_on_split_by_capture(self):
        self.assertEqual(self.pre1.split_by_capture(self.TEXT, include_empty=True), self.SPLIT_BY_GROUP)

    def test_pregex_on_compiled_split_by_capture(self):
        self.assertEqual(self.pre2.split_by_capture(self.TEXT, include_empty=True), self.SPLIT_BY_GROUP)

    def test_pregex_on_split_by_capture_without_empty(self):
        self.assertEqual(self.pre1.split_by_capture(self.TEXT, include_empty=False), self.SPLIT_BY_GROUP_WITHOUT_EMPTY)

    @patch("builtins.open", mock_open(read_data=TEXT))
    def test_pregex_on_split_by_capture_is_path(self):
        self.assertEqual(self.pre1.split_by_capture(None, is_path=True), self.SPLIT_BY_GROUP)

    def test_pregex_on_quantifiers(self):
        pre = Pregex('a')
        self.assertEqual(str(pre.optional()), f"{pre}?")
        self.assertEqual(str(pre.indefinite()), f"{pre}*")
        self.assertEqual(str(pre.one_or_more()), f"{pre}+")
        self.assertEqual(str(pre.exactly(n=3)), f"{pre}{{{3}}}")
        self.assertEqual(str(pre.at_least(n=3)), f"{pre}{{3,}}")
        self.assertEqual(str(pre.at_most(n=3)), f"{pre}{{,3}}")
        self.assertEqual(str(pre.at_least_at_most(n=3, m=5)), f"{pre}{{{3},{5}}}")

    def test_pregex_on_groups(self):
        pre = Pregex('a')
        self.assertEqual(str(pre.capture()), f"({pre})")
        self.assertEqual(str(pre.group()), f"(?:{pre})")
        self.assertEqual(str(pre.group(is_case_insensitive=True)), f"(?i:{pre})")

    def test_pregex_on_operators(self):
        pre, other_pre = Pregex('a'), Pregex("abc")
        self.assertEqual(str(pre.concat(other_pre)), f"{pre}{other_pre}")
        self.assertEqual(str(pre.concat(other_pre, on_right=False)), f"{other_pre}{pre}")
        self.assertEqual(str(pre.either(other_pre)), f"{pre}|{other_pre}")
        self.assertEqual(str(pre.either(other_pre, on_right=False)), f"{other_pre}|{pre}")
        self.assertEqual(str(pre.enclose(other_pre)), f"{other_pre}{pre}{other_pre}")

    def test_pregex_on_anchor_assertions(self):
        pre = Pregex('a')
        self.assertEqual(str(pre.match_at_start()), f"\\A{pre}")
        self.assertEqual(str(pre.match_at_line_start()), f"^{pre}")
        self.assertEqual(str(pre.match_at_end()), f"{pre}\\Z")
        self.assertEqual(str(pre.match_at_line_end()), f"{pre}$")
        self.assertEqual(str(pre + WordBoundary()), f"{pre}\\b")
        self.assertEqual(str(WordBoundary() + pre), f"\\b{pre}")
        self.assertEqual(str(WordBoundary() + pre + WordBoundary()), f"\\b{pre}\\b")
        self.assertEqual(str(pre + NonWordBoundary()), f"{pre}\\B")
        self.assertEqual(str(NonWordBoundary() + pre), f"\\B{pre}")
        self.assertEqual(str(NonWordBoundary() + pre + NonWordBoundary()), f"\\B{pre}\\B")

    def test_pregex_on_lookaround_assertions(self):
        pre, other = Pregex('a'), Pregex("abc")
        self.assertEqual(str(pre.followed_by(other)), f"{pre}(?={other})")
        self.assertEqual(str(pre.not_followed_by(other)), f"{pre}(?!{other})")
        self.assertEqual(str(pre.preceded_by(other)), f"(?<={other}){pre}")
        self.assertEqual(str(pre.not_preceded_by(other)), f"(?<!{other}){pre}")
        self.assertEqual(str(pre.enclosed_by(other)), f"(?<={other}){pre}(?={other})")
        self.assertEqual(str(pre.not_enclosed_by(other)), f"(?<!{other}){pre}(?!{other})")


    '''
    Test Protected Methods
    '''
    def test_pregex_on__concat_conditional_group(self):
        self.assertEqual(self.pre1._concat_conditional_group(), f"{self.pre1}")

    def test_pregex_on__quantify_conditional_group(self):
        self.assertEqual(self.pre1._quantify_conditional_group(), f"(?:{self.pre1})")

    def test_pregex_on__assert_conditional_group(self):
        self.assertEqual(self.pre1._assert_conditional_group(), f"{self.pre1}")

    def test_pregex_on_addition_operator(self):
        self.assertEqual(str(self.pre1 + self.pre2), f"{self.pre1}{self.pre2}")
        l1, l2 = "a", "b"
        self.assertEqual(str(Pregex(l1) + Pregex(l2)), l1 + l2)
        l1, l2 = "|", "?"
        self.assertEqual(str(Pregex(l1) + Pregex(l2)), f"\\{l1}\\{l2}")

    def test_pregex_on__to_pregex_invalid_argument_type_exception(self):
        self.assertRaises(InvalidArgumentTypeException, Pregex._to_pregex, True)


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
        self.assertEqual(str(self.pre1.__mul__(0)), "")
        self.assertRaises(InvalidArgumentValueException, self.pre1.__mul__, -1)
        for val in ["s", 1.1, True]:
            self.assertRaises(InvalidArgumentTypeException, self.pre1.__mul__, val)
        self.assertRaises(CannotBeRepeatedException, MatchAtStart("x").__mul__, 2)

    def test_pregex_on_right_side_multiplication(self):
        self.assertEqual(str(self.pre1.__rmul__(1)), self.PATTERN)
        self.assertEqual(str(self.pre1.__rmul__(2)), f"(?:{self.PATTERN}){{2}}")
        self.assertEqual(str(self.pre1.__rmul__(0)), "")
        self.assertRaises(InvalidArgumentValueException, self.pre1.__rmul__, -1)
        for val in ["s", 1.1, True]:
            self.assertRaises(InvalidArgumentTypeException, self.pre1.__rmul__, val)
        self.assertRaises(CannotBeRepeatedException, MatchAtStart("x").__rmul__, 2)

    '''
    Test Pregex's "__infer_type".
    '''
    def test_pregex_infer_type(self):
        self.assertEqual(Pregex("abc|acd", escape=False)._get_type(), _Type.Alternation)
        self.assertEqual(Pregex("(abc|acd)|(ab)?", escape=False)._get_type(), _Type.Alternation)
        self.assertEqual(Pregex("(?<!a)b|c", escape=False)._get_type(), _Type.Alternation)
        self.assertEqual(Pregex("(?<!a)b", escape=False)._get_type(), _Type.Assertion)
        self.assertEqual(Pregex("(?<=[(\s])a", escape=False)._get_type(), _Type.Assertion)
        self.assertEqual(Pregex("(?<!a)(?:b|c)", escape=False)._get_type(), _Type.Assertion)
        self.assertEqual(Pregex("(?<![)])(?:b|c)", escape=False)._get_type(), _Type.Assertion)
        self.assertEqual(Pregex("(?<!\))(?:b|c)", escape=False)._get_type(), _Type.Assertion)
        self.assertEqual(Pregex("[(.z;!\]]", escape=False)._get_type(), _Type.Class)
        self.assertEqual(Pregex("[\[a\]]", escape=False)._get_type(), _Type.Class)
        self.assertEqual(Pregex("(abc|acd)", escape=False)._get_type(), _Type.Group)
        self.assertEqual(Pregex("(a\\\\\))", escape=False)._get_type(), _Type.Group)
        self.assertEqual(Pregex("(?abc)", escape=False)._get_type(), _Type.Group)
        self.assertEqual(Pregex("\w\s", escape=False)._get_type(), _Type.Other)
        self.assertEqual(Pregex("([A-Za-z_])[0-9]+([a-z]?)", escape=False)._get_type(), _Type.Other)
        self.assertEqual(Pregex("(?abc)(abc)", escape=False)._get_type(), _Type.Other)
        self.assertEqual(Pregex("(abc|acd)\|(ab)?", escape=False)._get_type(), _Type.Other)
        self.assertEqual(Pregex("((abc|acd)|(ab))\\{1234,1245\\}", escape=False)._get_type(), _Type.Other)
        self.assertEqual(Pregex("((abc|acd)|(ab))?", escape=False)._get_type(), _Type.Quantifier)
        self.assertEqual(Pregex("((abc|acd)|(ab)){1234,1245}", escape=False)._get_type(), _Type.Quantifier)


class TestPregexEmpty(unittest.TestCase):

    pre = Pregex()
    text = "text"

    def test_empty(self):
        self.assertEqual(str(Pregex()), "")

    def test_empty_on_type(self):
        self.assertEqual(Pregex()._get_type(), _Type.Empty)

    def test_empty_on_match(self):
        self.assertTrue(Pregex().get_matches("") == [""])

    def test_empty_on_addition(self):
        self.assertEqual(str(self.pre + self.text), f"{self.text}")
        self.assertEqual(str(self.text + self.pre), f"{self.text}")

    def test_empty_on_multiplication(self):
        self.assertEqual(str(3 * self.pre), f"{self.pre}")
        self.assertEqual(str(self.pre * 3), f"{self.pre}")

    def test_empty_on_quantifiers(self):
        self.assertEqual(str(self.pre.optional()), f"{self.pre}")
        self.assertEqual(str(self.pre.indefinite()), f"{self.pre}")
        self.assertEqual(str(self.pre.one_or_more()), f"{self.pre}")
        self.assertEqual(str(self.pre.exactly(n=3)), f"{self.pre}")
        self.assertEqual(str(self.pre.at_least(n=3)), f"{self.pre}")
        self.assertEqual(str(self.pre.at_most(n=3)), f"{self.pre}")
        self.assertEqual(str(self.pre.at_least_at_most(n=3, m=5)), f"{self.pre}")

    def test_empty_on_groups(self):
        self.assertEqual(str(self.pre.capture()), '')
        self.assertEqual(str(self.pre.group()), '')

    def test_empty_on_operators(self):
        other_pre = Pregex("abc")
        self.assertEqual(str(self.pre.concat(other_pre)), f"{other_pre}")
        self.assertEqual(str(self.pre.concat(other_pre, on_right=False)), f"{other_pre}")
        self.assertEqual(str(self.pre.either(other_pre)), f"|{other_pre}")
        self.assertEqual(str(self.pre.either(other_pre, on_right=False)), f"{other_pre}|")
        self.assertEqual(str(self.pre.enclose(other_pre)), f"{other_pre}{other_pre}")

    def test_empty_on_anchor_assertions(self):
        self.assertEqual(str(self.pre.match_at_start()), "\\A")
        self.assertEqual(str(self.pre.match_at_line_start()), "^")
        self.assertEqual(str(self.pre.match_at_end()), "\\Z")
        self.assertEqual(str(self.pre.match_at_line_end()), "$")
        self.assertEqual(str(self.pre + WordBoundary()), "\\b")
        self.assertEqual(str(WordBoundary() + self.pre), "\\b")
        self.assertEqual(str(WordBoundary() + self.pre + WordBoundary()), "\\b\\b")
        self.assertEqual(str(self.pre + NonWordBoundary()), "\\B")
        self.assertEqual(str(NonWordBoundary() + self.pre), "\\B")
        self.assertEqual(str(NonWordBoundary() + self.pre + NonWordBoundary()), "\\B\\B")

    def test_empty_on_lookaround_assertions(self):
        other = Pregex("abc")
        self.assertEqual(str(self.pre.followed_by(other)), f"(?={other})")
        self.assertEqual(str(self.pre.not_followed_by(other)), f"(?!{other})")
        self.assertEqual(str(self.pre.preceded_by(other)), f"(?<={other})")
        self.assertEqual(str(self.pre.not_preceded_by(other)), f"(?<!{other})")
        self.assertEqual(str(self.pre.enclosed_by(other)), f"(?<={other})(?={other})")
        self.assertEqual(str(self.pre.not_enclosed_by(other)), f"(?<!{other})(?!{other})")


if __name__=="__main__":
    unittest.main()