import traceback
from typing import List, Dict
from urllib.parse import quote

from azure.devops.connection import Connection
from azure.devops.v7_1.git.models import GitPullRequestSearchCriteria, GitPullRequest, IdentityRefWithVote
from msrest.authentication import BasicAuthentication
from pydantic import ValidationError
from requests import Timeout

from .config import AzureDevOpsSettings
from .constants import AzureDevOpsConstants
from ...common.util import abbreviate_string, time_ago
from .. import PullRequest, PullRequestStatus, PullRequestsOverview, PullRequestException


def get_pull_requests_overview() -> PullRequestsOverview:
    try:
        settings = AzureDevOpsSettings()
    except ValidationError as e:
        return PullRequestsOverview.create([], [], PullRequestException(
            AzureDevOpsConstants.MODULE,
            f"Configuration error: {e}",
            e,
            traceback.format_exc()
        ))
    return PullRequestClient(settings).get_pull_requests_overview()


class PullRequestClient(object):
    def __init__(self, settings: AzureDevOpsSettings):
        self._settings = settings
        self._mapper = GitPullRequestMapper(settings)
        connection = Connection(
            base_url=settings.organization_url,
            creds=BasicAuthentication('', settings.personal_access_token)
        )
        self._git_client = connection.clients.get_git_client()

    def get_pull_requests_overview(self) -> PullRequestsOverview:
        _prs_to_review: List[PullRequest] = []
        _prs_authored_with_work: List[PullRequest] = []
        _exception = None

        try:
            joined_prs = []
            for project in self._settings.projects:
                joined_prs.extend(self._get_pull_requests_for_project(project, self._settings.pull_request_status))

            if self._settings.omit_draft:
                joined_prs = [pr for pr in joined_prs
                              if not pr.is_draft or (
                                  self._settings.include_own_drafts and
                                  self._settings.user_email in pr.created_by.unique_name.lower()
                              )]

            if self._settings.filter_by_reviewer:
                _prs_to_review = self._get_pull_requests_to_review(joined_prs)
            else:
                non_authored = [pr for pr in joined_prs
                                if self._settings.user_email not in pr.created_by.unique_name.lower()]
                _prs_to_review = self._mapper.to_pull_requests(non_authored)
            _prs_authored_with_work = self._get_pull_requests_authored(joined_prs)
        except Timeout as e:
            _exception = PullRequestException(AzureDevOpsConstants.MODULE, AzureDevOpsConstants.TIMEOUT_MESSAGE, e,
                                              traceback.format_exc())
        except ConnectionError as e:
            _exception = PullRequestException(AzureDevOpsConstants.MODULE, AzureDevOpsConstants.CONNECTION_MESSAGE, e,
                                              traceback.format_exc())
        except Exception as e:
            _exception = PullRequestException(AzureDevOpsConstants.MODULE, AzureDevOpsConstants.UNKNOWN_MESSAGE, e,
                                              traceback.format_exc())

        if _prs_to_review + _prs_authored_with_work == 0:
            _exception = PullRequestException(AzureDevOpsConstants.MODULE, AzureDevOpsConstants.NO_RESULTS, None, None)

        return PullRequestsOverview.create(_prs_to_review, _prs_authored_with_work, _exception)

    def _get_pull_requests_for_project(self, project, pr_status) -> List[GitPullRequest]:
        return self._git_client.get_pull_requests_by_project(project,
                                                             GitPullRequestSearchCriteria(status=pr_status))

    def _get_pull_requests_authored(self, prs: List[GitPullRequest]) -> List[PullRequest]:
        prs_authored = [pr for pr in prs if self._settings.user_email in pr.created_by.unique_name.lower()]
        return self._mapper.to_pull_requests(prs_authored, authored=True)

    def _get_pull_requests_to_review(self, prs: List[GitPullRequest]) -> List[PullRequest]:
        prs_to_review = [pr for pr in prs if self._is_reviewer_for_pr(pr)]
        return self._mapper.to_pull_requests(prs_to_review)

    def _is_reviewer_for_pr(self, pr: GitPullRequest) -> bool:
        unique_names = [r.unique_name.lower() for r in pr.reviewers]
        display_names = [r.display_name.lower() for r in pr.reviewers]
        reviewer_status = self._mapper.get_reviewer_status(pr.reviewers)

        is_reviewer = (
            (self._settings.user_email in unique_names) or
            any(team_name in display_name
                for display_name in display_names
                for team_name in self._settings.team_names)
        ) and self._settings.user_email not in pr.created_by.unique_name.lower()

        should_review = (
            self._settings.omit_reviewed_and_approved and reviewer_status != PullRequestStatus.APPROVED
        ) or not self._settings.omit_reviewed_and_approved

        return is_reviewer and should_review


class GitPullRequestMapper(object):
    _votes_mapping = {
        -10: PullRequestStatus.REJECTED,
        -5: PullRequestStatus.WAITING_FOR_AUTHOR,
        0: PullRequestStatus.UNAPPROVED,
        5: PullRequestStatus.APPROVED_WITH_SUGGESTIONS,
        10: PullRequestStatus.APPROVED
    }

    def __init__(self, settings: AzureDevOpsSettings):
        self._settings = settings

    @staticmethod
    def _short_ref(ref_name: str):
        return ref_name.replace('refs/heads/', '')

    def _to_pull_request(self, ado_pr: GitPullRequest, authored: bool = False) -> PullRequest:
        project = quote(ado_pr.repository.project.name, safe='')
        repo_href = f"{self._settings.organization_url}/{project}/_git/{ado_pr.repository.name}"
        all_prs_href = f"{repo_href}/pullrequests?_a=active"
        pr_href = f"{repo_href}/pullrequest/{ado_pr.pull_request_id}"

        status = (self.get_aggregate_reviewer_status(ado_pr.reviewers)
                  if authored
                  else self.get_reviewer_status(ado_pr.reviewers))

        return PullRequest(
            id=str(ado_pr.pull_request_id),
            title=abbreviate_string(ado_pr.title, self._settings.abbreviation_characters),
            slug=ado_pr.repository.name,
            from_ref=GitPullRequestMapper._short_ref(ado_pr.source_ref_name),
            to_ref=GitPullRequestMapper._short_ref(ado_pr.target_ref_name),
            overall_status=status,
            is_draft=ado_pr.is_draft or False,
            activity=ado_pr.creation_date,
            time_ago=time_ago(ado_pr.creation_date),
            all_prs_href=all_prs_href,
            href=pr_href
        )

    def to_pull_requests(self, ado_pull_requests: List[GitPullRequest], authored: bool = False) -> List[PullRequest]:
        return [self._to_pull_request(ado_pr, authored) for ado_pr in ado_pull_requests]

    def get_reviewer_status(self, reviewers: List[IdentityRefWithVote]) -> PullRequestStatus:
        user_review = [r for r in reviewers if r.unique_name.lower() == self._settings.user_email]

        if len(user_review) > 0:
            return self._votes_mapping[user_review[0].vote]
        else:
            return PullRequestStatus.UNAPPROVED

    def get_aggregate_reviewer_status(self, reviewers: List[IdentityRefWithVote]) -> PullRequestStatus:
        votes = [r.vote for r in reviewers if r.vote != 0]

        if not votes:
            return PullRequestStatus.UNAPPROVED
        if -10 in votes:
            return PullRequestStatus.REJECTED
        if -5 in votes:
            return PullRequestStatus.WAITING_FOR_AUTHOR
        if 10 in votes:
            return PullRequestStatus.APPROVED
        if 5 in votes:
            return PullRequestStatus.APPROVED_WITH_SUGGESTIONS
        return PullRequestStatus.UNAPPROVED
