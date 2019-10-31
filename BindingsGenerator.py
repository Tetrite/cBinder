from SourceHeaderPair import *
from WrapperBuilder import *
from cffi import FFI
import os
import shutil


class BindingsGenerator:

    def __init__(self, args):
        self.args = args

    def generate_bindings(self):
        path = self.args.files_path
        verbosity = self.args.verbose

        pairs = get_sourceheader_pairs(path)
        for pair in pairs:
            if verbosity:
                print(f'Processing {pair.header_filepath.name} and {pair.source_filepath.name}')
            if not os.path.isfile('./' + pair.header_filepath.name):
                shutil.copy2(str(pair.header_filepath), '.')
            if not os.path.isfile('./' + pair.source_filepath.name):
                shutil.copy2(str(pair.source_filepath), '.')

            ffibuilder = FFI()
            outputname = pair.source_filepath.stem
            sourcename = pair.source_filepath.name
            ffibuilder.cdef(pair.declarations)
            ffibuilder.set_source('_' + outputname, "',".join(pair.includes), sources=[sourcename])
            ffibuilder.compile(verbose=verbosity)

            if verbosity:
                print('Generating wrapper script')
            build_wrapper(outputname, pair.declarations)

        # os.remove('./' + pair.source_filepath.name)
        # os.remove('./' + pair.header_filepath.name)
