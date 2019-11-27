import CppHeaderParser
from Function import FunctionDeclaration
from Struct import StructDeclaration
from Enum import EnumDeclaration

class ScrapedData:
    def __init__(self, filepath):
        header = CppHeaderParser.CppHeader(filepath)
        self.enums = _get_enum_declarations(header)
        enum_names = set(e.name for e in self.enums)
        self.structs = _get_struct_declarations(header, enum_names)
        self.functions = _get_function_declarations(header, enum_names)
        self.includes = _get_includes(header)
        self.defines = _get_defines(header)


def _get_struct_declarations(header, enums):
    """
    Return declarations attribute with StructDeclaration objects

    Parameters
    ----------
    header : str
        CppHeader

    Returns
    -------
    declarations : list
        List of StructDeclaration objects
    """
    declarations = []
    for _, struct in header.classes.items():
        declarations.append(StructDeclaration(struct, enums))

    return declarations

def _get_function_declarations(header, enums):
    """
    Return declarations attribute with FunctionDeclaration objects

    Parameters
    ----------
    header : str
        CppHeader

    Returns
    -------
    declarations : list
        List of FunctionDeclaration objects
    """
    declarations = []
    for fun in header.functions:
        declarations.append(FunctionDeclaration(fun, enums))

    return declarations


def _get_enum_declarations(header):
    """
    Return declarations attribute with EnumDeclaration objects

    Parameters
    ----------
    header : str
        CppHeader

    Returns
    -------
    declarations : list
        List of EnumDeclaration objects
    """
    declarations = []
    for e in header.enums:
        declarations.append(EnumDeclaration(e))

    return declarations


def _get_includes(header):
    """
    Returns list of include directives

    Parameters
    ----------
    header : str
        CppHeader

    Returns
    -------
    includes : list
        List of include directive strings
    """
    includes = []
    for inc in header.includes:
        includes.append(f'#include {inc}')
    return includes


def _get_defines(header):
    """
    Returns list of define statements

    Parameters
    ----------
    header : str
        CppHeader

    Returns
    -------
    defines : list
        List of define directive strings
    """
    defines = []
    for inc in header.defines:
        defines.append(f'#define {inc}')
    return defines
