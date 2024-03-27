import traceback
from typing import List

import asyncio
from github import GithubException
from githubkit import GitHub
from requests import Timeout

from .config import GitHubPrsConfig, GitHubPrsConstants, GitHubGQLQueries
from ..common.util import abbreviate_string, time_ago, github_zulu_timestamp_string_to_datetime
from ..pull_requests import PullRequest, PullRequestsOverview, PullRequestException, PullRequestStatus

organizations = " ".join(list(map(lambda o: f"org:{o}", GitHubPrsConfig.ORGANIZATION_NAMES)))
labels_to_exclude = " ".join(list(map(lambda l: f"-label:{l}", GitHubPrsConfig.EXCLUDE_PRS_WITH_LABELS)))


async def get_pull_requests_to_review(_author_login, _gh):
    to_review = f"is:pr is:open {organizations} {labels_to_exclude} -author:{_author_login}"

    to_review_response = await _gh.async_graphql(query=GitHubGQLQueries.pull_requests,
                                                 variables={"githubQuery": to_review})

    return list(map(lambda pr: github_pr_to_pull_request(_author_login, pr), to_review_response["search"]["edges"]))


async def get_authored_pull_requests(_author_login, _gh):
    authored = f"is:pr is:open {organizations} {labels_to_exclude} author:{_author_login}"
    authored_response = await _gh.async_graphql(query=GitHubGQLQueries.pull_requests,
                                                variables={"githubQuery": authored})

    return list(map(lambda pr: github_pr_to_pull_request(_author_login, pr), authored_response["search"]["edges"]))


def github_pr_to_pull_request(_author_login, pr_node) -> PullRequest:
    pr = pr_node["node"]

    pr_activity = github_zulu_timestamp_string_to_datetime(pr["updatedAt"])

    reviews = pr["reviews"]["nodes"]
    non_approved_reviews = list(
        filter(lambda r: r["author"]["login"] != _author_login and r["state"] != "APPROVED", reviews))

    overall_status = PullRequestStatus.UNAPPROVED

    if len(non_approved_reviews) == 0 and len(reviews) > 0:
        overall_status = PullRequestStatus.APPROVED
    elif len(reviews) > 0:
        overall_status = PullRequestStatus.NEEDS_WORK

    return PullRequest(
        id=str(pr["number"]),
        title=abbreviate_string(pr["title"], GitHubPrsConfig.ABBREVIATION_CHARACTERS),
        slug=pr["repository"]["nameWithOwner"],
        from_ref=pr["headRefName"],
        to_ref=pr["baseRefName"],
        overall_status=overall_status,
        activity=pr_activity,
        time_ago=time_ago(pr_activity),
        all_prs_href=pr["url"],
        href=pr["url"]
    )


def get_pull_request_overview() -> PullRequestsOverview:
    _prs_to_review: List[PullRequest] = []
    _prs_authored_with_work: List[PullRequest] = []
    _exception = None

    _gh = GitHub(GitHubPrsConfig.PRIVATE_TOKEN)
    me = _gh.graphql(GitHubGQLQueries.login)

    loop = asyncio.get_event_loop()

    try:
        _prs_to_review_coroutine = get_pull_requests_to_review(me, _gh)
        _prs_authored_with_work_coroutine = get_authored_pull_requests(me, _gh)

        asyncio.gather(_prs_to_review_coroutine, _prs_authored_with_work_coroutine)

    except Timeout as e:
        _exception = PullRequestException(GitHubPrsConstants.MODULE, GitHubPrsConstants.TIMEOUT_MESSAGE, e,
                                          traceback.format_exc())
    except GithubException as e:
        _exception = PullRequestException(GitHubPrsConstants.MODULE, GitHubPrsConstants.CONNECTION_MESSAGE, e,
                                          traceback.format_exc())
    except Exception as e:
        _exception = PullRequestException(GitHubPrsConstants.MODULE, GitHubPrsConstants.UNKNOWN_MESSAGE, e,
                                          traceback.format_exc())

    return PullRequestsOverview.create(_prs_to_review, _prs_authored_with_work, _exception)
