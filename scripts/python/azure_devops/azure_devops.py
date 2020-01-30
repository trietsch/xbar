from datetime import datetime
from typing import List

from azure.devops.connection import Connection
from azure.devops.v5_1.git import GitPullRequestSearchCriteria, GitPullRequest
from msrest.authentication import BasicAuthentication
from requests import Timeout

from .config import AzureDevOpsConfig
from ..common.util import abbreviate_string
from ..pull_requests import PullRequest, PullRequestStatus, PullRequestsOverview


class AzureDevOpsClientFactory(object):
    _connection_factory = Connection(
        base_url=AzureDevOpsConfig.ORGANIZATION_URL,
        creds=BasicAuthentication('', AzureDevOpsConfig.PERSONAL_ACCESS_TOKEN)
    )

    @staticmethod
    def get_git_client():
        return AzureDevOpsClientFactory._connection_factory.clients.get_git_client()


class PullRequestClient(object):
    def __init__(self):
        self._git_client = AzureDevOpsClientFactory.get_git_client()

    def get_pull_requests_overview(self, project, pr_status, user_email) -> PullRequestsOverview:
        _prs_to_review: List[PullRequest] = []
        _prs_authored_with_work: List[PullRequest] = []
        _exception = None

        try:
            _prs_to_review = self._get_pull_request_to_be_reviewed_by(project, pr_status, user_email)

        except Timeout as e:
            _exception = "timeout"
        except ConnectionError as e:
            _exception = "connection error"
        except Exception as e:
            _exception = "unknown error"

        return PullRequestsOverview(_prs_to_review, _prs_authored_with_work, _exception)

    def _get_pull_requests_for_project(self, project, pr_status) -> List[GitPullRequest]:
        return self._git_client.get_pull_requests_by_project(project,
                                                             GitPullRequestSearchCriteria(status=pr_status))

    def _get_pull_request_to_be_reviewed_by(self, project, pr_status, user_email) -> List[PullRequest]:
        prs = self._get_pull_requests_for_project(project, pr_status)

        prs_to_review_by_user = list(
            filter(lambda pr: user_email in
                              map(lambda reviewer: reviewer.unique_name, pr.reviewers),
                   prs)
        )

        return GitPullRequestMapper.to_pull_requests(prs_to_review_by_user)


class GitPullRequestMapper(object):
    _votes_mapping = {
        -10: "REJECTED",
        -5: "WAITING_FOR_AUTHOR",
        0: "UNAPPROVED",
        5: "APPROVED_WITH_SUGGESTIONS",
        10: "APPROVED"
    }

    @staticmethod
    def _short_ref(ref_name: str):
        return ref_name.replace('refs/heads/', '')

    @staticmethod
    def _to_pull_request(ado_pr: GitPullRequest) -> PullRequest:
        repo_href = f"{AzureDevOpsConfig.ORGANIZATION_URL}/{ado_pr.repository.project.name}/_git/{ado_pr.repository.name}"
        pr_href = f"{repo_href}/pullrequest/{ado_pr.pull_request_id}"

        return PullRequest(
            id=str(ado_pr.pull_request_id),
            title=abbreviate_string(ado_pr.title, AzureDevOpsConfig.ABBREVIATION_CHARACTERS),
            slug=f"ado-{ado_pr.pull_request_id}",
            from_ref=GitPullRequestMapper._short_ref(ado_pr.source_ref_name),
            to_ref=GitPullRequestMapper._short_ref(ado_pr.target_ref_name),
            overall_status=PullRequestStatus.UNAPPROVED,  # TODO Map this
            activity=datetime.now(),  # TODO fix datetime
            time_ago="some time ago!",  # TODO fix timeago
            repo_href=repo_href,
            href=pr_href
        )

    @staticmethod
    def to_pull_requests(ado_pull_requests: List[GitPullRequest]) -> List[PullRequest]:
        return [GitPullRequestMapper._to_pull_request(ado_pr) for ado_pr in ado_pull_requests]
