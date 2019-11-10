import os
import pathlib
from Scrapers import *


"""
Class representing one C header file.

Attributes
----------
filepath : Path
    Path object pointing to header file
includes : list
    List of include directives strings scraped from the header
declarations : str
    String of all declarations scraped from header
declaration_data_list : list
    List of DeclarationData objects
"""
class HeaderFile:

    def __init__(self, h_path):
        self.filepath = h_path
        self.declarations = DeclarationsScraper().parse_and_return_decl(self.filepath)
        declaration_scraper = DeclarationsScraper()
        declaration_scraper.parse_file(self.filepath)
        self.declaration_data_list = declaration_scraper.declarations
        self.includes = IncludesScraper().extract_inludes(self.filepath)

    def __str__(self):
        return 'Header file path: ' + self.filepath.as_posix()


"""
Gets paths to all header files in directory (recursively)

Paramters
---------
dirpath : str
    Library directory path string

Returns
-------
paths : list
    List of Path objects
"""
def get_header_files(dirpath):
    headers = []
    for path, subdirs, files in os.walk(dirpath):
        for name in files:
            if name.endswith(('.h')):
                headers.append(HeaderFile(pathlib.Path(path, name)))
    return headers
