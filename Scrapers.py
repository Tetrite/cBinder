import CppHeaderParser


# TODO: change scraping declarations to be more generic
class DeclarationsScraper:

	def __init__(self, cpppath):
		self.cpp_path = cpppath
		self.declarations = []

	def parse_file(self, filepath):
		self.declarations.clear()
		header = CppHeaderParser.CppHeader(filepath.name)
		for fun in header.functions:
			self.declarations.append(fun['debug'])

	def parse_and_return_decl(self, filepath):
		self.parse_file(filepath)
		return ' '.join(self.declarations)


class IncludesScraper:

	def extract_inludes(self, path):
		header = CppHeaderParser.CppHeader(path.name)
		includes = []
		for inc in header.includes:
			includes.append(f'#include {inc}')
		return includes
