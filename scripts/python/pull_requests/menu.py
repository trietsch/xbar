import itertools
from typing import List, Dict

from .domain import PullRequest, PullRequestSort, PullRequestStatus, PullRequestsOverview, PullRequestException
from .notification import send_notification_new_pr
from ..common.icons import Icon, Icons


def sort_pull_requests(pull_requests: List[PullRequest], sort_on: PullRequestSort):
    return sorted(pull_requests, key=lambda p: p.activity,
                  reverse=True) if sort_on == PullRequestSort.ACTIVITY else sorted(pull_requests,
                                                                                   key=lambda p: p['title'])


def determine_repo_status(prs_list: List[PullRequest]):
    statuses = [_pr.overall_status for _pr in prs_list]

    if PullRequestStatus.REJECTED in statuses:
        return PullRequestStatus.REJECTED
    elif (PullRequestStatus.UNAPPROVED or PullRequestStatus.NO_VOTE) in statuses:
        return PullRequestStatus.UNAPPROVED
    elif (PullRequestStatus.NEEDS_WORK or PullRequestStatus.WAITING_FOR_AUTHOR) in statuses:
        return PullRequestStatus.NEEDS_WORK
    else:  # Approved / Approved with suggestions
        return PullRequestStatus.APPROVED


def print_prs(
        pr_type,
        pull_requests: List[PullRequest],
        sort_on: PullRequestSort,
        section_icon: Icon,
        status_icons: Dict[PullRequestStatus, Icon]):
    print(f"{pr_type} | templateImage={section_icon.base64_image}")
    print("---")

    prs_sorted_by_slug = sorted(pull_requests, key=lambda p: p.slug)

    for repo, repo_prs in itertools.groupby(prs_sorted_by_slug, key=lambda p: p.slug):
        repo_prs_list: List[PullRequest] = list(repo_prs)
        repo_status = determine_repo_status(repo_prs_list)
        repo_href = repo_prs_list[0].repo_href
        print(f"{repo} ({str(len(repo_prs_list))}) | href={repo_href} image={status_icons[repo_status].base64_image}")

        prs_sorted_by_to_ref = sorted(repo_prs_list, key=lambda p: p.to_ref)

        for to_ref, to_ref_prs in itertools.groupby(prs_sorted_by_to_ref, key=lambda p: p.to_ref):
            to_ref_prs_list: List[PullRequest] = sort_pull_requests(list(to_ref_prs), sort_on)
            print(f"--{to_ref}")

            for _pr in to_ref_prs_list:
                print(f"--{_pr.from_ref} -- {_pr.title} (#{_pr.id}) - {_pr.time_ago}" +
                      f"|href={_pr.href} image={status_icons[_pr.overall_status].base64_image}")


def print_bitbar_pull_request_menu(
        pr_overview: PullRequestsOverview,
        pr_statuses: Dict[PullRequestStatus, Icon],
        sort_on: PullRequestSort,
        cache_file: str,
        notifications_enabled: bool
):
    total_prs_to_review = len(pr_overview.prs_to_review)
    total_prs_authored_with_work = len(pr_overview.prs_authored_with_work)
    total_prs = total_prs_to_review + total_prs_authored_with_work

    if total_prs > 0:
        # Set menubar icon
        print(f"{str(total_prs)} | templateImage={Icons.PULL_REQUEST.base64_image}")

        # Start menu items
        if total_prs == 0:
            print("---")
            print(f"Nothing to review! | image={pr_statuses[PullRequestStatus.APPROVED].base64_image}")

        if total_prs_to_review > 0:
            print("---")
            print_prs("Reviewing", pr_overview.prs_to_review, sort_on, Icons.REVIEW, pr_statuses)

        if total_prs_authored_with_work > 0:
            print("---")
            print_prs("Authored", pr_overview.prs_authored_with_work, sort_on, Icons.AUTHORED, pr_statuses)

        if len(pr_overview.exceptions) > 0:
            print_and_log_exceptions(pr_overview.exceptions)

        if notifications_enabled:
            previous_pr_status = PullRequestsOverview.load_cached(cache_file)
            new_prs = pr_overview.determine_new_pull_requests_to_review(previous_pr_status)
            for pr in new_prs:
                send_notification_new_pr(pr.slug, pr.from_ref, pr.to_ref, pr.title, pr.href)

        pr_overview.store(cache_file)
    else:
        print(f"? | templateImage={Icons.PULL_REQUEST.base64_image}")
        print_and_log_exceptions(pr_overview.exceptions)


def print_and_log_exceptions(exceptions: List[PullRequestException]):
    for exception in exceptions:
        # TODO log exception to file
        print("---")
        print(f"Error: {exception.message} |templateImage={Icons.REVIEW.base64_image}")
