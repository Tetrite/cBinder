import Scrapers


class DoxygenParser:
    """
    Get metadata about a function from doxygen comment
    """

    def __init__(self, declaration_data_list: Scrapers.DeclarationData):
        self.declaration_data_list = declaration_data_list
