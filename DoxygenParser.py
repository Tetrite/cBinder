import re

from FunctionParameterTraits import *


class DoxygenParser:
    """
    Class used to retrieve information about parameters from doxygen comment

    Attributes
    ----------
    doxygen : str
        Single doxygen comment
    metadata : DoxygenFunctionMetadata
        Metadata about parameters parsed inside the class
    """

    REGEX_IN_PARAM_NAME = r'@param\[in\][\s]*([a-zA-Z_][a-zA-Z0-9_]*)'
    """ REGEX_IN_PARAM_NAME 
        Regex used to retrieve IN parameter name from doxygen comment line
        @param\[in\]  <-- indicates IN parameter
        [s]* <-- any number of whitespace characters
        ([a-zA-Z_][a-zA-Z0-9_]*) <-- parameter name (starts with a character, not a number)
        For example:        
        '* @param[in]   in_order   sample array (array of size n)'
        retrieves string 'in_order'
    """
    REGEX_OUT_PARAM_NAME = r'@param\[out\][\s]*([a-zA-Z_][a-zA-Z0-9_]*)'
    """ REGEX_OUT_PARAM_NAME 
        Regex used to retrieve OUT parameter name from doxygen comment line
        @param\[out\]  <-- indicates OUT parameter
        The rest - just like in REGEX_IN_PARAM_NAME
    """
    REGEX_ARRAY_SIZE = r'\(array of size ([A-Za-z0-9])\)'
    """ REGEX_ARRAY_SIZE 
        Regex used to retrieve size of an array
        For example:        
        '* @param[in]   in_order   sample array (array of size n)'
        retrieves string 'n'
    """

    def __init__(self, doxygen):
        self.doxygen = doxygen
        self.metadata = self.parse()

    def get_parameter(self, name):
        """ Returns a parameter from a list for a given parameter name """
        return self.metadata.get_parameter(name)

    def parse(self):
        """ Executes parsing of a doxygen comment (retrieves information about parameters)
            -parameter type (IN/OUT)
            -whether or not a parameter is an arry
                -size of an array
        """
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
    """
    Class used to represent metadata about a certain function
    It provides methods for accessing descriptions of function's parameters

    Attributes
    ----------
    parameters : list
        List of DoxygenFunctionParameters - every element
        in a list contains description of a single parameter, that was read while parsing
    """
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
    """
    Class used to represent a function parameter - it contains information that
    was gathered during the parsing of a doxygen comment

    Attributes
    ----------
    name: str
        Name of a parameter
    param_type: ParameterType
        Type of a parameter. It can be IN or OUT
    """
    def __init__(self, name, param_type: ParameterType):
        self.name = name
        self.param_type = param_type


class DoxygenFunctionArrayParameter(DoxygenFunctionParameter):
    """
    Class used to represent a function parameter that is an array

    Attributes
    ----------
    size:
        Size of an array (int or str)
    """

    def __init__(self, name, param_type: ParameterType, size):
        super().__init__(name, param_type)
        self.size = size
