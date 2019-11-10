import os
import pathlib
from Scrapers import *


"""
Class representing one C source file.

Attributes
----------
filepath : Path
    Path object pointing to source file
includes : list
    List of include directives strings scraped from source
"""
class SourceFile:

    def __init__(self, src_path):
        self.filepath = src_path
        self.includes = IncludesScraper().extract_inludes(self.filepath)

    def __str__(self):
        return 'Source file path: ' + self.filepath.as_posix()


"""
Gets paths to all source files in directory (recursively)

Paramters
---------
dirpath : str
    Library directory path string

Returns
-------
paths : list
    List of Path objects
"""
def get_source_files(dirpath):
    sources = []
    for path, subdirs, files in os.walk(dirpath):
        for name in files:
            if name.endswith(('.c')):
                sources.append(SourceFile(pathlib.Path(path, name)))
    return sources
