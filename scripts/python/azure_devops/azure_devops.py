from datetime import datetime
from typing import List

from azure.devops.connection import Connection
from azure.devops.v5_1.git import GitPullRequestSearchCriteria, GitPullRequest
from msrest.authentication import BasicAuthentication

from .config import AzureDevOpsConfig
from ..pull_requests import PullRequest, PullRequestStatus


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

    def get_pull_requests_for_project(self, project, pr_status) -> List[GitPullRequest]:
        return self._git_client.get_pull_requests_by_project(project,
                                                             GitPullRequestSearchCriteria(status=pr_status))

    def get_pull_request_to_be_reviewed_by(self, project, pr_status, user_email) -> List[GitPullRequest]:
        pull_requests = self.get_pull_requests_for_project(project, pr_status)

        return list(
            filter(lambda pr: user_email in map(lambda reviewer: reviewer.unique_name, pr.reviewers), pull_requests))


class GitPullRequestMapper(object):
    _votes_mapping = {
        -10: "REJECTED",
        -5: "WAITING_FOR_AUTHOR",
        0: "NO_VOTE",
        5: "APPROVED_WITH_SUGGESTIONS",
        10: "APPROVED"
    }

    @staticmethod
    def to_pull_requests(ado_pull_requests: List[GitPullRequest]) -> List[PullRequest]:
        # pull_requests: List[PullRequest] = list()

        return [PullRequest(
            id=f"ado-{ado_pr.pull_request_id}",
            title=ado_pr.title,
            slug="slug",
            from_ref="from_ref",
            to_ref="to_ref",
            overall_status=PullRequestStatus.UNAPPROVED,  # Map this
            activity=datetime.now(),
            time_ago="time_ago",
            repo_href="repo_href",
            href="href"
        ) for ado_pr in ado_pull_requests]

        # ado_pr: GitPullRequest
        # for ado_pr in ado_pull_requests:
        #     pr = PullRequest(
        #         id=f"ado-{ado_pr.pull_request_id}",
        #         title=ado_pr.title,
        #         slug="<slug>",
        #         from_ref="<from_ref>",
        #         to_ref="<to_ref>",
        #         overall_status=PullRequestStatus.UNAPPROVED,
        #         activity=datetime.now(),
        #         time_ago="<time_ago>",
        #         repo_href="<repo_href",
        #         href="<href>"
        #     )
