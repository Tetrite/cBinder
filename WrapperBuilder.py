import platform
import re
from WrapperArgumentsProcessing import _check_if_every_in_array_is_not_empty
from WrapperArgumentsProcessing import _check_if_every_in_array_of_the_same_size_has_indeed_same_size
from WrapperArgumentsProcessing import _check_array_sizes_consistency_when_there_are_only_out_arrays
from WrapperArgumentsProcessing import _initialize_array_size_params_inside_wrapper

unique_identifier_suffix = '__internal'


# TODO: better tool for indendation
# TODO: handle escaping when creating sorce that may contains trings

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
            if not self.wrap_dynamic_lib:
                f.write("from .lib import _" + header_name + "\n")
                f.write(f'from cffi import FFI\nffi = _{header_name}.ffi\n\n')
            else:
                f.write("from cffi import FFI\nffi = FFI()\n\n")
                decl = '\n'.join(decl.declaration_string for decl in header.structs)
                f.write(f'ffi.cdef("""{decl}""")\n')
                f.write("ffi.cdef(\"" + "\\\n".join([x.declaration_string for x in header.functions]) + "\")\n\n")
                f.write("import os\n\n")

            self._build_wrapper_for_header(header_name, f, header)

    def build_wrapper_for_functions(self, header_name, functions):
        """Creates wrapper file for given list of FunctionDeclaration objects"""
        with open(header_name + '.py', 'w+') as f:
            f.write("from .lib import _" + header_name + "\rfrom cffi import FFI\rffi = FFI()\r\n\n")

            for decl in functions:
                self._build_wrapper_for_function(header_name, f, decl)

    def _build_wrapper_for_header(self, header_name, f, header):
        for struct in header.structs:
            self._build_wrapper_for_struct(header_name, f, struct)

        for decl in header.functions:
            self._build_wrapper_for_function(header_name, f, decl)

    def _build_wrapper_for_struct(self, header_name, f, struct):
        s = self._build_python_wrapper_for_struct(header_name, struct)
        f.write(s)

    def _build_wrapper_for_function(self, header_name, f, function):
        s = self._build_python_wrapper_for_function(header_name, function)
        f.write(s)

    def _build_array_copy(self, name, _to, _from):
        return [
            f'\tfor i,v in enumerate({name}):',
            f'\t\t{name}{_to}[i] = {name}{_from}[i]'
        ]

    def _build_array_copy_struct_to_cffi(self, name, _to, _from):
        return [
            f'\tfor i,v in enumerate({name}):',
            # __keepalive must be in the scope
            f'\t\t{name}{_from}[i].to_cffi_out({name}{_to}[i], __keepalive)'
        ]

    def _build_python_wrapper_for_struct(self, module_name, struct):
        decl = 'typedef struct {int a;double b;char c;}simple_struct;'
        lines = [
            f'class {struct.name}:',
            f'\tdef __init__(self):'
        ]

        for member in struct.members:
            lines.append(f'\t\tself.{member.name}=None')

        lines += [
            f'\tdef to_cffi(self, keepalive):',
            f'\t\ts=ffi.new("{struct.name}*")'
        ]
        for member in struct.members:
            if member.struct:
                # TODO: handle nested structs
                #      use keepalive
                pass

            lines.append(f'\t\ts.{member.name}=self.{member.name}')

        lines.append(f'\t\treturn s\n')

        lines += [
            f'\tdef to_cffi_out(self, out, keepalive):',
        ]
        for member in struct.members:
            if member.struct:
                # TODO: handle nested structs
                #      use keepalive
                pass

            lines.append(f'\t\tout.{member.name}=self.{member.name}')

        lines.append('')

        return '\n'.join(lines)

    def _build_python_wrapper_for_function(self, module_name, function):
        lines = [
            f'def {function.name}(' + ','.join(self._get_relevant_parameters(function.parameters)) + '):'
        ]

        self._add_documentation_to_a_function(function, lines)

        self._add_series_of_array_arguments_checks(function.parameters, lines)

        if self.wrap_dynamic_lib:
            # not so pretty way of solving libs not being found - construct absolute path using wrapper file location
            lib_open_str = f'os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib/{module_name}{self.dynamic_lib_ext}")'
            lines.append(f'\tlib = ffi.dlopen({lib_open_str})\n')

        for parameter in function.parameters:
            if parameter.struct:
                lines.append(f'\t__keepalive=[]')
                break

        for parameter in function.parameters:
            if parameter.struct:
                if parameter.is_array:
                    size = str(parameter.sizes[0]) if parameter.sizes[0] else 'len(' + parameter.name + ')'
                    lines.append(
                        f'\t{parameter.name}{unique_identifier_suffix}_ = ffi.new("{parameter.struct}[]", {size})')
                    lines.append(
                        f'\t{parameter.name}{unique_identifier_suffix} = ffi.cast("{parameter.struct}*", {parameter.name}{unique_identifier_suffix}_)')
                    lines += self._build_array_copy_struct_to_cffi(parameter.name, unique_identifier_suffix, '')
                else:
                    lines.append(
                        f'\t{parameter.name}{unique_identifier_suffix} = {parameter.name}.to_cffi(__keepalive)')
            else:
                if parameter.is_out and parameter.is_array:
                    size = str(parameter.sizes[0]) if parameter.sizes[0] else 'len(' + parameter.name + ')'
                    lines.append(
                        f'\t{parameter.name}{unique_identifier_suffix} = ffi.new("{parameter.c_type.get_ffi_string_def()}[]", {size})')
                    lines += self._build_array_copy(parameter.name, unique_identifier_suffix, '')
                else:
                    lines.append(f'\t{parameter.name}{unique_identifier_suffix} = {parameter.name}')

        lines.append(
            '\t'
            + ('ret = ' if not function.returns.is_void else '')
            + (f'_{module_name}.lib' if not self.wrap_dynamic_lib else 'lib') + f'.{function.name}('
            + ','.join([x.name + unique_identifier_suffix for x in function.parameters])
            + ')')

        for parameter in function.parameters:
            if parameter.struct:
                if parameter.is_array and parameter.is_out:
                    # TODO: from_cffi
                    pass
            else:
                if not parameter.is_out:
                    continue
                if parameter.is_array:
                    lines += self._build_array_copy(parameter.name, '', unique_identifier_suffix)
                else:
                    lines.append(f'\t{parameter.name} = {parameter.name}{unique_identifier_suffix}')

        if not function.returns.is_void:
            lines.append(f'\treturn ret')

        lines.append('')
        lines.append('')

        return '\n'.join(lines)

    def _add_documentation_to_a_function(self, function, lines):
        """ Add documentation to a function, based on doxygen comment """
        relevant_parameters = self._get_relevant_parameters(function.parameters)
        # Regex used to get a parameter name from a doxygen comment line:
        REGEX_ANY_PARAM_NAME = r'@param\[.*\][\s]*([a-zA-Z_][a-zA-Z0-9_]*)'

        if function.doxygen is not None:
            lines.append(f'\t\"\"\"')
            for line in function.doxygen.splitlines():
                # Discard unnecessary char sequence
                if line.startswith('/**') or line.startswith('*/'):
                    continue
                if line.startswith('*') and line[1:]:
                    # Check if a line has a parameter description
                    parameter_name_matches = re.findall(REGEX_ANY_PARAM_NAME, line)

                    # Do not include unnecessary parameters inside a python doc
                    if len(parameter_name_matches) > 0:
                        name = parameter_name_matches[0]
                        if name not in relevant_parameters:
                            continue

                    lines.append('\t' + line[1:].strip())
            lines.append(f'\t\"\"\"')

    def _get_relevant_parameters(self, parameters):
        """ Relevant parameters - such parameters that will be on a parameter list in a wrapping
            python function. Every parameter that is a size of an array, will be discarded.
        """
        relevant_parameters = []
        for param in parameters:
            if not param.is_array_size:
                relevant_parameters.append(param.name)
        return relevant_parameters

    def _add_series_of_array_arguments_checks(self, parameters, lines):
        _initialize_array_size_params_inside_wrapper(parameters, lines)
        # Check 1:
        _check_if_every_in_array_is_not_empty(parameters, lines)
        # Check 2:
        _check_if_every_in_array_of_the_same_size_has_indeed_same_size(parameters, lines)
        # Check 3:
        _check_array_sizes_consistency_when_there_are_only_out_arrays(parameters, lines)
