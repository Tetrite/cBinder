from HeaderFile import get_header_files
from SourceFile import get_source_files
from LibraryFile import get_shared_library_files
from WrapperBuilder import WrapperBuilder
from WheelGenerator import WheelGenerator
from MiniPreprocessing import preprocess_headers
from cffi import FFI
import os
import shutil


def _get_pairs_and_remainder(headers, sources):
    """
    Pairs header and source files if possible.
    Unpaired sources are returned separately.
    """
    pairs = []
    lone_sources = []

    for source in sources:
        for header in headers:
            if header.filepath.stem == source.filepath.stem:
                pairs.append((header, source))
                break
        else:
            lone_sources.append(source)

    return pairs, lone_sources


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

        headers = []
        sources = []
        for path in paths:
            headers.extend(get_header_files(path))
            if self.args.mode == 'compile':
                sources.extend(get_source_files(path))
            else:
                sources.extend(get_shared_library_files(path))

        preprocess_headers(headers)

        if verbosity:
            print(f'Copying needed files to destination directory')

        self._copy_needed_files_to_output_dir(headers)
        self._copy_needed_files_to_output_dir(sources)

        pairs, lone_sources = _get_pairs_and_remainder(headers, sources)

        if self.args.mode == 'compile':
            self._generate_bindings_for_pairs(pairs)
            self._generate_bindings_for_remainder(lone_sources)
        else:
            self._generate_bindings_for_dynamic_libraries(pairs)

        if verbosity:
            print('Cleaning up output dir before wheel generation')
        # Cleaning up a directory causes imports to fail in some test cases under linux
        # self.cleanup_output_dir()
        WheelGenerator('.', self.args.package_name).generate_wheel()

    def _generate_bindings_for_dynamic_libraries(self, pairs):
        """Generates bindings and wrapper for each pair of shared/dynamic library and header files"""
        verbosity = self.args.verbose

        if len(pairs) == 0:
            if verbosity:
                print(f'No header source pairs to process')
            return

        for header, source in pairs:
            name = header.filepath.stem
            WrapperBuilder(wrap_dynamic_lib=True).build_wrapper_for_header(name, header)

    def _generate_bindings_for_pairs(self, pairs):
        """Generates bindings and wrapper for each pair of source and header files"""

        verbosity = self.args.verbose

        if len(pairs) == 0:
            if verbosity:
                print(f'No header source pairs to process')
            return

        for header, source in pairs:
            name = header.filepath.stem

            if verbosity:
                print(f'Compiling and creating bindings for {name}')

            ffibuilder = FFI()
            all_declaration_strings = ' '.join(decl.declaration_string for decl in header.declarations)
            ffibuilder.cdef(all_declaration_strings)
            ffibuilder.set_source('_' + name, '\n'.join(source.includes), sources=[source.filepath],
                                  include_dirs=self.args.include, libraries=self.args.library,
                                  library_dirs=self.args.lib_dir, extra_compile_args=self.args.extra_args)
            ffibuilder.compile(verbose=verbosity)
            WrapperBuilder().build_wrapper_for_header(name, header)

    def _generate_bindings_for_remainder(self, sources):
        """Generates bindings and wrapper the remainder of source files"""

        verbosity = self.args.verbose

        if len(sources) == 0:
            if verbosity:
                print(f'No remainder source files to process')
            return

        for source in sources:
            name = source.filepath.stem
            if verbosity:
                print(f'Compiling and creating bindings for {name}')

            declarations = source.get_declarations()
            ffibuilder = FFI()
            ffibuilder.cdef(' '.join([x.declaration_string for x in declarations]))
            ffibuilder.set_source('_'+name, '\n'.join(source.includes), sources=[source.filepath],
                                  include_dirs=self.args.include, libraries=self.args.library,
                                  library_dirs=self.args.lib_dir)
            ffibuilder.compile(verbose=verbosity)
            WrapperBuilder().build_wrapper_for_declarations(name, declarations)

    def _copy_needed_files_to_output_dir(self, files):
        """Copies all header or source files to output directory given in arguments"""

        for file in files:
            if not os.path.isfile('./' + file.filepath.name):
                shutil.copy2(str(file.filepath), '.')

    def _cleanup_output_dir(self):
        """Cleans output directory leaving only .pyd and .py files"""

        for (root, dirs, files) in os.walk(self.args.dest, topdown=False):
            for file in files:
                if not (file.endswith('.py') or file.endswith('.pyd')):
                    os.remove(os.path.join(root, file))
            for dirname in dirs:
                os.rmdir(os.path.join(root, dirname))
