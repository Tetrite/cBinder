from SourceHeaderPair import get_sourceheader_pairs
from WrapperBuilder import build_wrapper, build_wrapper_without_doxygen
from WheelGenerator import WheelGenerator
from cffi import FFI
import os
import shutil


class BindingsGenerator:
    """
    Class used to generate bindings for each source file using cffi library

    Attributes
    ----------
    args : Namespace
        Arguments parsed by argparse's ArgumentParser
    """

    def __init__(self, args):
        self.args = args

    def generate_bindings(self):
        """
        Generates bindings and wrapper for each source file found at path given in arguments
        and builds wheel out of created package
        """

        paths = self.args.files_path
        verbosity = self.args.verbose

        pairs = get_sourceheader_pairs(paths)

        if verbosity:
            print(f'Copying needed files to destination directory')
        self._copy_needed_files_to_output_dir(pairs)
        for pair in pairs:
            if verbosity:
                print(f'Processing {pair.header_filepath.name} and {pair.source_filepath.name}')

            ffibuilder = FFI()
            outputname = pair.source_filepath.stem
            sourcename = pair.source_filepath.name
            ffibuilder.cdef(pair.declarations)
            ffibuilder.set_source('_' + outputname, "',".join(pair.includes), sources=[sourcename],
                                  include_dirs=self.args.include, libraries=self.args.library,
                                  library_dirs=self.args.lib_dir)
            ffibuilder.compile(verbose=verbosity)

            if verbosity:
                print('Generating wrapper script')
            if pair.declaration_data_list[0].doxygen == '':
                build_wrapper_without_doxygen(outputname, pair.declarations)
            else:
                build_wrapper(outputname, pair.declaration_data_list)

        if verbosity:
            print('Cleaning up output dir before wheel generation')
        # Cleaning up a directory causes imports to fail in some test cases under linux
        # self.cleanup_output_dir()
        WheelGenerator('.', os.path.basename(self.args.files_path)).generate_wheel()

    def _copy_needed_files_to_output_dir(self, pairs):
        for pair in pairs:
            if not os.path.isfile('./' + pair.header_filepath.name):
                shutil.copy2(str(pair.header_filepath), '.')
            if not os.path.isfile('./' + pair.source_filepath.name):
                shutil.copy2(str(pair.source_filepath), '.')

    def _cleanup_output_dir(self):
        for (root, dirs, files) in os.walk(self.args.dest, topdown=False):
            for file in files:
                if not (file.endswith('.py') or file.endswith('.pyd')):
                    os.remove(os.path.join(root, file))
            for dirname in dirs:
                os.rmdir(os.path.join(root, dirname))
