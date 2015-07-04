def remove_none_values(dictionary):
    return_dictionary = {}
    for key, value in dictionary.items():
        if value is not None:
            return_dictionary[key] = value

    return return_dictionary
