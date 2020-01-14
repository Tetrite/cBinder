def preprocess_headers(headers):
    """Method used to substitute every #define NAME ??? in header files in order to parse doxygen
    comments correctly"""
    for header_file in headers:
        path_to_header = header_file.filepath
        defines_list = header_file.defines
        def_tuples = get_definitions_tuples(defines_list)
        preprocess_header(path_to_header, def_tuples)


def get_definitions_tuples(defines_list):
    def_tuples = []
    for define_statement_string in defines_list:
        elems = define_statement_string.split()
        if len(elems) != 3:  # When define statement is not a simple NAME <--> VALUE PAIR
            continue  # Do not preprocess this
        name = elems[1]
        value = elems[2]
        def_tuples.append((name, value, define_statement_string))
    return def_tuples


def preprocess_header(path_to_header, def_tuples):
    # Read in the file
    with open(path_to_header, 'r') as file:
        filedata = file.read()

    # it's important to start from the longest substitution
    def_tuples.sort(key=lambda def_tuple: len(def_tuple[1]), reverse=True)

    for idx, def_tuple in enumerate(def_tuples):
        def_name, def_value, full_define_statement = def_tuple
        modified_define_statement = f'#define __do_not_delete__{idx} ' + def_value
        filedata = filedata.replace(full_define_statement, modified_define_statement)

    for def_name, def_value, full_define_statement in def_tuples:
        # Replace the target string
        filedata = filedata.replace(def_name, def_value)

    for idx, def_tuple in enumerate(def_tuples):
        def_name, def_value, full_define_statement = def_tuple
        modified_define_statement = f'#define __do_not_delete__{idx} ' + def_value
        filedata = filedata.replace(modified_define_statement, full_define_statement)

    # Write the file out again
    with open(path_to_header, 'w') as file:
        file.write(filedata)
