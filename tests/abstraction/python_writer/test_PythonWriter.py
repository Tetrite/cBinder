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

    def test_writer_while(self):
        writer = PythonWriter()
        with writer.write_while('i==10'):
            writer.write_line('i=i+1')
        self.assertEqual(writer.get_string(), 'while i==10:\n\ti=i+1')

    def test_writer_if(self):
        writer = PythonWriter()
        with writer.write_if('i==10'):
            writer.write_line('j=i+1')
        self.assertEqual(writer.get_string(), 'if i==10:\n\tj=i+1')

    def test_writer_for(self):
        writer = PythonWriter()
        with writer.write_for('i', 'range(10)'):
            writer.write_line('j=i+1')
        self.assertEqual(writer.get_string(), 'for i in range(10):\n\tj=i+1')

    def test_writer_class_def(self):
        writer = PythonWriter()
        with writer.write_class('a'):
            with writer.write_def('__init__', ['self', 'i']):
                writer.write_line('self.i=i')
        self.assertEqual(writer.get_string(), 'class a:\n\tdef __init__(self, i):\n\t\tself.i=i')

