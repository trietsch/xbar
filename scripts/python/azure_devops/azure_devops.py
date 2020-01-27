import itertools
from typing import List

from azure.devops.connection import Connection
from azure.devops.v5_1.git import GitPullRequestSearchCriteria, GitPullRequest
from msrest.authentication import BasicAuthentication

from .domain import AzureDevOpsIcons
from .config import AzureDevOpsConfigReader


class AzureDevOpsClientFactory(object):
    _connection_factory = Connection(
        base_url=AzureDevOpsConfigReader.ORGANIZATION_URL,
        creds=BasicAuthentication('', AzureDevOpsConfigReader.PERSONAL_ACCESS_TOKEN)
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


class PullRequestPrinter(object):

    @staticmethod
    def print_pull_requests(pr_type, header_icon, pull_requests):
        print(pr_type + " | templateImage=" + header_icon)
        print("---")

        prs_sorted_by_slug = sorted(pull_requests, key=lambda p: p.slug)

        for repo, repo_prs in itertools.groupby(prs_sorted_by_slug, key=lambda p: p.slug):
            repo_prs_list: List[GitPullRequest] = list(repo_prs)
            repo_status = determine_repo_status(repo_prs_list)
            repo_href = repo_prs_list[0].repo_href
            print(
                repo + " (" + str(len(repo_prs_list)) + ") | href=" + repo_href + " image = " + AzureDevOpsIcons.STATUS[
                    repo_status])

            prs_sorted_by_to_ref = sorted(repo_prs_list, key=lambda p: p.to_ref)

            for to_ref, to_ref_prs in itertools.groupby(prs_sorted_by_to_ref, key=lambda p: p.to_ref):
                to_ref_prs_list: List[GitPullRequest] = sort_pull_requests(list(to_ref_prs))
                print("--" + to_ref)

                for _pr in to_ref_prs_list:
                    print("--" +
                          _pr.from_ref + " -- " + _pr.title + " (#" + _pr.id + ") - " + _pr.time_ago + "|href=" + _pr.href
                          + " image=" + AzureDevOpsIcons.STATUS[_pr.overall_status]
                          )
