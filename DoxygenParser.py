import re

from FunctionParameterTraits import *


class DoxygenParser:
    """
    Get metadata about a function from doxygen comment
    """
    REGEX_IN_PARAM_NAME = r'@param\[in\][\s]*([a-zA-Z_][a-zA-Z0-9_]*)'
    REGEX_OUT_PARAM_NAME = r'@param\[out\][\s]*([a-zA-Z_][a-zA-Z0-9_]*)'
    REGEX_ARRAY_SIZE = r'\(array of size ([A-Za-z0-9])\)'

    def __init__(self, doxygen):
        self.doxygen = doxygen
        self.metadata = self.parse()

    def get_parameter(self, name):
        return self.metadata.get_parameter(name)

    def parse(self):
        function_parameters = self.get_function_parameters(self.doxygen)
        return DoxygenFunctionMetadata(function_parameters)

    def get_function_parameters(self, doxygen):
        lines = doxygen.splitlines()
        function_parameters = []
        for line in lines:
            parameter = self.create_parameter_object(line)
            if parameter is not None:
                function_parameters.append(parameter)
        return function_parameters

    def create_parameter_object(self, line):
        parameter_type = self.get_parameter_type_from_line(line)
        parameter_name = ''
        if parameter_type is None:
            return None
        if parameter_type == ParameterType.IN:
            parameter_name = self.get_input_parameter_name(line)
        if parameter_type == ParameterType.OUT:
            parameter_name = self.get_output_parameter_name(line)

        array_size = self.get_size_of_array(line)
        if array_size is not None:
            return DoxygenFunctionArrayParameter(parameter_name, parameter_type, array_size)
        return DoxygenFunctionParameter(parameter_name, parameter_type)

    def get_parameter_type_from_line(self, line):
        if len(re.findall("@param\[in\]", line)) > 0:
            return ParameterType.IN
        if len(re.findall("@param\[out\]", line)) > 0:
            return ParameterType.OUT
        return None

    def get_size_of_array(self, line):
        matches = re.findall(self.REGEX_ARRAY_SIZE, line)
        if len(matches) == 0:
            return None
        size = matches[0]
        if size.isdigit():
            return int(size)
        return size

    def get_input_parameter_name(self, line):
        return self.get_parameter_name(line, self.REGEX_IN_PARAM_NAME)

    def get_output_parameter_name(self, line):
        return self.get_parameter_name(line, self.REGEX_OUT_PARAM_NAME)

    def get_parameter_name(self, line, REGEX_STRING):
        matches = re.findall(REGEX_STRING, line)
        if len(matches) == 0:
            return None
        return matches[0]


class DoxygenFunctionMetadata:

    def __init__(self, parameters):
        self.parameters = parameters

    def get_parameter(self, name):
        for param in self.parameters:
            if param.name == name:
                return param

        return None

    def param_type(self, name):
        for param in self.parameters:
            if param.name == name:
                return param.param_type

        return None

    def is_array(self, name):
        for param in self.parameters:
            if isinstance(param, DoxygenFunctionArrayParameter):
                return True

        return False


class DoxygenFunctionParameter:

    def __init__(self, name, param_type: ParameterType):
        self.name = name
        self.param_type = param_type


class DoxygenFunctionArrayParameter(DoxygenFunctionParameter):

    def __init__(self, name, param_type: ParameterType, size):
        super().__init__(name, param_type)
        self.size = size
