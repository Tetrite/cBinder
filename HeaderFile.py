import os
import pathlib
from Scrapers import DeclarationsScraper, IncludesScraper


class HeaderFile:
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

    def __init__(self, h_path):
        self.filepath = h_path
        declaration_scraper = DeclarationsScraper()
        self.declarations = declaration_scraper.parse_and_return_decl(self.filepath.as_posix())
        self.declaration_data_list = declaration_scraper.declarations
        self.includes = IncludesScraper().extract_inludes(self.filepath.as_posix())

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
        List of Path objects
    """
    headers = []
    for path, subdirs, files in os.walk(dirpath):
        for name in files:
            if name.endswith('.h'):
                headers.append(HeaderFile(pathlib.Path(path, name)))
    return headers
