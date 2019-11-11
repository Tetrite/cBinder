import re

from FunctionParameterTraits import *

class DoxygenParser:
    """
    Get metadata about a function from doxygen comment
    """
    REGEX_IN_PARAM = r'@param\[in\][\s]*[a-zA-Z_][a-zA-Z0-9_]{0,31}'
    REGEX_IN_PRE_PARAM_NAME = r'@param\[in\][\s]*'
    REGEX_OUT_PARAM = r'@param\[out\][\s]*[a-zA-Z_][a-zA-Z0-9_]{0,31}'
    REGEX_OUT_PRE_PARAM_NAME = r'@param\[out\][\s]*'

    REGEX_ARRAY_SIZE = r'\(array of size [A-Za-z0-9]\)'
    REGEX_PRE_ARRAY_SIZE = r'\(array of size '

    def __init__(self, doxygen):
        self.doxygen = doxygen
        self.metadata = self.parse()

    def parse(self):
        function_parameters = self.get_function_parameters(self.doxygen)
        function_metadata = FunctionMetadata(function_parameters)

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
        match = matches[0]
        string_preceding_size = re.findall(self.REGEX_PRE_ARRAY_SIZE, match)[0]
        size = match.replace(string_preceding_size, '')
        size = size.replace(')', '')
        if size.isdigit():
            return int(size)
        return size

    def get_input_parameter_name(self, line):
        return self.get_parameter_name(line, self.REGEX_IN_PARAM, self.REGEX_IN_PRE_PARAM_NAME)

    def get_output_parameter_name(self, line):
        return self.get_parameter_name(line, self.REGEX_OUT_PARAM, self.REGEX_OUT_PRE_PARAM_NAME)

    def get_parameter_name(self, line, REGEX_ALL, REGEX_PRE_NAME):
        matches = re.findall(REGEX_ALL, line)
        if len(matches) == 0:
            return None
        match = matches[0]
        string_preceding_name = re.findall(REGEX_PRE_NAME, match)[0]
        return match.replace(string_preceding_name, '')


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


# For debugging puproses:
def main():
    import Scrapers
    scr = Scrapers.DeclarationsScraper()
    scr.parse_file(
        "C:\\Users\\Mateusz\\Desktop\\AGH\\Semestr7\\Inżynierka\\cBinder\\tests\\functionwithdoxygen\\sources\\ex_doxygen.h")
    parser = DoxygenParser(scr.declarations[0])
    parser.metadata


if __name__ == '__main__':
    main()
