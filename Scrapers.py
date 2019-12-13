import CppHeaderParser
from Function import FunctionDeclaration
from Struct import StructDeclaration
from Enum import EnumDeclaration


class ScrapedData:
    def __init__(self, filepath, export_symbols):
        header = CppHeaderParser.CppHeader(filepath, encoding='UTF-8')
        self.enums = _get_enum_declarations(header, export_symbols)
        enum_names = set(e.name for e in self.enums)
        self.structs = _get_struct_declarations(header, enum_names, export_symbols)
        self.functions = _get_function_declarations(header, enum_names, export_symbols)
        self.includes = _get_includes(header)
        self.defines = _get_defines(header)


def _get_struct_declarations(header, enums, export_symbols):
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
        if 'name' not in struct:
            continue
        if export_symbols is None or struct['name'] in export_symbols:
            declarations.append(StructDeclaration(struct, enums))
    return declarations


def _get_function_declarations(header, enums, export_symbols):
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
        if 'name' not in fun:
            continue
        if export_symbols is None or fun['name'] in export_symbols:
            declarations.append(FunctionDeclaration(fun, enums))
    return declarations


def _get_enum_declarations(header, export_symbols):
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
        if 'name' not in e:
            declarations.append(EnumDeclaration(e))
        elif export_symbols is None or e['name'] in export_symbols:
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
