import unittest
import pathlib
import os

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
        os.system(r'python main.py compile -f ' + str(self.sources_path) + ' -d ' + str(self.destination_path))
        os.chdir(self.destination_path.joinpath('sources'))

    def test_generate_bindings_to_function_with_doxygen(self):
        pass

