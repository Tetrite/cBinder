import CppHeaderParser


# TODO: change scraping declarations to be more generic
class DeclarationsScraper:

    def __init__(self, cpppath):
        self.cpp_path = cpppath
        self.declarations = []

    def parse_file(self, filepath):
        self.declarations.clear()
        header = CppHeaderParser.CppHeader(filepath)
        for fun in header.functions:
            doxygen_comment = ''
            try:
                doxygen_comment = fun['doxygen']
            except KeyError:
                pass  # There was no doxygen comment for that function in the header file
            self.declarations.append(DeclarationData(doxygen_comment, fun['debug']))

    def parse_and_return_decl(self, filepath):
        self.parse_file(filepath)
        declaration_strings = []
        for declaration_data in self.declarations:
            declaration_strings.append(declaration_data.declaration)
        return ' '.join(declaration_strings)


class IncludesScraper:

    def extract_inludes(self, path):
        header = CppHeaderParser.CppHeader(path)
        includes = []
        for inc in header.includes:
            includes.append(f'#include {inc}')
        return includes


class DeclarationData:

    def __init__(self, doxygen_comment, declaration_string):
        self.doxygen = doxygen_comment
        self.declaration = declaration_string
