from . import AzureDevOpsConfig
from . import PullRequestClient
from .config import AzureDevOpsIcons
from ..pull_requests import print_xbar_pull_request_menu

print_xbar_pull_request_menu(
    PullRequestClient().get_pull_requests_overview(
        AzureDevOpsConfig.PROJECTS,
        AzureDevOpsConfig.PULL_REQUEST_STATUS,
        AzureDevOpsConfig.USER_EMAIL,
        AzureDevOpsConfig.TEAM_NAMES
    ),
    AzureDevOpsIcons.PR_STATUSES,
    AzureDevOpsConfig.SORT_ON,
    AzureDevOpsConfig.CACHE_FILE,
    AzureDevOpsConfig.NOTIFICATIONS_ENABLED
)
