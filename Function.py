from DoxygenParser import *
from FunctionParameterTraits import *

def get_c_type_for_type(t):
    for ct in CType:
        if ct.value == t:
            return ct

    return None

class FunctionParameter:

    def __init__(self, param):
        self.name = param['name']
        self.type = param['type']
        self.c_type = get_c_type_for_type(self.type)
        self.is_array = param['array'] != 0 or param['pointer'] != 0
        self.sizes = (None,)
        self.is_const = param['constant'] != 0
        self.is_out = self.is_array and not self.is_const
        self.struct = None

    def __str__(self):
        return self.name + (':' + self.struct if self.struct else '')

class FunctionReturn:

    def __init__(self, t):
        self.type = t
        self.c_type = get_c_type_for_type(t)
        self.is_void = t == 'void'

class FunctionDeclaration:

    def __init__(self, function):
        self.doxygen = function['doxygen'] if 'doxygen' in function.keys() else None
        self.name = function['name']
        self.declaration_string = function['debug']
        self.parameters = [FunctionParameter(param) for param in function['parameters']]
        self.returns = FunctionReturn(function['rtnType'])

        if self.doxygen:
            self.imbue_with_doxygen(doxygen)

    def imbue_with_doxygen(self, doxygen):
        meta = DoxygenParser(doxygen)
        param = meta.get_parameter(self.name)
        if isinstance(param, DoxygenFunctionArrayParameter):
            self.is_array = True
            self.sizes = (param.size,)
        else:
            self.is_array = False

        self.is_out = (param.param_type == ParameterType.OUT)
