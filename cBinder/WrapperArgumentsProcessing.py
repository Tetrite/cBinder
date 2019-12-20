def _check_if_every_in_array_is_not_empty(writer, parameters):
    """
    This function checks, if every IN array argument is not empty.
    For example (part of doxygen comment):
        * @param[in]   in_order   sample array (array of size n)
    If a user provides an empty list as in_order array - there is no data to work with.
    """
    # First, get a list of array IN parameters:
    array_in_params = [param.name for param in parameters if param.is_array and param.is_in]
    # Then, for every such parameter, add a checking procedure to the wrapper:
    if array_in_params:
        writer.write_line('# Procedure to check if an IN array is empty:')
        with writer.write_for('in_array_argument', '[' + ','.join(array_in_params) + ']'):
            with writer.write_if('not in_array_argument'):
                writer.write_line('warnings.warn(\"You passed an empty list as an IN parameter.\")')


def _check_if_every_in_array_of_the_same_size_has_indeed_same_size(writer, parameters):
    """
    This function checks, if every IN array of the same declared size, is passed to a function properly
    For example, part of a doxygen comment:
        * @param[in]   in_arr1   sample array (array of size n)
        * @param[in]   in_arr2   sample array (array of size n)
    There are two IN arrays of size n. When a user passes lists of different sizes
    as these IN parameters, it is an incorrect use of the function.
    """
    # First, get the list of every array IN parameter
    array_in_params = [param for param in parameters if param.is_array and param.is_in]
    # Then, check if every such parameter has the same size
    _check_if_every_array_of_the_same_size_and_type_has_indeed_same_size(writer, array_in_params, True)


def _check_array_sizes_consistency_when_there_are_only_out_arrays(writer, parameters):
    """
    When function is defined in such way, that there are only OUT array parameters, there is no way
    to initialize these OUT parameters based on IN arrays of the same size. Therefore, it is necessary
    to check if a user passed these OUT arrays correctly.
    This function checks, if every OUT array of the same declared size, is passed with same size
    For example, part of a doxygen comment:
        * @param[out]   out_arr1   sample array (array of size n)
        * @param[out]   out_arr2   sample array (array of size n)
    There are two OUT arrays of size n. User should pass lists of the same size as these parameters.
    """
    # Check if there are only out array parameters:
    for param in parameters:
        if param.is_array and param.is_in:
            return
    # Get the list of every out parameter
    array_out_params = [param for param in parameters if param.is_array and param.is_out]
    # Then, check if every such parameter has the same size
    _check_if_every_array_of_the_same_size_and_type_has_indeed_same_size(writer, array_out_params, False)


def _check_if_every_array_of_the_same_size_and_type_has_indeed_same_size(writer, array_parameters, is_in_type):
    """
    This function applies analogous check for IN or OUT parameter type.
    It takes array_parameters list argument, and creates a wrapping script for IN or OUT type.
    It is verified, if every IN or OUT parameter of the same declared size is passed to
    a function with correct size.
    """
    type_str = 'IN' if is_in_type else 'OUT'
    # Get the list of parameters with the same size (list of ArraysSameSize objects)
    arrays_same_sizes_list = _get_arrays_of_same_size_list(array_parameters)

    for arr_same_size_object in arrays_same_sizes_list:
        # For every object inside this list, get its size and list of parameters
        size = arr_same_size_object.size
        param_list = arr_same_size_object.parameters_list
        if len(param_list) < 2:
            continue  # Perform a check only if there are 2 or more arrays of the same size
        # For one given size, add checking script to a wrapping function
        _add_checking_procedure_for_one_array_size(writer, size, arr_same_size_object.parameters_list, type_str)


def _add_checking_procedure_for_one_array_size(writer, size, arr_param_list, type_str):
    """
    This function, for a given parameters list, size, and string indicating type (IN/OUT),
    adds a checking script to a wrapping function
    """
    writer.write_line(
        '# Procedure to check if every ' + type_str + ' array of the same declared size, has indeed same size:')
    writer.write_line('# For arrays of declared size: ' + str(size))
    declared_arr_size_variable_name = 'declared_in_arr_param_size__' + str(size)
    writer.write_line(declared_arr_size_variable_name + ' = len(' + arr_param_list[0].name + ')')
    with writer.write_for('in_array_argument', '[' + ','.join([param.name for param in arr_param_list]) + ']'):
        with writer.write_if('len(in_array_argument) != ' + declared_arr_size_variable_name):
            writer.write_line('raise ValueError(\"You passed as parameters two or more lists ' +
                              'that should have the same size, with different sizes.\")')


def _initialize_out_arrays_if_necessary_and_check_sizes(writer, parameters):
    """
    (1)
    There is a possibility, that a function has multiple array parameters, both IN and OUT.
    When there is at least one IN array of a certain declared size, every OUT array of the same
    declared size can be initialized based on the length of the IN array (it is assumed that IN array
    is passed with correct size).
    This function, adds a correct initializing script to a wrapping function - when it is possible.
    For example, part of a doxygen comment:
        * @param[in]   in_arr   sample array (array of size n)
        * @param[out]   out_arr   sample array (array of size n)
    (2)
    This function also adds a check, when there is no IN parameter of a declared size, yet there are
    at least two OUT array parameters of this size - then, both of them should be passed with the same size.
    """
    # First, get every array parameter
    array_params = [param for param in parameters if param.is_array]
    # Get the list of parameters with the same size (list of ArraysSameSize objects)
    arrays_same_sizes_list = _get_arrays_of_same_size_list(array_params)

    for arr_same_size_obj in arrays_same_sizes_list:
        # Check, if there is at least one IN array parameter of a certain size
        arr_same_size_obj.check_for_decisive_in_param()

    # Get a list of OUT array parameters (not IN, not IN/OUT)
    array_out_params = [param for param in parameters if param.is_array and param.is_out and not param.is_in]
    # Local list variable to perform a size consistency check later, if there is no IN array parameter
    # to infer proper size from
    arrays_out_to_check_size_consistency = []
    for arr_out in array_out_params:
        same_arr_size_obj = _get_object_for_given_param(arrays_same_sizes_list, arr_out)
        decisive_parameter_name = same_arr_size_obj.decisive_param_name
        if decisive_parameter_name is not None:
            # If the initialization is possible, add a correct script
            _initialize_one_out_array(writer, arr_out, decisive_parameter_name)
        else:
            arrays_out_to_check_size_consistency.append(arr_out)
    if len(arrays_out_to_check_size_consistency) > 1:
        _check_if_every_array_of_the_same_size_and_type_has_indeed_same_size(writer,
                                                                             arrays_out_to_check_size_consistency,
                                                                             False)

def _initialize_non_array_out_parameters_if_necessary(writer, parameters):
    """
    When user wants to return a value from a C language function not through return statement
    but using OUT non-array parameter - that is, a pointer, the only option to actually
    return a value from a wrapping function is to treat this parameter as an array of size 1.
    (1)
    Firstly, because such parameters have to be processed as arrays of size 1, user has to
    pass it as array type in Python. Appropriate check is performed and error thrown in case
    incorrect argument is passed
    (2)
    If user passed an array type, but it does not have size 1, warning is raised and
    auto-initialization is done
    """
    # First, get every OUT parameter of size 1
    non_array_out_params = [param for param in parameters if param.is_out and param.sizes[0] == 1]
    # Add checking if every parameter is passed as an array
    for param in non_array_out_params:
        with writer.write_if('not isinstance(' + param.name + ', list)'):
            writer.write_line('out_param_err = \"You passed OUT parameter not as an array.\"')
            writer.write_line('raise ValueError(out_param_err)')
    # Then add checking procedure with initialization
    for param in non_array_out_params:
        with writer.write_if('len(' + param.name + ') != 1'):
            writer.write_line('out_param_auto_init = \"\\nWarning: OUT parameter (not an array)' +
                              ' was passed with incorrect size.\\n\" + \\')
            writer.write_line('\t\"Wrapper initializes it with size 1\"')
            writer.write_line('warnings.warn(out_param_auto_init)')
            writer.write_line(param.name + '.clear()')
            if 'char' in param.type:
                # Char type has to be initialized with string
                writer.write_line(param.name + ' += [\'\']')
            else:
                writer.write_line(param.name + ' += [0]')

def _initialize_one_out_array(writer, arr_out_param, decisive_param_name):
    """ This function adds an array size initialization script to a wrapping function """
    writer.write_line('# Procedure to check if OUT array ' + arr_out_param.name + ' is passed correctly:')
    with writer.write_if('len(' + arr_out_param.name + ') != len(' + decisive_param_name + ')'):
        writer.write_line('out_array_auto_init = \"\\nWarning: OUT array parameter ' + arr_out_param.name +
                          ' was passed with incorrect size.\\n\" + \\')
        writer.write_line('\t\"Wrapper initializes it with a correct value ' +
                          'based on an IN array parameter of the same declared size\"')
        writer.write_line('warnings.warn(out_array_auto_init)')
        writer.write_line(arr_out_param.name + '.clear()')
        writer.write_line(arr_out_param.name + ' += [0]*' + 'len(' + decisive_param_name + ')')


def _initialize_array_size_params_inside_wrapper(writer, parameters):
    """
    Every parameter in C language function, that indicates a certain size of an array
    is unnecessary - it is removed from Python wrapping function parameters list.
    Inside a wrapping function, it should be initialized based on array lengths.
    """
    # Get every array type parameter, that has a size definition not as a digit (size passed as function argument)
    array_params = [param for param in parameters if param.is_array and not str(param.sizes[0]).isdigit()]
    # Get the list of parameters with the same size (list of ArraysSameSize objects)
    arrays_same_sizes_list = _get_arrays_of_same_size_list(array_params)
    if len(arrays_same_sizes_list) < 1:
        return
    writer.write_line('# Array sizes variables initialization:')
    for arr_same_sizes_obj in arrays_same_sizes_list:
        size = 'p_' + str(arr_same_sizes_obj.size)
        first_available_param = arr_same_sizes_obj.parameters_list[0]
        writer.write_line(size + ' = len(' + first_available_param.name + ')')


class ArraysSameSize:
    """
    Class used to store information about arrays that have the same declared size

    Attributes
    ----------
    size :
        Size of an array
    parameters_list : list
        List of parameters that share the same declared size
    decisive_param_name: str
        Name of an IN array parameter of the same declared size (if it exists), that can be used
        to initialize OUT arrays properly. None - when there is no such IN array.
    """

    def __init__(self, size, parameters_list):
        self.size = size
        self.parameters_list = parameters_list
        self.decisive_param_name = None

    def check_for_decisive_in_param(self):
        """
        This method checks if there is an IN parameter of a certain size.
        If there is an IN parameter, there is a possibility to initialize OUT parameter
        of the same declared size, using len(in_param) expression
        """
        for param in self.parameters_list:
            if param.is_in:
                self.decisive_param_name = param.name


# Extra utility functions:
def _get_arrays_of_same_size_list(array_parameters):
    """ This method returns a list of ArraysSameSize objects, based on an parameter list """
    arrays_same_sizes_list = []
    for param in array_parameters:
        size = param.sizes[0]

        # If a declared size is not yet represented in a result list:
        if not _size_in_list(arrays_same_sizes_list, size):
            # Append an object with this size to a list
            arrays_same_sizes_list.append(ArraysSameSize(size, [param]))
        else:
            # In a result list, there is already an object that gathers every array parameter of the same size
            # Get this object
            arr_same_size_object = _get_arr_same_size_object(arrays_same_sizes_list, size)
            # Add another parameter to its parameter_list (as it is another parameter of the size)
            arr_same_size_object.parameters_list.append(param)
    return arrays_same_sizes_list


def _size_in_list(same_arr_size_list, size):
    """
    This function, for a given list of ArraysSameSize objects, checks
    if a certain size in inside that list
    """
    for elem in same_arr_size_list:
        if elem.size == size:
            return True
    return False


def _get_arr_same_size_object(same_arr_size_list, size):
    """
    This function, for a given list of ArraysSameSize objects, returns
    the object that represents arrays of the size passed as argument
    """
    for elem in same_arr_size_list:
        if elem.size == size:
            return elem
    return None


def _get_object_for_given_param(same_arr_size_list, param):
    """
    This function, for a given list of ArraysSameSize objects, returns
    the object has a certain param in its parameters list
    """
    for elem in same_arr_size_list:
        if param in elem.parameters_list:
            return elem
    return None
