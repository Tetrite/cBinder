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
    LONG_INT = 'long int'
    LONG_INT_POINTER = 'long int *'
    SIGNED_LONG = 'signed long'
    SIGNED_LONG_POINTER = 'signed long *'
    SIGNED_LONG_INT = 'signed long int'
    SIGNED_LONG_INT_POINTER = 'signed long int *'
    UNSIGNED_LONG = 'unsigned long'
    UNSIGNED_LONG_POINTER = 'unsigned long *'
    UNSIGNED_LONG_INT = 'unsigned long int'
    UNSIGNED_LONG_INT_POINTER = 'unsigned long int *'
    LONG_LONG = 'long long'
    LONG_LONG_POINTER = 'long long *'
    LONG_LONG_INT = 'long long int'
    LONG_LONG_INT_POINTER = 'long long int *'
    SIGNED_LONG_LONG = 'signed long long'
    SIGNED_LONG_LONG_POINTER = 'signed long long *'
    SIGNED_LONG_LONG_INT = 'signed long long int'
    SIGNED_LONG_LONG_INT_POINTER = 'signed long long int *'
    UNSIGNED_LONG_LONG = 'unsigned long long'
    UNSIGNED_LONG_LONG_POINTER = 'unsigned long long *'
    UNSIGNED_LONG_LONG_INT = 'unsigned long long int'
    UNSIGNED_LONG_LONG_INT_POINTER = 'unsigned long long int *'
    LONG_DOUBLE = 'long double'
    LONG_DOUBLE_POINTER = 'long double *'


    def get_ffi_string_def(self):
        """Returns type name for memory allocation in cffi"""
        if self.value.endswith(' *'):
            return self.value[:-2]
        else:
            return self.value
