from HeaderFile import get_header_files
from SourceFile import get_source_files
from LibraryFile import get_shared_library_files
from WrapperBuilder import WrapperBuilder
from WheelGenerator import WheelGenerator
from MiniPreprocessing import preprocess_headers
from LibPaths import LibPaths
import pathlib
from cffi import FFI
import os
import sys
import shutil
import re

def get_soname_path(libpath, lib_dir):
    """
    if name contains more than one number after .so (.so.25.0.0)
    it should be shortened (.so.25)
    """
    if sys.platform in ("win32", "cygwin"):
        return libpath
    so_index = libpath.find(".so")
    libpath = libpath[:libpath.find(".", so_index + 4)]
    return os.path.join(lib_dir, libpath)

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

        if verbosity:
            print(f'Copying needed files to destination directory')

        self._copy_needed_files_to_output_dir(headers)
        self._copy_needed_files_to_output_dir(sources)

        self._handle_passed_dynamic_libraries()

        preprocess_headers('.')
        headers = get_header_files('.')

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

        """ Attention: temporary measure.
            To properly compile sources that have internal dependencies,
            (for example: including function defined in other .c file)
            it is necessary to pass all needed sources for a given .c file
            to ffibuilder.set_source(.... sources=[?]) instead of just itself.
            It is ineffective though.
         """
        sources_combined = []
        for header, source in pairs:
            sources_combined.append(source.relativepath)
        """ Temporary measure - end """

        for header, source in pairs:
            name = header.filepath.stem

            if verbosity:
                print(f'Compiling and creating bindings for {name}')

            ffibuilder = FFI()
            all_declaration_strings = ' '.join(decl.declaration_string for decl in header.structs)
            all_declaration_strings += ' '.join(decl.declaration_string for decl in header.functions)
            ffibuilder.cdef(header.read())
            win_args = [f'/LIBPATH:./{self.args.package_name}/lib/']
            linux_args = ["-Wl,-rpath=$ORIGIN"]
            extra_link_args = win_args if sys.platform in ("win32", "cygwin") else linux_args
            libs_path = pathlib.Path(f"./{self.args.package_name}/lib")
            libraries = []
            if sys.platform in ("win32", "cygwin") and self.args.library:
                libraries = list(str(libs_path / (libname + ".lib")) for libname in self.args.library)
            ffibuilder.set_source('_' + name, '\n'.join(source.includes), sources=sources_combined,
                                  include_dirs=self.args.include, libraries=self.args.library,
                                  library_dirs=self.args.lib_dir,
                                  extra_link_args=extra_link_args)
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

            functions = source.functions
            structs = source.structs
            ffibuilder = FFI()
            all_declaration_strings = ' '.join(decl.declaration_string for decl in structs)
            all_declaration_strings += ' '.join(decl.declaration_string for decl in functions)
            ffibuilder.cdef(all_declaration_strings)
            win_args = [f'/LIBPATH ../{self.args.package_name}/lib/']
            linux_args = ["-Wl,-rpath=$ORIGIN"]
            extra_link_args = win_args if sys.platform in ("win32", "cygwin") else linux_args
            ffibuilder.set_source('_' + name, '\n'.join(source.includes), sources=[source.filepath],
                                  include_dirs=self.args.include, libraries=self.args.library,
                                  library_dirs=self.args.lib_dir, extra_link_args=extra_link_args)
            ffibuilder.compile(verbose=verbosity)
            WrapperBuilder().build_wrapper_for_structs_and_functions(name, structs, functions)

    def _copy_needed_files_to_output_dir(self, files):
        """Copies all header or source files to output directory given in arguments"""

        for file in files:
            if not os.path.isfile('./' + file.filepath.name):
                shutil.copy2(str(file.filepath), '.')


    def _handle_passed_dynamic_libraries(self):
        lib_dirs = getattr(self.args, "lib_dir", None)
        if not lib_dirs or not self.args.library:
            return
        package_dir = os.path.join(self.args.dest, self.args.package_name)
        package_lib_dir = os.path.join(package_dir, 'lib')
        os.makedirs(package_lib_dir, exist_ok=True)

        if sys.platform in ("win32", "cygwin"):
            exts = (".dll", ".lib")
            prefix = ""
        else:
            exts = (".so", ".a")
            prefix = "lib"
        libnames = set(self.args.library)

        lib_path_dict = {libname:LibPaths() for libname in libnames}
        for lib_dir in lib_dirs:
            dir_content = os.listdir(lib_dir)
            for libname in libnames:
                for ext in exts:
                    fullname = prefix + libname + ext
                    if fullname in dir_content:
                        libpath = os.path.join(lib_dir, fullname)
                        libpath = os.readlink(libpath) if os.path.islink(libpath) else libpath
                        libpath = get_soname_path(libpath, lib_dir)
                        lib_path_dict[libname].set_path(libpath)
        for libpath in lib_path_dict.values():
            if libpath.dynamic_path:
                shutil.copy2(libpath.dynamic_path, package_lib_dir)

        for libname, libpath in lib_path_dict.items():
            # print missing
            if not libpath:
                print(f"Library not found: {libname}")
        print("Assuming libs not found are system's")

    def _cleanup_output_dir(self):
        """Cleans output directory leaving only .pyd and .py files"""

        for (root, dirs, files) in os.walk(self.args.dest, topdown=False):
            for file in files:
                if not (file.endswith('.py') or file.endswith('.pyd')):
                    os.remove(os.path.join(root, file))
            for dirname in dirs:
                os.rmdir(os.path.join(root, dirname))
