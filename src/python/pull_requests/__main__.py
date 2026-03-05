import concurrent.futures

from . import PullRequestsOverview
from .config import pr_settings
from .contants import PullRequestConstants
from ..pull_requests import print_xbar_pull_request_menu

executor = concurrent.futures.ThreadPoolExecutor()

pr_overview = PullRequestsOverview([], [], [])
pr_statuses = {}

if PullRequestConstants.GITLAB_MODULE in pr_settings.enabled_pr_modules:
    from ..gitlab_mrs import get_merge_request_overview as gitlab_mrs_overview
    from ..gitlab_mrs import GitlabMrsIcons

    gl_future = executor.submit(gitlab_mrs_overview)
    pr_overview = pr_overview.join(gl_future.result())
    pr_statuses = {**pr_statuses, **GitlabMrsIcons.PR_STATUSES}

if PullRequestConstants.AZURE_DEVOPS_MODULE in pr_settings.enabled_pr_modules:
    from ..azure_devops import PullRequestClient
    from ..azure_devops.config import ado_settings, AzureDevOpsIcons

    client = PullRequestClient(ado_settings)
    azure_future = executor.submit(client.get_pull_requests_overview)
    pr_overview = pr_overview.join(azure_future.result())
    pr_statuses = {**pr_statuses, **AzureDevOpsIcons.PR_STATUSES}

if PullRequestConstants.BITBUCKET_MODULE in pr_settings.enabled_pr_modules:
    from ..bitbucket import get_pull_request_overview as bitbucket_prs_overview
    from ..bitbucket import bitbucket_settings, BitbucketIcons

    bitbucket_future = executor.submit(
        bitbucket_prs_overview,
        bitbucket_settings.private_token,
        bitbucket_settings.bitbucket_host
    )
    pr_overview = pr_overview.join(bitbucket_future.result())
    pr_statuses = {**pr_statuses, **BitbucketIcons.PR_STATUSES}

print_xbar_pull_request_menu(
    pr_overview,
    pr_statuses,
    pr_settings.sort_on,
    pr_settings.cache_file,
    pr_settings.notifications_enabled
)
