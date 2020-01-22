import sys
import platform
import unittest
import pathlib
import os
import shutil


class ArgumentTypesTest(unittest.TestCase):

    @classmethod
    @unittest.skipIf(sys.platform in ("win32", "cygwin") or platform.architecture()[0] != "64bit", "Test linux x64 specific")
    def setUpClass(self):
        self.current_working_directory_path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
        # Dependecies (GSL):
        self.deps_path = self.current_working_directory_path / 'dependencies'
        os.makedirs(self.deps_path, exist_ok=True)
        os.chdir(self.deps_path)
        os.system(r'curl "http://cz.archive.ubuntu.com/ubuntu/pool/universe/g/gsl/libgsl-dev_2.5+dfsg-6_amd64.deb" --output libgsl-dev.deb')
        os.system(r'curl "http://cz.archive.ubuntu.com/ubuntu/pool/universe/g/gsl/libgsl23_2.5+dfsg-6_amd64.deb" --output libgsl.deb')
        os.system(r'curl "http://cz.archive.ubuntu.com/ubuntu/pool/universe/g/gsl/libgslcblas0_2.5+dfsg-6_amd64.deb" --output libgslcblas.deb')
        os.system(r'dpkg -x libgsl-dev.deb . && dpkg -x libgsl.deb . && dpkg -x libgslcblas.deb .')
        self.include_path = self.current_working_directory_path.joinpath('dependencies/usr/include')
        self.libs_main_dir = self.current_working_directory_path.joinpath('dependencies/usr/lib')
        self.libs_path = self.libs_main_dir.joinpath(os.listdir(self.libs_main_dir)[0])

        os.chdir(self.current_working_directory_path)
        self.libamtrack_path = self.current_working_directory_path.joinpath('library')
        if os.path.exists(str(self.libamtrack_path)):
            shutil.rmtree(self.libamtrack_path)
        os.system('git clone https://github.com/libamtrack/library.git')
        self.sources_path = self.current_working_directory_path.joinpath('library').joinpath('src')
        self.headers_path = self.current_working_directory_path.joinpath('library').joinpath('include')
        self.destination_path = self.current_working_directory_path.joinpath('generated')
        self.export_symbols_path = self.current_working_directory_path.joinpath('libamtrack_export_symbols_full.txt')
        if os.path.exists(str(self.destination_path)):
            shutil.rmtree(self.destination_path)
        os.makedirs(str(self.destination_path))
        os.chdir(self.current_working_directory_path)
        os.chdir("../..")
        os.system(r'python cBinder libamtrack '
                  + ' -f ' + str(self.sources_path)
                  + ' -f ' + str(self.headers_path)
                  + ' -d ' + str(self.destination_path)
                  + ' -es ' + str(self.export_symbols_path)
                  + ' -mono libAT'
                  + ' compile '
                  + ' -i ' + str(self.include_path)
                  + ' -i ' + str(self.headers_path)
                  + ' -b ' + str(self.libs_path)
                  + ' -l gsl'
                  + ' -l gslcblas'
                  + ' -l m')

        os.chdir(self.destination_path)

    def test_libamtrack_AT_lambda_Landau_Mode(self):
        from tests.libamtrack.generated.libamtrack import libAT
        a = libAT.AT_lambda_Landau_Mode()
        self.assertEqual(a, -0.2258)

    def test_libamtrack_AT_average_A_from_composition(self):
        from tests.libamtrack.generated.libamtrack import libAT
        average_A = []
        libAT.AT_average_A_from_composition([1, 16], [2. / 18., 16. / 18.], average_A)
        self.assertEqual(len(average_A), 1)
        self.assertAlmostEqual(average_A[0], 14.333333, places=6)

    def test_libamtrack_AT_material_name_from_number(self):
        from tests.libamtrack.generated.libamtrack import libAT
        name = []
        libAT.AT_particle_name_from_particle_no_single(222, name)
        self.assertEqual(len(name), 1)
        self.assertEqual('222??', name[0])

    def test_libamtrack_AT_Z_from_element_acronym_single(self):
        from tests.libamtrack.generated.libamtrack import libAT
        a = libAT.AT_Z_from_element_acronym_single('Ag')
        self.assertEqual(a, 47)

    def test_libamtrack_AT_Z_from_element_acronym(self):
        from tests.libamtrack.generated.libamtrack import libAT
        acronyms = ['Ag', 'Rh']
        numbers = []
        _ = libAT.AT_Z_from_element_acronym(acronyms, numbers)
        self.assertEqual(numbers[0], 47)
        self.assertEqual(numbers[1], 45)
