_trans = str.maketrans({
            '\t': '\\\t',
            '\n': '\\\n',
            '\r': '\\\r',
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
            pass

        def __enter__(self):
            self.writer._indent_level += 1

        def __exit__(self, exc_type, exc_value, traceback):
            self.writer._indent_level -= 1

    def __init__(self):
        self._lines = []
        self._indent = '\t'
        self._indent_level = 0

    def get_string(self):
        return '\n'.join(self._lines) + '\n'

    def write_line(self, line):
        if self._indent_level > 0:
            self._lines.append(self._indent * self._indent_level + line)
        else:
            self._lines.append(line)

    def escaped(self, text):
        return _escape_string(text)

    def indent(self):
        return PythonWriter.Indent(self)
