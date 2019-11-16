def _check_if_every_in_array_is_not_empty(parameters, lines):
    array_in_params = [param.name for param in parameters if param.is_array and param.is_in]
    if array_in_params:
        lines.append('\tfor in_array_parameter in [' + ','.join(array_in_params) + ']:')
        lines.append('\t\tif not in_array_parameter:')
        lines.append('\t\t\traise ValueError(\"You passed an empty list as an IN parameter.\")')
