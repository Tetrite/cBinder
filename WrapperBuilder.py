from DoxygenParser import *
from Function import *

def get_declaration(declaration):
    return Declaration(declaration)

# TODO: what does this function name mean?
def _get_rewriter_into_array(name):
    s = '    for i,v in enumerate(' + name + '):\r'
    s = s + '        ' + name + '2[i] = ' + name + '[i]\r'
    return s

def _get_rewriter_into_list(name):
    s = '    for i,v in enumerate(' + name + '2):\r'
    s = s + '        ' + name + '[i] = ' + name + '2[i]\r'
    return s

# TODO: just appending 2 to the parameter is not safe, there may be collisions
#       use more sophisticated mangling, for example prepend/append $
def _build_python_function_wrapper_for_declaration(module_name, declaration):
    s = 'def ' + declaration.name + '('
    s = s + ','.join([x.name for x in declaration.parameters])
    s = s + '):\r'

    for parameter in declaration.parameters:
        if parameter.is_out and parameter.is_array:
            size = str(parameter.sizes[0]) if parameter.sizes[0] else 'len(' + parameter.name + ')'
            s = s + '    ' + parameter.name + '2 = ffi.new("' + parameter.c_type.value + '[]", ' + size + ')\r'
            s = s + _get_rewriter_into_array(parameter.name)
        else:
            s = s + '    ' + parameter.name + '2 = ' + parameter.name + '\r'

    s = s + '    ' + ('ret = ' if not declaration.returns.is_void else '') + '_' + module_name + '.lib.' + \
        declaration.name + '(' + ','.join([x.name + '2' for x in declaration.parameters]) + ')\r'

    for parameter in declaration.parameters:
        if not parameter.is_out:
            continue
        if parameter.is_array:
            s = s + _get_rewriter_into_list(parameter.name)
        else:
            s = s + '    ' + parameter.name + ' = ' + parameter.name + '2\r'

    if not declaration.returns.is_void:
        s = s + '    return ret'

    return s + '\r\n\n'

def _build_wrapper_for_declaration(header_name, f, declaration):
    s = _build_python_function_wrapper_for_declaration(header_name, declaration)
    f.write(s)

def _build_wrapper_for_header(header_name, f, header):
    for decl in header.declarations:
        _build_wrapper_for_declaration(header_name, f, decl)

def build_wrapper_for_header(header_name, header):
    with open(header_name + '.py', 'w+') as f:
        f.write("from . import _" + header_name + "\rfrom cffi import FFI\rffi = FFI()\r\n\n")

        _build_wrapper_for_header(header_name, f, header)

def build_wrapper_for_declarations(header_name, declarations):
    with open(header_name + '.py', 'w+') as f:
        f.write("from . import _" + header_name + "\rfrom cffi import FFI\rffi = FFI()\r\n\n")

        for decl in declarations:
            _build_wrapper_for_declaration(header_name, f, decl)
