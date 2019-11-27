import unittest
import os
import pathlib

from tests._util.folder_clearing import clear_folder_contents


class SimpleEnumsTest(unittest.TestCase):

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

    def test_generate_bindings_to_enum(self):
        from tests.simplecases.simpleenums.generated.sources import enum
        self.assertEqual(enum.SomeEnum.A.value, 0)
        self.assertEqual(enum.SomeEnum.B.value, 1)
        self.assertEqual(enum.SomeEnum.C.value, 123)

    def test_generate_bindings_to_function_taking_enum(self):
        from tests.simplecases.simpleenums.generated.sources import enum
        self.assertEqual(enum.some_enum_to_int(enum.SomeEnum.A), 0)
        self.assertEqual(enum.some_enum_to_int(enum.SomeEnum.B), 1)
        self.assertEqual(enum.some_enum_to_int(enum.SomeEnum.C), 123)
