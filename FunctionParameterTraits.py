from enum import Enum

class ParameterType(Enum):
    IN = 'in'
    OUT = 'out'


class CType(Enum):
    INT = 'int'
    FLOAT = 'float'
    DOUBLE = 'double'