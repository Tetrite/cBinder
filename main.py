import argparse
import os
from BindingsGenerator import BindingsGenerator


def main():
	arg_parser = argparse.ArgumentParser('Generate python bindings')
	optional_args = arg_parser._action_groups.pop()
	required_args = arg_parser.add_argument_group('required arguments')
	required_args.add_argument('mode', choices=['compile', 'shared'], help='Mode of usage. Compile will compile all \
											given source files. Shared will create bindings to dynamic/shared libraries')
	required_args.add_argument('-f', '--files_path', action='append', required=True, help='Path to C files',
																									metavar='path')
	required_args.add_argument('-d', '--dest', action='store', required=True, help='Path to destination directory',
																									metavar='path')
	optional_args.add_argument('-i', '--include', action='append', help='Path to external library header \
																			files to be included', metavar='path')
	optional_args.add_argument('-l', '--library', action='append', help='Name of dynamic library to be linked with',
																									metavar='lib_name')
	optional_args.add_argument('-b', '--lib_dir', action='append', help='Path to directory with dynamic libraries',
																									metavar='path')
	optional_args.add_argument('-v', '--verbose', action='store_true', help='Verbosity of output')
	arg_parser._action_groups.append(optional_args)

	args = arg_parser.parse_args()
	args.dest = os.path.abspath(args.dest)
	for i, path in enumerate(args.files_path):
		args.files_path[i] = os.path.abspath(path)
	for i, path in enumerate(args.include):
		args.include[i] = os.path.abspath(path)
	for i, path in enumerate(args.lib_dir):
		args.lib_dir[i] = os.path.abspath(path)
	if not os.path.isdir(args.dest):
		os.mkdir(args.dest)
	os.chdir(args.dest)
	BindingsGenerator(args).generate_bindings()


if __name__ == '__main__':
	main()
