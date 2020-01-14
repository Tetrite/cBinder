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
        os.system(
            r'python cBinder sources -v -f ' + str(self.sources_path) + ' -d ' + str(self.destination_path) + ' compile')
        os.chdir(self.destination_path.joinpath('sources'))

    def test_standard_types(self):
        from tests.withdoxygen.argument_types.generated.sources import standard_types as st
        a = 5
        b = 3
        self.assertEqual(st.add_short(a, b), 8)
        self.assertEqual(st.add_short_int(a, b), 8)
        self.assertEqual(st.add_signed_short(a, b), 8)
        self.assertEqual(st.add_signed_short_int(a, b), 8)
        self.assertEqual(st.add_unsigned_short(a, b), 8)
        self.assertEqual(st.add_unsigned_short_int(a, b), 8)
        self.assertEqual(st.add_signed_int(a, b), 8)
        self.assertEqual(st.add_signed(a, b), 8)
        self.assertEqual(st.add_unsigned(a, b), 8)
        self.assertEqual(st.add_unsigned_int(a, b), 8)
        self.assertEqual(st.add_long_int(a, b), 8)
        self.assertEqual(st.add_signed_long(a, b), 8)
        self.assertEqual(st.add_signed_long_int(a, b), 8)
        self.assertEqual(st.add_unsigned_long(a, b), 8)
        self.assertEqual(st.add_unsigned_long_int(a, b), 8)
        self.assertEqual(st.add_long_long(a, b), 8)
        self.assertEqual(st.add_long_long_int(a, b), 8)
        self.assertEqual(st.add_signed_long_long(a, b), 8)
        self.assertEqual(st.add_signed_long_long_int(a, b), 8)
        self.assertEqual(st.add_unsigned_long_long(a, b), 8)
        self.assertEqual(st.add_unsigned_long_long_int(a, b), 8)

    #TODO: Solve long double problem
    # def test_standard_types_long_double(self):
    #     from tests.withdoxygen.argument_types.generated.sources import standard_types as st
    #     a = 5.0
    #     b = 3.0
    #     self.assertEqual(st.add_long_double(a, b), 8.0)

    def test_array_types_different(self):
        from tests.withdoxygen.argument_types.generated.sources import array_different as ad
        in_array = [1, 2, 3]
        out_array = []
        return_value = ad.reverse_array_diff(in_array, out_array)
        self.assertEqual(return_value, 0)
        self.assertEqual(out_array, [3, 2, 1])

    def test_array_types_double(self):
        from tests.withdoxygen.argument_types.generated.sources import array_types as at
        in_array = [1.0, 2.0, 3.0]
        out_array = []
        return_value = at.reverse_array_order_double(in_array, out_array)
        self.assertEqual(return_value, 0)
        self.assertEqual(out_array, [3.0, 2.0, 1.0])

    def test_array_types_long(self):
        from tests.withdoxygen.argument_types.generated.sources import array_types as at
        in_array = [1, 2, 3]
        out_array = []
        return_value = at.reverse_array_order_long(in_array, out_array)
        self.assertEqual(return_value, 0)
        self.assertEqual(out_array, [3, 2, 1])

    def test_array_types_float(self):
        from tests.withdoxygen.argument_types.generated.sources import array_types as at
        in_array = [1.0, 2.0, 3.0]
        out_array = []
        return_value = at.reverse_array_order_float(in_array, out_array)
        self.assertEqual(return_value, 0)
        self.assertEqual(out_array, [3.0, 2.0, 1.0])

    # TODO: Solve long double problem
    # def test_array_types_long_double(self):
    #     from tests.withdoxygen.argument_types.generated.sources import array_types as at
    #     in_array = [1.0, 2.0, 3.0]
    #     out_array = []
    #     return_value = at.reverse_array_order_long_double(in_array, out_array)
    #     self.assertEqual(return_value, 0)
    #     self.assertEqual(out_array, [3.0, 2.0, 1.0])

    def test_array_types_int_alike(self):
        from tests.withdoxygen.argument_types.generated.sources import array_types as at
        in_array = [1, 2, 3]
        out_array = [5, 6, 7]
        at.reverse_array_order_short(in_array, out_array)
        self.assertEqual(out_array, [3, 2, 1])
        out_array = [5, 6, 7]
        at.reverse_array_order_short_int(in_array, out_array)
        self.assertEqual(out_array, [3, 2, 1])
        out_array = [5, 6, 7]
        at.reverse_array_order_signed_short(in_array, out_array)
        self.assertEqual(out_array, [3, 2, 1])
        out_array = [5, 6, 7]
        at.reverse_array_order_signed_short_int(in_array, out_array)
        self.assertEqual(out_array, [3, 2, 1])
        out_array = [5, 6, 7]
        at.reverse_array_order_unsigned_short(in_array, out_array)
        self.assertEqual(out_array, [3, 2, 1])
        out_array = [5, 6, 7]
        at.reverse_array_order_unsigned_short_int(in_array, out_array)
        self.assertEqual(out_array, [3, 2, 1])
        out_array = [5, 6, 7]
        at.reverse_array_order_signed_int(in_array, out_array)
        self.assertEqual(out_array, [3, 2, 1])
        out_array = [5, 6, 7]
        at.reverse_array_order_signed(in_array, out_array)
        self.assertEqual(out_array, [3, 2, 1])
        out_array = [5, 6, 7]
        at.reverse_array_order_unsigned(in_array, out_array)
        self.assertEqual(out_array, [3, 2, 1])
        out_array = [5, 6, 7]
        at.reverse_array_order_unsigned_int(in_array, out_array)
        self.assertEqual(out_array, [3, 2, 1])
        out_array = [5, 6, 7]
        at.reverse_array_order_long_int(in_array, out_array)
        self.assertEqual(out_array, [3, 2, 1])
        out_array = [5, 6, 7]
        at.reverse_array_order_signed_long(in_array, out_array)
        self.assertEqual(out_array, [3, 2, 1])
        out_array = [5, 6, 7]
        at.reverse_array_order_signed_long_int(in_array, out_array)
        self.assertEqual(out_array, [3, 2, 1])
        out_array = [5, 6, 7]
        at.reverse_array_order_unsigned_long(in_array, out_array)
        self.assertEqual(out_array, [3, 2, 1])
        out_array = [5, 6, 7]
        at.reverse_array_order_unsigned_long_int(in_array, out_array)
        self.assertEqual(out_array, [3, 2, 1])
        out_array = [5, 6, 7]
        at.reverse_array_order_long_long(in_array, out_array)
        self.assertEqual(out_array, [3, 2, 1])
        out_array = [5, 6, 7]
        at.reverse_array_order_long_long_int(in_array, out_array)
        self.assertEqual(out_array, [3, 2, 1])
        out_array = [5, 6, 7]
        at.reverse_array_order_signed_long_long(in_array, out_array)
        self.assertEqual(out_array, [3, 2, 1])
        out_array = [5, 6, 7]
        at.reverse_array_order_signed_long_long_int(in_array, out_array)
        self.assertEqual(out_array, [3, 2, 1])
        out_array = [5, 6, 7]
        at.reverse_array_order_unsigned_long_long(in_array, out_array)
        self.assertEqual(out_array, [3, 2, 1])
        out_array = [5, 6, 7]
        at.reverse_array_order_unsigned_long_long_int(in_array, out_array)
        self.assertEqual(out_array, [3, 2, 1])