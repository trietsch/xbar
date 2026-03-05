from ..azure_devops import PullRequestClient
from ..azure_devops.config import ado_settings, AzureDevOpsIcons
from ..bitbucket import get_pull_request_overview, bitbucket_settings, BitbucketIcons, BitbucketConstants
from ..pull_requests import print_xbar_pull_request_menu

azure_devops_prs = PullRequestClient(ado_settings).get_pull_requests_overview()

bitbucket_prs = get_pull_request_overview(
    bitbucket_settings.private_token,
    bitbucket_settings.bitbucket_host
)

all_prs = azure_devops_prs.join(bitbucket_prs)
pr_statuses = {**AzureDevOpsIcons.PR_STATUSES, **BitbucketIcons.PR_STATUSES}
cache_file = f"{ado_settings.cache_file}_{BitbucketConstants.MODULE}_combined"

print_xbar_pull_request_menu(
    all_prs,
    pr_statuses,
    ado_settings.sort_on,
    cache_file,
    ado_settings.notifications_enabled
)
