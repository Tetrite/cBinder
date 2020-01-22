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
        os.system(r'python cBinder sources -f ' + str(self.sources_path) + ' -d ' + str(self.destination_path) + ' compile')
        os.chdir(self.destination_path.joinpath('sources'))

    def test_generate_bindings_to_function_with_doxygen(self):
        from tests.withdoxygen.out_non_array.generated.sources import returnfive as rf
        retval = [1]
        return_value = rf.return_five(retval)
        self.assertEqual(return_value, 0)
        self.assertEqual(retval, [5])

    def test_generate_bindings_to_function_with_doxygen_err(self):
        from tests.withdoxygen.out_non_array.generated.sources import returnfive as rf
        with self.assertRaises(ValueError):
            retval = 3
            return_value = rf.return_five(retval)
            self.assertEqual(return_value, 0)
            self.assertEqual(retval, [5])

    def test_generate_bindings_to_function_with_doxygen_warn_1(self):
        from tests.withdoxygen.out_non_array.generated.sources import returnfive as rf
        with self.assertWarns(Warning):
            retval = []
            return_value = rf.return_five(retval)
            self.assertEqual(return_value, 0)
            self.assertEqual(retval, [5])

    def test_generate_bindings_to_function_with_doxygen_warn_2(self):
        from tests.withdoxygen.out_non_array.generated.sources import returnfive as rf
        with self.assertWarns(Warning):
            retval = [1, 2, 3, 4, 5]
            return_value = rf.return_five(retval)
            self.assertEqual(return_value, 0)
            self.assertEqual(retval, [5])
