import CppHeaderParser
from Function import FunctionDeclaration


def get_function_declarations(filepath):
    """
    Parses file at given path and fills declarations attribute with FunctionDeclaration objects

    Parameters
    ----------
    filepath : str
        Filepath string

    Returns
    -------
    declarations : list
        List of FunctionDeclaration objects
    """
    declarations = []
    header = CppHeaderParser.CppHeader(filepath)
    for fun in header.functions:
        declarations.append(FunctionDeclaration(fun))

    return declarations


def get_includes(filepath):
    """
    Parses file at given path and returns list of include directives

    Parameters
    ----------
    filepath : str
        Filepath string

    Returns
    -------
    includes : list
        List of include directive strings
    """
    header = CppHeaderParser.CppHeader(filepath)
    includes = []
    for inc in header.includes:
        includes.append(f'#include {inc}')
    return includes


def get_defines(filepath):
    """
    Parses file at given path and returns list of define statements

    Parameters
    ----------
    filepath : str
        Filepath string

    Returns
    -------
    defines : list
        List of define directive strings
    """
    header = CppHeaderParser.CppHeader(filepath)
    defines = []
    for inc in header.defines:
        defines.append(f'#define {inc}')
    return defines
