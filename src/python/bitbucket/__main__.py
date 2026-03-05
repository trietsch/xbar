from . import get_pull_request_overview, bitbucket_settings, BitbucketIcons
from ..pull_requests import print_xbar_pull_request_menu

print_xbar_pull_request_menu(
    get_pull_request_overview(
        bitbucket_settings.private_token,
        bitbucket_settings.bitbucket_host
    ),
    BitbucketIcons.PR_STATUSES,
    bitbucket_settings.sort_on,
    bitbucket_settings.cache_file,
    bitbucket_settings.notifications_enabled
)
