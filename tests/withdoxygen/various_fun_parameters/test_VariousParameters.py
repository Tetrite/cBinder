import unittest
import pathlib
import os

"""
    This test is designed to check if cBinder can generate wrapping functions
    that will infer array sizes from c function parameters and doxygen comments.

    Supported cases:

    I) Only one array as a function parameter (IN/OUT/BOTH)
       - wrapper will assume that argument passed to function has proper size

    II) More than one array as a parameter:

       1) Every array passed as a parameter is of the same size
          (defined as another function parameter or a constant)

             - wrapper will check if every IN or IN/OUT array has indeed the same size
             : if there are two or more arrays defined within doxygen comment to be of
             size n (passed as parameter) or x (constant), but the user passed as args
               two or more arrays that don't have the same size, the wrapper will raise
               an error: incorrect array sizes in arguments

             a) There are only OUT or IN/OUT arrays as parameters
                - the wrapper will check if these arrays have the same sizes : if not, error

             b) There are only IN or IN/OUT arrays as parameters:
                - the wrapper will check if these arrays have the same sizes : if not, error

             c) There are both IN and OUT arrays as parameters:
                 - firstly, the wrapper will check, if every IN or IN/OUT parameters indeed
                   have the same sizes

                 - secondly, it will assume, that the sizes of IN parameters is the correct size
                  and in case the OUT arrays are empty or of incorrect size, then whe wrapper
                   will show a WARNING, but initialize OUT array arguments with proper size

       2) There are two or more groups of arrays that do not share the same array size

          - the rules explained previously will apply to groups of arrays of the same declared size
"""

from tests._util.folder_clearing import clear_folder_contents


class VariousParametersTest(unittest.TestCase):

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

    def test_generate_bindings_to_function(self):
        #from tests.withdoxygen.various_fun_parameters.generated.sources import single_array as sa
        pass
