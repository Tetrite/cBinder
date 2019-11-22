from enum import Enum


def get_c_type_for_type(t):
    """
    Returns CType object for given type,
    None if no CType object with this type was found
    """
    for ct in CType:
        if ct.value == t:
            return ct

    return None


class CType(Enum):
    """Enum describing C language types"""
    SHORT = 'short'
    SHORT_POINTER = 'short *'
    SHORT_INT = 'short int'
    SHORT_INT_POINTER = 'short int *'
    SIGNED_SHORT = 'signed short'
    SIGNED_SHORT_POINTER = 'signed short *'
    SIGNED_SHORT_INT = 'signed short int'
    SIGNED_SHORT_INT_POINTER = 'signed short int *'
    UNSIGNED_SHORT = 'unsigned short'
    UNSIGNED_SHORT_POINTER = 'unsigned short *'
    UNSIGNED_SHORT_INT = 'unsigned short int'
    UNSIGNED_SHORT_INT_POINTER = 'unsigned short int *'
    SIGNED_INT = 'signed int'
    SIGNED_INT_POINTER = 'signed int *'
    SIGNED = 'signed'
    SIGNED_POINTER = 'signed *'
    UNSIGNED = 'unsigned'
    UNSIGNED_POINTER = 'unsigned *'
    UNSIGNED_INT = 'unsigned int'
    UNSIGNED_INT_POINTER = 'unsigned int *'
    INT = 'int'
    INT_POINTER = 'int *'
    FLOAT = 'float'
    FLOAT_POINTER = 'float *'
    DOUBLE = 'double'
    DOUBLE_POINTER = 'double *'
    LONG = 'long'
    LONG_POINTER = 'long *'

    def get_ffi_string_def(self):
        """Returns type name for memory allocation in cffi"""
        if self.value.endswith(' *'):
            return self.value[:-2]
        else:
            return self.value
