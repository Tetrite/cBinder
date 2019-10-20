import unittest
import os
import pathlib
from tests.util.folder_clearing import clear_folder_contents

class SimpleFunctionsTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.current_working_directory_path = pathlib.Path(os.getcwd())
        self.sources_path = self.current_working_directory_path.joinpath('sources')
        self.destination_path = self.current_working_directory_path.joinpath('generated')
        clear_folder_contents(self.destination_path)
        os.chdir("../..")
        os.system(r'python main.py -f ' + str(self.sources_path) + ' -d ' + str(self.destination_path))
        os.chdir(self.destination_path)

    def test_generate_bindings_to_function_with_array(self):
        self.fix_incorrect_import_in_wrapper()

        from generated import arraytest
        a = []
        arraytest.func(a)
        self.assertEqual(a, [0.0, 1.0, 2.0, 3.0, 4.0])

    def test_generate_bindings_to_function_with_array_sum(self):
        self.fix_incorrect_import_in_wrapper()

        from generated import arraytest
        a = [2.0, 3.0]
        i = arraytest.sum(4.0, a)
        self.assertEqual(i, 9.0)

    def fix_incorrect_import_in_wrapper(self):
        with open(str(self.destination_path.joinpath("arraytest.py"))) as f:
            newText = f.read().replace('import _arraytest', 'from . import _arraytest')
        with open(str(self.destination_path.joinpath("arraytest.py")), "w") as f:
            f.write(newText)
