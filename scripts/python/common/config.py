import os
from configparser import ConfigParser
from pathlib import Path

from ..common.util import get_config_file


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
