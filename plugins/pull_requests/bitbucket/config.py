import traceback
from typing import Dict

from pydantic import ValidationError, computed_field, field_validator
from pydantic_settings import BaseSettings

from .constants import BitbucketConstants
from common.config import TomlConfigSettingsSource, get_cache_path
from common.icons import Icon, Icons
from pull_requests import PullRequestSort, PullRequestStatus, PullRequestException


class BitbucketSettings(BaseSettings):
    bitbucket_host: str
    private_token: str
    user_slug: str
    sort_on: PullRequestSort = PullRequestSort.ACTIVITY
    abbreviation_characters: int = 30
    omit_reviewed_and_approved: bool = False
    notifications_enabled: bool = False

    @field_validator('sort_on', mode='before')
    @classmethod
    def parse_sort_on(cls, v) -> PullRequestSort:
        if isinstance(v, str):
            return PullRequestSort[v.upper()]
        return v

    @computed_field
    @property
    def cache_file(self) -> str:
        return get_cache_path(BitbucketConstants.MODULE)

    @classmethod
    def settings_customise_sources(cls, settings_cls, **kwargs):
        return (TomlConfigSettingsSource(settings_cls, "pull_requests", "bitbucket"),)


_settings_error = None
try:
    bitbucket_settings = BitbucketSettings()
except ValidationError as e:
    bitbucket_settings = None
    _settings_error = PullRequestException(
        BitbucketConstants.MODULE,
        f"Configuration error: {e}",
        e,
        traceback.format_exc()
    )


class BitbucketIcons(object):
    BITBUCKET = Icon(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAOCAYAAAAmL5yKAAAAAXNSR0IArs4c6QAAAAlwSFlzAAAOxAAADsQBlSsOGwAAActpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIgogICAgICAgICAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyI+CiAgICAgICAgIDx4bXA6Q3JlYXRvclRvb2w+d3d3Lmlua3NjYXBlLm9yZzwveG1wOkNyZWF0b3JUb29sPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KGMtVWAAAAjVJREFUKBWFU8tqVEEQPVXdfe9NHBKU4FvBLARFA+78EtEfEP8hm1mo/yCuXPgN2blz4UpcaIyTBBIxIEExcTJM7u3u8vSdKLqyhurbj6pzqk/1yPXHtgbDLQjGBjgBV/+3yJBF+lvP4ZJfxOU0AdRx9TudSP/YX/uWyHQKiAfY94x7nVvctsgKEuoTAIaALMZj6VPNrMT2FNyImMi8CN54LkY9M1AxKdBNAoLOZrMimGlRQILMDS1AjtEpYdvz7utkL8SOXCYKyR1G9I8MbMhs4qRN0+ObKdqyWRcZ7GXSALnb8ITbyseILMfzoNWalUzxamNVHs3oZ6Pee/fCwsKyHe23EMfY1PJCm+pa7DHkixY5iWks0gx3+hUFKDcq3sw1K3Xl4OtapGogql/PNPmzvh/KmMFbQgBG5qIwbfnGE7vArw2HkKWHO+d9Fa55NYS61lDPwVVh5/vLu4daosmxAc6ogxQA6rCUDFfK2XAoOXp/LjQLi07NXAjqWYH31aicnxSO9ZJNc/xSNUiK8fnV1aPdnJKmrruYi/5VgETVzBZYDutTbvUATvGJqhcrrcwFzNV+RemRHdLjhDj9aahqUek0U/lcNx9KQg8gGdsEGFOEAZP7NhEmlra6XO7ERxAqFY1IQowUW6lk8w9AaLDHpvxw8xjwSVdS3huJy+C8g1J9x0piTGR06CYHhxrP7pZzCj8z/qmecXaf/o0+08ZOzvkI+ZOUU8xdPJ1zXNt5OniAoekvT/f0vYI/tMoAAAAASUVORK5CYII=")

    PULL_REQUEST = Icons.PULL_REQUEST

    PR_STATUSES: Dict[PullRequestStatus, Icon] = {
        PullRequestStatus.UNAPPROVED: Icons.GREY_CIRCLE,
        PullRequestStatus.NEEDS_WORK: Icons.ORANGE_CIRCLE,
        PullRequestStatus.APPROVED: Icons.GREEN_CIRCLE
    }
