from enum import Enum


class ParameterType(Enum):
    IN = 'in'
    OUT = 'out'


class CType(Enum):
    INT = 'int'
    INT_POINTER = 'int *'
    FLOAT = 'float'
    FLOAT_POINTER = 'float *'
    DOUBLE = 'double'
    DOUBLE_POINTER = 'double *'

    def get_ffi_string_def(self):
        if self.name == CType.INT or self.name == self.INT_POINTER.name:
            return 'int'
        elif self.name == CType.FLOAT or self.name == self.FLOAT_POINTER.name:
            return 'float'
        elif self.name == CType.DOUBLE or self.name == self.DOUBLE_POINTER.name:
            return 'double'
