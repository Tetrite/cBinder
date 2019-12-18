import platform
import re
from WrapperArgumentsProcessing import _check_if_every_in_array_is_not_empty
from WrapperArgumentsProcessing import _check_if_every_in_array_of_the_same_size_has_indeed_same_size
from WrapperArgumentsProcessing import _check_array_sizes_consistency_when_there_are_only_out_arrays
from WrapperArgumentsProcessing import _initialize_array_size_params_inside_wrapper
from WrapperArgumentsProcessing import _initialize_out_arrays_if_necessary_and_check_sizes
from WrapperArgumentsProcessing import _initialize_non_array_out_parameters_if_necessary
from PythonWriter import *

unique_identifier_suffix = '__internal'


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
    dynamic_lib_name : str
        name of dll/so filename
    """

    def __init__(self, args, wrap_dynamic_lib=False, dynamic_lib_name=None):
        self.args = args
        self.wrap_dynamic_lib = wrap_dynamic_lib
        self.dynamic_lib_name = dynamic_lib_name
        self.dynamic_lib_ext = '.so' if platform.system() == 'Linux' else '.dll'

    def build_wrapper_for_header(self, header_name, header):
        self.build_wrapper_for_structs_and_functions(header_name, header.enums, header.structs, header.functions)

    def build_wrapper_for_structs_and_functions(self, header_name, enums, structs, functions):
        """Creates wrapper file for given list of FunctionDeclaration objects"""
        with open(header_name + '.py', 'w+') as f:
            writer = PythonWriter()
            if not self.wrap_dynamic_lib:
                writer.write_line('import warnings')
                writer.write_line('from .lib import _' + header_name)
                writer.write_line('from cffi import FFI')
                writer.write_line(f'ffi = _{header_name}.ffi')
            else:
                writer.write_line('import warnings')
                writer.write_line('from cffi import FFI')
                writer.write_line('ffi = FFI()')

                enum_decls = writer.escaped('\n'.join(decl.declaration_string for decl in enums))
                struct_decls = writer.escaped('\n'.join(decl.declaration_string for decl in structs))
                func_decls = writer.escaped('\n'.join(decl.declaration_string for decl in functions))
                writer.write_line(f'ffi.cdef("""{struct_decls}""")')
                writer.write_line(f'ffi.cdef("""{func_decls}""")')
                writer.write_line('import os')
                writer.write_line('')

            writer.write_line('')

            self._build_wrapper_for_structs_and_functions(writer, header_name, enums, structs, functions)

            writer.write_line('')

            f.write(writer.get_string())

    def _build_wrapper_for_structs_and_functions(self, writer, header_name, enums, structs, functions):
        verbosity = self.args.verbose

        if enums:
            writer.write_line('from enum import Enum\n')

        for enum in enums:
            if verbosity:
                print(f'Building wrapper in module {header_name} for enum: {enum.declaration_string}')
            self._build_wrapper_for_enum(writer, header_name, enum)

        for struct in structs:
            if verbosity:
                print(f'Building wrapper in module {header_name} for struct: {struct.declaration_string}')
            self._build_wrapper_for_struct(writer, header_name, struct)

        for decl in functions:
            if verbosity:
                print(f'Building wrapper in module {header_name} for function: {decl.declaration_string}')
            # Procedure to eliminate case of parameter names that are keywords in Python
            for parameter in decl.parameters:
                parameter.name = 'p_' + parameter.name
            self._build_wrapper_for_function(writer, header_name, decl)

    def _build_wrapper_for_enum(self, writer, header_name, enum):
        self._build_python_wrapper_for_enum(writer, header_name, enum)

    def _build_wrapper_for_struct(self, writer, header_name, struct):
        self._build_python_wrapper_for_struct(writer, header_name, struct)

    def _build_wrapper_for_function(self, writer, header_name, function):
        self._build_python_wrapper_for_function(writer, header_name, function)

    def _build_array_copy(self, writer, name, _to, _from):
        with writer.write_for('i,v', f'enumerate({name}{_from})'):
            writer.write_line(f'{name}{_to}[i] = v')

    def _build_array_copy_enum_to_cffi(self, writer, name, _to, _from):
        with writer.write_for('i,v', f'enumerate({name}{_from})'):
            writer.write_line(f'{name}{_to}[i] = v.value')

    def _build_array_copy_enum_from_cffi(self, writer, enum, name, _to, _from):
        with writer.write_for('i,v', f'enumerate({name}{_from})'):
            writer.write_line(f'{name}{_to}[i] = {enum}(v)')

    def _build_array_copy_struct_to_cffi(self, writer, name, _to, _from):
        with writer.write_for('i', f'range(len({name}{_from}))'):
            # __keepalive must be in the scope
            writer.write_line(f'{name}{_from}[i].to_cffi_out({name}{_to}[i], __keepalive)')

    def _build_array_copy_struct_from_cffi(self, writer, name, _to, _from):
        with writer.write_for('i', f'range(len({name}{_from}))'):
            # __keepalive must be in the scope
            writer.write_line(f'{name}{_to}[i].from_cffi({name}{_from}[i])')

    def _build_python_wrapper_for_enum(self, writer, module_name, enum):
        if enum.name:
            td = 'enum ' if not enum.typedef else ''
            writer.write_line(f'{enum.name} = Enum(\'{enum.name}\', ffi.typeof(\'{td}{enum.name}\').relements)')
        else:
            for e in enum.values:
                name = e['name']
                value = e['value']
                writer.write_line(f'{name}={value}')

    def _build_python_wrapper_for_struct(self, writer, module_name, struct):
        with writer.write_class(struct.name):
            with writer.write_def('__init__', ['self']):
                for member in struct.members:
                    writer.write_line(f'self.{member.name}=None')

            with writer.write_def('to_cffi', ['self', 'keepalive']):
                writer.write_line(f's=ffi.new("{struct.name}*")')

                for member in struct.members:
                    if member.struct:
                        # TODO: handle nested structs, use keepalive
                        pass

                    writer.write_line(f's.{member.name}=self.{member.name}')

                writer.write_line(f'return s')

            with writer.write_def('from_cffi', ['self', 'ffi_struct']):
                for member in struct.members:
                    if member.struct:
                        # TODO: handle nested structs, use keepalive
                        pass

                    writer.write_line(f'self.{member.name}=ffi_struct.{member.name}')

            with writer.write_def('to_cffi_out', ['self', 'out', 'keepalive']):
                for member in struct.members:
                    if member.struct:
                        # TODO: handle nested structs, use keepalive
                        pass

                    writer.write_line(f'out.{member.name}=self.{member.name}')

    def _build_python_wrapper_for_function(self, writer, module_name, function):
        if self.wrap_dynamic_lib:
            module_name = self.dynamic_lib_name
        with writer.write_def(function.name, self._get_relevant_parameters(function.parameters)):
            if function.doxygen is not None:
                self._add_documentation_to_a_function(writer, function)
                self._add_series_of_array_arguments_checks(writer, function.parameters)

            if self.wrap_dynamic_lib:
                # not so pretty way of solving libs not being found - construct absolute path using wrapper file location
                lib_open_str = f'os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib/{module_name}{self.dynamic_lib_ext}")'
                writer.write_line(f'lib = ffi.dlopen({lib_open_str})')

            for parameter in function.parameters:
                if parameter.struct:
                    writer.write_line(f'__keepalive = []')
                    break

            for parameter in function.parameters:
                if parameter.struct:
                    if parameter.is_array:
                        with writer.write_if(f'hasattr({parameter.name}, \'__len__\')'):
                            size = str(parameter.sizes[0]) if parameter.sizes[0] else 'len(' + parameter.name + ')'
                            # If size is defined as a function parameter, in a wrapper it has to be named with prefix
                            # to avoid case when a function parameter name is a keyword in Python
                            if parameter.sizes[0] and isinstance(parameter.sizes[0], str) and not parameter.sizes[0].isdigit():
                                size = 'p_' + size
                            writer.write_line(
                                f'{parameter.name}{unique_identifier_suffix}_ = ffi.new("{parameter.struct}[]", {size})')
                            writer.write_line(
                                f'{parameter.name}{unique_identifier_suffix} = ffi.cast("{parameter.struct}*", {parameter.name}{unique_identifier_suffix}_)')
                            self._build_array_copy_struct_to_cffi(writer, parameter.name, unique_identifier_suffix, '')

                        with writer.write_else():
                            writer.write_line(f'{parameter.name}{unique_identifier_suffix} = ffi.new("{parameter.struct}*")')
                            writer.write_line(f'{parameter.name}.to_cffi_out({parameter.name}{unique_identifier_suffix}[0], __keepalive)')
                    else:
                        writer.write_line(
                            f'{parameter.name}{unique_identifier_suffix} = {parameter.name}.to_cffi(__keepalive)[0]')
                elif parameter.enum:
                    if parameter.is_out and parameter.is_array:
                        size = str(parameter.sizes[0]) if parameter.sizes[0] else 'len(' + parameter.name + ')'
                        # If size is defined as a function parameter, in a wrapper it has to be named with prefix
                        # to avoid case when a function parameter name is a keyword in Python
                        if parameter.sizes[0] and isinstance(parameter.sizes[0], str) and not parameter.sizes[0].isdigit():
                            size = 'p_' + size
                        writer.write_line(
                            f'{parameter.name}{unique_identifier_suffix} = ffi.new("int[]", {size})')
                        self._build_array_copy_enum_to_cffi(writer, parameter.name, unique_identifier_suffix, '')
                    else:
                        writer.write_line(f'{parameter.name}{unique_identifier_suffix} = {parameter.name}.value')
                else:
                    if parameter.is_out and parameter.is_array:
                        size = str(parameter.sizes[0]) if parameter.sizes[0] else 'len(' + parameter.name + ')'
                        # If size is defined as a function parameter, in a wrapper it has to be named with prefix
                        # to avoid case when a function parameter name is a keyword in Python
                        if parameter.sizes[0] and isinstance(parameter.sizes[0], str) and not parameter.sizes[0].isdigit():
                            size = 'p_' + size
                        writer.write_line(
                            f'{parameter.name}{unique_identifier_suffix} = ffi.new("{parameter.c_type.get_ffi_string_def()}[]", {size})')
                        self._build_array_copy(writer, parameter.name, unique_identifier_suffix, '')
                    elif parameter.type == 'char * *' or (parameter.is_pointer_to_array and parameter.type == 'char *'):
                        writer.write_line(f'arg_keepalive = [ffi.new("char[]", x.encode() if type(x) is str else x) for x in {parameter.name}]')
                        writer.write_line(f'{parameter.name}{unique_identifier_suffix} = ffi.new("char* []", arg_keepalive)')
                    else:
                        writer.write_line(f'{parameter.name}{unique_identifier_suffix} = {parameter.name}')

            writer.write_line(
                ('ret = ' if not function.returns.is_void else '')
                + (f'_{module_name}.lib' if not self.wrap_dynamic_lib else 'lib') + f'.{function.name}('
                + ','.join([x.name + unique_identifier_suffix + '.encode() if ' +
                            'type(' + x.name + unique_identifier_suffix + ') is str ' +
                            'else ' + x.name + unique_identifier_suffix
                            for x in function.parameters])
                + ')')

            if function.returns.struct and not function.returns.is_void:
                writer.write_line(f'ret_ = {function.returns.struct}()')
                writer.write_line('ret_.from_cffi(ret)')
                writer.write_line('ret = ret_')

            for parameter in function.parameters:
                if parameter.struct:
                    if parameter.is_array and parameter.is_out:
                        with writer.write_if(f'hasattr({parameter.name}, \'__len__\')'):
                            self._build_array_copy_struct_from_cffi(writer, parameter.name, '', unique_identifier_suffix + '_')

                        with writer.write_else():
                            writer.write_line(f'{parameter.name}.from_cffi({parameter.name}{unique_identifier_suffix}[0])')
                    else:
                        # this shouldn't happen, only parameters passed by pointer/array can be out
                        pass
                elif parameter.enum:
                    if not parameter.is_out:
                        # this shouldn't happen, only parameters passed by pointer/array can be out
                        continue
                    if parameter.is_array:
                        self._build_array_copy_enum_from_cffi(writer, parameter.enum, parameter.name, '', unique_identifier_suffix)
                    else:
                        # TODO: evaluate, can this actually even happen? Similar to struct case
                        writer.write_line(f'{parameter.name} = {parameter.enum}({parameter.name}{unique_identifier_suffix})')
                else:
                    if not parameter.is_out:
                        continue
                    if parameter.is_array:
                        self._build_array_copy(writer, parameter.name, '', unique_identifier_suffix)
                    else:
                        # TODO: evaluate, can this actually even happen? Similar to struct case
                        writer.write_line(f'{parameter.name} = {parameter.name}{unique_identifier_suffix}')

            if not function.returns.is_void:
                writer.write_line(f'return ret')

            # PEP8 empty line after function
            writer.write_line('')

    def _add_documentation_to_a_function(self, writer, function):
        """ Add documentation to a function, based on a doxygen comment """
        if function.doxygen is not None:
            writer.write_line(f'\"\"\"')
            writer.write_line(f'Wrapping function generated for C language function documented as follows:')
            for line in function.doxygen.splitlines():
                line = line.replace("\"\"\"", "")  # To prevent SQL-injection-like error
                if line.startswith('/**') or line.startswith('*/'):
                    continue
                if line.startswith('*') and line[1:]:
                    writer.write_line(line[1:].strip())
            writer.write_line(f'\"\"\"')

    def _get_relevant_parameters(self, parameters):
        """ Relevant parameters - such parameters that will be on a parameter list in a wrapping
            python function. Every parameter that is a size of an array, will be discarded.
        """
        relevant_parameters = []
        for param in parameters:
            if not param.is_array_size:
                relevant_parameters.append(param.name)
        return relevant_parameters

    def _add_series_of_array_arguments_checks(self, writer, parameters):
        # Check 1:
        _check_if_every_in_array_is_not_empty(writer, parameters)
        # Check 2:
        _check_if_every_in_array_of_the_same_size_has_indeed_same_size(writer, parameters)
        # Check 3:
        _check_array_sizes_consistency_when_there_are_only_out_arrays(writer, parameters)

        # Initialize OUT arrays if necessary:
        _initialize_out_arrays_if_necessary_and_check_sizes(writer, parameters)
        # Initialize non-array OUT parameters if necessary:
        _initialize_non_array_out_parameters_if_necessary(writer, parameters)
        # Array sizes variables initialization:
        _initialize_array_size_params_inside_wrapper(writer, parameters)
