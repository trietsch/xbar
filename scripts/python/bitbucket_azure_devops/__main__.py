from ..azure_devops import AzureDevOpsConfig, PullRequestClient
from ..azure_devops.config import AzureDevOpsIcons
from ..bitbucket import get_pull_request_overview, BitbucketConfig
from ..pull_requests import print_bitbar_pull_request_menu

azure_devops_prs = PullRequestClient().get_pull_requests_overview(
    AzureDevOpsConfig.PROJECTS[0],
    AzureDevOpsConfig.PULL_REQUEST_STATUS,
    AzureDevOpsConfig.USER_EMAIL,
    AzureDevOpsConfig.TEAM_NAME
)

bitbucket_prs = get_pull_request_overview(
    BitbucketConfig.PRIVATE_TOKEN,
    BitbucketConfig.BITBUCKET_HOST
)

all_prs = azure_devops_prs.join(bitbucket_prs)

print_bitbar_pull_request_menu(
    all_prs,
    AzureDevOpsIcons.PULL_REQUEST,
    AzureDevOpsIcons.AZURE_DEVOPS,
    AzureDevOpsIcons.PR_STATUSES,
    AzureDevOpsConfig.SORT_ON,
    AzureDevOpsConfig.CACHE_FILE,
    AzureDevOpsConfig.NOTIFICATIONS_ENABLED
)
