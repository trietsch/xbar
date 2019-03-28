#!/Users/rtrietsch/.pyenv/versions/3.6.1/bin/python3.6
# -*- coding: utf-8 -*-

# <bitbar.title>Gitlab CI (CCMenu functionality)</bitbar.title>
# <bitbar.desc>Shows the most recent build status for your projects</bitbar.desc>
# <bitbar.version>CHANGE_ME</bitbar.version>
# <bitbar.author>Robin Trietsch</bitbar.author>
# <bitbar.author.github>trietsch</bitbar.author.github>
# <bitbar.dependencies>python3</bitbar.dependencies>
# <bitbar.image>CHANGE_ME_TO_GITHUB_IMAGE_PREVIEW</bitbar.image>
# <bitbar.abouturl>CHANGE_ME_TO_GITHUB_URL</bitbar.abouturl>

# Settings can be found in the .gitlab-config.py file
# You don't have to change anything below
# -------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------

import json
import math
import os
from configparser import ConfigParser
from datetime import datetime
from enum import Enum

import dateutil.parser
import requests

# Get preferences
config = ConfigParser()
config.read(os.path.dirname(os.path.realpath(__file__)) + '/.gitlab-config.ini')
preferences = config._sections

CHECK_MEMBERSHIP = bool(preferences['preferences']['check_membership'])
CHECK_STARRED_ONLY = bool(preferences['preferences']['check_starred_only'])
SORT_ON = preferences['preferences']['sort_on']

GITLAB_HOSTS = json.loads(preferences['preferences']['gitlab_hosts'])

# API paths
API_PROJECTS = '/api/v4/projects'
API_PIPELINES = '/pipelines'

# Pipeline status
PipelineStatus = Enum('Status', 'SUCCESS FAILURE FAILURE_BUILDING SUCCESS_BUILDING INACTIVE MANUAL')
GitlabCiStatus = Enum('CiStatus', 'running pending success failed canceled skipped manual')

# Gitlab Favicon
gitlab_image = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAOCAYAAAAmL5yKAAAAAXNSR0IArs4c6QAAAi5JREFUKBV1Us9rE1EQnpm3+bFpatMG0tJE6o9YF+JJaIoKRbOlh5YcPBvx7kE8qBQvXvwH/Ac86aV/gBTBm17sWSVNLUYrWg+i2Cab7L43zm6zREIdeDvz3vfN92ZmH8DA9lwn/9l1Hsb7//l2zVnfdy9MxzjFATNVEej+l9p8MT4b9buSSIj3uqwvx9hQgGB13KKcAVWLwVGv2CxlLcojwmqMRQLvrlaywLwSMAMQ1GNw1BNxXQsFGJY/Lp+ZCPFIYMwPFiQodwMDYGDpQ9XJjya3FssnjIaaJxwLcI48+1LIscLPVJXXrJ9MvmaW8qYzB/i0fc35hpG8XCi6dg4K6TEzK3S2FKKeMmvwGjaRN0q26dtb9AkrZh8AFUD/F8HvPQIRiyzsbKJoIDlpgLWUXZBCT3GLUsmLVtBLLxJhRZeE+0cmcQhItuGAELSGSIIIGG0DJpB9RjRKwlF0LvD0FWJDHbnpq7KFe1ZELGCSJhMZFjWpV1ZSYpWQZMFCjspEut8t4gNK3tp+29fosg+bKidSp6VywdPj4biPLJXlo3bmpMNJRPb5FRrtYqP5JhpT+maz2fZ7102fH0l/XSoipGwGknmEKy0V0Kw8sxnoGR8eY7JTx8bO+1A+qmVwUeT8Z+UVAnpCu+j82BJY5lZYYOQytAzyXevG9ot/+YMfNTxKNHZeegpdKJrnWXnx2RlAc5I3PBW4o8nDrGMiGR4drs/f7jw4f0diaeR4+wuHx8azyo51NwAAAABJRU5ErkJggg=="


def get_projects(api_key, url):
    """
    Parse all pages of projects
    :return: list
    """
    return get_project_page(api_key, url, 1, [])


# Get projects and print build status
def get_project_page(_api_key, _url, _page, _projects):
    params = dict(
        private_token=_api_key,
        per_page=100,
        page=_page,
        membership=CHECK_MEMBERSHIP,
        starred=CHECK_STARRED_ONLY,
        simple='true'
    )
    r = requests.get(_url + API_PROJECTS, params=params)

    # Parse the JSON returned by GitLab and extract the projects
    result = _projects + r.json()

    nextpage = r.headers.get('X-Next-Page')
    if nextpage:
        result = get_project_page(_api_key, _url, nextpage, result)

    return result


def get_most_recent_project_pipeline_status(_api_key, _url, _project_id, _element_index=0):
    number_of_page_elements = 2 + _element_index

    params = dict(
        private_token=_api_key,
        per_page=number_of_page_elements,
        order_by='id',
        sort='desc'
    )
    r = requests.get(_url + API_PROJECTS + "/" + str(_project_id) + API_PIPELINES, params=params)

    result = r.json()

    if len(result) == 0 or r.status_code != 200:
        return PipelineStatus.INACTIVE

    current_job_status = result[_element_index]['status']
    previous_job_status = result[_element_index + 1]['status']

    # Current is running, previous is successful
    if ((current_job_status == GitlabCiStatus.running.name or
         current_job_status == GitlabCiStatus.pending.name) and
            previous_job_status == GitlabCiStatus.success.name):
        return PipelineStatus.SUCCESS_BUILDING
    elif ((current_job_status == GitlabCiStatus.running.name or
           current_job_status == GitlabCiStatus.pending.name) and
          previous_job_status == GitlabCiStatus.failed.name):
        return PipelineStatus.FAILURE_BUILDING
    elif current_job_status == GitlabCiStatus.success.name:
        return PipelineStatus.SUCCESS
    elif current_job_status == GitlabCiStatus.failed.name:
        return PipelineStatus.FAILURE
    elif current_job_status == GitlabCiStatus.manual.name:
        return PipelineStatus.MANUAL
    elif current_job_status == GitlabCiStatus.canceled.name or current_job_status == GitlabCiStatus.skipped.name:
        return get_most_recent_project_pipeline_status(_api_key, _url, _project_id, _element_index + 1)
    else:
        print("Current Job Status: " + current_job_status)


def get_status_image(_pipeline_status):
    icon_success = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAAbdJREFUOBGVU80rRFEUP+fOYxrlI/bWirCyMIySjI+NjbJTWBArlmp6jZWNUmTjPyB2GIuRhiyF+AOU1GSIjeK9e5xzzXvd1Kvnbu655/x+5/si/Dn5i2y7r2GOAIaBqNWYER8R4DShYDfXV7i3Kaz/Pe79ZK1+/dgAggUiUoHevhFRA8KOam5Ydtv3vsRmHAjZr7wfM3nQJkTKCMVES+OoODGRqpHjkcUrBzIcFtG9HO/QvncTlXaQBQJucl/qmT0jOinHUdCpyPdmY5DPOjINK0kgl4v+FAfCkWY7ptuiiT5PyqmbeniAhEbcZ2YqgApXhaOqajnVF87vzTwRvsFRk276sEyVj02O2hOQzc1jNk0MlZwe1zVU4yQGEKHMlS6vpU+ucucj05poPsRZguJoj+GbIPVNkM31Ht0lAbvXMoWtfCnbRah3QowtMFfJhtk6LmmdI7qrmcKzez3R5BEd8NjCum2scFFW19Nw+3cSCnGD025jwphNCuRgjGYTc6XsFmlaDIxxblS4ne8vLJkmym7zfItxiAbDWMPhh3EgOy27LV7Nh4nwJDbBBP9AYKYEG//f7/wDKPq20ttyqQEAAAAASUVORK5CYII='
    icon_failure = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAAYpJREFUOBGVk0tKA0EQhqtjyMozeACj8Q5ZBHIBNSKo4EZ0FQh4BheuHNwoPuNj41aIkDsYNQeYK+hKTfT7OzOTVlScgmLq9f9V1d3j7Js8mZUHZuvOrEZqKknHH2adCbODshklY6FuJERLAHcJbFBcSOPhl9yQ3D5ETYhelfMECfgWvxoC/rC7kNRF4jupcw6weKsJxpx2Hpr1grF3KOihx2gRlQwYdRVV7bYCWofulYIOLABr+X7FrM2IDereE23Mmp1T1xdYIoywRZhqOJnQ4fCR3djv8oHOJBzgG2KL5I6yQiXAOoqeIZgME9h+ZHVVnDWXYDrFZLCxQPDiD3Ec+mK9pR5g2eGgacofUow3nUXoDuvyjNk10y0oziSyHQwXuOEUsU75Ds0IGGsN8BWAeQBtcoadkpSInSkmwe78eI20uGfsE2qya8RegXwOUEtgbH+NfP2l7/HZlJ1DIq57yx8iHZsAuznAesrCjH4avWkCdfxIo/1GlOQi1QqjOr9CCNDTZv9//86fOzh2PypLeVgAAAAASUVORK5CYII='
    icon_failure_building = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAbtJREFUOBGtU00ohFEUPW8aSlEsxGq21GDBhlLKYhqspFiJhTCZ1ayoWcxCsrIQzRQb7JSs/NdkobCw8ZNsZ0XJwkZJ85z7fj5m2ChvenPfO/ec+969930KZUOvIIowJgjHOCPOXaA9xgfWVRJ3DjNG+Y3OoBKNWOI+AYWQx0usRpH7LB6RUhm8i88EcOID7nrLBJvEosQ6yvA8g/RJEHuSnFwuBq6I7eIVPdDYLwkgXHtbKJfzNck2mMYbBaMqgR0v0suoZ4IP5NR5jJwia9IWNgXzYvFqjItY5xDnupakS4rlBnLAIucspyQfEq2AUm0/bijeNmJFkcIYxed0NvO8tJrCHIPeejJtTAL4VsnpQpYxyan4i9M2CMB1t7MXxtq/iM3bI1+pmBZ52NkKY20rA5cEKAQ7jU5HOnPYE291xLXmXDOYQpfziSlIgJMAUGhh/gsszzyxe+YtATco71fTONRZDHPfGvD5On+20XpfaJpYtGdPpniIddjirDKYa6N9iTms0DHjyc7u8RGNoJpdCiFNrL3Er7HKWyVtEfm2ec18CQEYQA1OKR78RSxPOSX8//mYvp/818/5E8gChFfaQn19AAAAAElFTkSuQmCC'
    icon_success_building = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAiZJREFUOBGVUz1oU1EUPuc+6zOooC0S6NC1QvwBdWihJSS2pdZJxDr5M4ggOnWy+DolFhed/Bl0sV2kRToZNa1pCkJ1cFGrdHUQiuJoSmru8Ts379aX6uIheefe75zv/N17mbbIRCWXoaDtEpEMkVCXMzN9IeIyNTYeFfKLK0kK+82Zmcz27nTnHSa+Asx4fIu2QvJgde3r2OzoSl1tLkBMfg5yPkkQoSlmygA72oKTVBDkhAZxmeLMLWQQ3pE05mrrlBWRUjKAJlKOYhz3/B5rFwwl1qQh527mF5560nipf1+wM7WKcvd6DNpiJoe2NQf2p2cmuVgEOVo8PswU7JE6veWQSqjCEPMtEK/HQYxykRXTjgVOHwrZhRklkzElYbpAoSxjUvthiwrZ8jj0R++vXLN5VEDR27Iamc1lrCE0jE/aYcb0qRaiN6qd4Jhd335vCWVChNkdkcedFmlTjT5sEsdeL0lTMKQeXYm1r50WWcPuJQaLn33oMJJe1U7ANWJpfnPPfCCqDk6i7CJ6/fxLNnpwcx6TtSPF3KsXE0sDo7Ad9P5otvzXMcbGHz9tvft2rvrdO9+oDJzmgKcxm1SMuWN0NzFaGrwLw1Xv3NTyrLbOZ8NQhpA1guORpB093Stm56+5oendBlBJOqC8kztCqYJ46h9kvcpj6h/o59Pst0Z6JPWkY9fudlRyDJCrDJk78T+sPrHoY7oP8vmWx+Stqv/3Of8GAyfgwIRMWmoAAAAASUVORK5CYII='
    icon_inactive = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAQhJREFUOBFjZEADqamp2oyMjClAYTcgloNKPwLSu/7//z9n9uzZV6FiYIoRxgkNDWUTFBTsA/IzgZgJJo5G/wPyp79//75o9erVv0ByYANAmgUEBLYDbXZC04CVC3TJvg8fPniCDAHbBLKZWM1gW4EWQV3LwAj18yWgBC5nY3UFUPAf0CV6TNAAI1UzyFCwXpBGUGiTC9xABsCiihxD5MhxOopFIAMeoYiQxnkEMmAXaXpQVO9iAiVPoBAohZEKQNE4hwmatqeTqhuofjpILzgQQWkblDyJNQSkFqQHpJ4ZRFy7du2vsrLyCk5OTiEg1wSI4ZkMJI8EQF6dBswHcSiZCUkBA6nZGQBHemGgvqxYAAAAAABJRU5ErkJggg=='
    icon_pause = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAR1JREFUOBGlUzsOgkAQ3cWEhA48AA2liZUnsCDxALRWUth6EEspsKA04QAmFB7CRA7ABaDTkAjOWxcCG2MUJllm5/PeDLs7nCni+/6Mc74ht0vLluGMdFLX9TEMw5v0CcUbw/M83bKsPdlbWlrjV3RFdpDn+S6O4xIxQQCwaZpnqrxUAB9N6uRSFMUKJKISKv8KFlWpkOyWcfnPVwq0bZdlaSBR1/U7tGrDR1JRJ3NNHlgLRiSKogcW9hDVfnuZwAKI0x4qLgiaqxpCYvdaH8IAgmwIUGIyECQjCJLx1yjfdtDtAvffvAH4VVvmBsCKQ8TbxvPsknzbIxcY5EzwSdP06TjOyTCMKZkLWu2QId4RDNOB5mDdG6ZOAvt3nF9NcH5P4R94wQAAAABJRU5ErkJggg=='

    if _pipeline_status == PipelineStatus.SUCCESS:
        return icon_success
    elif _pipeline_status == PipelineStatus.FAILURE:
        return icon_failure
    elif _pipeline_status == PipelineStatus.FAILURE_BUILDING:
        return icon_failure_building
    elif _pipeline_status == PipelineStatus.SUCCESS_BUILDING:
        return icon_success_building
    elif _pipeline_status == PipelineStatus.INACTIVE:
        return icon_inactive
    elif _pipeline_status == PipelineStatus.MANUAL:
        return icon_pause


def relative_time(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """

    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(math.floor(second_diff)) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(math.floor(second_diff / 60)) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(math.floor(second_diff / 3600)) + " hours ago"
    if day_diff == 1:
        return "yesterday"
    if day_diff < 7:
        return str(math.floor(day_diff)) + " days ago"
    if day_diff < 31:
        return str(math.floor(day_diff / 7)) + " weeks ago"
    if day_diff < 365:
        return str(math.floor(day_diff / 30)) + " months ago"
    return str(math.floor(day_diff / 365)) + " years ago"


if __name__ == "__main__":
    # First collect all info about the projects, in order to determine the overall status
    overall_status = PipelineStatus.INACTIVE
    bitbar_gitlab_projects = []

    # Overall status counters
    status_failure_building = 0
    status_success_building = 0
    status_failure = 0
    status_success = 0

    for gitlab_instance in GITLAB_HOSTS:
        host = preferences[gitlab_instance]['host']
        private_token = preferences[gitlab_instance]['private_token']

        gitlab_instance_projects = []

        try:
            projects = get_projects(private_token, host)

            for project in projects:
                project_id = project['id']
                project_name_and_path = project['path_with_namespace']
                project_href = project['web_url'] + "/pipelines"
                project_activity = dateutil.parser.parse(project['last_activity_at'])

                pipeline_status = get_most_recent_project_pipeline_status(
                    private_token,
                    host,
                    project_id
                )

                if pipeline_status == PipelineStatus.FAILURE_BUILDING:
                    status_failure_building += 1
                elif pipeline_status == PipelineStatus.SUCCESS_BUILDING:
                    status_success_building += 1
                elif pipeline_status == PipelineStatus.FAILURE:
                    status_failure += 1
                elif pipeline_status == PipelineStatus.SUCCESS:
                    status_success += 1

                time_ago = relative_time(project_activity.replace(tzinfo=None))

                gitlab_instance_projects.append(dict(
                    id=project_id,
                    name=project_name_and_path,
                    activity=project_activity,
                    time_ago=time_ago,
                    href=project_href,
                    status=pipeline_status,
                    image=get_status_image(pipeline_status)
                ))

            bitbar_gitlab_projects.append(dict(gitlab_name=gitlab_instance, projects=gitlab_instance_projects))
        except:
            bitbar_gitlab_projects.append(dict(gitlab_name=gitlab_instance, projects=gitlab_instance_projects))
            continue

    # Now construct the bitbar menu
    if status_failure_building > 0:
        overall_status = PipelineStatus.FAILURE_BUILDING
    elif status_success_building > 0:
        overall_status = PipelineStatus.SUCCESS_BUILDING
    elif status_failure > 0:
        overall_status = PipelineStatus.FAILURE
    elif status_success > 0:
        overall_status = PipelineStatus.SUCCESS

    # Set menubar icon
    if overall_status == PipelineStatus.FAILURE:
        print(str(status_failure) + "|image=" + get_status_image(overall_status))
    else:
        print("|image=" + get_status_image(overall_status))

    for gitlab_instance in bitbar_gitlab_projects:
        # Start menu items
        gitlab_name = gitlab_instance['gitlab_name']
        print("---")
        print(gitlab_name + "|templateImage=" + gitlab_image)

        sorted_projects = sorted(gitlab_instance['projects'], key=lambda p: p['activity'],
                                 reverse=True) if SORT_ON == 'activity' else sorted(gitlab_instance['projects'],
                                                                                    key=lambda p: p['name'])

        for project in sorted_projects:
            print(project['name'] + "  -  " + project['time_ago'] + "|href=" + project['href'] + " image=" + project[
                'image'])
