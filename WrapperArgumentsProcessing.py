def _initialize_array_size_params_inside_wrapper(parameters, lines):
    array_params = [param for param in parameters if param.is_array and not str(param.sizes[0]).isdigit()]
    arrays_same_sizes_list = _get_arrays_of_same_size_list(array_params)
    lines.append('\t# Array sizes variables initialization:')
    for arr_same_sizes_obj in arrays_same_sizes_list:
        size = str(arr_same_sizes_obj.size)
        first_available_param = arr_same_sizes_obj.parameters_list[0]
        lines.append('\t' + size + ' = len(' + first_available_param.name + ')')


def _initialize_out_arrays_if_necessary(parameters, lines):
    array_params = [param for param in parameters if param.is_array]
    arrays_same_sizes_list = _get_arrays_of_same_size_list(array_params)
    for arr_same_size_obj in arrays_same_sizes_list:
        arr_same_size_obj.check_for_decisive_in_param()

    array_out_params = [param for param in parameters if param.is_array and param.is_out and not param.is_in]
    for arr_out in array_out_params:
        same_arr_size_obj = _get_object_for_given_param(arrays_same_sizes_list, arr_out)
        decisive_parameter_name = same_arr_size_obj.decisive_param_name
        if decisive_parameter_name is not None:
            _initialize_out_array_if_necessary(lines, arr_out, decisive_parameter_name)


def _initialize_out_array_if_necessary(lines, arr_out_param, decisive_param_name):
    lines.append('\t# Procedure to check if OUT array ' + arr_out_param.name + ' is passed correctly:')
    lines.append('\tif len(' + arr_out_param.name + ') != len(' + decisive_param_name + '):')
    lines.append('\t\twarnings.warn(\"Warning: OUT array parameter ' + arr_out_param.name +
                 ' was passed with incorrect size. Wrapper initializes it with a correct value ' +
                 'based on an IN array parameter of the same declared size' + '\")')
    lines.append('\t\t' + arr_out_param.name + ' = list(range(len(' + decisive_param_name + ')))')


def _check_if_every_in_array_is_not_empty(parameters, lines):
    array_in_params = [param.name for param in parameters if param.is_array and param.is_in]
    if array_in_params:
        lines.append('\t# Procedure to check if an IN array is empty:')
        lines.append('\tfor in_array_argument in [' + ','.join(array_in_params) + ']:')
        lines.append('\t\tif not in_array_argument:')
        lines.append('\t\t\traise ValueError(\"You passed an empty list as an IN parameter.\")')


def _check_if_every_in_array_of_the_same_size_has_indeed_same_size(parameters, lines):
    array_in_params = [param for param in parameters if param.is_array and param.is_in]
    _check_if_every_array_of_the_same_size_and_type_has_indeed_same_size(array_in_params, lines, True)


def _check_array_sizes_consistency_when_there_are_only_out_arrays(parameters, lines):
    # Check if there are only out array parameters:
    for param in parameters:
        if param.is_array and param.is_in:
            return
    array_out_params = [param for param in parameters if param.is_array and param.is_out]
    _check_if_every_array_of_the_same_size_and_type_has_indeed_same_size(array_out_params, lines, False)


def _check_if_every_array_of_the_same_size_and_type_has_indeed_same_size(array_parameters, lines, is_in_type):
    type_str = 'IN' if is_in_type else 'OUT'
    # Variable used to store all possible array sizes inside a function
    arrays_same_sizes_list = _get_arrays_of_same_size_list(array_parameters)

    for arr_same_size_object in arrays_same_sizes_list:
        size = arr_same_size_object.size
        param_list = arr_same_size_object.parameters_list
        if len(param_list) < 2:
            continue
        _add_checking_procedure_for_one_array_size(lines, size, arr_same_size_object.parameters_list, type_str)


def _size_in_list(same_arr_size_list, size):
    for elem in same_arr_size_list:
        if elem.size == size:
            return True
    return False


def _get_arr_same_size_object(same_arr_size_list, size):
    for elem in same_arr_size_list:
        if elem.size == size:
            return elem
    return None


def _get_object_for_given_param(same_arr_size_list, param):
    for elem in same_arr_size_list:
        if elem.object_contains_param(param):
            return elem
    return None


def _get_arrays_of_same_size_list(array_parameters):
    arrays_same_sizes_list = []
    for param in array_parameters:
        size = param.sizes[0]
        if not _size_in_list(arrays_same_sizes_list, size):
            arrays_same_sizes_list.append(ArraysSameSize(size, [param]))
        else:
            arr_same_size_object = _get_arr_same_size_object(arrays_same_sizes_list, size)
            arr_same_size_object.parameters_list.append(param)
    return arrays_same_sizes_list


def _add_checking_procedure_for_one_array_size(lines, size, arr_param_list, type):
    lines.append('\t# Procedure to check if every ' + type + ' array of the same declared size, has indeed same size:')
    lines.append('\t# For arrays of declared size: ' + str(size))
    declared_arr_size_variable_name = 'declared_in_arr_param_size__' + str(size)
    lines.append('\t' + declared_arr_size_variable_name + ' = len(' + arr_param_list[0].name + ')')
    lines.append('\tfor in_array_argument in [' + ','.join([param.name for param in arr_param_list]) + ']:')
    lines.append('\t\tif (len(in_array_argument) != ' + declared_arr_size_variable_name + '):')
    lines.append('\t\t\traise ValueError(\"You passed as parameters two or more lists ' +
                 'that should have the same size, with different sizes.\")')


class ArraysSameSize:
    """
    Class used to store information about arrays that have the same declared size

    Attributes
    ----------
    size :
        Size of an array
    parameters_list : list
        List of parameters that share the same declared size
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

    def object_contains_param(self, parameter):
        return parameter in self.parameters_list
