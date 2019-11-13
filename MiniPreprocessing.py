import re


def preprocess_headers(headers):
    """Method used to substitute every #define NAME ??? in header files in order to parse doxygen
    comments correctly"""
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
        filedata = filedata.replace('#define ' + def_name + ' ' + def_value, '')
        filedata = filedata.replace(def_name, def_value)

    # Write the file out again
    with open(path_to_header, 'w') as file:
        file.write(filedata)
