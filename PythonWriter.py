_trans = str.maketrans({
            '\t': '\\t',
            '\n': '\\n',
            '\r': '\\r',
            '\'': '\\\'',
            '\\': '\\\\',
            '\"': '\\\"'
            })

def _escape_string(s):
    return s.translate(_trans)


class PythonWriter:
    class Indent:
        def __init__(self, writer):
            self.writer = writer

        def __enter__(self):
            self.writer._indent_level += 1

        def __exit__(self, exc_type, exc_value, traceback):
            self.writer._indent_level -= 1
            self.writer.write_line('')

    class For:
        def __init__(self, writer, what, _in):
            self.writer = writer
            self.what = what
            self._in = _in

        def __enter__(self):
            self.writer.write_line(f'for {self.what} in {self._in}:')
            self.writer._indent_level += 1

        def __exit__(self, exc_type, exc_value, traceback):
            self.writer._indent_level -= 1
            self.writer.write_line('')

    class While:
        def __init__(self, writer, cond):
            self.writer = writer
            self.cond = cond

        def __enter__(self):
            self.writer.write_line(f'while {self.cond}:')
            self.writer._indent_level += 1

        def __exit__(self, exc_type, exc_value, traceback):
            self.writer._indent_level -= 1
            self.writer.write_line('')

    class If:
        def __init__(self, writer, cond):
            self.writer = writer
            self.cond = cond

        def __enter__(self):
            self.writer.write_line(f'if {self.cond}:')
            self.writer._indent_level += 1

        def __exit__(self, exc_type, exc_value, traceback):
            self.writer._indent_level -= 1
            self.writer.write_line('')

    class Elif:
        def __init__(self, writer, cond):
            self.writer = writer
            self.cond = cond

        def __enter__(self):
            self.writer.write_line(f'elif {cond}:')
            self.writer._indent_level += 1

        def __exit__(self, exc_type, exc_value, traceback):
            self.writer._indent_level -= 1
            self.writer.write_line('')

    class Else:
        def __init__(self, writer):
            self.writer = writer

        def __enter__(self):
            self.writer.write_line('else:')
            self.writer._indent_level += 1

        def __exit__(self, exc_type, exc_value, traceback):
            self.writer._indent_level -= 1
            self.writer.write_line('')

    class Class:
        def __init__(self, writer, name, inherits=[]):
            self.writer = writer
            self.name = name
            self.inherits = inherits

        def __enter__(self):
            if len(self.inherits) == 0:
                self.writer.write_line(f'class {self.name}:')
            else:
                inherited_s = ', '.join(self.inherits)
                self.writer.write_line(f'class {self.name}({inherited_s}):')

            self.writer._indent_level += 1

        def __exit__(self, exc_type, exc_value, traceback):
            self.writer._indent_level -= 1
            self.writer.write_line('')

    class Def:
        def __init__(self, writer, name, params=[]):
            self.writer = writer
            self.name = name
            self.params = params

        def __enter__(self):
            if len(self.params) == 0:
                self.writer.write_line(f'def {self.name}:')
            else:
                params_s = ', '.join(self.params)
                self.writer.write_line(f'def {self.name}({params_s}):')

            self.writer._indent_level += 1

        def __exit__(self, exc_type, exc_value, traceback):
            self.writer._indent_level -= 1
            self.writer.write_line('')

    def __init__(self):
        self._lines = []
        self._indent = '\t'
        self._indent_level = 0

    def get_string(self):
        return '\n'.join(self._lines)

    def write_line(self, line):
        if self._indent_level > 0:
            self._lines.append(self._indent * self._indent_level + line)
        else:
            self._lines.append(line)

    def write_for(self, what, _in):
        return PythonWriter.For(self, what, _in)

    def write_if(self, cond):
        return PythonWriter.If(self, cond)

    def write_while(self, cond):
        return PythonWriter.While(self, cond)

    def write_elif(self, cond):
        return PythonWriter.Elif(self, cond)

    def write_else(self):
        return PythonWriter.Else(self)

    def write_class(self, name, inherits=[]):
        return PythonWriter.Class(self, name, inherits)

    def write_def(self, name, params=[]):
        return PythonWriter.Def(self, name, params)

    def escaped(self, text):
        return _escape_string(text)

    def add_indent(self):
        self._indent += 1

    def remove_indent(self):
        self._indent -= 1

    def indent(self):
        return PythonWriter.Indent(self)
