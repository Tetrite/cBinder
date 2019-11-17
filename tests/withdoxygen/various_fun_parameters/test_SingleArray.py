import unittest
import pathlib
import os

from tests._util.folder_clearing import clear_folder_contents


class SingleArrayTest(unittest.TestCase):

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
            r'python main.py sources -f ' + str(self.sources_path) + ' -d ' + str(self.destination_path) + ' compile')
        os.chdir(self.destination_path.joinpath('sources'))

    # /**
    #   * Case 1: there is only one IN array
    #   * The function returns sum of one array
    #   * @param[in]   n         number of elements in array
    #   * @param[in]   in_arr   sample array (array of size n)
    #   * @return                sum of elements
    #   */
    #
    # int sum_of_array(int n, int* in_arr);
    def test_single_sum_of_array_correct(self):
        from tests.withdoxygen.various_fun_parameters.generated.sources import single_array as sa
        return_value = sa.sum_of_array([1, 2, 3])
        self.assertEqual(return_value, 6)

    def test_single_array_sum_of_array_empty_list(self):
        from tests.withdoxygen.various_fun_parameters.generated.sources import single_array as sa
        with self.assertRaises(ValueError):
            sa.sum_of_array([])

    # /**
    # * Case 2: there is only one IN array - size defined as constant
    # * The function returns sum of one array
    # * @param[in]   in_arr   sample array (array of size 5)
    # * @return                sum of elements
    # */
    #
    # int sum_of_array_constant(int* in_arr);
    def test_sum_of_array_constant_correct(self):
        from tests.withdoxygen.various_fun_parameters.generated.sources import single_array as sa
        return_value = sa.sum_of_array_constant([2, 2, 2, 2, 2])
        self.assertEqual(return_value, 10)

    def test_sum_of_array_constant_empty_list(self):
        from tests.withdoxygen.various_fun_parameters.generated.sources import single_array as sa
        with self.assertRaises(ValueError):
            sa.sum_of_array_constant([])

    # /**
    # * Case 3: there is only one IN/OUT array
    # * The function doubles the values of an array
    # * @param[in]   n         number of elements in array
    # * @param[in,out]   in_out_arr   sample array (array of size n)
    # * @return                sum of elements
    # */
    #
    # int double_the_values_inside_array(int n, int* in_out_arr);
    def test_double_the_values_inside_array_correct(self):
        from tests.withdoxygen.various_fun_parameters.generated.sources import single_array as sa
        in_out_array = [1, 2, 3]
        return_value = sa.double_the_values_inside_array(in_out_array)
        self.assertEqual(return_value, 0)
        self.assertEqual(in_out_array, [2, 4, 6])

    def test_double_the_values_inside_array_empty_list(self):
        from tests.withdoxygen.various_fun_parameters.generated.sources import single_array as sa
        with self.assertRaises(ValueError):
            sa.double_the_values_inside_array([])


