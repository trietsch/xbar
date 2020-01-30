from . import get_pull_request_overview, BitbucketIcons, BitbucketConfig
from ..pull_requests import print_bitbar_pull_request_menu

print_bitbar_pull_request_menu(
    get_pull_request_overview(
        BitbucketConfig.PRIVATE_TOKEN,
        BitbucketConfig.BITBUCKET_HOST
    ),
    BitbucketIcons.PULL_REQUEST,
    BitbucketIcons.BITBUCKET,
    BitbucketIcons.PR_STATUSES,
    BitbucketConfig.SORT_ON,
    BitbucketConfig.CACHE_FILE,
    BitbucketConfig.NOTIFICATIONS_ENABLED
)
