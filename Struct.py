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

    def __init__(self, member):
        self.name = member['name']
        self.type = member['type']
        self.is_array = member['array'] != 0 or member['pointer'] != 0
        self.sizes = (None,)
        self.struct = None

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

    def __init__(self, struct):
        self.name = struct['name']
        self.members = [StructMember(member) for member in struct['properties']['public']]
