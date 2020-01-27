from distutils.util import strtobool

from ..common import AppConfigReader


class PullRequestConfig(object):
    _config = AppConfigReader.read("bitbucket")

    BITBUCKET_HOST = _config['preferences']['bitbucket_host']
    PRIVATE_TOKEN = _config['preferences']['private_token']
    USER_SLUG = _config['preferences']['user_slug']
    SORT_ON = _config['preferences']['sort_on']
    ABBREVIATION_CHARACTERS = int(_config['preferences']['abbreviation_characters'])
    OMIT_REVIEWED_AND_APPROVED = strtobool(_config['preferences']['omit_reviewed_and_approved'])
    NOTIFICATIONS_ENABLED = strtobool(_config['preferences']['notifications_enabled'])

    BITBUCKET_API_PULL_REQUESTS = '/rest/api/1.0/dashboard/pull-requests'
    CACHE_FILE = _config['common']['cache_path']
