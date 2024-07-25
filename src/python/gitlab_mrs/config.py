from distutils.util import strtobool
from typing import Dict

from .constants import GitlabMrsConstants
from ..common.config import AppConfigReader
from ..common.icons import Icon, Icons
from ..pull_requests import PullRequestSort, PullRequestStatus


class GitlabMrsConfig(object):
    _config = AppConfigReader.read(GitlabMrsConstants.MODULE)

    GITLAB_HOST = _config["preferences"].get("gitlab_host", "https://gitlab.com")
    PRIVATE_TOKEN = _config["preferences"]["private_token"]  # no default, crash
    SORT_ON = PullRequestSort[_config["preferences"]["sort_on"].upper()]
    ABBREVIATION_CHARACTERS = int(_config["preferences"].get("abbreviation_characters", "30"))
    OMIT_REVIEWED_AND_APPROVED = strtobool(_config["preferences"].get("omit_reviewed_and_approved", "False"))
    OMIT_DRAFT = strtobool(_config["preferences"].get("omit_draft", "True"))
    NOTIFICATIONS_ENABLED = strtobool(_config["preferences"].get("notifications_enabled", "False"))
    GROUP_NAME = _config["preferences"]["group_name"]
    OTHER_GROUPS_MRS_FOR_GROUP_MEMBERS = set(_config["preferences"].get("show_other_mrs_for_group_owners_in_these_groups", "").split(","))
    EXCLUDE_MRS_WITH_LABELS = set(_config["preferences"].get("exclude_mrs_with_labels", "").split(","))

    CACHE_FILE = _config["common"]["cache_path"]


class GitlabMrsIcons(object):
    GITLAB_LOGO = Icon(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAOCAYAAAAmL5yKAAAAAXNSR0IArs4c6QAAAi5JREFUKBV1Us9rE1EQnpm3+bFpatMG0tJE6o9YF+JJaIoKRbOlh5YcPBvx7kE8qBQvXvwH/Ac86aV/gBTBm17sWSVNLUYrWg+i2Cab7L43zm6zREIdeDvz3vfN92ZmH8DA9lwn/9l1Hsb7//l2zVnfdy9MxzjFATNVEej+l9p8MT4b9buSSIj3uqwvx9hQgGB13KKcAVWLwVGv2CxlLcojwmqMRQLvrlaywLwSMAMQ1GNw1BNxXQsFGJY/Lp+ZCPFIYMwPFiQodwMDYGDpQ9XJjya3FssnjIaaJxwLcI48+1LIscLPVJXXrJ9MvmaW8qYzB/i0fc35hpG8XCi6dg4K6TEzK3S2FKKeMmvwGjaRN0q26dtb9AkrZh8AFUD/F8HvPQIRiyzsbKJoIDlpgLWUXZBCT3GLUsmLVtBLLxJhRZeE+0cmcQhItuGAELSGSIIIGG0DJpB9RjRKwlF0LvD0FWJDHbnpq7KFe1ZELGCSJhMZFjWpV1ZSYpWQZMFCjspEut8t4gNK3tp+29fosg+bKidSp6VywdPj4biPLJXlo3bmpMNJRPb5FRrtYqP5JhpT+maz2fZ7102fH0l/XSoipGwGknmEKy0V0Kw8sxnoGR8eY7JTx8bO+1A+qmVwUeT8Z+UVAnpCu+j82BJY5lZYYOQytAzyXevG9ot/+YMfNTxKNHZeegpdKJrnWXnx2RlAc5I3PBW4o8nDrGMiGR4drs/f7jw4f0diaeR4+wuHx8azyo51NwAAAABJRU5ErkJggg==")

    MERGE_REQUEST = Icons.PULL_REQUEST

    PR_STATUSES: Dict[PullRequestStatus, Icon] = {
        PullRequestStatus.UNAPPROVED: Icons.GREY_CIRCLE,
        PullRequestStatus.NEEDS_WORK: Icons.ORANGE_CIRCLE,
        PullRequestStatus.APPROVED: Icons.GREEN_CIRCLE,
        PullRequestStatus.APPROVED_WITH_SUGGESTIONS: Icons.GREEN_CIRCLE
    }
