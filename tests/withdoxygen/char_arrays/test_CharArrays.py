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
        os.system(
            r'python cBinder sources -v -f ' + str(self.sources_path) + ' -d ' + str(self.destination_path) + ' compile')
        os.chdir(self.destination_path.joinpath('sources'))

    def test_get_string_length_pointer_1(self):
        from tests.withdoxygen.char_arrays.generated.sources import chararray as cha
        string_ex = "example"
        self.assertEqual(7, cha.get_string_length_pointer(string_ex))

    def test_get_string_length_pointer_2(self):
        from tests.withdoxygen.char_arrays.generated.sources import chararray as cha
        string_ex = 'example'
        self.assertEqual(7, cha.get_string_length_pointer(string_ex))

    def test_get_string_length_braces(self):
        from tests.withdoxygen.char_arrays.generated.sources import chararray as cha
        string_ex = "example"
        self.assertEqual(7, cha.get_string_length_braces(string_ex))

    def test_get_sum_of_string_lengths_pointers(self):
        from tests.withdoxygen.char_arrays.generated.sources import chararray as cha
        arr_of_strings = []
        arr_of_strings.append("one")
        arr_of_strings.append("two")
        arr_of_strings.append("three")
        self.assertEqual(11, cha.get_sum_of_string_lengths_pointers(arr_of_strings, 3))

    def test_get_sum_of_string_lengths_mix(self):
        from tests.withdoxygen.char_arrays.generated.sources import chararray as cha
        arr_of_strings = []
        arr_of_strings.append("one")
        arr_of_strings.append("two")
        arr_of_strings.append("three")
        self.assertEqual(11, cha.get_sum_of_string_lengths_mix(arr_of_strings, 3))

    def test_fill_with_agh_pointer(self):
        from tests.withdoxygen.char_arrays.generated.sources import chararray as cha
        ex = ['']
        cha.fill_with_agh_pointer(ex)
        self.assertEqual('agh', ex[0])

    def test_fill_with_agh_brackets(self):
        from tests.withdoxygen.char_arrays.generated.sources import chararray as cha
        ex = ['']
        cha.fill_with_agh_brackets(ex)
        self.assertEqual('agh', ex[0])

    # def test_fill_with_a_2D(self):
    #     from tests.withdoxygen.char_arrays.generated.sources import chararray as cha
    #     arr_of_strings = ['bbbb', 'ccccccc', 'dddd']
    #     self.assertEqual(11, cha.get_sum_of_string_lengths_mix(arr_of_strings, 3))

