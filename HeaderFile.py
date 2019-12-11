import os
import pathlib
from Scrapers import ScrapedData


class HeaderFile:
    """
    Class representing one C header file.

    Attributes
    ----------
    filepath : Path
        Path object pointing to header file
    includes : list
        List of include directives strings scraped from the header
    functions : list
        List of FunctionDeclaration objects scraped from header
    structs : list
        List of StructDeclaration objects scraped from header
    defines : list
        List of define directives strings scraped from header
    """

    def __init__(self, h_path, export_symbols):
        d = ScrapedData(h_path, export_symbols)
        self.filepath = h_path
        self.enums = d.enums
        self.functions = d.functions
        self.structs = d.structs
        self.includes = d.includes
        self.defines = d.defines

    def __str__(self):
        return 'Header file path: ' + self.filepath.as_posix()

    def read(self):
        with open(self.filepath, 'r') as h:
            return h.read()


def get_header_files(dirpath, export_symbols=None):
    """
    Gets paths to all header files in directory (recursively)

    Parameters
    ---------
    dirpath : str
        Library directory path string
    export_symbols: dict
        Dict containing lists of export symbols

    Returns
    -------
    paths : list
        List of HeaderFile objects
    """
    headers = []
    for path, subdirs, files in os.walk(dirpath):
        for name in files:
            if name.endswith('.h'):
                headers.append(HeaderFile(pathlib.Path(path, name), export_symbols))
    return headers
