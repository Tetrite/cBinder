import CppHeaderParser
from Function import *


def get_function_declarations(filepath):
    """
    Parses file at given path and fills declarations attribute with FunctionDeclaration objects

    Parameters
    ----------
    filepath : str
        Filepath string
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
