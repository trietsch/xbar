from . import get_merge_request_overview, GitlabMrsIcons, GitlabMrsConfig
from ..pull_requests import print_xbar_pull_request_menu

print_xbar_pull_request_menu(
    get_merge_request_overview(),
    GitlabMrsIcons.PR_STATUSES,
    GitlabMrsConfig.SORT_ON,
    GitlabMrsConfig.CACHE_FILE,
    GitlabMrsConfig.NOTIFICATIONS_ENABLED
)
