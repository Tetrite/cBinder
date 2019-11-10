import CppHeaderParser


class DeclarationsScraper:
    """
    Class used to parse file and return declarations

    Attributes
    ----------
    declarations : list
        A list of scraped declarations in DeclarationData object
    """

    def __init__(self):
        self.declarations = []

    def parse_file(self, filepath):
        """
        Parses file at given path and fills declarations attribute with DeclarationData objects

        Parameters
        ----------
        filepath : str
            Filepath string
        """

        self.declarations.clear()
        header = CppHeaderParser.CppHeader(filepath)
        for fun in header.functions:
            doxygen_comment = fun['doxygen'] if 'doxygen' in fun.keys() else ''
            self.declarations.append(DeclarationData(doxygen_comment, fun['debug']))

    def parse_and_return_decl(self, filepath):
        """
        Parses file using parse_file method and returns joined declarations' strings

        Parameters
        ----------
        filepath : str
            Filepath string

        Returns
        -------
        str
            String of declarations' strings joined together
        """

        self.parse_file(filepath)
        declaration_strings = []
        for declaration_data in self.declarations:
            declaration_strings.append(declaration_data.declaration)
        return ' '.join(declaration_strings)


class IncludesScraper:
    """
    Class used to parse file and return include directives
    """

    def extract_inludes(self, path):
        """
        Parses file at given path and returns list of include directives

        Parameters
        ----------
        path : str
            Filepath string

        Returns
        -------
        includes : list
            List of include directive strings
        """

        header = CppHeaderParser.CppHeader(path)
        includes = []
        for inc in header.includes:
            includes.append(f'#include {inc}')
        return includes


class DeclarationData:
    """
    Class representing declaration

    Attributes
    ----------
    doxygen : str
        A doxygen string related to declaration
    declaration : str
        Declaration string
    """

    def __init__(self, doxygen_comment, declaration_string):
        self.doxygen = doxygen_comment
        self.declaration = declaration_string
