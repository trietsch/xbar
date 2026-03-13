class BitbucketConstants(object):
    MODULE = "bitbucket"

    BITBUCKET_API_PULL_REQUESTS = '/rest/api/1.0/dashboard/pull-requests'

    TIMEOUT_MESSAGE = "Timeout while trying to connect to Bitbucket host."
    CONNECTION_MESSAGE = "Failed to connect to Bitbucket host."
    UNKNOWN_MESSAGE = "An unknown exception occurred while trying to fetch PRs."
