import traceback
from typing import List

from gitlab import Gitlab
from gitlab.v4.objects import ProjectMergeRequest
from requests import Timeout

from .config import GitlabMrsConfig, GitlabMrsConstants
from ..common.util import abbreviate_string, time_ago, zulu_timestamp_string_to_datetime
from ..pull_requests import PullRequestStatus, PullRequest, PullRequestsOverview, PullRequestException


def get_merge_requests_to_review(_author_id, _mrs):
    mrs_and_overall_status = list()

    for mr in _mrs:
        if mr.author["id"] != _author_id:
            approvals = list(
                filter(lambda approval: approval["user"]["id"] == _author_id, mr.approvals.get().approved_by))

            if len(approvals) != 0 and not GitlabMrsConfig.OMIT_REVIEWED_AND_APPROVED:
                mrs_and_overall_status.append(get_overall_status(mr, _author_id))
            else:
                mrs_and_overall_status.append(get_overall_status(mr, _author_id))

    return mrs_and_overall_status


def get_authored_merge_requests(_author_id, _mrs):
    mrs_and_overall_status = list()

    for mr in _mrs:
        if mr.author["id"] == _author_id:
            mrs_and_overall_status.append(get_overall_status(mr, _author_id))

    return mrs_and_overall_status


def get_overall_status(_mr, _author_id) -> (ProjectMergeRequest, PullRequestStatus):
    unresolved_threads = list(filter(lambda note: not getattr(note, 'resolved', True), _mr.notes.list()))
    approvals = list(filter(lambda approval: approval["user"]["id"] != _author_id, _mr.approvals.get().approved_by))

    if len(unresolved_threads) > 0:
        return _mr, PullRequestStatus.NEEDS_WORK
    elif len(approvals) > 0:
        return _mr, PullRequestStatus.APPROVED
    else:
        return _mr, PullRequestStatus.UNAPPROVED


def extract_pull_request_data(_raw_merge_requests) -> List[PullRequest]:
    merge_requests: List[PullRequest] = list()

    for mr, overall_status in _raw_merge_requests:
        pr_activity = zulu_timestamp_string_to_datetime(mr.updated_at)

        merge_requests.append(PullRequest(
            id=str(mr.iid),
            title=abbreviate_string(mr.title, GitlabMrsConfig.ABBREVIATION_CHARACTERS),
            slug=mr.references["full"].replace(mr.references["short"], ""),
            from_ref=mr.source_branch,
            to_ref=mr.target_branch,
            overall_status=overall_status,
            activity=pr_activity,
            time_ago=time_ago(pr_activity),
            all_prs_href=mr.web_url.replace(f"/{mr.iid}", ""),
            href=mr.web_url
        ))

    return merge_requests


def group_mrs(_gl):
    group = _gl.groups.get(GitlabMrsConfig.GROUP_NAME)
    all_open_mrs = group.mergerequests.list(state="opened", all=True)

    # Ensure we only keep MRs that have none of the labels in the exclusions list
    mrs = list(
        filter(
            lambda mr: len(GitlabMrsConfig.EXCLUDE_MRS_WITH_LABELS.intersection(mr.labels)) == 0, all_open_mrs
        )
    )

    projects_and_mrs = list()
    projects = dict()
    for mr in mrs:
        if mr.project_id in projects:
            project = projects[mr.project_id]
        else:
            project = _gl.projects.get(mr.project_id, lazy=True)
            projects[mr.project_id] = project

        projects_and_mrs.append(project.mergerequests.get(mr.iid))

    return projects_and_mrs


def get_merge_request_overview() -> PullRequestsOverview:
    _prs_to_review: List[PullRequest] = []
    _prs_authored_with_work: List[PullRequest] = []
    _exception = None

    _gl = Gitlab(url=GitlabMrsConfig.GITLAB_HOST, private_token=GitlabMrsConfig.PRIVATE_TOKEN)
    _gl.auth()
    _author_id = _gl.user.id

    mrs = group_mrs(_gl)

    try:
        _prs_to_review: List[PullRequest] = extract_pull_request_data(
            get_merge_requests_to_review(_author_id, mrs)
        )
        _prs_authored_with_work: List[PullRequest] = extract_pull_request_data(
            get_authored_merge_requests(_author_id, mrs)
        )
    except Timeout as e:
        _exception = PullRequestException(GitlabMrsConstants.MODULE, GitlabMrsConstants.TIMEOUT_MESSAGE, e,
                                          traceback.format_exc())
    except ConnectionError as e:
        _exception = PullRequestException(GitlabMrsConstants.MODULE, GitlabMrsConstants.CONNECTION_MESSAGE, e,
                                          traceback.format_exc())
    except Exception as e:
        _exception = PullRequestException(GitlabMrsConstants.MODULE, GitlabMrsConstants.UNKNOWN_MESSAGE, e,
                                          traceback.format_exc())

    return PullRequestsOverview.create(_prs_to_review, _prs_authored_with_work, _exception)
