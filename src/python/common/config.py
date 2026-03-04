import logging
import os
import tomllib
from logging.handlers import RotatingFileHandler
from pathlib import Path
from sys import platform

from ..common.util import get_config_file

log_path = os.path.abspath(str(Path.home().absolute()) + "/Library/Application Support/dev.trietsch.xbar")

_config_sources: dict = {}  # module_name -> (config_filename, section_name)


def set_config_source(module: str, config_file: str, section: str):
    _config_sources[module] = (config_file, section)


def get_logger(name: str, loglevel=logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(name)
    filename = name.replace('python.', '').replace('.', '-')

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    file_handler = RotatingFileHandler(f"{log_path}/{filename}.log",
                                       mode='a', maxBytes=5 * 1024 * 1024,
                                       backupCount=2, encoding=None, delay=0)
    file_handler.setLevel(loglevel)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.level = loglevel

    return logger


class AppConfigReader(object):
    @staticmethod
    def read(module_name: str, config_file: str = None, section: str = None):
        if config_file is None or section is None:
            if module_name in _config_sources:
                config_file, section = _config_sources[module_name]
            else:
                config_file, section = module_name, "preferences"

        config_path = get_config_file(config_file)
        try:
            with open(config_path, 'rb') as f:
                raw = tomllib.load(f)
        except FileNotFoundError:
            raw = {}

        config = {"preferences": raw.get(section, {})}
        AppConfigReader._add_cache_path(config, module_name)
        return config

    @staticmethod
    def _add_cache_path(config: dict, filename: str):
        if platform == "linux" or platform == "linux2":
            cache_path = os.path.join(os.path.expanduser(os.getenv("XDG_CACHE_HOME", "~/.cache")), "dev.trietsch.xbar")
        else:
            cache_path = os.path.abspath(str(Path.home().absolute()) + "/Library/Caches/dev.trietsch.xbar")

        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        config.setdefault('common', {})
        config['common']['cache_path'] = f'{cache_path}/{filename}'