import re
import pregex.pre as _pre
import pregex.exceptions as _exceptions


class __Group(_pre.Pregex):
    '''
    Every "Group" class must inherit from this class.
    '''
    def __init__(self, pre: str or _pre.Pregex, transform) -> _pre.Pregex:
        pre = transform(__class__._to_pregex(pre))
        super().__init__(str(pre), pre._get_group_on_concat(), pre._get_group_on_quantify())


class CapturingGroup(__Group):
    '''
    Creates a capturing group out of the provided pattern.

    NOTE:
        - Creating a capturing group out of a capturing group does nothing to it.
        - Creating a capturing group out of a non-capturing group converts it to a capturing group.
        - Creating a named capturing group out of an unnamed capturing group, assigns a name to it.
        - Creating a named capturing group out of a named capturing group, changes the group's name.
    '''

    def __init__(self, pre: str or _pre.Pregex, name: str = ''):
        '''
        Creates a capturing group out of the provided pattern.

        :param Pregex | str pre: The pattern out of which the capturing group is created.
        :param str name: The name that is assigned to the captured group for backreference purposes.

        NOTE:
            - Creating a capturing group out of a capturing group does nothing to it.
            - Creating a capturing group out of a non-capturing group converts it to a capturing group.
            - Creating a named capturing group out of an unnamed capturing group, assigns a name to it.
            - Creating a named capturing group out of a named capturing group, changes the group's name.
        '''
        super().__init__(pre, lambda pre: pre._capturing_group(name))
        self.name = name


class NonCapturingGroup(__Group):
    '''
    Creates a non-capturing group out of the provided pattern.

    NOTE:
        - Creating a non-capturing group out of a non-capturing group does nothing to it.
        - Creating a non-capturing group out of a capturing group converts it to a non-capturing group.
    '''

    def __init__(self, pre: str or _pre.Pregex):
        '''
        Creates a non-capturing group out of the provided pattern.

        :param Pregex | str pre: The expression out of which the non-capturing group is created.

        NOTE:
            - Creating a non-capturing group out of a non-capturing group does nothing to it.
            - Creating a non-capturing group out of a capturing group converts it to a non-capturing group.
        '''
        super().__init__(pre, lambda pre: pre._non_capturing_group())


class Backreference(_pre.Pregex):
    '''
    Creates a backreference to some previously declared named capturing group.\
    A backreference matches the same text as the text that was most recently \
    matched by the captured group with the same name.

    Consider for example the pattern "(?<g1>[A-Za-z])[0-9]\k<g1>{2}" which\
    contains a capturing group named "g1", along with a (quantified) backreference\
    "\k<g1>{2}". Here are some examples that will match this pattern and some that won't:

    - MATCHES: ["a0aa", "B5BB", "Y7YY"]
    - NON-MATCHES: ["aaaa", "a0bb", "a0ab"], 
    '''
    def __init__(self, name: str):
        if not isinstance(name, str):
            raise _exceptions.NonStringArgumentException()
        if re.fullmatch("[A-Za-z_][A-Za-z_0-9]*", name) is None:
            raise _exceptions.InvalidCapturingGroupNameException(name)
        super().__init__(f"(?P={name})", group_on_concat=False, group_on_quantify=False)