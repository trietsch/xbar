import os
from datetime import datetime, timezone

import timeago


def get_absolute_path_to_repo_file(repo_path):
    return os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/../../../' + repo_path)


def get_config_file(filename):
    return get_absolute_path_to_repo_file(f"config/{filename}-config.ini")


def epoch_ms_to_datetime(epoch_ms):
    return datetime.fromtimestamp(epoch_ms / 1000.0, tz=timezone.utc)


def abbreviate_string(s: str, max_characters: int):
    return s[:max_characters] + "..." if len(s) > max_characters else s


def time_ago(date_time: datetime) -> str:
    return timeago.format(date_time.replace(tzinfo=timezone.utc).astimezone(tz=None).replace(tzinfo=None),
                          datetime.now())
