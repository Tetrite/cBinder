from cffi import FFI
import argparse


def main():
	argparser = argparse.ArgumentParser()
	argparser.add_argument('source_file')
	argparser.add_argument('header_file')
	argparser.add_argument('definition')
	argparser.add_argument('output_name')
	args = argparser.parse_args()
	source = args.source_file
	header = args.header_file
	definition = args.definition
	output_name = args.output_name

	ffi = FFI()
	ffi.cdef(definition)
	includes = '#include "' + header + '"'
	ffi.set_source(output_name, includes, sources=[source])
	ffi.compile(verbose=True)


if __name__ == '__main__':
	main()
