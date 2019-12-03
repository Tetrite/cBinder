import unittest
import pathlib
import os

from tests._util.folder_clearing import clear_folder_contents


class TwoArraysSameSizeTest(unittest.TestCase):

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

    # /* -------------------------  TWO ARRAYS OF THE SAME TYPE  ------------------------- */
    # /**
    #   * Case 1: there are two IN arrays of the same size - parameter
    #   * The function sums the values of two separate arrays and returns it
    #   * @param[in]   n         number of elements in array
    #   * @param[in]   in_arr1   sample array (array of size n)
    #   * @param[in]   in_arr2   sample array (array of size n)
    #   * @return                sum of elements
    #   */
    #
    # int sum_of_two_arrays(int n, int* in_arr1, int* in_arr2);
    def test_sum_of_two_arrays_correct(self):
        from tests.withdoxygen.various_fun_array_parameters.generated.sources import two_arrays_same_size as tw
        return_value = tw.sum_of_two_arrays([1, 2, 3], [1, 2, 3])
        self.assertEqual(return_value, 12)

    def test_sum_of_two_arrays_err1(self):
        """
        In this test, there are two in arrays of the same size,
        but the user passes two arrays of different size
        """
        from tests.withdoxygen.various_fun_array_parameters.generated.sources import two_arrays_same_size as tw
        with self.assertRaises(ValueError):
            tw.sum_of_two_arrays([1, 2], [1, 2, 3])

    def test_sum_of_two_arrays_err2(self):
        """
        In this test, there are two in arrays of the same size,
        but the user passes one empty array
        """
        from tests.withdoxygen.various_fun_array_parameters.generated.sources import two_arrays_same_size as tw
        with self.assertRaises(ValueError):
            tw.sum_of_two_arrays([], [1, 2, 3])

    # /**
    #   * Case 2: there are two IN arrays of the same size - constant
    #   * The function sums the values of two separate arrays and returns it
    #   * @param[in]   in_arr1   sample array (array of size 5)
    #   * @param[in]   in_arr2   sample array (array of size 5)
    #   * @return                sum of elements
    #   */
    #
    # int sum_of_two_arrays_constant_size(int* in_arr1, int* in_arr2);
    def test_sum_of_two_arrays_constant_size_correct(self):
        from tests.withdoxygen.various_fun_array_parameters.generated.sources import two_arrays_same_size as tw
        return_value = tw.sum_of_two_arrays_constant_size([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
        self.assertEqual(return_value, 30)

    def test_sum_of_two_arrays_constant_size_err(self):
        from tests.withdoxygen.various_fun_array_parameters.generated.sources import two_arrays_same_size as tw
        with self.assertRaises(ValueError):
            tw.sum_of_two_arrays_constant_size([1, 2], [1, 2, 3])

    # /**
    #   * Case 3: there are two IN,OUT arrays of the same size
    #   * The function doubles the values of two separate arrays
    #   * @param[in]   n         number of elements in array
    #   * @param[in,out]   in_out_arr1   sample array (array of size n)
    #   * @param[in,out]   in_out_arr2   sample array (array of size n)
    #   * @return                sum of elements
    #   */
    #
    # int double_the_values_inside_two_arrays(int n, int* in_out_arr1, int* in_out_arr2);
    def test_double_the_values_inside_two_arrays_correct(self):
        from tests.withdoxygen.various_fun_array_parameters.generated.sources import two_arrays_same_size as tw
        arr_1 = [1, 2, 3]
        arr_2 = [1, 2, 3]
        return_value = tw.double_the_values_inside_two_arrays(arr_1, arr_2)
        self.assertEqual(return_value, 0)
        self.assertEqual(arr_1, [2, 4, 6])
        self.assertEqual(arr_2, [2, 4, 6])

    def test_double_the_values_inside_two_arrays_err(self):
        from tests.withdoxygen.various_fun_array_parameters.generated.sources import two_arrays_same_size as tw
        with self.assertRaises(ValueError):
            tw.double_the_values_inside_two_arrays([1, 2, 3], [1, 2, 3, 4])

    # /**
    #   * Case 4: there are two OUT arrays of the same size
    #   * The function fills the arrays with integer==2 constant value
    #   * @param[in]   n         number of elements in array
    #   * @param[out]   out_arr1   sample array (array of size n)
    #   * @param[out]   out_arr2   sample array (array of size n)
    #   * @return                sum of elements
    #   */
    #
    # int fill_two_arrays_with_twos(int n, int* out_arr1, int* out_arr2);
    def test_fill_two_arrays_with_twos_correct(self):
        from tests.withdoxygen.various_fun_array_parameters.generated.sources import two_arrays_same_size as tw
        arr_1 = [1, 2, 3]
        arr_2 = [1, 2, 3]
        return_value = tw.fill_two_arrays_with_twos(arr_1, arr_2)
        self.assertEqual(return_value, 0)
        self.assertEqual(arr_1, [2, 2, 2])
        self.assertEqual(arr_2, [2, 2, 2])

    def test_fill_two_arrays_with_twos_err(self):
        from tests.withdoxygen.various_fun_array_parameters.generated.sources import two_arrays_same_size as tw
        with self.assertRaises(ValueError):
            tw.fill_two_arrays_with_twos([1, 2], [1, 2, 3, 4])

    # /* -------------------------  TWO ARRAYS OF DIFFERENT TYPES  ------------------------- */
    # /**
    #   * Case 1: there are two arrays: one IN and one OUT
    #   * The function takes values from IN array and writes it into OUT array in reversed order
    #   * @param[in]   n   size of an array
    #   * @param[in]   in_order   sample array (array of size n)
    #   * @param[out]  reverse_order    sample reversed array (array of size n)
    #   * @return                status
    #   */
    #
    # int reverse_array_order(int n, int* in_order, int* reverse_order );
    def test_reverse_array_order_correct(self):
        from tests.withdoxygen.various_fun_array_parameters.generated.sources import two_arrays_same_size as tw
        in_order = [1, 2, 3]
        reverse_order = [1, 2, 3]
        return_value = tw.reverse_array_order(in_order, reverse_order)
        self.assertEqual(return_value, 0)
        self.assertEqual(reverse_order, [3, 2, 1])

    def test_reverse_array_order_correct_with_warning1(self):
        from tests.withdoxygen.various_fun_array_parameters.generated.sources import two_arrays_same_size as tw
        with self.assertWarns(Warning):
            in_order = [1, 2, 3]
            reverse_order = []
            return_value = tw.reverse_array_order(in_order, reverse_order)
            self.assertEqual(return_value, 0)
            self.assertEqual(reverse_order, [3, 2, 1])

    def test_reverse_array_order_correct_with_warning2(self):
        from tests.withdoxygen.various_fun_array_parameters.generated.sources import two_arrays_same_size as tw
        with self.assertWarns(Warning):
            in_order = [1, 2, 3]
            reverse_order = [1, 2, 3, 4, 5, 6, 7]
            return_value = tw.reverse_array_order(in_order, reverse_order)
            self.assertEqual(return_value, 0)
            self.assertEqual(reverse_order, [3, 2, 1])

    def test_reverse_array_order_warning(self):
        from tests.withdoxygen.various_fun_array_parameters.generated.sources import two_arrays_same_size as tw
        with self.assertWarns(Warning):
            tw.reverse_array_order([], [1, 2, 3, 4])

    # /**
    #   * Case 2: there are two arrays: one IN,OUT and one OUT
    #   * The function takes values from IN array and writes it into OUT array in reversed order
    #   * it also reverses an order of IN,OUT array
    #   * @param[in]   n   size of an array
    #   * @param[in,out]   in_order   sample array (array of size n)
    #   * @param[out]  reverse_order    sample reversed array (array of size n)
    #   * @return                status
    #   */
    #
    # int reverse_both_arrays_order(int n, int* in_order, int* reverse_order );
    def test_reverse_both_arrays_order_correct(self):
        from tests.withdoxygen.various_fun_array_parameters.generated.sources import two_arrays_same_size as tw
        in_order = [1, 2, 3]
        reverse_order = [4, 5, 6]
        return_value = tw.reverse_both_arrays_order(in_order, reverse_order)
        self.assertEqual(return_value, 0)
        self.assertEqual(in_order, [3, 2, 1])
        self.assertEqual(reverse_order, [3, 2, 1])

    def test_reverse_both_arrays_order_with_warning1(self):
        from tests.withdoxygen.various_fun_array_parameters.generated.sources import two_arrays_same_size as tw
        with self.assertWarns(Warning):
            in_order = [1, 2, 3]
            reverse_order = []
            return_value = tw.reverse_both_arrays_order(in_order, reverse_order)
            self.assertEqual(return_value, 0)
            self.assertEqual(in_order, [3, 2, 1])
            self.assertEqual(reverse_order, [3, 2, 1])

    def test_reverse_both_arrays_order_warning(self):
        from tests.withdoxygen.various_fun_array_parameters.generated.sources import two_arrays_same_size as tw
        with self.assertWarns(Warning):
            tw.reverse_both_arrays_order([], [1, 2, 3, 4])

    # /**
    #   * Case 3: there are two arrays: one IN and one IN,OUT
    #   * The function performs for every i: arrayIN,OUT[i] = arrayIN[i] + arrayIN,OUT[i]
    #   * it also reverses an order of IN,OUT array
    #   * @param[in]   n   size of an array
    #   * @param[in]   array_1   sample array (array of size n)
    #   * @param[in,out]  array_2    sample array (array of size n)
    #   * @return                status
    #   */
    #
    # int array_adding(int n, int* array_1, int* array_2);

    def test_array_adding_correct(self):
        from tests.withdoxygen.various_fun_array_parameters.generated.sources import two_arrays_same_size as tw
        array_1 = [1, 2, 3]
        array_2 = [4, 5, 6]
        return_value = tw.array_adding(array_1, array_2)
        self.assertEqual(return_value, 0)
        self.assertEqual(array_2, [5, 7, 9])

    def test_array_adding_err1(self):
        from tests.withdoxygen.various_fun_array_parameters.generated.sources import two_arrays_same_size as tw
        with self.assertRaises(ValueError):
            tw.array_adding([], [1, 2, 3, 4])

    def test_array_adding_err2(self):
        from tests.withdoxygen.various_fun_array_parameters.generated.sources import two_arrays_same_size as tw
        with self.assertRaises(ValueError):
            tw.array_adding([1, 2], [1, 2, 3, 4])
