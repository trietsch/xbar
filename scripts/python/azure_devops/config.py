import json
from distutils.util import strtobool
from typing import Dict

from ..common.config import AppConfigReader
from ..common.icons import Icons, Icon
from ..pull_requests import PullRequestSort, PullRequestStatus


class AzureDevOpsConstants(object):
    MODULE = "azure_devops"

    TIMEOUT_MESSAGE = "Timeout while trying to connect to Azure DevOps."
    CONNECTION_MESSAGE = "Failed to connect to Azure DevOps."
    UNKNOWN_MESSAGE = "An unknown exception occurred while trying to fetch PRs."


class AzureDevOpsConfig(object):
    _config = AppConfigReader.read(AzureDevOpsConstants.MODULE)

    ORGANIZATION_URL = f'https://dev.azure.com/{_config["preferences"]["organization"]}'
    PERSONAL_ACCESS_TOKEN = _config['preferences']['personal_access_token']
    PROJECTS = json.loads(_config['preferences']['projects'])
    PULL_REQUEST_STATUS = _config['preferences']['pull_request_status']
    USER_EMAIL = _config['preferences']['user_email'].lower()
    TEAM_NAME = _config['preferences']['team_name'].lower()

    SORT_ON = PullRequestSort[_config['preferences']['sort_on'].upper()]
    ABBREVIATION_CHARACTERS = int(_config['preferences']['abbreviation_characters'])
    OMIT_REVIEWED_AND_APPROVED = strtobool(_config['preferences']['omit_reviewed_and_approved'])
    NOTIFICATIONS_ENABLED = strtobool(_config['preferences']['notifications_enabled'])

    CACHE_FILE = _config['common']['cache_path']


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
        PullRequestStatus.APPROVED: Icons.GREEN_CIRCLE
    }
