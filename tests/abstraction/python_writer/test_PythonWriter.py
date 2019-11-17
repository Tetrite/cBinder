import unittest
import pathlib
import os

from PythonWriter import PythonWriter

class PythonWriterTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_writer_unindented(self):
        writer = PythonWriter()
        writer.write_line('x=1');
        writer.write_line('y=2');
        self.assertEqual(writer.get_string(), 'x=1\ny=2')

    def test_writer_indented(self):
        writer = PythonWriter()
        writer.write_line('def a()')
        with writer.indent():
            writer.write_line('x=1')
            writer.write_line('y=2')

        self.assertEqual(writer.get_string(), 'def a()\n\tx=1\n\ty=2')

    def test_writer_escape(self):
        writer = PythonWriter()
        s = writer.escaped('""""')
        writer.write_line(f'x="{s}"')
        self.assertEqual(writer.get_string(), 'x="\\\"\\\"\\\"\\\""')

