import re
from HeaderFile import get_header_files


def preprocess_headers(path_to_directory):
    """Method used to substitute every #define NAME ??? in header files in order to parse doxygen
    comments correctly"""
    headers = get_header_files(path_to_directory)
    for header_file in headers:
        path_to_header = header_file.filepath
        defines_list = header_file.defines
        def_pairs = get_definitions_pairs(defines_list)
        preprocess_header(path_to_header, def_pairs)


def get_definitions_pairs(defines_list):
    def_pairs = {}
    for define_statement_string in defines_list:
        elems = re.split(" ", define_statement_string)
        if len(elems) > 3:  # When define statement is not a simple NAME <--> VALUE PAIR
            continue  # Do not preprocess this
        name = elems[1]
        value = elems[2]
        def_pairs[name] = value
    return def_pairs


def preprocess_header(path_to_header, def_pairs):
    # Read in the file
    with open(path_to_header, 'r') as file:
        filedata = file.read()

    for def_name, def_value in def_pairs.items():
        # Replace the target string
        full_define_statement = '#define ' + def_name + ' ' + def_value
        modified_define_statement = '#define ' + '__do_not_delete__' + ' ' + def_value
        filedata = filedata.replace(full_define_statement, modified_define_statement)
        filedata = filedata.replace(def_name, def_value)
        filedata = filedata.replace(modified_define_statement, full_define_statement)

    # Write the file out again
    with open(path_to_header, 'w') as file:
        file.write(filedata)
