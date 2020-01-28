import itertools
from typing import List, Dict

from .domain import PullRequest, PullRequestSort, PullRequestStatus, PullRequestsOverview
from .notification import send_notification_new_pr
from ..common.icons import Icon
from ..common.util import get_absolute_path_to_repo_file


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
        vendor_icon: Icon,
        status_icons: Dict[PullRequestStatus, Icon]):
    print(pr_type + " | templateImage=" + vendor_icon.base64_image)
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


def print_bitbar_pull_request_menu(
        pr_overview: PullRequestsOverview,
        pr_icon: Icon,
        provider_icon: Icon,
        pr_statuses: Dict[PullRequestStatus, Icon],
        sort_on: PullRequestSort,
        cache_file: str,
        notifications_enabled: bool
):
    if pr_overview.exception is not None:
        print("? | templateImage=" + pr_icon.base64_image)
        print("---")
        print("Error: " + pr_overview.exception + "|templateImage=" + provider_icon.base64_image)
    else:
        # Set menubar icon
        total_prs_to_review = len(pr_overview.prs_to_review)
        total_prs_authored_with_work = len(pr_overview.prs_authored_with_work)
        total_prs = str(total_prs_to_review + total_prs_authored_with_work)
        print(total_prs + " | templateImage=" + pr_icon.base64_image)

        # Start menu items
        if total_prs == 0:
            print("---")
            print("Nothing to review! | image = " + pr_statuses[PullRequestStatus.APPROVED].base64_image)

        if total_prs_to_review > 0:
            print("---")
            print_prs("Reviewing", pr_overview.prs_to_review, sort_on, provider_icon, pr_statuses)

        if total_prs_authored_with_work > 0:
            print("---")
            print_prs("Authored", pr_overview.prs_authored_with_work, sort_on, provider_icon, pr_statuses)

        previous_pr_status = PullRequestsOverview.load_cached(cache_file)
        new_prs = pr_overview.determine_new_pull_requests_to_review(previous_pr_status)

        if notifications_enabled:
            for pr in new_prs:
                send_notification_new_pr(pr.slug, pr.from_ref, pr.to_ref, pr.title,
                                         get_absolute_path_to_repo_file('assets/pr-logo.png'))

        pr_overview.store(cache_file)
