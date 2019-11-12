import unittest
import os
import pathlib

from tests.util.folder_clearing import clear_folder_contents


class SimpleFunctionsTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.current_working_directory_path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
        self.sources_path = self.current_working_directory_path.joinpath('sources')
        self.destination_path = self.current_working_directory_path.joinpath('generated')
        if not os.path.exists(str(self.destination_path)):
            os.makedirs(str(self.destination_path))
        clear_folder_contents(self.destination_path)
        os.chdir(self.current_working_directory_path)
        os.chdir("../..")
        os.system(r'python main.py sources -f ' + str(self.sources_path) + ' -d ' + str(self.destination_path) + ' compile')
        os.chdir(self.destination_path)

    def test_generate_bindings_to_simple_add_function_integer(self):
        from tests.simplefunctions.generated.sources import add
        sum = add.add(1, 2)
        self.assertEqual(sum, 3)

    def test_generate_bindings_to_simple_add_function_float(self):
        from tests.simplefunctions.generated.sources import add
        sum = add.addF(1.1, 2.2)
        self.assertAlmostEqual(sum, 3.3, places=6)

    def test_generate_bindings_to_simple_print_char_function(self):
        from tests.simplefunctions.generated.sources import char
        char = char.printChar('a'.encode('ascii'))
        self.assertEqual(char, 97)
