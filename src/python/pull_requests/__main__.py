import concurrent.futures

from . import PullRequestsOverview
from .config import PullRequestsConfig
from ..azure_devops.constants import AzureDevOpsConstants
from ..bitbucket.config import BitbucketConstants
from ..gitlab_mrs.config import GitlabMrsConstants
from ..pull_requests import print_xbar_pull_request_menu

executor = concurrent.futures.ThreadPoolExecutor()

pr_overview = PullRequestsOverview([], [], [])
pr_statuses = {}

if GitlabMrsConstants.MODULE in PullRequestsConfig.ENABLED_PR_MODULES:
    from ..gitlab_mrs import get_merge_request_overview as gitlab_mrs_overview
    from ..gitlab_mrs import GitlabMrsIcons

    gl_future = executor.submit(gitlab_mrs_overview)
    pr_overview = pr_overview.join(gl_future.result())
    pr_statuses = {**pr_statuses, **GitlabMrsIcons.PR_STATUSES}

if AzureDevOpsConstants.MODULE in PullRequestsConfig.ENABLED_PR_MODULES:
    from ..azure_devops import AzureDevOpsConfig, PullRequestClient
    from ..azure_devops import AzureDevOpsIcons

    client = PullRequestClient()
    azure_future = executor.submit(client.get_pull_requests_overview,
                                   (AzureDevOpsConfig.PROJECTS,
                                    AzureDevOpsConfig.PULL_REQUEST_STATUS,
                                    AzureDevOpsConfig.USER_EMAIL,
                                    AzureDevOpsConfig.TEAM_NAMES))
    pr_overview = pr_overview.join(azure_future.result())
    pr_statuses = {**pr_statuses, **AzureDevOpsIcons.PR_STATUSES}

if BitbucketConstants.MODULE in PullRequestsConfig.ENABLED_PR_MODULES:
    from ..bitbucket import BitbucketConfig, BitbucketIcons
    from ..bitbucket import get_pull_request_overview as bitbucket_prs_overview

    bitbucket_future = executor.submit(bitbucket_prs_overview,
                                       (BitbucketConfig.PRIVATE_TOKEN, BitbucketConfig.BITBUCKET_HOST))
    pr_overview = pr_overview.join(bitbucket_future.result())
    pr_statuses = {**pr_statuses, **BitbucketIcons.PR_STATUSES}

print_xbar_pull_request_menu(
    pr_overview,
    pr_statuses,
    PullRequestsConfig.SORT_ON,
    PullRequestsConfig.CACHE_FILE,
    PullRequestsConfig.NOTIFICATIONS_ENABLED
)
