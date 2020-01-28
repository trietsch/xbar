import os


def get_absolute_path_to_repo_file(repo_path):
    return os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/../../../' + repo_path)


def get_config_file(filename):
    return get_absolute_path_to_repo_file(f"config/{filename}-config.ini")
