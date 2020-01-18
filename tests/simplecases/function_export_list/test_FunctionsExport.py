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
        self.export_fun_path = self.current_working_directory_path.joinpath('export') / 'functions_to_export.txt'
        if not os.path.exists(str(self.destination_path)):
            os.makedirs(str(self.destination_path))
        clear_folder_contents(self.destination_path)
        os.chdir(self.current_working_directory_path)
        os.chdir("../../..")
        call_string = r'python cBinder sources ' + \
                  r'-f ' + str(self.sources_path) + \
                  r' -d ' + str(self.destination_path) + \
                  r' -es ' + str(self.export_fun_path) + \
                  r' compile'
        print(call_string)
        os.system(call_string)
        os.chdir(self.destination_path.joinpath('sources'))

    def test_generate_bindings_to_function_with_export_list(self):
        from tests.simplecases.function_export_list.generated.sources import exportlist as el
        self.assertEqual(True, 'mul' in dir(el))
        self.assertEqual(True, 'sum' in dir(el))
        self.assertEqual(False, 'diff' in dir(el))
