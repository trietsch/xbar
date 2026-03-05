from typing import Dict, Set

from pydantic import computed_field, field_validator
from pydantic_settings import BaseSettings

from .constants import GitlabMrsConstants
from ..common.config import TomlConfigSettingsSource, get_cache_path
from ..common.icons import Icon, Icons
from ..pull_requests import PullRequestSort, PullRequestStatus


class GitlabMrsSettings(BaseSettings):
    gitlab_host: str = "https://gitlab.com"
    private_token: str
    group_name: str
    sort_on: PullRequestSort = PullRequestSort.ACTIVITY
    abbreviation_characters: int = 30
    omit_reviewed_and_approved: bool = False
    omit_draft: bool = True
    notifications_enabled: bool = False
    show_other_mrs_for_group_owners_in_these_groups: Set[str] = set()
    exclude_mrs_with_labels: Set[str] = set()

    @field_validator('sort_on', mode='before')
    @classmethod
    def parse_sort_on(cls, v) -> PullRequestSort:
        if isinstance(v, str):
            return PullRequestSort[v.upper()]
        return v

    @computed_field
    @property
    def cache_file(self) -> str:
        return get_cache_path(GitlabMrsConstants.MODULE)

    @classmethod
    def settings_customise_sources(cls, settings_cls, **kwargs):
        return (TomlConfigSettingsSource(settings_cls, "pull_requests", "gitlab_mrs"),)


gitlab_mrs_settings = GitlabMrsSettings()


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
