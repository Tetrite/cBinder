import SourceHeaderPair as shp
import Scrapers as scr
import argparse
from cffi import FFI
import os
import shutil


def generate_bindings(args):
	path = args.files_path
	verbosity = args.verbose

	pairs = shp.get_sourceheader_pairs(path)
	ds = scr.DeclarationsScraper(None)
	ins = scr.IncludesScraper()
	for pair in pairs:
		if verbosity:
			print(f'Processing {pair.header_filepath.name} and {pair.source_filepath.name}')
		# TODO: check for existing file
		shutil.copy2(str(pair.header_filepath), '.')
		shutil.copy2(str(pair.source_filepath), '.')

		ffibuilder = FFI()
		declarations = ds.parse_and_return_decl(pair.header_filepath)
		includes = ins.extract_inludes(pair.source_filepath)
		outputname = pair.source_filepath.stem
		sourcename = pair.source_filepath.name
		ffibuilder.cdef(declarations)
		ffibuilder.set_source('_' + outputname, "',".join(includes), sources=[sourcename])
		ffibuilder.compile(verbose=verbosity)

		# os.remove('./' + pair.source_filepath.name)
		# os.remove('./' + pair.header_filepath.name)


def main():
	arg_parser = argparse.ArgumentParser('Generate python bindings')
	arg_parser.add_argument('-f', '--files_path', action='store', required=True, help='Path to C library')
	arg_parser.add_argument('-d', '--dest', action='store', required=True, help='Path to destination directory')
	arg_parser.add_argument('-v', '--verbose', action='store_true', help='Verbosity output')
	args = arg_parser.parse_args()
	if not os.path.isdir(args.dest):
		os.mkdir(args.dest)
	os.chdir(args.dest)
	generate_bindings(args)


if __name__ == '__main__':
	main()
