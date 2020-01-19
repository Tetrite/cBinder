import unittest
import os
import sys
import platform
import pathlib

from tests._util.folder_clearing import clear_folder_contents


class DynamicDependencesOnLinux64(unittest.TestCase):

    @unittest.skipIf(sys.platform in ("win32", "cygwin") or platform.architecture()[0] != "64bit", "Test linux x64 specific")
    def test_generate_bindings_to_gsl_sf_bessel_J(self):
        self.current_working_directory_path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
        self.deps_path = self.current_working_directory_path / 'dependencies'
        os.makedirs(self.deps_path, exist_ok=True)
        os.chdir(self.deps_path)
        # get gsl - dependency of source
        os.system(r'curl "http://cz.archive.ubuntu.com/ubuntu/pool/universe/g/gsl/libgsl-dev_2.5+dfsg-6_amd64.deb" --output libgsl-dev.deb')
        os.system(r'curl "http://cz.archive.ubuntu.com/ubuntu/pool/universe/g/gsl/libgsl23_2.5+dfsg-6_amd64.deb" --output libgsl.deb')
        os.system(r'curl "http://cz.archive.ubuntu.com/ubuntu/pool/universe/g/gsl/libgslcblas0_2.5+dfsg-6_amd64.deb" --output libgslcblas.deb')
        os.system(r'dpkg -x libgsl-dev.deb . && dpkg -x libgsl.deb . && dpkg -x libgslcblas.deb .')
        self.sources_path = self.current_working_directory_path.joinpath('sources/gsl_dependent')
        self.include_path = self.current_working_directory_path.joinpath('dependencies/usr/include')
        self.libs_main_dir = self.current_working_directory_path.joinpath('dependencies/usr/lib')
        # there is one thing in "libs_main_dir" directory containing libs
        # name of this dir can vary, hence below line
        self.libs_path = self.libs_main_dir.joinpath(os.listdir(self.libs_main_dir)[0])
        self.destination_path = self.current_working_directory_path.joinpath('generated')
        if not os.path.exists(str(self.destination_path)):
            os.makedirs(str(self.destination_path))
        clear_folder_contents(self.destination_path)
        os.chdir("../../../..")
        os.system(r'python cBinder sources -f ' + str(self.sources_path) + ' -d ' + str(self.destination_path) + ' compile '
                  + ' -i ' + str(self.include_path) + ' -b ' + str(self.libs_path) + ' -l gsl -l gslcblas -l m ')
        os.chdir(self.destination_path)
        os.environ['PATH'] = os.getcwd() + os.pathsep + os.environ['PATH']

        from tests.simplecases.externaldeps.generated.sources import example
        # c function return 0 if call was successful
        self.assertEqual(example.print_gsl_sf_bessel_J0(1.7), 0)


class DynamicDependencesOnWin64(unittest.TestCase):

    @unittest.skipUnless(sys.platform in ("win32", "cygwin") and platform.architecture()[0] == "64bit", "Test windows x64 specific")
    def test_generate_bindings_to_function_return1(self):
        self.current_working_directory_path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
        self.deps_path = self.current_working_directory_path / 'dependencies'
        os.makedirs(self.deps_path, exist_ok=True)
        os.chdir(self.deps_path)
        # dynamic lib should already be there - included in repo
        self.sources_path = self.current_working_directory_path.joinpath('sources/return_n_dependent')
        self.include_path = self.current_working_directory_path.joinpath('dependencies')
        self.libs_path = self.current_working_directory_path.joinpath('dependencies')
        self.destination_path = self.current_working_directory_path.joinpath('generated/example2')
        if not os.path.exists(str(self.destination_path)):
            os.makedirs(str(self.destination_path))
        clear_folder_contents(self.destination_path)
        os.chdir("../../../..")
        print(r'python cBinder sources2 -f ' + str(self.sources_path)
              + ' -d ' + str(self.destination_path) + ' compile '
              + ' -i ' + str(self.include_path)
              + ' -b ' + str(self.libs_path) + ' -l return_n ')
        os.system(r'python cBinder sources2 -f ' + str(self.sources_path)
                  + ' -d ' + str(self.destination_path) + ' compile '
                  + ' -i ' + str(self.include_path)
                  + ' -b ' + str(self.libs_path) + ' -l return_n ')
        os.chdir(self.destination_path)
        os.environ['PATH'] = os.getcwd() + os.pathsep + os.environ['PATH']

        from tests.simplecases.externaldeps.generated.example2.sources2 import example2
        # c function return 0 if call was succesful
        self.assertEqual(example2.print_and_return_n(1), 1)
