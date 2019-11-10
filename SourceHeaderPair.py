import os
import pathlib
from Scrapers import *


class SourceHeaderPair:
	"""
	Class used to hold paths to source and header files

	Attributes
	----------
	source_filepath : Path
		Path object pointing to source file
	header_filepath : Path
		Path object pointing to header file
	includes : list
		List of include directives strings scraped from source
	declarations : str
		String of all declarations scraped from header
	declaration_data_list : list
		List of DeclarationData objects
	"""

	def __init__(self, src_path, h_path):
		self.source_filepath = src_path
		self.header_filepath = h_path
		self.includes = IncludesScraper().extract_inludes(self.source_filepath)
		declaration_scraper = DeclarationsScraper()
		self.declarations = declaration_scraper.parse_and_return_decl(self.header_filepath)
		self.declaration_data_list = declaration_scraper.declarations

	def __str__(self):
		return 'Source file path: ' + self.source_filepath.as_posix() + \
				' ; Header file path: ' + self.header_filepath.as_posix()


def create_pairs(sources: list):
	"""
	Creates SourceHeaderPair objects using list of paths

	Parameters
	----------
	sources : list
		List of Path objects

	Returns
	-------
	pairs : list
		List of SourceHeaderPair objects
	"""

	pairs = []
	while sources:
		filepath = sources.pop()
		if filepath.name.endswith('.c'):
			name_to_find = filepath.name.replace('.c', '.h')
			header = next((x for x in sources if x.name == name_to_find), None)
			if header:
				sources.remove(header)
				pairs.append(SourceHeaderPair(filepath, header))
		else:
			name_to_find = filepath.name.replace('.h', '.c')
			source = next((x for x in sources if x.name == name_to_find), None)
			if source:
				sources.remove(source)
				pairs.append(SourceHeaderPair(source, filepath))
	return pairs


def get_paths(dirpath):
	"""
	Gets paths to all source and header files in directory

	Paramters
	---------
	dirpath : str
		Library directory path string

	Returns
	-------
	paths : list
		List of Path objects
	"""

	paths = []
	for path, subdirs, files in os.walk(dirpath):
		for name in files:
			if name.endswith(('.c', '.h')):
				paths.append(pathlib.Path(path, name))
	return paths


def get_sourceheader_pairs(dirpath):
	"""
	Gets paths to all source and header files and returns SourceHeaderPair objects

	Parameters
	----------
	dirpath : str
		Library directory path string

	Returns
	-------
	list
		List of SourceHeaderPair objects
	"""

	paths = get_paths(dirpath)
	return create_pairs(paths)
