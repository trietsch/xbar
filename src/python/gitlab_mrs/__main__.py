from . import get_merge_request_overview, gitlab_mrs_settings, GitlabMrsIcons
from ..pull_requests import print_xbar_pull_request_menu

print_xbar_pull_request_menu(
    get_merge_request_overview(),
    GitlabMrsIcons.PR_STATUSES,
    gitlab_mrs_settings.sort_on,
    gitlab_mrs_settings.cache_file,
    gitlab_mrs_settings.notifications_enabled
)
