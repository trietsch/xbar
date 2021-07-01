from ..azure_devops import AzureDevOpsConfig, PullRequestClient
from ..azure_devops.config import AzureDevOpsIcons
from ..bitbucket import get_pull_request_overview, BitbucketConfig, BitbucketIcons, BitbucketConstants
from ..pull_requests import print_bitbar_pull_request_menu

azure_devops_prs = PullRequestClient().get_pull_requests_overview(
    AzureDevOpsConfig.PROJECTS,
    AzureDevOpsConfig.PULL_REQUEST_STATUS,
    AzureDevOpsConfig.USER_EMAIL,
    AzureDevOpsConfig.TEAM_NAMES
)

bitbucket_prs = get_pull_request_overview(
    BitbucketConfig.PRIVATE_TOKEN,
    BitbucketConfig.BITBUCKET_HOST
)

# Merge contents
all_prs = azure_devops_prs.join(bitbucket_prs)
pr_statuses = {**AzureDevOpsIcons.PR_STATUSES, **BitbucketIcons.PR_STATUSES}
cache_file = f"{AzureDevOpsConfig.CACHE_FILE}_{BitbucketConstants.MODULE}_combined"

print_bitbar_pull_request_menu(
    all_prs,
    pr_statuses,
    AzureDevOpsConfig.SORT_ON,
    cache_file,
    AzureDevOpsConfig.NOTIFICATIONS_ENABLED
)
