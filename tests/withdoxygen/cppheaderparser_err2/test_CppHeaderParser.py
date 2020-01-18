import unittest
import pathlib
import os
import shutil


class ArgumentTypesTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.current_working_directory_path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
        self.sources_path = self.current_working_directory_path.joinpath('sources')
        self.destination_path = self.current_working_directory_path.joinpath('generated')
        if os.path.exists(str(self.destination_path)):
            shutil.rmtree(self.destination_path)
        os.makedirs(str(self.destination_path))
        os.chdir(self.current_working_directory_path)
        os.chdir("../../..")
        os.system(r'python cBinder sources -f ' + str(self.sources_path) + ' -d ' + str(self.destination_path) + ' compile')
        os.chdir(self.destination_path.joinpath('sources'))

    def test_standard_types(self):
        from tests.withdoxygen.cppheaderparser_err2.generated.sources import parser_err_2 as par
        self.assertEqual(par.sum(2, 3), 5)
