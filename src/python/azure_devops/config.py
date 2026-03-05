from typing import Dict, List

from pydantic import computed_field, field_validator
from pydantic_settings import BaseSettings

from .constants import AzureDevOpsConstants
from ..common.config import TomlConfigSettingsSource, get_cache_path
from ..common.icons import Icons, Icon
from ..pull_requests import PullRequestSort, PullRequestStatus


class AzureDevOpsSettings(BaseSettings):
    organization: str
    personal_access_token: str
    projects: List[str]
    pull_request_status: str
    user_email: str
    team_names: List[str] = []
    sort_on: PullRequestSort = PullRequestSort.ACTIVITY
    abbreviation_characters: int = 30
    omit_reviewed_and_approved: bool = False
    omit_draft: bool = False
    filter_by_reviewer: bool = True
    notifications_enabled: bool = True

    @field_validator('user_email', mode='before')
    @classmethod
    def lowercase_email(cls, v: str) -> str:
        return v.lower()

    @field_validator('team_names', mode='before')
    @classmethod
    def lowercase_team_names(cls, v: List[str]) -> List[str]:
        return [name.lower() for name in v]

    @field_validator('sort_on', mode='before')
    @classmethod
    def parse_sort_on(cls, v) -> PullRequestSort:
        if isinstance(v, str):
            return PullRequestSort[v.upper()]
        return v

    @computed_field
    @property
    def organization_url(self) -> str:
        return f'https://dev.azure.com/{self.organization}'

    @computed_field
    @property
    def cache_file(self) -> str:
        return get_cache_path(AzureDevOpsConstants.MODULE)

    @classmethod
    def settings_customise_sources(cls, settings_cls, **kwargs):
        return (TomlConfigSettingsSource(settings_cls, "pull_requests", "azure_devops"),)


ado_settings = AzureDevOpsSettings()


class AzureDevOpsIcons(object):
    AZURE_DEVOPS = Icon(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAACXBIWXMAAAsTAAALEwEAmpwYAAABWWlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS40LjAiPgogICA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyI+CiAgICAgICAgIDx0aWZmOk9yaWVudGF0aW9uPjE8L3RpZmY6T3JpZW50YXRpb24+CiAgICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgpMwidZAAAChUlEQVQ4EY1SS0hUURj+zn3MaDPiA3GhI1kQ1C0pKNq1chNt2qQURdCmRdBKsVsuvDtD2kQEYauo1bhtEwkSbRVLnUkRYooopKmmuY7zuI/Td+51DG3Tgfs43//9r+//gf3HmTci6F7uFOzVZ3ByXdFdSoGmrelDLCY7UsPXRR29pwM4wo/svl9Eqvs6qqWLsFdsCPGEuA/FtSAwIgJijDqc1TE7EjSDYux9D8zEWUj/MiAuEU/iQCew/SsPIe9gavDlLnd0oVtEl4n1PoT+FUg5xPs5Zk5BTwBehTkb/FZdBisDco6558khFxn+9wmMr7VB8/PoGsiQCLibkoQ1PqsM+I6Oi5BBDtMnvxAD7NwoOjMP8PsbLxIGnbPMmMGPwlMILQuEH9EyWKAWYeTQfDnSiPSRYQOVn6T5dZpMBjDOo7ENaOI5pqy3TT6yUsfcooZelxW9CSly3K6mCehKe9qZ0WAkD0bSJEKleJxcAo7lRSoDf8V1JrXIvu+lQJaq2t4Zn2XRSSjgv46BRCrJeTJMEJeYL5hcmPg/913i+LDEJDPM7LSwL6yBxtYLBrnGKmLRnEO1PZxZ3hz1OHE7YSiigjlDfrlI6thLAxDJIcY4yOo/ES5BhEXeyzBaSqhuudDTdUwfdbnet9Da8ZgbWqOGLQI3F0zMnPHgLHWgZn5Guqct2gfVVq2stKgzWY3ZOCpZpD7txPphtmrkVeIKbm8k8ehIHeMrx6DreWbeJMlDa3sGITtTC6Y6VOMLPC53msHdAkJ5IR6Nclbjmx78QDEn6LyB+yf6US3fQMN9FY1aOalgyTYQf4162Yr4JP977OWre0B7+TDuroxxjdf5PNy1cTv/AISCCLMovX8qAAAAAElFTkSuQmCC")

    PULL_REQUEST = Icons.PULL_REQUEST

    PR_STATUSES: Dict[PullRequestStatus, Icon] = {
        PullRequestStatus.REJECTED: Icons.RED_CIRCLE,
        PullRequestStatus.WAITING_FOR_AUTHOR: Icons.ORANGE_CIRCLE,
        PullRequestStatus.NO_VOTE: Icons.GREY_CIRCLE,
        PullRequestStatus.UNAPPROVED: Icons.GREY_CIRCLE,
        PullRequestStatus.APPROVED_WITH_SUGGESTIONS: Icons.GREEN_CIRCLE,
        PullRequestStatus.APPROVED: Icons.GREEN_CIRCLE,
        PullRequestStatus.NEEDS_WORK: Icons.ORANGE_CIRCLE
    }