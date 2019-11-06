import re
from DoxygenParser import *

class Argument:

	def __init__(self, name, typ):
		self.name = name
		self.type = typ
		self.struct = None
		self.is_out_param = True # TODO: identify out params

	def __str__(self):
		return self.name + (':' + self.struct if self.struct else '')


def get_arguments(parts):
	args = []
	arg, parts = get_argument(parts)
	args.append(arg)
	while parts:
		arg, parts = get_argument(parts)
		args.append(arg)
	return args


def get_argument(parts):
	if not parts:
		return None, None
	arg = Argument(parts[1], parts[0])
	if len(parts) > 2 and parts[2] == '[':
		arg.struct = 'list'
		return arg, parts[4:]
	return arg, parts[2:]


class Declaration:

	def __init__(self, declaration):
		parts = re.split('[ ,()]', declaration)
		parts = [x for x in parts if x != '']
		self.is_void = parts[0] == 'void'
		self.name = parts[1]
		self.arguments = get_arguments(parts[2:])

	def __str__(self):
		s = 'def '+self.name+'('
		s = s + ','.join([str(x) for x in self.arguments])
		s = s + '):\r'
		return s

	def get_rewriter_into_array(self, name):
		s = '    for i,v in enumerate(' + name + '):\r'
		s = s + '        ' + name + '2[i] = ' + name + '[i]\r'
		return s

	def get_rewriter_into_list(self, name):
		s = '    for i,v in enumerate(' + name + '2):\r'
		s = s + '        ' + name + '.append(' + name + '2[i])\r'
		return s

	def build_body(self, module_name):
		s = ''
		for arg in self.arguments:
			if arg.struct:
				# TODO: get size of array to be allocated
				s = s + '    ' + arg.name + '2 = ffi.new("' + arg.type + '[]", 5)\r'
				s = s + self.get_rewriter_into_array(arg.name)
			else:
				s = s + '    ' + arg.name + '2 = ' + arg.name + '\r'
		s = s + '    ' + ('ret = ' if not self.is_void else '') + '_' + module_name + '.lib.' +\
			self.name + '(' + ','.join([x.name + '2' for x in self.arguments]) + ')\r'
		for arg in self.arguments:
			if not arg.is_out_param:
				continue
			if arg.struct:
				s = s + self.get_rewriter_into_list(arg.name)
			else:
				s = s + '    ' + arg.name + ' = ' + arg.name + '2\r'

		if not self.is_void:
			s = s + '    return ret'
		return s


def get_declaration(declaration):
	return Declaration(declaration)


def build_wrapper(name, declaration_data_list):
	with open(name+'.py', 'w+') as f:
		f.write("from . import _"+name+"\rfrom cffi import FFI\rffi = FFI()\r\n\n")
		function_metadata_list = DoxygenParser(declaration_data_list).parse_and_get_metadata()

		decls = []
		# for declaration_data in declaration_data_list:
		# 	decls.append(declaration_data.declaration.replace(';', ''))
		for decl in decls:
			df = get_declaration(decl)
			s = str(df)
			s = s + df.build_body(name)
			s = s + '\r\n\n'
			f.write(s)
