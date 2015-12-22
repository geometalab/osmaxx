def select_keys(dictionary, key_list):
    return {key: dictionary[key] for key in key_list}


def are_all_keys_in(dictionary, keys):
    return all(key in dictionary for key in keys)
