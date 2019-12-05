import unittest
import os
import sys
import platform
import pathlib
import urllib.request
import shutil
import zipfile

from tests._util.folder_clearing import clear_folder_contents

class StaticDependencesOnLinux64(unittest.TestCase):
    @unittest.skipIf(sys.platform in ("win32", "cygwin") or platform.architecture()[0] != "64bit", "Test linux x64 specific")
    def test_generate_bindings_to_gsl_sf_bessel_J(self):
        self.current_working_directory_path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
        self.deps_path = self.current_working_directory_path / 'dependencies'
        os.makedirs(self.deps_path, exist_ok=True)
        os.chdir(self.deps_path)
        # get gsl - dependency of source
        os.system(r'curl "http://cz.archive.ubuntu.com/ubuntu/pool/universe/g/gsl/libgsl-dev_2.5+dfsg-6_amd64.deb" --output libgsl-dev.deb')
        os.system(r'dpkg -x libgsl-dev.deb .')
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
        os.system(r'python main.py sources -f ' + str(self.sources_path)
                  + ' -d ' + str(self.destination_path) + ' compile '
                  + ' -i ' + str(self.include_path)
                  + ' -b ' + str(self.libs_path) + ' -l gsl -l gslcblas -l m ')
        os.chdir(self.destination_path)
        os.environ['PATH'] = os.getcwd() + os.pathsep + os.environ['PATH']

        from tests.simplecases.externaldeps.generated.sources import example
        # c function return 0 if call was succesful
        self.assertEqual(example.print_gsl_sf_bessel_J0(1.7), 0)

class StaticDependencesOnWin64(unittest.TestCase):
    @unittest.skipUnless(sys.platform in ("win32", "cygwin") and platform.architecture()[0] == "64bit", "Test linux x64 specific")
    def test_generate_bindings_to_gsl_sf_bessel_J(self):
        self.current_working_directory_path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)))
        self.deps_path = self.current_working_directory_path / 'dependencies'
        os.makedirs(self.deps_path, exist_ok=True)
        os.chdir(self.deps_path)
        # get gsl - dependency of source
        zipped_lib_name = "gsl_2_2_msvc2017_64.zip"
        with urllib.request.urlopen(r'https://www.bruot.org/hp/media/files/libraries/' + zipped_lib_name) as response, open(zipped_lib_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        with zipfile.ZipFile(zipped_lib_name, 'r') as zip_ref:
            zip_ref.extractall('.')
        self.sources_path = self.current_working_directory_path.joinpath('sources/gsl_dependent')
        self.include_path = self.current_working_directory_path.joinpath('dependencies/msvc2017_64/include')
        self.libs_main_dir = self.current_working_directory_path.joinpath('dependencies/msvc2017_64/lib')
        # there is one thing in "libs_main_dir" directory containing libs
        # name of this dir can vary, hence below line
        self.libs_path = self.libs_main_dir.joinpath('gsl')
        self.destination_path = self.current_working_directory_path.joinpath('generated')
        if not os.path.exists(str(self.destination_path)):
            os.makedirs(str(self.destination_path))
        clear_folder_contents(self.destination_path)
        os.chdir("../../../..")
        print(r'python main.py sources -f ' + str(self.sources_path)
                  + ' -d ' + str(self.destination_path) + ' compile '
                  + ' -i ' + str(self.include_path)
                  + ' -b ' + str(self.libs_path) + ' -l gsl -l cblas ')
        os.system(r'python main.py sources -f ' + str(self.sources_path)
                  + ' -d ' + str(self.destination_path) + ' compile '
                  + ' -i ' + str(self.include_path)
                  + ' -b ' + str(self.libs_path) + ' -l gsl -l cblas ')
        os.chdir(self.destination_path)
        os.environ['PATH'] = os.getcwd() + os.pathsep + os.environ['PATH']

        from tests.simplecases.externaldeps.generated.sources import example
        # c function return 0 if call was succesful
        self.assertEqual(example.print_gsl_sf_bessel_J0(1.7), 0)
