#!/Users/rtrietsch/.pyenv/versions/3.6.0/bin/python
# -*- coding: utf-8 -*-

# <bitbar.title>Bitbucket PR</bitbar.title>
# <bitbar.desc>Shows the status of PRs in a Bitbucket instance</bitbar.desc>
# <bitbar.author>Robin Trietsch</bitbar.author>
# <bitbar.author.github>trietsch</bitbar.author.github>
# <bitbar.dependencies>python3</bitbar.dependencies>
# <bitbar.abouturl>https://gitlab.com/trietsch/bitbar</bitbar.abouturl>

# Settings can be found in the .bitbucket-config.ini file
# You don't have to change anything below
# -------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------

import itertools
import os
import pickle
from configparser import ConfigParser
from datetime import datetime, timezone
from distutils.util import strtobool
from pathlib import Path
from subprocess import Popen
from typing import List

import requests
import timeago
from requests import Timeout


def get_absolute_bitbar_file_path(repo_path):
    return os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/../' + repo_path)


class PullRequestConfig(object):
    _config_parser = ConfigParser()
    _config_parser.read(get_absolute_bitbar_file_path('config/bitbucket-config.ini'))
    _config = _config_parser._sections

    BITBUCKET_HOST = _config['preferences']['bitbucket_host']
    PRIVATE_TOKEN = _config['preferences']['private_token']
    USER_SLUG = _config['preferences']['user_slug']
    SORT_ON = _config['preferences']['sort_on']
    ABBREVIATION_CHARACTERS = int(_config['preferences']['abbreviation_characters'])
    OMIT_REVIEWED_AND_APPROVED = strtobool(_config['preferences']['omit_reviewed_and_approved'])
    NOTIFICATIONS_ENABLED = strtobool(_config['preferences']['notifications_enabled'])

    BITBUCKET_API_PULL_REQUESTS = '/rest/api/1.0/dashboard/pull-requests'


class PullRequestStatus(object):
    NEEDS_WORK = "NEEDS_WORK"
    UNAPPROVED = "UNAPPROVED"
    APPROVED = "APPROVED"


class PullRequestIcons(object):
    BITBUCKET = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAOCAYAAAAmL5yKAAAAAXNSR0IArs4c6QAAAAlwSFlzAAAOxAAADsQBlSsOGwAAActpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIgogICAgICAgICAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyI+CiAgICAgICAgIDx4bXA6Q3JlYXRvclRvb2w+d3d3Lmlua3NjYXBlLm9yZzwveG1wOkNyZWF0b3JUb29sPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KGMtVWAAAAjVJREFUKBWFU8tqVEEQPVXdfe9NHBKU4FvBLARFA+78EtEfEP8hm1mo/yCuXPgN2blz4UpcaIyTBBIxIEExcTJM7u3u8vSdKLqyhurbj6pzqk/1yPXHtgbDLQjGBjgBV/+3yJBF+lvP4ZJfxOU0AdRx9TudSP/YX/uWyHQKiAfY94x7nVvctsgKEuoTAIaALMZj6VPNrMT2FNyImMi8CN54LkY9M1AxKdBNAoLOZrMimGlRQILMDS1AjtEpYdvz7utkL8SOXCYKyR1G9I8MbMhs4qRN0+ObKdqyWRcZ7GXSALnb8ITbyseILMfzoNWalUzxamNVHs3oZ6Pee/fCwsKyHe23EMfY1PJCm+pa7DHkixY5iWks0gx3+hUFKDcq3sw1K3Xl4OtapGogql/PNPmzvh/KmMFbQgBG5qIwbfnGE7vArw2HkKWHO+d9Fa55NYS61lDPwVVh5/vLu4daosmxAc6ogxQA6rCUDFfK2XAoOXp/LjQLi07NXAjqWYH31aicnxSO9ZJNc/xSNUiK8fnV1aPdnJKmrruYi/5VgETVzBZYDutTbvUATvGJqhcrrcwFzNV+RemRHdLjhDj9aahqUek0U/lcNx9KQg8gGdsEGFOEAZP7NhEmlra6XO7ERxAqFY1IQowUW6lk8w9AaLDHpvxw8xjwSVdS3huJy+C8g1J9x0piTGR06CYHhxrP7pZzCj8z/qmecXaf/o0+08ZOzvkI+ZOUU8xdPJ1zXNt5OniAoekvT/f0vYI/tMoAAAAASUVORK5CYII="

    PULL_REQUEST = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAVCAYAAABPPm7SAAAAAXNSR0IArs4c6QAAAAlwSFlzAAALEwAACxMBAJqcGAAAAVlpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KTMInWQAAAbVJREFUOBGNlD0ohVEYxw/XZ4muiZHFbMFgllLKJKuFYlAWm0ExKCmT3WBS7qyLO8soE5uPRVEGHxf/33H+b++te+Nfv/s85/l6zznvvTeE+mpWuC2lpmSnk0+sKfk1ZlGritgTxVxmTP63mMnFcAv59ZYWFJXEm7gRaFx8CXK7YlZMCCsbQsFqig7I0rQvXgQ5hmLNpfxBgQqclUQ/K6lPcMY78SzqaVjBU9ElqhQsCYaUBU87E2hIPAly64LGA+FjrcnPdCSPQrZdzKIh+EhzKdYr66GHxFpS4jVZBvg1dci/FSPCQ6lnl4gHZgM8COsB7yl/QWESZ+beMnkRpymKtU/Rp6DGryyfiw/yAIobyZdWN/+fAXUbHfQAnxtr3zV563piNUf4SFWcmS03EjlqULSe2P0bCz2yvrD8TuxjXcs3MWpFn9xuWfDqzkVebiZ2Iqihlp5lEZ1tHIkvDYlJFlKr8I74JZIbFYieqo/wGEMhPCTbnizGO+hMsftkqY39G3KYXBJs70q4CeuHsJNrwYUfC3o2RdS8PjnXjvAluZEC+/wm+NeqiAUR5ad5jXXDX7HwA+nmXWV5F/zGAAAAAElFTkSuQmCC"

    STATUS = {
        PullRequestStatus.NEEDS_WORK: "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAfElEQVQ4T2NkQAOpqanasxxmX0EXB/HTDqTqzJ49+yqyHCOMExoayrYqYPVPbBrRxcI2hLKvXr36F0gcbAApmmGGwQwBG/B/KcN/YmxGV8MYzcDIiM/PhAwFhQkjubbDDB81gIGB8jCgOBopTkhUScqkGoKRmZCTLKnZGQCX5FCXyXSbYwAAAABJRU5ErkJggg==",
        PullRequestStatus.UNAPPROVED: "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAQhJREFUOBFjZEADqamp2oyMjClAYTcgloNKPwLSu/7//z9n9uzZV6FiYIoRxgkNDWUTFBTsA/IzgZgJJo5G/wPyp79//75o9erVv0ByYANAmgUEBLYDbXZC04CVC3TJvg8fPniCDAHbBLKZWM1gW4EWQV3LwAj18yWgBC5nY3UFUPAf0CV6TNAAI1UzyFCwXpBGUGiTC9xABsCiihxD5MhxOopFIAMeoYiQxnkEMmAXaXpQVO9iAiVPoBAohZEKQNE4hwmatqeTqhuofjpILzgQQWkblDyJNQSkFqQHpJ4ZRFy7du2vsrLyCk5OTiEg1wSI4ZkMJI8EQF6dBswHcSiZCUkBA6nZGQBHemGgvqxYAAAAAABJRU5ErkJggg==",
        PullRequestStatus.APPROVED: "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAARlJREFUOBGVk7FtAkEQRf8MyKGRIKcBJFfgyAGWC6ADElIKQMgFkFlO3IELsCAgcgVINOAcJAgR3DJ/zKGT2V2dN7nT/HkzO7t/BX/W6/dz71RgGIA+Qui6LPIjwKKh+Jg8ztdVxOK/a7oe3BXb/QwBoxCClvHqV0QKCN61fT+e9j4P1LwA4dNm92XwUxVI/guWjU7rhUW806VzPZhVrZEz9iuc+Vhgldp2ahccp6l4UD+wxMwpmHE2JKt+2rnMjEZWr1eVSUxKds3R60oCEUFhJonE64WMVTqsXvZtFlmlPd1ht3o2QoasurfNntnsmGgMWT9EettMvYzlRWOW64yJXoCeprdF5S03DjXmlO+Axa+vsez03+d8BpC2a0RVWrdkAAAAAElFTkSuQmCC"
    }


class PullRequest(object):
    def __init__(self, id, title, slug, from_ref, to_ref, overall_status, activity, time_ago, repo_href, href):
        self.id = str(id)
        self.title = title
        self.slug = slug
        self.from_ref = from_ref
        self.to_ref = to_ref
        self.overall_status = overall_status
        self.activity = activity
        self.time_ago = time_ago
        self.repo_href = repo_href
        self.href = href

    def get_uuid(self):
        return f'{self.slug}-{self.id}'


class PullRequestsOverview(object):
    CACHE_PATH = os.path.abspath(str(Path.home().absolute()) + '/Library/Caches/nl.robintrietsch.bitbar')
    CACHE_FILE = f'{CACHE_PATH}/last-pr-status'

    def __init__(self, _prs_to_review: List[PullRequest], _prs_authored_with_work: List[PullRequest], _exception):
        self.prs_to_review: List[PullRequest] = _prs_to_review
        self.prs_authored_with_work: List[PullRequest] = _prs_authored_with_work
        self.exception = _exception

    def determine_new_pull_requests_to_review(self, other):
        current = [_pr.get_uuid() for _pr in self.prs_to_review]
        previous = [_pr.get_uuid() for _pr in other.prs_to_review]
        new = set(current) - set(previous)

        return [_pr for _pr in self.prs_to_review if _pr.get_uuid() in new]

    def store(self):
        if not os.path.exists(PullRequestsOverview.CACHE_PATH):
            os.makedirs(PullRequestsOverview.CACHE_PATH)

        pickle.dump(self, open(PullRequestsOverview.CACHE_FILE, 'wb'))

    @staticmethod
    def load_cached():
        try:
            return pickle.load(open(PullRequestsOverview.CACHE_FILE, 'rb'))
        except Exception as e:
            return PullRequestsOverview(list(), list(), None)


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
    reviewers_filtered = list(filter(lambda reviewer: reviewer['user']['slug'] == PullRequestConfig.USER_SLUG, _pr['reviewers']))

    if len(reviewers_filtered) > 0 and (
            True if not PullRequestConfig.OMIT_REVIEWED_AND_APPROVED else reviewers_filtered[0]['status'] != PullRequestStatus.APPROVED
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
    return s[:PullRequestConfig.ABBREVIATION_CHARACTERS] + "..." if len(s) > PullRequestConfig.ABBREVIATION_CHARACTERS else s


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
                  reverse=True) if PullRequestConfig.SORT_ON == 'activity' else sorted(pull_requests, key=lambda p: p['title'])


def print_prs(pr_type, pull_requests):
    print(pr_type + " | templateImage=" + PullRequestIcons.BITBUCKET)
    print("---")

    prs_sorted_by_slug = sorted(pull_requests, key=lambda p: p.slug)

    for repo, repo_prs in itertools.groupby(prs_sorted_by_slug, key=lambda p: p.slug):
        repo_prs_list: List[PullRequest] = list(repo_prs)
        repo_status = determine_repo_status(repo_prs_list)
        repo_href = repo_prs_list[0].repo_href  # ugly yes, but that's because Bitbucket v1 api is ugly
        print(repo + " (" + str(len(repo_prs_list)) + ") | href=" + repo_href + " image = " + PullRequestIcons.STATUS[repo_status])

        prs_sorted_by_to_ref = sorted(repo_prs_list, key=lambda p: p.to_ref)

        for to_ref, to_ref_prs in itertools.groupby(prs_sorted_by_to_ref, key=lambda p: p.to_ref):
            to_ref_prs_list: List[PullRequest] = sort_pull_requests(list(to_ref_prs))
            print("--" + to_ref)

            for _pr in to_ref_prs_list:
                print("--" +
                      _pr.from_ref + " -- " + _pr.title + " (#" + _pr.id + ") - " + _pr.time_ago + "|href=" + _pr.href
                      + " image=" + PullRequestIcons.STATUS[_pr.overall_status]
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


if __name__ == "__main__":
    pr_status = get_pr_status()

    if pr_status.exception is not None:
        print("? | templateImage=" + PullRequestIcons.PULL_REQUEST)
        print("---")
        print("Error: " + pr_status.exception + "|templateImage=" + PullRequestIcons.BITBUCKET)
    else:
        # Set menubar icon
        total_prs_to_review = len(pr_status.prs_to_review)
        total_prs_authored_with_work = len(pr_status.prs_authored_with_work)
        total_prs = str(total_prs_to_review + total_prs_authored_with_work)
        print(total_prs + " | templateImage=" + PullRequestIcons.PULL_REQUEST)

        # Start menu items
        if total_prs == 0:
            print("---")
            print("Nothing to review! | image = " + PullRequestIcons.STATUS[PullRequestStatus.APPROVED])

        if total_prs_to_review > 0:
            print("---")
            print_prs("Reviewing", pr_status.prs_to_review)

        if total_prs_authored_with_work > 0:
            print("---")
            print_prs("Authored", pr_status.prs_authored_with_work)

        previous_pr_status = PullRequestsOverview.load_cached()
        new_prs = pr_status.determine_new_pull_requests_to_review(previous_pr_status)

        if PullRequestConfig.NOTIFICATIONS_ENABLED:
            for pr in new_prs:
                send_notification_new_pr(pr.slug, pr.from_ref, pr.to_ref, pr.title)

        pr_status.store()
