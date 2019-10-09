import SourceHeaderPair as shp
import Scrapers as scr
from cffi import FFI
import os


def main():
	path = 'C:\\engineerka\\cBinder\\test_library'
	pairs = shp.get_sourceheader_pairs(path)
	ds = scr.DeclarationsScraper(None)
	ins = scr.IncludesScraper()
	for pair in pairs:
		ffibuilder = FFI()
		declarations = ds.parse_and_return_decl(pair.header_filepath)
		includes = ins.extract_inludes(pair.source_filepath)
		outputname = pair.source_filepath.stem
		sourcename = pair.source_filepath.name
		ffibuilder.cdef(declarations)
		ffibuilder.set_source('_'+outputname, "',".join(includes), sources=[sourcename])
		ffibuilder.compile(verbose=True)


if __name__ == '__main__':
	os.chdir('./test_library')
	main()
