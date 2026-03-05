import logging
import os
import tomllib
from logging.handlers import RotatingFileHandler
from pathlib import Path
from sys import platform
from typing import Any, Tuple, Type

from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource

from ..common.util import get_config_file

log_path = os.path.abspath(str(Path.home().absolute()) + "/Library/Application Support/dev.trietsch.xbar")


def get_cache_path(filename: str) -> str:
    if platform in ("linux", "linux2"):
        cache_path = os.path.join(os.path.expanduser(os.getenv("XDG_CACHE_HOME", "~/.cache")), "dev.trietsch.xbar")
    else:
        cache_path = os.path.abspath(str(Path.home().absolute()) + "/Library/Caches/dev.trietsch.xbar")

    if not os.path.exists(cache_path):
        os.makedirs(cache_path)

    return f'{cache_path}/{filename}'


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


class TomlConfigSettingsSource(PydanticBaseSettingsSource):
    def __init__(self, settings_cls: Type[BaseSettings], config_file: str, section: str):
        super().__init__(settings_cls)
        config_path = get_config_file(config_file)
        try:
            with open(config_path, 'rb') as f:
                raw = tomllib.load(f)
            self._data = raw.get(section, {})
        except FileNotFoundError:
            self._data = {}

    def get_field_value(self, field: FieldInfo, field_name: str) -> Tuple[Any, str, bool]:
        return self._data.get(field_name), field_name, False

    def __call__(self) -> dict:
        return dict(self._data)