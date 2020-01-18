import unittest
import pathlib
import os

from tests._util.folder_clearing import clear_folder_contents


class MonolitTest(unittest.TestCase):

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
        os.system(r'python cBinder sources -mono mono -f ' + str(self.sources_path) + ' -d ' + str(self.destination_path) + ' compile')
        os.chdir(self.destination_path.joinpath('sources'))

    def test_all(self):

        # These cases are just copied from other tests, but here we compile into one module.

        from tests.simplecases.monolith.generated.sources import mono

        a = [0] * 5
        mono.func(a)
        self.assertEqual(a, [0.0, 1.0, 2.0, 3.0, 4.0])

        a = [2.0, 3.0, 4.0, 5.0, 6.0]
        i = mono.sum(4.0, a)
        self.assertEqual(i, 24.0)

        self.assertEqual(mono.SomeEnum.A.value, 0)
        self.assertEqual(mono.SomeEnum.B.value, 1)
        self.assertEqual(mono.SomeEnum.C.value, 123)

        self.assertEqual(mono.some_enum_to_int(mono.SomeEnum.A), 0)
        self.assertEqual(mono.some_enum_to_int(mono.SomeEnum.B), 1)
        self.assertEqual(mono.some_enum_to_int(mono.SomeEnum.C), 123)

        self.assertEqual(mono.UNNAMED_0, 0)
        self.assertEqual(mono.UNNAMED_1, 1)
        mono.print_unnamed_enum_value(mono.UNNAMED_0)

        s = mono.simple_struct()
        s.a = 123
        s.b = 123.0
        s.c = b'a'

        s0 = mono.simple_struct()
        s0.a = 123
        s0.b = 123.0
        s0.c = b'a'
        s1 = mono.simple_struct()
        s1.a = 123
        s1.b = 321.0
        s1.c = b'a'
        b = mono.get_b_sum([s0, s1])
        self.assertAlmostEqual(b, s0.b + s1.b, places=6)

        s = mono.simple_struct()
        s.a = 123
        s.b = 123.0
        s.c = b'a'
        b = mono.get_b(s)
        self.assertEqual(b, s.b)

        s = mono.simple_struct()
        s.a = 123
        s.b = 123.0
        s.c = b'a'
        b = mono.get_b_value(s)
        self.assertEqual(b, s.b)

        s = mono.simple_struct()
        s.a = 123
        s.b = 123.0
        s.c = b'a'
        mono.print(s)

        s = mono.simple_struct()
        s.a = 123
        s.b = 123.0
        s.c = b'a'
        mono.increment_b(s)
        self.assertAlmostEqual(s.b, 124.0, places=6)

        s = mono.make_simple_struct(123, 321.0, b'a')
        self.assertEqual(type(s), mono.simple_struct)
        self.assertEqual(s.a, 123)
        self.assertEqual(s.b, 321.0)
        self.assertEqual(s.c, b'a')

        sum = mono.add(1, 2)
        self.assertEqual(sum, 3)

        sum = mono.addF(1.1, 2.2)
        self.assertAlmostEqual(sum, 3.3, places=6)

        char = mono.printChar('a'.encode('ascii'))
        self.assertEqual(char, 97)
