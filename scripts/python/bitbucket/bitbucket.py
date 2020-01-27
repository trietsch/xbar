import itertools
from datetime import datetime, timezone
from subprocess import Popen
from typing import List

import requests
import timeago
from requests import Timeout

from .domain import PullRequestStatus, PullRequest, BitbucketIcons, PullRequestsOverview
from ..pull_requests import get_absolute_bitbar_file_path
from .config import PullRequestConfig


def get_open_pull_requests_to_review(_api_key, _url):
    params = dict(
        limit=50,
        state='OPEN',
        role='REVIEWER'
    )

    return list(filter(pr_should_be_reviewed_by_me, get_pull_requests(_api_key, _url, params)))


def get_authored_pull_requests_with_work(_api_key, _url):
    params = dict(
        limit=50,
        state='OPEN',
        role='AUTHOR'
    )

    return list(map(pr_is_marked_as_needs_work, get_pull_requests(_api_key, _url, params)))


def get_pull_requests(_api_key, _url, _params):
    headers = dict(
        Authorization=f'Bearer {_api_key}'
    )
    r = requests.get(_url + PullRequestConfig.BITBUCKET_API_PULL_REQUESTS, params=_params, timeout=5, headers=headers)

    body = r.json()
    pull_requests = body['values']

    is_last_page = body['isLastPage']
    if not is_last_page:
        _params['start'] = body['nextPageStart']
        pull_requests = pull_requests + get_pull_requests(_api_key, _url, _params)

    return pull_requests


def pr_should_be_reviewed_by_me(_pr):
    reviewers_filtered = list(
        filter(lambda reviewer: reviewer['user']['slug'] == PullRequestConfig.USER_SLUG, _pr['reviewers']))

    if len(reviewers_filtered) > 0 and (
            True if not PullRequestConfig.OMIT_REVIEWED_AND_APPROVED else reviewers_filtered[0][
                                                                              'status'] != PullRequestStatus.APPROVED
    ):
        _pr['overallStatus'] = reviewers_filtered[0]['status']
        return _pr


def pr_is_marked_as_needs_work(_pr):
    reviewers_status = [reviewer['status'] for reviewer in _pr['reviewers']]

    if PullRequestStatus.NEEDS_WORK in reviewers_status:
        _pr['overallStatus'] = PullRequestStatus.NEEDS_WORK
    elif PullRequestStatus.APPROVED not in reviewers_status:
        _pr['overallStatus'] = PullRequestStatus.UNAPPROVED
    else:
        _pr['overallStatus'] = PullRequestStatus.APPROVED

    return _pr


def epoch_ms_to_datetime(epoch_ms):
    return datetime.fromtimestamp(epoch_ms / 1000.0, tz=timezone.utc)


def abbreviate_string(s):
    return s[:PullRequestConfig.ABBREVIATION_CHARACTERS] + "..." if len(
        s) > PullRequestConfig.ABBREVIATION_CHARACTERS else s


def extract_pull_request_data(_raw_pull_requests) -> List[PullRequest]:
    pull_requests: List[PullRequest] = list()

    for _pr in _raw_pull_requests:
        pr_activity = epoch_ms_to_datetime(_pr['updatedDate'])
        time_ago = timeago.format(
            pr_activity.replace(tzinfo=timezone.utc)
                .astimezone(tz=None)
                .replace(tzinfo=None),
            datetime.now()
        )

        pull_requests.append(PullRequest(
            id=_pr['id'],
            title=abbreviate_string(_pr['title']),
            slug=_pr['toRef']['repository']['slug'],
            from_ref=_pr['fromRef']['displayId'],
            to_ref=_pr['toRef']['displayId'],
            overall_status=_pr['overallStatus'],
            activity=pr_activity,
            time_ago=time_ago,
            repo_href=_pr['toRef']['repository']['links']['self'][0]['href'].replace('browse', 'pull-requests'),
            href=_pr['links']['self'][0]['href']
        ))

    return pull_requests


def sort_pull_requests(pull_requests):
    return sorted(pull_requests, key=lambda p: p.activity,
                  reverse=True) if PullRequestConfig.SORT_ON == 'activity' else sorted(pull_requests,
                                                                                       key=lambda p: p['title'])


def print_prs(pr_type, pull_requests):
    print(pr_type + " | templateImage=" + BitbucketIcons.BITBUCKET)
    print("---")

    prs_sorted_by_slug = sorted(pull_requests, key=lambda p: p.slug)

    for repo, repo_prs in itertools.groupby(prs_sorted_by_slug, key=lambda p: p.slug):
        repo_prs_list: List[PullRequest] = list(repo_prs)
        repo_status = determine_repo_status(repo_prs_list)
        repo_href = repo_prs_list[0].repo_href  # ugly yes, but that's because Bitbucket v1 api is ugly
        print(repo + " (" + str(len(repo_prs_list)) + ") | href=" + repo_href + " image = " + BitbucketIcons.STATUS[
            repo_status])

        prs_sorted_by_to_ref = sorted(repo_prs_list, key=lambda p: p.to_ref)

        for to_ref, to_ref_prs in itertools.groupby(prs_sorted_by_to_ref, key=lambda p: p.to_ref):
            to_ref_prs_list: List[PullRequest] = sort_pull_requests(list(to_ref_prs))
            print("--" + to_ref)

            for _pr in to_ref_prs_list:
                print("--" +
                      _pr.from_ref + " -- " + _pr.title + " (#" + _pr.id + ") - " + _pr.time_ago + "|href=" + _pr.href
                      + " image=" + BitbucketIcons.STATUS[_pr.overall_status]
                      )


def determine_repo_status(prs_list: List[PullRequest]):
    statuses = [_pr.overall_status for _pr in prs_list]

    if PullRequestStatus.UNAPPROVED in statuses:
        return PullRequestStatus.UNAPPROVED
    elif PullRequestStatus.NEEDS_WORK in statuses:
        return PullRequestStatus.NEEDS_WORK
    else:
        return PullRequestStatus.APPROVED


def send_notification_new_pr(_repo_slug, _from_ref, _to_ref, _title):
    send_notification(f'New pull request for {_repo_slug}', f'{_title}\n{_from_ref} -> {_to_ref}')


def send_notification(title, message):
    arguments = f"-title '{title}' -message '{message}' -appIcon '{get_absolute_bitbar_file_path('assets/pr-logo.png')}'"

    Popen(["/bin/bash", "-c",
           f"{get_absolute_bitbar_file_path('notifications/terminal-notifier.app/Contents/MacOS/terminal-notifier')} {arguments}"])


def get_pr_status():
    _prs_to_review: List[PullRequest] = []
    _prs_authored_with_work: List[PullRequest] = []
    _exception = None
    try:
        _prs_to_review: List[PullRequest] = extract_pull_request_data(
            get_open_pull_requests_to_review(PullRequestConfig.PRIVATE_TOKEN, PullRequestConfig.BITBUCKET_HOST)
        )
        _prs_authored_with_work: List[PullRequest] = extract_pull_request_data(
            get_authored_pull_requests_with_work(PullRequestConfig.PRIVATE_TOKEN, PullRequestConfig.BITBUCKET_HOST)
        )
    except Timeout as e:
        _exception = "timeout"
    except ConnectionError as e:
        _exception = "connection error"
    except Exception as e:
        _exception = "unknown error"

    return PullRequestsOverview(_prs_to_review, _prs_authored_with_work, _exception)
