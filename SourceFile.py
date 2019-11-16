import os
import pathlib
from Scrapers import ScrapedData


class SourceFile:
    """
    Class representing one C source file.

    Attributes
    ----------
    filepath : Path
        Path object pointing to source file
    includes : list
        List of include directives strings scraped from source
    """

    def __init__(self, src_path):
        d = ScrapedData(src_path)
        self.filepath = src_path
        self.includes = d.includes
        self.functions = d.functions

    def __str__(self):
        return 'Source file path: ' + self.filepath.as_posix()

    def get_functions(self):
        return self.functions


def get_source_files(dirpath):
    """
    Gets paths to all source files in directory (recursively)

    Parameters
    ---------
    dirpath : str
        Library directory path string

    Returns
    -------
    paths : list
        List of SourceFile objects
    """
    sources = []
    for path, subdirs, files in os.walk(dirpath):
        for name in files:
            if name.endswith('.c'):
                sources.append(SourceFile(pathlib.Path(path, name)))
    return sources
