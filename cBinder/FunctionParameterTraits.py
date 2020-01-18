from enum import Enum


class ParameterType(Enum):
    """Enum describing doxygen parameter type [in] or [out]"""
    IN = 'in'
    OUT = 'out'
    IN_AND_OUT = 'in_and_out'
