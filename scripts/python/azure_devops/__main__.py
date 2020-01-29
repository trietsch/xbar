from typing import List

from . import AzureDevOpsConfig
from . import PullRequestClient
from .azure_devops import GitPullRequestMapper
from .config import AzureDevOpsIcons
from ..pull_requests import PullRequest, print_bitbar_pull_request_menu, PullRequestsOverview

pr_client = PullRequestClient()

filtered = pr_client.get_pull_request_to_be_reviewed_by(AzureDevOpsConfig.PROJECTS[0],
                                                        AzureDevOpsConfig.PULL_REQUEST_STATUS,
                                                        AzureDevOpsConfig.USER_EMAIL)

prs_to_review: List[PullRequest] = GitPullRequestMapper.to_pull_requests(filtered)

pr_overview = PullRequestsOverview(prs_to_review, list(), None)

print_bitbar_pull_request_menu(
    pr_overview,
    AzureDevOpsIcons.PULL_REQUEST,
    AzureDevOpsIcons.AZURE_DEVOPS,
    AzureDevOpsIcons.PR_STATUSES,
    AzureDevOpsConfig.SORT_ON,
    AzureDevOpsConfig.CACHE_FILE,
    AzureDevOpsConfig.NOTIFICATIONS_ENABLED
)
