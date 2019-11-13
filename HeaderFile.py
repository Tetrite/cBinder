import os
import pathlib
from Scrapers import get_function_declarations, get_includes, get_defines


class HeaderFile:
    """
    Class representing one C header file.

    Attributes
    ----------
    filepath : Path
        Path object pointing to header file
    includes : list
        List of include directives strings scraped from the header
    declarations : list
        List of FunctionDeclaration objects scraped from header
    defines : list
        List of define directives strings scraped from header
    """

    def __init__(self, h_path):
        self.filepath = h_path
        self.declarations = get_function_declarations(self.filepath)
        self.includes = get_includes(self.filepath)
        self.defines = get_defines(self.filepath)

    def __str__(self):
        return 'Header file path: ' + self.filepath.as_posix()


def get_header_files(dirpath):
    """
    Gets paths to all header files in directory (recursively)

    Parameters
    ---------
    dirpath : str
        Library directory path string

    Returns
    -------
    paths : list
        List of HeaderFile objects
    """
    headers = []
    for path, subdirs, files in os.walk(dirpath):
        for name in files:
            if name.endswith('.h'):
                headers.append(HeaderFile(pathlib.Path(path, name)))
    return headers
