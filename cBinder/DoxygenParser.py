import re
from cBinder.FunctionParameterTraits import ParameterType


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
    REGEX_IN_AND_OUT_PARAM_NAME = r'@param\[in,out\][\s]*([a-zA-Z_][a-zA-Z0-9_]*)'
    """ REGEX_IN_AND_OUT_PARAM_NAME
        Regex used to retrieve IN&OUT parameter name from doxygen comment line
    """
    REGEX_IN_PARAM_NAME_SIMPLIFIED = r'@param[\s]*([a-zA-Z_][a-zA-Z0-9_]*)'
    """ REGEX_IN_PARAM_NAME_SIMPLIFIED
        Regex used to retrieve IN&OUT parameter name from doxygen comment line
    """
    REGEX_ARRAY_SIZE = r'\(array of size ([A-Za-z0-9_]*)\)'
    """ REGEX_ARRAY_SIZE
        Regex used to retrieve size of an array
        For example:
        '* @param[in]   in_order   sample array (array of size n)'
        retrieves string 'n'
    """

    def __init__(self, doxygen):
        self.doxygen = doxygen
        self.metadata = self._parse()

    def get_parameter(self, name):
        """ Returns a parameter from a list for a given parameter name """
        return self.metadata.get_parameter(name)

    def _parse(self):
        """ Executes parsing of a doxygen comment (retrieves information about parameters)
            -parameter type (IN/OUT)
            -whether or not a parameter is an array
                -size of an array
        """
        function_parameters = self._get_function_parameters(self.doxygen)
        return DoxygenFunctionMetadata(function_parameters)

    def _get_function_parameters(self, doxygen):
        lines = doxygen.splitlines()
        function_parameters = []
        for line in lines:
            parameter = self._create_parameter_object(line)
            if parameter is not None:
                function_parameters.append(parameter)
        return function_parameters

    def _create_parameter_object(self, line):
        parameter_type = self._get_parameter_type_from_line(line)
        parameter_name = ''
        if parameter_type is None:
            return None
        if parameter_type == ParameterType.IN:
            parameter_name = self._get_input_parameter_name(line)
        if parameter_type == ParameterType.OUT:
            parameter_name = self._get_output_parameter_name(line)
        if parameter_type == ParameterType.IN_AND_OUT:
            parameter_name = self._get_in_and_out_parameter_name(line)

        array_size = self._get_size_of_array(line)
        if array_size is not None:
            return DoxygenFunctionArrayParameter(parameter_name, parameter_type, array_size)
        return DoxygenFunctionParameter(parameter_name, parameter_type)

    @staticmethod
    def _get_parameter_type_from_line(line):
        if len(re.findall("@param\[in\]", line)) > 0:
            return ParameterType.IN
        if len(re.findall("@param\[out\]", line)) > 0:
            return ParameterType.OUT
        if len(re.findall("@param\[in,out\]", line)) > 0:
            return ParameterType.IN_AND_OUT
        if len(re.findall("@param", line)) > 0:
            return ParameterType.IN
        return None

    def _get_size_of_array(self, line):
        matches = re.findall(self.REGEX_ARRAY_SIZE, line)
        if len(matches) == 0:
            return None
        size = matches[0]
        if size.isdigit():
            return int(size)
        return size

    def _get_input_parameter_name(self, line):
        in_parameter_name = self._get_parameter_name(line, self.REGEX_IN_PARAM_NAME)
        if in_parameter_name is None:
            in_parameter_name = self._get_parameter_name(line, self.REGEX_IN_PARAM_NAME_SIMPLIFIED)
        return in_parameter_name

    def _get_output_parameter_name(self, line):
        return self._get_parameter_name(line, self.REGEX_OUT_PARAM_NAME)

    def _get_in_and_out_parameter_name(self, line):
        return self._get_parameter_name(line, self.REGEX_IN_AND_OUT_PARAM_NAME)

    @staticmethod
    def _get_parameter_name(line, REGEX_STRING):
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
        """
        Getter for parameter in parameters list

        Parameters
        ----------
        name : str
            Name of wanted parameter

        Returns
        -------
        param : DoxygenFunctionParameter
            DoxygenFunctionParameter object if parameter if specified name was found,
            None otherwise
        """
        for param in self.parameters:
            if param.name == name:
                return param

        return None

    def param_type(self, name):
        """
        Getter for parameter type in parameters list

        Parameters
        ----------
        name : str
            Name of wanted parameter's type

        Returns
        -------
        param_type : ParameterType
            ParameterType object if parameter if specified name was found,
            None otherwise
        """
        for param in self.parameters:
            if param.name == name:
                return param.param_type

        return None

    def is_any_array(self):
        """
        Checks if any parameter object is of type DoxygenFunctionArrayParameter

        Returns
        -------
        bool
            True if any parameter is of type DoxygenFunctionArrayParameter
        """
        for param in self.parameters:
            if isinstance(param, DoxygenFunctionArrayParameter):
                return True

        return False

    def is_array_size(self, name):
        """
        Checks if a parameter object is in fact an array size definition
        common use: n - parameter defining a size of an input array passed
        as another parameter

        Returns
        -------
        bool
            True if the parameter is an array size
        """
        array_sizes_parameters = []
        for parameter in self.parameters:
            if isinstance(parameter, DoxygenFunctionArrayParameter):
                array_sizes_parameters.append(parameter.size)
        for parameter in self.parameters:
            if parameter.name == name:
                return name in array_sizes_parameters
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
        self.is_array_size = False


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
