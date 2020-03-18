import itertools
import os
from collections import defaultdict
from datetime import datetime, timezone
from typing import Set, List

import timeago


def get_absolute_path_to_repo_file(repo_path):
    return os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/../../../' + repo_path)


def get_config_file(filename):
    return get_absolute_path_to_repo_file(f"config/{filename}-config.ini")


def epoch_ms_to_datetime(epoch_ms):
    return datetime.fromtimestamp(epoch_ms / 1000.0, tz=timezone.utc)


def abbreviate_string(s: str, max_characters: int):
    return s.replace("|", "-")[:max_characters] + "..." if len(s) > max_characters else s


def time_ago(date_time: datetime) -> str:
    return timeago.format(date_time.replace(tzinfo=timezone.utc).astimezone(tz=None).replace(tzinfo=None),
                          datetime.now())


def zip_list_of_dicts(shared_key: str, required_keys: Set[str], *iterables: List[dict]):
    result = defaultdict(dict)
    for dictionary in itertools.chain.from_iterable(iterables):
        result[dictionary[shared_key]].update(dictionary)

    for dict_name, dictionary in list(result.items()):
        contains_all_required_keys = required_keys.issubset(dictionary.keys())

        if not contains_all_required_keys:
            result.pop(dict_name)

    return result
