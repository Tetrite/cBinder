import os
import pathlib
from Scrapers import DeclarationsScraper, IncludesScraper


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
        self.filepath = src_path
        self.includes = IncludesScraper().extract_inludes(self.filepath.as_posix())

    def __str__(self):
        return 'Source file path: ' + self.filepath.as_posix()

    def get_declarations(self):
        declaration_scraper = DeclarationsScraper()
        declaration_scraper.parse_and_return_decl(self.filepath.as_posix())
        return declaration_scraper.declaration_data_list


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
        List of Path objects
    """
    sources = []
    for path, subdirs, files in os.walk(dirpath):
        for name in files:
            if name.endswith('.c'):
                sources.append(SourceFile(pathlib.Path(path, name)))
    return sources
