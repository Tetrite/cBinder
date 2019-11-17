import unittest
import pathlib
import os

from tests._util.folder_clearing import clear_folder_contents


class MultipleArraysTest(unittest.TestCase):

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
    #   * Case 1: there are three arrays: two IN, and one OUT, same size
    #   * The function adds a to b and result is in c
    #   * @param[in]   n   size of an array
    #   * @param[in]   a   sample array (array of size n)
    #   * @param[in]   b    sample array (array of size n)
    #   * @param[out]  c    sample array (array of size n)
    #   * @return                status
    #   */
    #
    # int array_adding_result_in_separate(int n, int* a, int* b, int* c);
    def test_array_adding_result_in_separate_correct(self):
        from tests.withdoxygen.various_fun_parameters.generated.sources import multiple_arrays as ma
        c = [0, 0, 0]
        return_value = ma.array_adding_result_in_separate([1, 2, 3], [4, 5, 6])
        self.assertEqual(return_value, 0)
        self.assertEqual(c, [5, 7, 9])

    def test_array_adding_result_in_separate_correct_warning(self):
        from tests.withdoxygen.various_fun_parameters.generated.sources import multiple_arrays as ma
        with self.assertWarns(Warning):
            c = []
            return_value = ma.array_adding_result_in_separate([1, 2, 3], [4, 5, 6])
            self.assertEqual(return_value, 0)
            self.assertEqual(c, [5, 7, 9])

    def test_array_adding_result_in_separate_err1(self):
        from tests.withdoxygen.various_fun_parameters.generated.sources import two_arrays_same_size as tw
        with self.assertRaises(ValueError):
            tw.sum_of_two_arrays([1, 2], [1, 2, 3], [1, 2, 3])

    def test_sum_of_two_arrays_err2(self):
        from tests.withdoxygen.various_fun_parameters.generated.sources import two_arrays_same_size as tw
        with self.assertRaises(ValueError):
            tw.sum_of_two_arrays([], [1, 2, 3], [1, 2, 3])

    # /**
    #   * Case 2: there are four arrays: two IN, and two OUT, different sizes
    #   * The function takes two arrays of size n_1: array_1 and array_2
    #   * and returns in:
    #   *   - array_result_1 accordingly, n_2 first elements of array_1, 0s for indexes beyond n_1 -1
    #   *   - array_result_2 accordingly, n_2 first elements of array_2, 0s for indexes beyond n_2 -1
    #   * @param[in]   n_1   size of an array
    #   * @param[in]   n_2   size of an array
    #   * @param[in]   array_1   sample array (array of size n_1)
    #   * @param[in]   array_2    sample array (array of size n_1)
    #   * @param[out]  array_result_1    sample array (array of size n_2)
    #   * @param[out]  array_result_2    sample array (array of size n_2)
    #   * @return                status
    #   */
    #
    # int get_first_n_elems(int n_1, int n_2,
    #                 int* array_1, int* array_2,
    #                 int* array_result_1, int* array_result_2);
    def test_get_first_n_elems_correct(self):
        from tests.withdoxygen.various_fun_parameters.generated.sources import multiple_arrays as ma
        array_1 = [1, 2, 3, 4]
        array_2 = [5, 6, 7, 8]
        array_result_1 = [0, 0]
        array_result_2 = [0, 0]
        return_value = ma.get_first_n_elems(array_1, array_2, array_result_1, array_result_2)
        self.assertEqual(return_value, 0)
        self.assertEqual(array_result_1, [1, 2])
        self.assertEqual(array_result_2, [5, 6])

    def test_get_first_n_elems_error1(self):
        from tests.withdoxygen.various_fun_parameters.generated.sources import multiple_arrays as ma
        with self.assertRaises(ValueError):
            array_1 = [1, 2, 3, 4]
            array_2 = [5, 6, 7]
            array_result_1 = [0, 0]
            array_result_2 = [0, 0]
            ma.get_first_n_elems(array_1, array_2, array_result_1, array_result_2)

    def test_get_first_n_elems_error2(self):
        from tests.withdoxygen.various_fun_parameters.generated.sources import multiple_arrays as ma
        with self.assertRaises(ValueError):
            array_1 = [1, 2, 3, 4]
            array_2 = [5, 6, 7, 8]
            array_result_1 = [0, 0]
            array_result_2 = [0, 0, 0]
            ma.get_first_n_elems(array_1, array_2, array_result_1, array_result_2)

    def test_get_first_n_elems_error3(self):
        from tests.withdoxygen.various_fun_parameters.generated.sources import multiple_arrays as ma
        with self.assertRaises(ValueError):
            array_1 = []
            array_2 = [5, 6, 7, 8]
            array_result_1 = [0, 0]
            array_result_2 = [0, 0]
            ma.get_first_n_elems(array_1, array_2, array_result_1, array_result_2)

    # /**
    #   * Case 3: there are three arrays:
    #   *      - two arrays of the same size, one IN and one OUT (array_in_1, and array_out)
    #   *      - one array of a different size, IN (array_in_2)
    #   * The function adds to every element of array_in_1, sum of elements in array_in_2,
    #   * and rewrites these sums into OUT array: array_out
    #   * @param[in]   n_1   size of an array
    #   * @param[in]   n_2   size of an array
    #   * @param[in]   array_in_1   sample array (array of size n_1)
    #   * @param[out]   array_out    sample array (array of size n_1)
    #   * @param[in]  array_in_2    sample array (array of size n_2)
    #   * @return                status
    #   */
    #
    # int combine_arrays(int n_1, int n_2, int* array_in_1, int* array_out, int* array_in_2);
    def test_combine_arrays_correct(self):
        from tests.withdoxygen.various_fun_parameters.generated.sources import multiple_arrays as ma
        array_in_1 = [1, 2, 3, 4]
        array_out = [0, 0, 0, 0]
        array_in_2 = [1, 2]
        return_value = ma.combine_arrays(array_in_1, array_out, array_in_2)
        self.assertEqual(return_value, 0)
        self.assertEqual(array_out, [4, 5, 6, 7])

    def test_combine_arrays_error1(self):
        from tests.withdoxygen.various_fun_parameters.generated.sources import multiple_arrays as ma
        with self.assertRaises(ValueError):
            array_in_1 = []
            array_out = [0, 0, 0, 0]
            array_in_2 = [1, 2]
            return_value = ma.combine_arrays(array_in_1, array_out, array_in_2)
            self.assertEqual(return_value, 0)
            self.assertEqual(array_out, [4, 5, 6, 7])

    def test_combine_arrays_warning_1(self):
        from tests.withdoxygen.various_fun_parameters.generated.sources import multiple_arrays as ma
        with self.assertWarns(Warning):
            array_in_1 = [1, 2, 3, 4]
            array_out = []
            array_in_2 = [1, 2]
            return_value = ma.combine_arrays(array_in_1, array_out, array_in_2)
            self.assertEqual(return_value, 0)
            self.assertEqual(array_out, [4, 5, 6, 7])

    def test_combine_arrays_warning_2(self):
        from tests.withdoxygen.various_fun_parameters.generated.sources import multiple_arrays as ma
        with self.assertWarns(Warning):
            array_in_1 = [1, 2, 3, 4]
            array_out = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            array_in_2 = [1, 2]
            return_value = ma.combine_arrays(array_in_1, array_out, array_in_2)
            self.assertEqual(return_value, 0)
            self.assertEqual(array_out, [4, 5, 6, 7])
