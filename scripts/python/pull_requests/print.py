import itertools
from typing import List, Dict

from .domain import PullRequest, PullRequestSort, PullRequestStatus
from ..common.icons import Icon


def sort_pull_requests(pull_requests: List[PullRequest], sort_on: PullRequestSort):
    return sorted(pull_requests, key=lambda p: p.activity,
                  reverse=True) if sort_on == PullRequestSort.ACTIVITY else sorted(pull_requests,
                                                                                   key=lambda p: p['title'])


def determine_repo_status(prs_list: List[PullRequest]):
    statuses = [_pr.overall_status for _pr in prs_list]

    # TODO add statuses for Azure DevOps
    if PullRequestStatus.UNAPPROVED in statuses:
        return PullRequestStatus.UNAPPROVED
    elif PullRequestStatus.NEEDS_WORK in statuses:
        return PullRequestStatus.NEEDS_WORK
    else:
        return PullRequestStatus.APPROVED


def print_prs(
        pr_type,
        pull_requests: List[PullRequest],
        sort_on: PullRequestSort,
        vendor_icon: str,
        status_icons: Dict[PullRequestStatus, Icon]):
    print(pr_type + " | templateImage=" + vendor_icon)
    print("---")

    prs_sorted_by_slug = sorted(pull_requests, key=lambda p: p.slug)

    for repo, repo_prs in itertools.groupby(prs_sorted_by_slug, key=lambda p: p.slug):
        repo_prs_list: List[PullRequest] = list(repo_prs)
        repo_status = determine_repo_status(repo_prs_list)
        repo_href = repo_prs_list[0].repo_href  # ugly yes, but that's because Bitbucket v1 api is ugly
        print(repo + " (" + str(len(repo_prs_list)) + ") | href=" + repo_href + " image = " + status_icons[
            repo_status].base64_image)

        prs_sorted_by_to_ref = sorted(repo_prs_list, key=lambda p: p.to_ref)

        for to_ref, to_ref_prs in itertools.groupby(prs_sorted_by_to_ref, key=lambda p: p.to_ref):
            to_ref_prs_list: List[PullRequest] = sort_pull_requests(list(to_ref_prs), sort_on)
            print("--" + to_ref)

            for _pr in to_ref_prs_list:
                print("--" +
                      _pr.from_ref + " -- " + _pr.title + " (#" + _pr.id + ") - " + _pr.time_ago + "|href=" + _pr.href
                      + " image=" + status_icons[_pr.overall_status].base64_image
                      )
