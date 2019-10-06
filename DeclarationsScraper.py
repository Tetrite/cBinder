from pycparser import c_ast, parse_file


class DeclarationsScraper:

	def __init__(self, cpppath):
		self.cpp_path = cpppath
		self.declarations = []

	def parse_file(self, filepath):
		if self.cpp_path is None:
			ast = parse_file(filepath, use_cpp=True)
		else:
			ast = parse_file(filepath, use_cpp=True, cpp_path=self.cpp_path)

		self.declarations = [x for x in ast.ext if isinstance(x, c_ast.Decl)]

	def print(self):
		s = [self.get_node_str(x) for x in self.declarations]
		print('\r\n'.join(s))

	def get_node_str(self, node):
		ret_str = self.get_decl(node)
		args = [self.get_args_str(x) for x in node.type.args.params]
		ret_str = ret_str + '(' + ', '.join(args) + ');'
		return ret_str

	def get_decl(self, node):
		type_decl = node.type.type
		return type_decl.type.names[0] + ' ' + type_decl.declname

	def get_args_str(self, decl):
		return self.get_args_type(decl) + ' ' + decl.name

	def get_args_type(self, decl):
		return decl.type.type.names[0]

if __name__ == "__main__":
	d = DeclarationsScraper(None)
	d.parse_file('test.h')
	d.print()
