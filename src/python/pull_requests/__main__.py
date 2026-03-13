import concurrent.futures

from . import PullRequestsOverview, print_xbar_pull_request_menu
from .config import pr_settings
from .constants import PullRequestConstants
from .domain import PullRequestException

executor = concurrent.futures.ThreadPoolExecutor()

pr_overview = PullRequestsOverview([], [], [])
pr_statuses = {}

if not pr_settings.enabled_pr_modules:
    pr_overview.exceptions.append(PullRequestException(
        "pull_requests",
        "No PR modules configured. Add 'enabled_pr_modules' to pull_requests-config.toml under [preferences].",
        None,
        None
    ))

known_modules = {
    PullRequestConstants.GITLAB_MODULE,
    PullRequestConstants.AZURE_DEVOPS_MODULE,
    PullRequestConstants.BITBUCKET_MODULE,
}

futures = {}

for module in pr_settings.enabled_pr_modules:
    if module not in known_modules:
        pr_overview.exceptions.append(PullRequestException(
            module,
            f"Unknown module '{module}'. Known modules: {', '.join(sorted(known_modules))}.",
            None,
            None
        ))
        continue

    if module == PullRequestConstants.GITLAB_MODULE:
        from .gitlab_mrs import get_merge_request_overview, GitlabMrsIcons
        futures[module] = (executor.submit(get_merge_request_overview), GitlabMrsIcons.PR_STATUSES)

    elif module == PullRequestConstants.AZURE_DEVOPS_MODULE:
        from .azure_devops import get_pull_requests_overview, AzureDevOpsIcons
        futures[module] = (executor.submit(get_pull_requests_overview), AzureDevOpsIcons.PR_STATUSES)

    elif module == PullRequestConstants.BITBUCKET_MODULE:
        from .bitbucket import get_pull_request_overview, BitbucketIcons
        futures[module] = (executor.submit(get_pull_request_overview), BitbucketIcons.PR_STATUSES)

for module, (future, statuses) in futures.items():
    pr_overview = pr_overview.join(future.result())
    pr_statuses = {**pr_statuses, **statuses}

print_xbar_pull_request_menu(
    pr_overview,
    pr_statuses,
    pr_settings.sort_on,
    pr_settings.cache_file,
    pr_settings.notifications_enabled
)
