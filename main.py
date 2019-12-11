import argparse
import os
from BindingsGenerator import BindingsGenerator


def main():
    arg_parser = argparse.ArgumentParser(description='generate python bindings')
    optional_args = arg_parser._action_groups.pop()
    required_args = arg_parser.add_argument_group('required arguments')
    required_args.add_argument('package_name', action='store', help='name of package')
    required_args.add_argument('-f', '--files_path', action='append', required=True, help='path to C files',metavar='PATH')
    required_args.add_argument('-d', '--dest', action='store', required=True, help='path to destination directory',metavar='PATH')
    optional_args.add_argument('-v', '--verbose', action='store_true', help='output verbosity')
    optional_args.add_argument('-ef', '--export_functions', action='store',help='path to list of functions to be wrapped')
    optional_args.add_argument('-es', '--export_structs', action='store', help='path to list of structs to be wrapped')
    optional_args.add_argument('-ee', '--export_enums', action='store', help='path to list of enums to be wrapped')
    arg_parser._action_groups.append(optional_args)
    subparsers = arg_parser.add_subparsers(title='mode', dest='mode')

    compile_parser = subparsers.add_parser('compile', help='compile all given source files')
    compile_parser.add_argument('-i', '--include', action='append',help='path to external library header files to be included', metavar='PATH')
    compile_parser.add_argument('-l', '--library', action='append', help='name of dynamic library to be linked with',metavar='NAME')
    compile_parser.add_argument('-b', '--lib_dir', action='append', help='path to directory with dynamic libraries',metavar='PATH')
    compile_parser.add_argument('-e', '--extra_args', action='append', help='extra arguments passed to compiler',metavar='ARGS')

    shared_parser = subparsers.add_parser('shared',help='create bindings to dynamic/shared libraries (requires header files too)')

    args = arg_parser.parse_args()
    if args.mode is None:
        print('Error: No mode specified')
        return

    args.dest = os.path.abspath(args.dest)
    for i, path in enumerate(args.files_path):
        args.files_path[i] = os.path.abspath(path)
    if args.mode == 'compile':
        if args.include:
            for i, path in enumerate(args.include):
                args.include[i] = os.path.abspath(path)
        if args.lib_dir:
            for i, path in enumerate(args.lib_dir):
                args.lib_dir[i] = os.path.abspath(path)
    if not os.path.isdir(args.dest):
        os.mkdir(args.dest)
    os.chdir(args.dest)
    BindingsGenerator(args).generate_bindings()


if __name__ == '__main__':
    main()
