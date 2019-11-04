import argparse
import os
from BindingsGenerator import *


def main():
	arg_parser = argparse.ArgumentParser('Generate python bindings')
	arg_parser.add_argument('-f', '--files_path', action='store', required=True, help='Path to C library', metavar='path')
	arg_parser.add_argument('-d', '--dest', action='store', required=True, help='Path to destination directory',
																									metavar='path')
	arg_parser.add_argument('-i', '--include', action='append', help='Path to external library to be include',
																									metavar='path')
	arg_parser.add_argument('-v', '--verbose', action='store_true', help='Verbosity output')
	args = arg_parser.parse_args()
	args.dest = os.path.abspath(args.dest)
	args.files_path = os.path.abspath(args.files_path)
	if not os.path.isdir(args.dest):
		os.mkdir(args.dest)
	os.chdir(args.dest)
	BindingsGenerator(args).generate_bindings()


if __name__ == '__main__':
	main()
