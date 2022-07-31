import re
import pregex.pre as _pre
import pregex.exceptions as _exceptions


class __Group(_pre.Pregex):
    '''
    Every "Group" class must inherit from this class.
    '''
    def __init__(self, pre: _pre.Pregex or str, transform) -> _pre.Pregex:
        pre = transform(__class__._to_pregex(pre))
        super().__init__(str(pre), pre._get_group_on_concat(), pre._get_group_on_quantify())


class CapturingGroup(__Group):
    '''
    Creates a capturing group out of the provided pattern.

    :param Pregex | str pre: The pattern out of which the capturing group is created.
    :param str name: The name that is assigned to the captured group for backreference purposes. \
        A value of "''" indicates that no name is to be assigned to the group. Defaults to "''".

    NOTE:
        - Creating a capturing group out of a capturing group does nothing to it.
        - Creating a capturing group out of a non-capturing group converts it to a capturing group.
        - Creating a named capturing group out of an unnamed capturing group, assigns a name to it.
        - Creating a named capturing group out of a named capturing group, changes the group's name.
    '''

    def __init__(self, pre: _pre.Pregex or str, name: str = ''):
        '''
        Creates a capturing group out of the provided pattern.

        :param Pregex | str pre: The pattern out of which the capturing group is created.
        :param str name: The name that is assigned to the captured group for backreference purposes. \
            A value of "''" indicates that no name is to be assigned to the group. Defaults to "''".

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

    :param Pregex | str pre: The expression out of which the non-capturing group is created.

    NOTE:
        - Creating a non-capturing group out of a non-capturing group does nothing to it.
        - Creating a non-capturing group out of a capturing group converts it to a non-capturing group.
    '''

    def __init__(self, pre: _pre.Pregex or str):
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
    matched by the captured group with the specified name.

    :param str name: The name of the referenced capturing group.
    '''

    def __init__(self, name: str):
        '''
        Creates a backreference to some previously declared named capturing group.\
        A backreference matches the same text as the text that was most recently \
        matched by the captured group with the specified name.

        :param str name: The name of the referenced capturing group.
        '''
        if not isinstance(name, str):
            raise _exceptions.NonStringArgumentException()
        if re.fullmatch("[A-Za-z_][A-Za-z_0-9]*", name) is None:
            raise _exceptions.InvalidCapturingGroupNameException(name)
        super().__init__(f"(?P={name})", group_on_concat=False, group_on_quantify=False)

    
class Conditional(_pre.Pregex):
    '''
    Given the name of a capturing-group, matches 'pre1' only if said capturing-group has \
    been previously matched. Furthermore, if a second pattern 'pre2' is provided, then this \
    pattern is matched in case the referenced capturing-group was not matched, though one \
    should be aware that for this to be possible, the referenced capturing group must be optional.

    :param str name: The name of the referenced capturing group.
    :param Pregex | str pre1: The pattern that is to be matched in case condition is true.
    :param Pregex | str pre2: The pattern that is to be matched in case condition is false. \
        Defaults to "''".
    '''

    def __init__(self, name: str, pre1: _pre.Pregex or str, pre2: _pre.Pregex or str = ''):
        '''
        Given the name of a capturing-group, matches 'pre1' only if said capturing-group has\
        been previously matched. Furthermore, if a second pattern 'pre2' is provided, then this \
        pattern is matched in case the referenced capturing-group was not matched, though one \
        should be aware that for this to be possible, the referenced capturing group must be optional.

        :param str name: The name of the referenced capturing group.
        :param Pregex | str pre1: The pattern that is to be matched in case condition is true.
        :param Pregex | str pre2: The pattern that is to be matched in case condition is false. \
            Defaults to "''".
        '''
        if not isinstance(name, str):
            raise _exceptions.NonStringArgumentException()
        if re.fullmatch("[A-Za-z_][A-Za-z_0-9]*", name) is None:
            raise _exceptions.InvalidCapturingGroupNameException(name)
        super().__init__(f"(?({name}){pre1}{'|' + str(pre2) if pre2 != '' else ''})", group_on_concat=False, group_on_quantify=False)