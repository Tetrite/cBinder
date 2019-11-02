import re
from enum import Enum


class DoxygenParser:
    """
    Get metadata about a function from doxygen comment
    """

    def __init__(self, declaration_data_list):
        self.declaration_data_list = declaration_data_list
        self.function_metadata_list = []

    def parse_doxygen(self):
        for declaration_data in self.declaration_data_list:
            # Data from header:
            doxygen = declaration_data.doxygen
            declaration = declaration_data.declaration

            # Data to be taken from declaration data:
            function_name = self.get_function_name(declaration)
            function_parameters = []

    def get_function_name(self, declaration):
        declaration_parts = re.split('[ ,()]', declaration)
        return declaration_parts[1]


class FunctionMetadata:

    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters


class ParameterType(Enum):
    IN = 'in'
    OUT = 'out'


class Parameter:

    def __init__(self, name, param_type: ParameterType):
        self.name = name
        self.param_type = param_type


class Array(Parameter):

    def __init__(self, name, param_type: ParameterType, size):
        super().__init__(name, param_type)
        self.size = size


# For debugging puproses:
def main():
    import Scrapers
    scr = Scrapers.DeclarationsScraper('')
    scr.parse_file(
        "C:\\Users\\Mateusz\\Desktop\\AGH\\Semestr7\\Inżynierka\\cBinder\\tests\\functionwithdoxygen\\sources\\ex_doxygen.h")
    parser = DoxygenParser(scr.declarations)
    parser.parse_doxygen()


if __name__ == '__main__':
    main()
