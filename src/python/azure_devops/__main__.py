from . import AzureDevOpsConfig
from . import PullRequestClient
from .config import AzureDevOpsIcons
from ..pull_requests import print_bitbar_pull_request_menu

print_bitbar_pull_request_menu(
    PullRequestClient().get_pull_requests_overview(
        AzureDevOpsConfig.PROJECTS[0],
        AzureDevOpsConfig.PULL_REQUEST_STATUS,
        AzureDevOpsConfig.USER_EMAIL,
        AzureDevOpsConfig.TEAM_NAME
    ),
    AzureDevOpsIcons.PR_STATUSES,
    AzureDevOpsConfig.SORT_ON,
    AzureDevOpsConfig.CACHE_FILE,
    AzureDevOpsConfig.NOTIFICATIONS_ENABLED
)
