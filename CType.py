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
    INT = 'int'
    INT_POINTER = 'int *'
    FLOAT = 'float'
    FLOAT_POINTER = 'float *'
    DOUBLE = 'double'
    DOUBLE_POINTER = 'double *'

    def get_ffi_string_def(self):
        """Returns type name for memory allocation in cffi"""
        if self.name == self.INT.name or self.name == self.INT_POINTER.name:
            return 'int'
        elif self.name == self.FLOAT.name or self.name == self.FLOAT_POINTER.name:
            return 'float'
        elif self.name == self.DOUBLE.name or self.name == self.DOUBLE_POINTER.name:
            return 'double'
