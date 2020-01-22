from cBinder.CType import get_c_type_for_type


class StructMember:
    """
    Class representing a single member of a struct

    Attributes
    ----------
    name : str
        Member name
    type : str
        Member type
    is_array : bool
        True if member is an array
    sizes : tuple
        Sizes of the array, default (None,)
    struct : str
        Python object type used to hold this member in wrapper
    """

    def __init__(self, member, enums):
        self.name = member['name']
        self.type = member['type']
        self.c_type = get_c_type_for_type(self.type)
        self.is_array = member['array'] != 0 or member['pointer'] != 0
        self.sizes = (None,)
        self.struct = member['class']['name'] if member['class'] != 0 else None
        self.enum = self.type if self.type in enums else None

    def __str__(self):
        return self.name + (':' + self.struct if self.struct else '')


class StructDeclaration:
    """
    Class representing a struct declaration

    Attributes
    ----------
    name : str
        struct name
    members : list
        List of StructMember objects
    """

    def __init__(self, struct, enums):
        self.name = struct['name']
        self.members = [StructMember(member, enums) for member in struct['properties']['public']]
        self.declaration_string = self._build_declaration_string(struct)

    def _build_declaration_string(self, struct):
        parts = ['typedef struct{']
        for member, member_info in zip(self.members, struct['properties']['public']):
            asterisks = '*' * member_info['pointer']
            if not member_info['array']:
                arrays = ''
            elif not member_info.get('multi_dimensional_array', 0):
                arrays = f'[{member_info["array_size"]}]'
            elif member_info['multi_dimensional_array_size']:
                sizes_description = member_info['multi_dimensional_array_size']
                arr_sizes = [int(arr_size) for arr_size in sizes_description.split('x')]
                arrays = ''.join([f'[{arr_size}]' for arr_size in arr_sizes])
            # because we go through this process twice, first time without minipreprocessing
            # this alternative makes sure no error will be thrown
            else:
                arrays = '[]' * member_info.get['multi_dimensional_array']
            parts.append(member.type + ' ' + asterisks + member.name + arrays + ';')
        parts += ['}', self.name, ';\n']

        return ''.join(parts)
