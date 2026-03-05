from . import PullRequestClient
from .config import ado_settings, AzureDevOpsIcons
from ..pull_requests import print_xbar_pull_request_menu

print_xbar_pull_request_menu(
    PullRequestClient(ado_settings).get_pull_requests_overview(),
    AzureDevOpsIcons.PR_STATUSES,
    ado_settings.sort_on,
    ado_settings.cache_file,
    ado_settings.notifications_enabled
)