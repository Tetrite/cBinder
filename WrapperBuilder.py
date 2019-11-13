import platform

unique_identifier_suffix = '__internal'

# TODO: better tool for indendation


class WrapperBuilder:
    """
    Class holding all related info and methods for wrapper building

    Attributes
    ----------
    wrap_dynamic_lib : bool
        True if wrapper should be created for dynamic library
    dynamic_lib_ext : str
        .so if running os is Linux, .dll if Windows
    """

    def __init__(self, wrap_dynamic_lib=False):
        self.wrap_dynamic_lib = wrap_dynamic_lib
        self.dynamic_lib_ext = '.so' if platform.system() == 'Linux' else '.dll'

    def build_wrapper_for_header(self, header_name, header):
        """Creates wrapper file for given HeaderFile"""
        with open(header_name + '.py', 'w+') as f:
            f.write("from cffi import FFI\nffi = FFI()\n\n")
            if not self.wrap_dynamic_lib:
                f.write("from lib import _" + header_name + "\n")
            else:
                f.write("ffi.cdef(\"" + "\\\n".join([x.declaration_string for x in header.declarations]) + "\")\n\n")
                f.write("import os\n\n")

            self._build_wrapper_for_header(header_name, f, header)

    def build_wrapper_for_declarations(self, header_name, declarations):
        """Creates wrapper file for given list of FunctionDeclaration objects"""
        with open(header_name + '.py', 'w+') as f:
            f.write("from lib import _" + header_name + "\rfrom cffi import FFI\rffi = FFI()\r\n\n")

            for decl in declarations:
                self._build_wrapper_for_declaration(header_name, f, decl)

    def _build_wrapper_for_header(self, header_name, f, header):
        for decl in header.declarations:
            self._build_wrapper_for_declaration(header_name, f, decl)

    def _build_wrapper_for_declaration(self, header_name, f, declaration):
        s = self._build_python_function_wrapper_for_declaration(header_name, declaration)
        f.write(s)

    def _build_array_copy(self, name, _from, to):
        return [
            f'\tfor i,v in enumerate({name}):',
            f'\t\t{name}{_from}[i] = {name}{to}[i]'
        ]

    def _build_python_function_wrapper_for_declaration(self, module_name, declaration):
        lines = [
            f'def {declaration.name}(' + ','.join([x.name for x in declaration.parameters]) + '):'
        ]

        if self.wrap_dynamic_lib:
            # not so pretty way of solving libs not being found - construct absolute path using wrapper file location
            lib_open_str = f'os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib/{module_name}{self.dynamic_lib_ext}")'
            lines.append(f'\tlib = ffi.dlopen({lib_open_str})\n')

        for parameter in declaration.parameters:
            if parameter.is_out and parameter.is_array:
                size = str(parameter.sizes[0]) if parameter.sizes[0] else 'len(' + parameter.name + ')'
                lines.append(f'\t{parameter.name}{unique_identifier_suffix} = ffi.new("{parameter.c_type.get_ffi_string_def()}[]", {size})')
                lines += self._build_array_copy(parameter.name, unique_identifier_suffix, '')
            else:
                lines.append(f'\t{parameter.name}{unique_identifier_suffix} = {parameter.name}')

        lines.append(
            '\t'
            + ('ret = ' if not declaration.returns.is_void else '')
            + (f'_{module_name}.lib' if not self.wrap_dynamic_lib else 'lib') + f'.{declaration.name}('
            + ','.join([x.name + unique_identifier_suffix for x in declaration.parameters])
            + ')')

        for parameter in declaration.parameters:
            if not parameter.is_out:
                continue
            if parameter.is_array:
                lines += self._build_array_copy(parameter.name, '', unique_identifier_suffix)
            else:
                lines.append(f'\t{parameter.name} = {parameter.name}{unique_identifier_suffix}')

        if not declaration.returns.is_void:
            lines.append(f'\treturn ret')

        lines.append('')
        lines.append('')

        return '\n'.join(lines)
