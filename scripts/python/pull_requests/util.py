import os


def get_config_file(filename):
    return get_absolute_bitbar_file_path(f"config/{filename}-config.ini")


def get_absolute_bitbar_file_path(repo_path):
    return os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/../../../' + repo_path)
