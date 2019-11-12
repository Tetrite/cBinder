unique_identifier_suffix = '__internal'

# TODO: better tool for indendation


def build_wrapper_for_header(header_name, header):
    """Creates wrapper file for given HeaderFile"""
    with open(header_name + '.py', 'w+') as f:
        f.write("from . import _" + header_name + "\nfrom cffi import FFI\nffi = FFI()\n\n")

        _build_wrapper_for_header(header_name, f, header)


def build_wrapper_for_declarations(header_name, declarations):
    """Creates wrapper file for given list of FunctionDeclaration objects"""
    with open(header_name + '.py', 'w+') as f:
        f.write("from . import _" + header_name + "\rfrom cffi import FFI\rffi = FFI()\r\n\n")

        for decl in declarations:
            _build_wrapper_for_declaration(header_name, f, decl)


def build_wrapper_for_dynamic_library(header_name, header):
    pass


def _build_array_copy(name, _from, to):
    return [
        f'\tfor i,v in enumerate({name}):',
        f'\t\t{name}{_from}[i] = {name}{to}[i]'
    ]


def _build_python_function_wrapper_for_declaration(module_name, declaration):
    lines = [
        f'def {declaration.name}(' + ','.join([x.name for x in declaration.parameters]) + '):'
    ]

    for parameter in declaration.parameters:
        if parameter.is_out and parameter.is_array:
            size = str(parameter.sizes[0]) if parameter.sizes[0] else 'len(' + parameter.name + ')'
            lines.append(f'\t{parameter.name}{unique_identifier_suffix} = ffi.new("{parameter.c_type.get_ffi_string_def()}[]", {size})')
            lines += _build_array_copy(parameter.name, unique_identifier_suffix, '')
        else:
            lines.append(f'\t{parameter.name}{unique_identifier_suffix} = {parameter.name}')

    lines.append(
        '\t'
        + ('ret = ' if not declaration.returns.is_void else '')
        + f'_{module_name}.lib.{declaration.name}('
        + ','.join([x.name + unique_identifier_suffix for x in declaration.parameters])
        + ')')

    for parameter in declaration.parameters:
        if not parameter.is_out:
            continue
        if parameter.is_array:
            lines += _build_array_copy(parameter.name, '', unique_identifier_suffix)
        else:
            lines.append(f'\t{parameter.name} = {parameter.name}{unique_identifier_suffix}')

    if not declaration.returns.is_void:
        lines.append(f'\treturn ret')

    lines.append('')
    lines.append('')

    return '\n'.join(lines)


def _build_wrapper_for_declaration(header_name, f, declaration):
    s = _build_python_function_wrapper_for_declaration(header_name, declaration)
    f.write(s)


def _build_wrapper_for_header(header_name, f, header):
    for decl in header.declarations:
        _build_wrapper_for_declaration(header_name, f, decl)
