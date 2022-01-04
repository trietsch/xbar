from datetime import datetime, timedelta

import requests

from . import PipelineStatus, GitlabConfig, GitlabCiStatus


def get_projects(api_key, url, only_projects_last_weeks):
    """
    Parse all pages of projects
    :return: list
    """
    if only_projects_last_weeks is not None:
        last_activity_after = (datetime.today() - timedelta(weeks=2)).replace(microsecond=0).isoformat() + 'Z'
        return get_project_page(api_key, url, last_activity_after, 1, [])
    else:
        return get_project_page(api_key, url, None, 1, [])


# Get projects and print build status
def get_project_page(_api_key, _url, _last_activity_after, _page, _projects):
    params = dict(
        private_token=_api_key,
        per_page=100,
        page=_page,
        membership=GitlabConfig.CHECK_MEMBERSHIP,
        starred=GitlabConfig.CHECK_STARRED_ONLY,
        simple='true'
    )
    if _last_activity_after is not None:
        params['last_activity_after'] = _last_activity_after

    r = requests.get(_url + GitlabConfig.API_PROJECTS, params=params, timeout=5)

    # Parse the JSON returned by GitLab and extract the projects
    result = _projects + r.json()

    nextpage = r.headers.get('X-Next-Page')
    if nextpage:
        result = get_project_page(_api_key, _url, _last_activity_after, nextpage, result)

    return result


def get_most_recent_project_pipeline_status(_api_key, _url, _project_id, _element_index=0):
    number_of_page_elements = 2 + _element_index

    params = dict(
        private_token=_api_key,
        per_page=number_of_page_elements,
        order_by='id',
        sort='desc'
    )
    r = requests.get(_url + GitlabConfig.API_PROJECTS + "/" + str(_project_id) + GitlabConfig.API_PIPELINES,
                     params=params)

    result = r.json()

    if len(result) == 0 or r.status_code != 200:
        return PipelineStatus.INACTIVE, None

    elif len(result) > 1:
        current_job_status = result[_element_index]['status'].lower()
        current_job_web_url = result[_element_index]['web_url']
        previous_job_status = GitlabCiStatus.unknown.name if _element_index + 1 >= len(result) else \
            result[_element_index + 1]['status'].lower()

        # Current is running, previous is successful
        if ((current_job_status == GitlabCiStatus.running.name or
             current_job_status == GitlabCiStatus.pending.name) and
            (previous_job_status == GitlabCiStatus.success.name or
             previous_job_status == GitlabCiStatus.manual.name)):
            return PipelineStatus.SUCCESS_BUILDING, current_job_web_url
        elif ((current_job_status == GitlabCiStatus.running.name or
               current_job_status == GitlabCiStatus.pending.name) and
              previous_job_status == GitlabCiStatus.failed.name):
            return PipelineStatus.FAILURE_BUILDING, current_job_web_url
        elif current_job_status == GitlabCiStatus.success.name:
            return PipelineStatus.SUCCESS, current_job_web_url
        elif current_job_status == GitlabCiStatus.failed.name:
            return PipelineStatus.FAILURE, current_job_web_url
        elif current_job_status == GitlabCiStatus.manual.name:
            return PipelineStatus.MANUAL, current_job_web_url
        elif current_job_status == GitlabCiStatus.running.name:
            return PipelineStatus.SUCCESS_BUILDING, current_job_web_url
        elif current_job_status == GitlabCiStatus.canceled.name or current_job_status == GitlabCiStatus.skipped.name:
            # Exclude cancelled and skipped pipelines, i.e. go to the next pipeline
            # Verify whether it's actually possible to retrieve the next element
            next_index = _element_index + 1
            if next_index >= len(result) - 1:  # if there is no next element, fall back to unknown
                return PipelineStatus.UNKNOWN, ""

            return get_most_recent_project_pipeline_status(_api_key, _url, _project_id, next_index)
        else:
            # Unhandled pipeline statuses end up here
            return PipelineStatus.ERROR, current_job_status

    elif len(result) == 1:
        current_job_status = result[_element_index]['status'].lower()
        current_job_web_url = result[_element_index]['web_url']

        if current_job_status == GitlabCiStatus.running.name or current_job_status == GitlabCiStatus.pending.name:
            return PipelineStatus.SUCCESS_BUILDING, current_job_web_url
        elif current_job_status == GitlabCiStatus.success.name:
            return PipelineStatus.SUCCESS, current_job_web_url
        elif current_job_status == GitlabCiStatus.failed.name:
            return PipelineStatus.FAILURE, current_job_web_url
        elif current_job_status == GitlabCiStatus.manual.name:
            return PipelineStatus.MANUAL, current_job_web_url
