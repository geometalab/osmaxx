import os


def get_file_only_path_list_in_directory(directory):
    """
    returns a list of the files (no directories!) contained in the specified directory, no recursion

    :param directory: directory to look into
    :return: path list to result file
    """
    file_paths = []
    for name in os.listdir(directory):
        result_file_path = os.path.join(directory, name)
        if os.path.isfile(result_file_path):
            file_paths.append(result_file_path)
    return file_paths
