import unittest
import os
import pathlib

from tests._util.folder_clearing import clear_folder_contents


class SimpleStructsTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.current_working_directory_path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
        self.sources_path = self.current_working_directory_path.joinpath('sources')
        self.destination_path = self.current_working_directory_path.joinpath('generated')
        if not os.path.exists(str(self.destination_path)):
            os.makedirs(str(self.destination_path))
        clear_folder_contents(self.destination_path)
        os.chdir(self.current_working_directory_path)
        os.chdir("../../..")
        os.system(r'python main.py sources -f ' + str(self.sources_path) + ' -d ' + str(self.destination_path) + ' compile')
        os.chdir(self.destination_path)

    def test_generate_bindings_to_make_struct_instance(self):
        from tests.simplecases.simplestructs.generated.sources import struct
        s = struct.simple_struct()
        s.a = 123
        s.b = 123.0
        s.c = b'a'

    def test_generate_bindings_to_simple_function_with_struct(self):
        from tests.simplecases.simplestructs.generated.sources import struct
        s = struct.simple_struct()
        s.a = 123
        s.b = 123.0
        s.c = b'a'
        b = struct.get_b([s])
        self.assertEqual(b, s.b)

    def test_generate_bindings_to_simple_function_with_struct2(self):
        from tests.simplecases.simplestructs.generated.sources import struct
        s = struct.simple_struct()
        s.a = 123
        s.b = 123.0
        s.c = b'a'
        struct.print([s])