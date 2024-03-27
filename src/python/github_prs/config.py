from distutils.util import strtobool
from typing import Dict

from ..common.config import AppConfigReader
from ..common.icons import Icon, Icons
from ..pull_requests import PullRequestSort, PullRequestStatus


class GitHubPrsConstants(object):
    MODULE = "github_prs"

    TIMEOUT_MESSAGE = "Timeout while trying to connect to GitHub."
    CONNECTION_MESSAGE = "Failed to connect to GitHub."
    UNKNOWN_MESSAGE = "An unknown exception occurred while trying to fetch PRs."
    NO_RESULTS = "There are no pull requests in GitHub."

    APPROVED = "APPROVED"
    CHANGES_REQUESTED = 'CHANGES_REQUESTED'
    COMMENTED = 'COMMENTED'


class GitHubPrsConfig(object):
    _config = AppConfigReader.read(GitHubPrsConstants.MODULE)

    PRIVATE_TOKEN = _config["preferences"]["private_token"]  # no default, crash
    SORT_ON = PullRequestSort[_config["preferences"]["sort_on"].upper()]
    ABBREVIATION_CHARACTERS = int(_config["preferences"].get("abbreviation_characters", "30"))
    OMIT_REVIEWED_AND_APPROVED = strtobool(_config["preferences"].get("omit_reviewed_and_approved", "False"))
    NOTIFICATIONS_ENABLED = strtobool(_config["preferences"].get("notifications_enabled", "False"))
    ORGANIZATION_NAMES = set(_config["preferences"].get("organization_names", "").split(","))
    EXCLUDE_PRS_WITH_LABELS = set(_config["preferences"].get("exclude_prs_with_labels", "").split(","))

    CACHE_FILE = _config["common"]["cache_path"]


class GitlabPrsIcons(object):
    PULL_REQUEST = Icons.PULL_REQUEST

    PR_STATUSES: Dict[PullRequestStatus, Icon] = {
        PullRequestStatus.UNAPPROVED: Icons.GREY_CIRCLE,
        PullRequestStatus.NEEDS_WORK: Icons.ORANGE_CIRCLE,
        PullRequestStatus.APPROVED: Icons.GREEN_CIRCLE
    }


class GitHubGQLQueries(object):
    login = """
    query {
      viewer {
        login
      }
    }
    """

    pull_requests = """
query($githubQuery: String!){
  search(query: $githubQuery, type: ISSUE, first: 100) {
    issueCount
    edges {
      node {
        ... on PullRequest {
          number
          baseRefName
          headRefName
          title
          author {
            login
          }
          repository {
            nameWithOwner
          }
          reviews(first: 100) {
            nodes {
              author {
                login
              }
              state
              comments(first: 10) {
                totalCount
              }
            }
          }
          updatedAt
          url
        }
      }
    }
  }
}
"""
