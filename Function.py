from DoxygenParser import DoxygenParser, DoxygenFunctionArrayParameter
from FunctionParameterTraits import ParameterType
from CType import CType, get_c_type_for_type


class FunctionParameter:
    """
    Class representing single function parameter

    Attributes
    ----------
    name : str
        Parameter name
    type : str
        Parameter type
    c_type : CType
        CType enum for type attribute
    is_array : bool
        True if parameter is array
    sizes : tuple
        Sizes of array, default (None,)
    is_const : bool
        True if parameter is constant
    is_out : bool
        True if parameter is of ParameterType OUT,
        default True if parameter is array and not constant
    struct : str
        Python object type used to hold this parameter in wrapper
    """

    def __init__(self, param, enums):
        self.name = param['name']
        self.type = param['type']
        self.c_type = get_c_type_for_type(self.type)
        self.is_array = param['array'] != 0 or param['pointer'] != 0
        self.sizes = (None,)
        self.is_const = param['constant'] != 0
        self.is_out = self.is_array and not self.is_const
        self.is_in = not self.is_out
        self.struct = param['class']['name'] if param['class'] != 0 else None
        self.enum = self.type if self.type in enums else None
        self.is_array_size = False
        self.is_pointer_to_array = param['array'] != 0 and param['pointer'] != 0

    def __str__(self):
        return self.name + (':' + self.struct if self.struct else '')


class FunctionReturn:
    """
    Class for holding return info of function

    Attributes
    ----------
    type : str
        Return type string
    c_type : CType
        CType enum for type attribute
    is_void : bool
        True if return type is void
    """

    def __init__(self, t, enums):
        self.type = t
        self.c_type = get_c_type_for_type(t)
        self.is_void = t == 'void'
        self.struct = t if not self.is_void and self.c_type is None else None
        self.enum = t if t in enums else None


class FunctionDeclaration:
    """
    Class representing function declaration

    Attributes
    ----------
    doxygen : str
        Doxygen comment string if exists, None otherwise
    name : str
        Function name string
    declaration_string : str
        String representation of whole declaration
    parameters : list
        List of FunctionParameter objects
    returns : FunctionReturn
        FunctionReturn object
    """

    def __init__(self, function, enums):
        self.doxygen = function['doxygen'] if 'doxygen' in function.keys() else None
        self.name = function['name']
        self.declaration_string = function['debug']
        self.parameters = [FunctionParameter(param, enums) for param in function['parameters']]
        self.returns = FunctionReturn(function['rtnType'], enums)

        self.set_parameters_names_if_empty()

        if self.doxygen and self._is_valid_doxygen(self.doxygen):
            self.imbue_with_doxygen(self.doxygen)

    def _is_valid_doxygen(self, doxygen):
        return doxygen.find("/**") >= 0 and doxygen.find("*/") >= 0 and doxygen.find("@param") >0

    def set_parameters_names_if_empty(self):
        i = 0
        for param in self.parameters:
            if param.name == '':
                param.name = '__gen_name__' + str(i) + '__'
                i += 1

    def imbue_with_doxygen(self, doxygen):
        """Parses doxygen comment and fills attributes with relevant info"""
        parser = DoxygenParser(doxygen)
        for parameter in self.parameters:
            doxygen_function_param = parser.get_parameter(parameter.name)
            if isinstance(doxygen_function_param, DoxygenFunctionArrayParameter):
                parameter.is_array = True
                parameter.sizes = (doxygen_function_param.size,)
            else:
                # Case when a parameter is OUT type, but is not an array
                # according to doxygen comment. It is a pointer OUT type.
                # It should be processed as array of size 1.
                if not parameter.is_out:
                    parameter.is_array = False
                else:
                    parameter.sizes = (1,)

            parameter.is_out = doxygen_function_param.param_type == ParameterType.OUT or \
                               doxygen_function_param.param_type == ParameterType.IN_AND_OUT

            parameter.is_in = doxygen_function_param.param_type == ParameterType.IN or \
                              doxygen_function_param.param_type == ParameterType.IN_AND_OUT

            parameter.is_array_size = parser.metadata.is_array_size(parameter.name)
