from . import get_pull_request_overview, GitlabPrsIcons, GitHubPrsConfig
from ..pull_requests import print_xbar_pull_request_menu

print_xbar_pull_request_menu(
    get_pull_request_overview(),
    GitlabPrsIcons.PR_STATUSES,
    GitHubPrsConfig.SORT_ON,
    GitHubPrsConfig.CACHE_FILE,
    GitHubPrsConfig.NOTIFICATIONS_ENABLED
)
