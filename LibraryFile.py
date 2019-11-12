import os
import pathlib
import platform


class LibraryFile:
	"""
	Class representing shared/dynamic library file

	Attributes
	----------
	filepath : Path
		Path object pointing to source file
	"""
	def __init__(self, path):
		self.filepath = path

	def __str__(self):
		return 'Source file path: ' + self.filepath.as_posix()


def get_shared_library_files(dirpath):
	"""
	Gets paths to all source files in directory (recursively)

	Parameters
	---------
	dirpath : str
		Library directory path string

	Returns
	-------
	libraries : list
		List of LibraryFile objects
	"""
	library_ext = '.so' if platform.system() == 'Linux' else '.dll'
	libraries = []
	for path, subdirs, files in os.walk(dirpath):
		for name in files:
			if name.endswith(library_ext):
				libraries.append(LibraryFile(pathlib.Path(path, name)))
	return libraries
