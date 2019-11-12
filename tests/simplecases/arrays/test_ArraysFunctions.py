import unittest
import pathlib
import os

from tests._util.folder_clearing import clear_folder_contents


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
        os.chdir("../../..")
        os.system(r'python main.py sources -f ' + str(self.sources_path) + ' -d ' + str(self.destination_path) + ' compile')
        os.chdir(self.destination_path.joinpath('sources'))

    def test_generate_bindings_to_function_with_array(self):

        from tests.simplecases.arrays.generated.sources import arraytest
        a = [0]*5
        arraytest.func(a)
        self.assertEqual(a, [0.0, 1.0, 2.0, 3.0, 4.0])

    def test_generate_bindings_to_function_with_array_sum(self):

        from tests.simplecases.arrays.generated.sources import arraytest
        a = [2.0, 3.0, 4.0, 5.0, 6.0]
        i = arraytest.sum(4.0, a)
        self.assertEqual(i, 24.0)

