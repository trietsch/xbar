from azure.devops.v5_1.git import GitPullRequest, IdentityRefWithVote

from . import AzureDevOpsConfigReader
from . import PullRequestClient

pr_client = PullRequestClient()

filtered = pr_client.get_pull_request_to_be_reviewed_by(AzureDevOpsConfigReader.PROJECTS[0],
                                                        AzureDevOpsConfigReader.PULL_REQUEST_STATUS,
                                                        AzureDevOpsConfigReader.USER_EMAIL)

pr: GitPullRequest
for pr in filtered:
    print(pr.pull_request_id)
    r: IdentityRefWithVote
    for r in pr.reviewers:
        print(r.display_name)

    print("\n-------------------------\n")
