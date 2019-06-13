from cffi import FFI
import argparse


def main():
	argparser = argparse.ArgumentParser()
	argparser.add_argument('source_file')
	argparser.add_argument('header_file')
	argparser.add_argument('output_name')
	args = argparser.parse_args()
	source = args.source_file
	header = args.header_file
	output_name = args.output_name

	with open(header) as f:
		lines = f.readlines()

	lines = [x.strip() for x in lines]
	lines = list(filter(lambda x: x[0] != '#', lines))
	definition = ""
	for l in lines:
		definition = definition + l
	ffi = FFI()
	ffi.cdef(definition)
	includes = '#include "' + header + '"'
	ffi.set_source(output_name, includes, sources=[source])
	ffi.compile(verbose=True)


if __name__ == '__main__':
	main()
