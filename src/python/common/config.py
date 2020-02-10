import logging
import os
from configparser import ConfigParser
from logging.handlers import RotatingFileHandler
from pathlib import Path

from ..common.util import get_config_file

log_path = os.path.abspath(str(Path.home().absolute()) + "/Library/Application Support/nl.robintrietsch.bitbar")


def get_logger(name: str, filename: str, loglevel=logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(name)

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
    def read(filename: str):
        config_parser = ConfigParser()
        config_parser.read(get_config_file(filename))
        AppConfigReader._add_cache_path(config_parser, filename)

        return config_parser._sections

    @staticmethod
    def _add_cache_path(config_parser: ConfigParser, filename: str):
        cache_path = os.path.abspath(str(Path.home().absolute()) + "/Library/Caches/nl.robintrietsch.bitbar")

        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        config_parser.add_section("common")
        config_parser.set("common", "cache_path", f'{cache_path}/{filename}')
