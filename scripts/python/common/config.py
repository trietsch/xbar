from configparser import ConfigParser
import os
from pathlib import Path

from ..pull_requests import get_config_file


class AppConfigReader(object):
    @staticmethod
    def read(filename: str):
        config_parser = ConfigParser()
        config_parser.read(get_config_file(filename))
        AppConfigReader._add_cache_path(config_parser, filename)

        return config_parser._sections

    @staticmethod
    def _add_cache_path(config_parser: ConfigParser, filename: str):
        config_parser.add_section("common")
        config_parser.set("common", "cache_path", f'{os.path.abspath(str(Path.home().absolute()) + "/Library/Caches/nl.robintrietsch.bitbar")}/{filename}.bitbarcache')
