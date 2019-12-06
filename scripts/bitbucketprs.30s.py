#!/Users/rtrietsch/.pyenv/versions/3.6.0/bin/python
# -*- coding: utf-8 -*-

# <bitbar.title>Bitbucket PR</bitbar.title>
# <bitbar.desc>Shows the status of PRs in a Bitbucket instance</bitbar.desc>
# <bitbar.author>Robin Trietsch</bitbar.author>
# <bitbar.author.github>trietsch</bitbar.author.github>
# <bitbar.dependencies>python3</bitbar.dependencies>
# <bitbar.abouturl>https://gitlab.com/trietsch/bitbar</bitbar.abouturl>

# Settings can be found in the .gitlab-config.py file
# You don't have to change anything below
# -------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------

import itertools
import os
from configparser import ConfigParser
from datetime import datetime, timezone
from distutils.util import strtobool

import requests
import timeago
from requests import Timeout

config_parser = ConfigParser()
config_parser.read(os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + '/../config/bitbucket-config.ini'))
config = config_parser._sections

BITBUCKET_HOST = config['preferences']['bitbucket_host']
PRIVATE_TOKEN = config['preferences']['private_token']
USER_SLUG = config['preferences']['user_slug']
SORT_ON = config['preferences']['sort_on']
ABBREVIATION_CHARACTERS = int(config['preferences']['abbreviation_characters'])
OMIT_REVIEWED_AND_APPROVED = strtobool(config['preferences']['omit_reviewed_and_approved'])

# API paths
API_PULL_REQUESTS = '/rest/api/1.0/dashboard/pull-requests'

# PR status
STATUS_NEEDS_WORK = "NEEDS_WORK"
STATUS_UNAPPROVED = "UNAPPROVED"
STATUS_APPROVED = "APPROVED"

# Bitbucket Favicon
bitbucket_image = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAOCAYAAAAmL5yKAAAAAXNSR0IArs4c6QAAAAlwSFlzAAAOxAAADsQBlSsOGwAAActpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIgogICAgICAgICAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyI+CiAgICAgICAgIDx4bXA6Q3JlYXRvclRvb2w+d3d3Lmlua3NjYXBlLm9yZzwveG1wOkNyZWF0b3JUb29sPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KGMtVWAAAAjVJREFUKBWFU8tqVEEQPVXdfe9NHBKU4FvBLARFA+78EtEfEP8hm1mo/yCuXPgN2blz4UpcaIyTBBIxIEExcTJM7u3u8vSdKLqyhurbj6pzqk/1yPXHtgbDLQjGBjgBV/+3yJBF+lvP4ZJfxOU0AdRx9TudSP/YX/uWyHQKiAfY94x7nVvctsgKEuoTAIaALMZj6VPNrMT2FNyImMi8CN54LkY9M1AxKdBNAoLOZrMimGlRQILMDS1AjtEpYdvz7utkL8SOXCYKyR1G9I8MbMhs4qRN0+ObKdqyWRcZ7GXSALnb8ITbyseILMfzoNWalUzxamNVHs3oZ6Pee/fCwsKyHe23EMfY1PJCm+pa7DHkixY5iWks0gx3+hUFKDcq3sw1K3Xl4OtapGogql/PNPmzvh/KmMFbQgBG5qIwbfnGE7vArw2HkKWHO+d9Fa55NYS61lDPwVVh5/vLu4daosmxAc6ogxQA6rCUDFfK2XAoOXp/LjQLi07NXAjqWYH31aicnxSO9ZJNc/xSNUiK8fnV1aPdnJKmrruYi/5VgETVzBZYDutTbvUATvGJqhcrrcwFzNV+RemRHdLjhDj9aahqUek0U/lcNx9KQg8gGdsEGFOEAZP7NhEmlra6XO7ERxAqFY1IQowUW6lk8w9AaLDHpvxw8xjwSVdS3huJy+C8g1J9x0piTGR06CYHhxrP7pZzCj8z/qmecXaf/o0+08ZOzvkI+ZOUU8xdPJ1zXNt5OniAoekvT/f0vYI/tMoAAAAASUVORK5CYII="

pr_image = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAVCAYAAABPPm7SAAAAAXNSR0IArs4c6QAAAAlwSFlzAAALEwAACxMBAJqcGAAAAVlpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KTMInWQAAAbVJREFUOBGNlD0ohVEYxw/XZ4muiZHFbMFgllLKJKuFYlAWm0ExKCmT3WBS7qyLO8soE5uPRVEGHxf/33H+b++te+Nfv/s85/l6zznvvTeE+mpWuC2lpmSnk0+sKfk1ZlGritgTxVxmTP63mMnFcAv59ZYWFJXEm7gRaFx8CXK7YlZMCCsbQsFqig7I0rQvXgQ5hmLNpfxBgQqclUQ/K6lPcMY78SzqaVjBU9ElqhQsCYaUBU87E2hIPAly64LGA+FjrcnPdCSPQrZdzKIh+EhzKdYr66GHxFpS4jVZBvg1dci/FSPCQ6lnl4gHZgM8COsB7yl/QWESZ+beMnkRpymKtU/Rp6DGryyfiw/yAIobyZdWN/+fAXUbHfQAnxtr3zV563piNUf4SFWcmS03EjlqULSe2P0bCz2yvrD8TuxjXcs3MWpFn9xuWfDqzkVebiZ2Iqihlp5lEZ1tHIkvDYlJFlKr8I74JZIbFYieqo/wGEMhPCTbnizGO+hMsftkqY39G3KYXBJs70q4CeuHsJNrwYUfC3o2RdS8PjnXjvAluZEC+/wm+NeqiAUR5ad5jXXDX7HwA+nmXWV5F/zGAAAAAElFTkSuQmCC"

pr_merge_into_image = "iVBORw0KGgoAAAANSUhEUgAAABUAAAAVCAYAAACpF6WWAAAAAXNSR0IArs4c6QAAAAlwSFlzAAALEwAACxMBAJqcGAAAAVlpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDUuNC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KTMInWQAAAe9JREFUOBGllL9LllEUx580ymqIwhREQqilJahoEgzSpaFJmlxsKAhaoqm15v6BfqxFU1P4Byg0FAUKIi1CgvRDdCioIbPP533veTg+r/147cDnveece8/3nufeq1W1s+1Jaf0cp6n/d/9ZuKexVxSeIv8EnsFEWdNbxr8OWVR/C47CI1iGObgPZ+AH9EFXFl1eoGo+VT7Ev1viQyn/W3dvmlHUThdhDa7BRxiBB6DZbVemaHQ7ju8G8gI0z3Rfy2v/uHY/eCRR155p/MZlHCG/Cop+gMugKXKgjPkrvY+oxd1ucXEnSH+C6PY9/vntS1vRcX5PpnzUp1RVRXKY7AYoul5GN7kFp8GursMMvITbEBYaEdeiQ2S+gRdzE55DdK34EryBS+Bzew1joHWcb+xip99BoXOg3QPFQvytyWKzjFcjaKoq+hMGYQG8sItgkXYMPMN+uAFfwBrXTYFPsCffIHHduk9HAe1we6h8+J8LpjzLaXD+MShok1u50+jSjZ7CV1gBO50EixT2WLTN9lD/tgTrqDixwSjxqzTpX9OdEh8so2vzV/YSR319266NpB35ST4dX8FZeAfZvCxfhl8ndm2uw0LUiSvgTfuPJbp0XoGuLQvb7UBS2JVgqu9w82Ydk83EnxbnuR3PqykW8S+3vVJFVTuJIAAAAABJRU5ErkJggg=="

pr_status = {
    STATUS_NEEDS_WORK: "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAfElEQVQ4T2NkQAOpqanasxxmX0EXB/HTDqTqzJ49+yqyHCOMExoayrYqYPVPbBrRxcI2hLKvXr36F0gcbAApmmGGwQwBG/B/KcN/YmxGV8MYzcDIiM/PhAwFhQkjubbDDB81gIGB8jCgOBopTkhUScqkGoKRmZCTLKnZGQCX5FCXyXSbYwAAAABJRU5ErkJggg==",
    STATUS_UNAPPROVED: "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAQhJREFUOBFjZEADqamp2oyMjClAYTcgloNKPwLSu/7//z9n9uzZV6FiYIoRxgkNDWUTFBTsA/IzgZgJJo5G/wPyp79//75o9erVv0ByYANAmgUEBLYDbXZC04CVC3TJvg8fPniCDAHbBLKZWM1gW4EWQV3LwAj18yWgBC5nY3UFUPAf0CV6TNAAI1UzyFCwXpBGUGiTC9xABsCiihxD5MhxOopFIAMeoYiQxnkEMmAXaXpQVO9iAiVPoBAohZEKQNE4hwmatqeTqhuofjpILzgQQWkblDyJNQSkFqQHpJ4ZRFy7du2vsrLyCk5OTiEg1wSI4ZkMJI8EQF6dBswHcSiZCUkBA6nZGQBHemGgvqxYAAAAAABJRU5ErkJggg==",
    STATUS_APPROVED: "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAARlJREFUOBGVk7FtAkEQRf8MyKGRIKcBJFfgyAGWC6ADElIKQMgFkFlO3IELsCAgcgVINOAcJAgR3DJ/zKGT2V2dN7nT/HkzO7t/BX/W6/dz71RgGIA+Qui6LPIjwKKh+Jg8ztdVxOK/a7oe3BXb/QwBoxCClvHqV0QKCN61fT+e9j4P1LwA4dNm92XwUxVI/guWjU7rhUW806VzPZhVrZEz9iuc+Vhgldp2ahccp6l4UD+wxMwpmHE2JKt+2rnMjEZWr1eVSUxKds3R60oCEUFhJonE64WMVTqsXvZtFlmlPd1ht3o2QoasurfNntnsmGgMWT9EettMvYzlRWOW64yJXoCeprdF5S03DjXmlO+Axa+vsez03+d8BpC2a0RVWrdkAAAAAElFTkSuQmCC"
}


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
    r = requests.get(_url + API_PULL_REQUESTS, params=_params, timeout=5, headers=headers)

    body = r.json()
    pull_requests = body['values']

    is_last_page = body['isLastPage']
    if not is_last_page:
        _params['start'] = body['nextPageStart']
        pull_requests = pull_requests + get_pull_requests(_api_key, _url, _params)

    return pull_requests


def pr_should_be_reviewed_by_me(pr):
    reviewers_filtered = list(filter(lambda reviewer: reviewer['user']['slug'] == USER_SLUG, pr['reviewers']))

    if len(reviewers_filtered) > 0 and (
            True if not OMIT_REVIEWED_AND_APPROVED else reviewers_filtered[0]['status'] != STATUS_APPROVED
    ):
        pr['overallStatus'] = reviewers_filtered[0]['status']
        return pr


def pr_is_marked_as_needs_work(pr):
    reviewers_status = [reviewer['status'] for reviewer in pr['reviewers']]

    if STATUS_NEEDS_WORK in reviewers_status:
        pr['overallStatus'] = STATUS_NEEDS_WORK
    elif STATUS_APPROVED not in reviewers_status:
        pr['overallStatus'] = STATUS_UNAPPROVED
    else:
        pr['overallStatus'] = STATUS_APPROVED

    return pr


def epoch_ms_to_datetime(epoch_ms):
    return datetime.fromtimestamp(epoch_ms / 1000.0)


def abbreviate_string(s):
    return s[:ABBREVIATION_CHARACTERS] + "..." if len(s) > ABBREVIATION_CHARACTERS else s


def extract_pull_request_data(_pull_requests):
    pull_requests = list()

    for pr in _pull_requests:
        pr_activity = epoch_ms_to_datetime(pr['updatedDate'])
        time_ago = timeago.format(
            pr_activity.replace(tzinfo=timezone.utc)
                .astimezone(tz=None)
                .replace(tzinfo=None),
            datetime.now()
        )

        pull_requests.append(dict(
            title=abbreviate_string(pr['title']),
            slug=pr['toRef']['repository']['slug'],
            from_ref=pr['fromRef']['displayId'],
            to_ref=pr['toRef']['displayId'],
            overall_status=pr['overallStatus'],
            activity=pr_activity,
            time_ago=time_ago,
            href=pr['links']['self'][0]['href']
        ))

    return pull_requests


def sort_pull_requests(pull_requests):
    return sorted(pull_requests, key=lambda p: p['activity'],
                  reverse=True) if SORT_ON == 'activity' else sorted(pull_requests, key=lambda p: p['title'])


def print_prs(pr_type, pull_requests):
    print(pr_type + " | templateImage=" + bitbucket_image)
    print("---")

    prs_sorted_by_slug = sorted(pull_requests, key=lambda p: p['slug'])

    for repo, repo_prs in itertools.groupby(prs_sorted_by_slug, key=lambda p: p['slug']):
        repo_prs_list = list(repo_prs)
        repo_status = determine_repo_status(repo_prs_list)
        print(repo + " (" + str(len(repo_prs_list)) + ") | image = " + pr_status[repo_status])

        prs_sorted_by_to_ref = sorted(repo_prs_list, key=lambda p: p['to_ref'])

        for to_ref, to_ref_prs in itertools.groupby(prs_sorted_by_to_ref, key=lambda p: p['to_ref']):
            to_ref_prs_list = sort_pull_requests(list(to_ref_prs))
            print("--" + to_ref)

            for pr in to_ref_prs_list:
                print("--" +
                      pr['from_ref'] + " -- " + pr['title'] + " - " + pr['time_ago'] + "|href=" + pr['href']
                      + " image=" + pr_status[pr['overall_status']]
                      )


def determine_repo_status(prs_list):
    statuses = [pr['overall_status'] for pr in prs_list]

    if STATUS_UNAPPROVED in statuses:
        return STATUS_UNAPPROVED
    elif STATUS_NEEDS_WORK in statuses:
        return STATUS_NEEDS_WORK
    else:
        return STATUS_APPROVED


if __name__ == "__main__":
    prs_to_review = None
    prs_authored_with_work = None
    exception = None

    try:
        prs_to_review = extract_pull_request_data(
            get_open_pull_requests_to_review(PRIVATE_TOKEN, BITBUCKET_HOST)
        )
        prs_authored_with_work = extract_pull_request_data(
            get_authored_pull_requests_with_work(PRIVATE_TOKEN, BITBUCKET_HOST)
        )
    except Timeout as e:
        exception = "timeout"
    except ConnectionError as e:
        exception = "connection error"
    except Exception as e:
        exception = "unknown error"

    if exception is not None:
        print("? | templateImage=" + pr_image)
        print("---")
        print("Error: " + exception + "|templateImage=" + bitbucket_image)
    else:
        # Set menubar icon
        total_prs_to_review = len(prs_to_review)
        total_prs_authored_with_work = len(prs_authored_with_work)
        total_prs = str(total_prs_to_review + total_prs_authored_with_work)
        print(total_prs + " | templateImage=" + pr_image)

        # Start menu items
        if total_prs == 0:
            print("---")
            print("Nothing to review! | image = " + pr_status[STATUS_APPROVED])

        if total_prs_to_review > 0:
            print("---")
            print_prs("Reviewing", prs_to_review)

        if total_prs_authored_with_work > 0:
            print("---")
            print_prs("Authored", prs_authored_with_work)
