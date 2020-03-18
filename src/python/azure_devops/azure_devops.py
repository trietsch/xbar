import traceback
from typing import List, Dict

from azure.devops.connection import Connection
from azure.devops.v5_1.git import GitPullRequestSearchCriteria, GitPullRequest, IdentityRefWithVote
from msrest.authentication import BasicAuthentication
from requests import Timeout

from .config import AzureDevOpsConfig, AzureDevOpsConstants
from ..common.util import abbreviate_string, time_ago
from ..pull_requests import PullRequest, PullRequestStatus, PullRequestsOverview, PullRequestException


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

    def get_pull_requests_overview(self, project, pr_status, user_email, team_name) -> PullRequestsOverview:
        _prs_to_review: List[PullRequest] = []
        _prs_authored_with_work: List[PullRequest] = []
        _exception = None

        try:
            prs = self._get_pull_requests_for_project(project, pr_status)
            _prs_to_review = self._get_pull_request_to_be_reviewed_by(prs, user_email, team_name)
            _prs_authored_with_work = self._get_pull_requests_authored(prs, user_email)
        except Timeout as e:
            _exception = PullRequestException(AzureDevOpsConstants.MODULE, AzureDevOpsConstants.TIMEOUT_MESSAGE, e,
                                              traceback.format_exc())
        except ConnectionError as e:
            _exception = PullRequestException(AzureDevOpsConstants.MODULE, AzureDevOpsConstants.CONNECTION_MESSAGE, e,
                                              traceback.format_exc())
        except Exception as e:
            _exception = PullRequestException(AzureDevOpsConstants.MODULE, AzureDevOpsConstants.UNKNOWN_MESSAGE, e,
                                              traceback.format_exc())

        return PullRequestsOverview.create(_prs_to_review, _prs_authored_with_work, _exception)

    def _get_pull_requests_for_project(self, project, pr_status) -> List[GitPullRequest]:
        return self._git_client.get_pull_requests_by_project(project,
                                                             GitPullRequestSearchCriteria(status=pr_status))

    @staticmethod
    def _get_pull_requests_authored(prs: List[GitPullRequest], user_email: str) -> List[PullRequest]:
        prs_authored = list(filter(lambda pr: user_email in pr.created_by.unique_name.lower(), prs))
        return GitPullRequestMapper.to_pull_requests(prs_authored)

    @staticmethod
    def _get_pull_request_to_be_reviewed_by(prs: List[GitPullRequest], user_email: str, team_name: str) -> List[
        PullRequest]:
        prs_to_review_by_user = list(filter(lambda pr:
                                            PullRequestClient._is_reviewer_for_pr(
                                                user_email,
                                                team_name,
                                                pr),
                                            prs))

        return GitPullRequestMapper.to_pull_requests(prs_to_review_by_user)

    @staticmethod
    def _is_reviewer_for_pr(user_email, team_name, pr: GitPullRequest) -> bool:
        reviewer_names = PullRequestClient._get_reviewer_names(pr)
        reviewer_status = GitPullRequestMapper.get_reviewer_status(pr.reviewers)

        # If OMIT = True, don't show if status = Approved
        # If OMIT = False, show all
        is_reviewer = ((user_email in reviewer_names['unique_names']) or any(
            team_name in r for r in reviewer_names['display_names'])) and not (
                user_email in pr.created_by.unique_name.lower())

        should_review = (AzureDevOpsConfig.OMIT_REVIEWED_AND_APPROVED and reviewer_status != PullRequestStatus.APPROVED) \
                        or not AzureDevOpsConfig.OMIT_REVIEWED_AND_APPROVED

        return is_reviewer and should_review

    @staticmethod
    def _get_reviewer_names(pr: GitPullRequest) -> Dict[List[str], List[str]]:
        unique_names = list(map(lambda r: r.unique_name.lower(), pr.reviewers))
        display_names = list(map(lambda r: r.display_name.lower(), pr.reviewers))

        return dict(pr=pr, unique_names=unique_names, display_names=display_names)


class GitPullRequestMapper(object):
    _votes_mapping = {
        -10: PullRequestStatus.REJECTED,
        -5: PullRequestStatus.WAITING_FOR_AUTHOR,
        0: PullRequestStatus.UNAPPROVED,
        5: PullRequestStatus.APPROVED_WITH_SUGGESTIONS,
        10: PullRequestStatus.APPROVED
    }

    @staticmethod
    def _short_ref(ref_name: str):
        return ref_name.replace('refs/heads/', '')

    @staticmethod
    def _to_pull_request(ado_pr: GitPullRequest) -> PullRequest:
        repo_href = f"{AzureDevOpsConfig.ORGANIZATION_URL}/{ado_pr.repository.project.name}/_git/{ado_pr.repository.name}"
        all_prs_href = f"{repo_href}/pullrequests?_a=active"
        pr_href = f"{repo_href}/pullrequest/{ado_pr.pull_request_id}"

        return PullRequest(
            id=str(ado_pr.pull_request_id),
            title=abbreviate_string(ado_pr.title, AzureDevOpsConfig.ABBREVIATION_CHARACTERS),
            slug=ado_pr.repository.name,
            from_ref=GitPullRequestMapper._short_ref(ado_pr.source_ref_name),
            to_ref=GitPullRequestMapper._short_ref(ado_pr.target_ref_name),
            # TODO fix overall status for authored work?
            overall_status=GitPullRequestMapper.get_reviewer_status(ado_pr.reviewers),
            activity=ado_pr.creation_date,
            time_ago=time_ago(ado_pr.creation_date),
            all_prs_href=all_prs_href,
            href=pr_href
        )

    @staticmethod
    def to_pull_requests(ado_pull_requests: List[GitPullRequest]) -> List[PullRequest]:
        return [GitPullRequestMapper._to_pull_request(ado_pr) for ado_pr in ado_pull_requests]

    @staticmethod
    def get_reviewer_status(reviewers: List[IdentityRefWithVote]) -> PullRequestStatus:
        user_review = list(filter(lambda r: r.unique_name.lower() == AzureDevOpsConfig.USER_EMAIL.lower(), reviewers))

        if len(user_review) > 0:
            return GitPullRequestMapper._votes_mapping[user_review[0].vote]
        else:
            return PullRequestStatus.UNAPPROVED
