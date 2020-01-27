import json
from distutils.util import strtobool

from ..common import AppConfigReader


class AzureDevOpsConfigReader(object):
    _config = AppConfigReader.read("azure_devops")

    ORGANIZATION_URL = f'https://dev.azure.com/{_config["preferences"]["organization"]}'
    PERSONAL_ACCESS_TOKEN = _config['preferences']['personal_access_token']
    PROJECTS = json.loads(_config['preferences']['projects'])
    PULL_REQUEST_STATUS = _config['preferences']['pull_request_status']
    USER_EMAIL = _config['preferences']['user_email']

    SORT_ON = _config['preferences']['sort_on']
    ABBREVIATION_CHARACTERS = int(_config['preferences']['abbreviation_characters'])
    OMIT_REVIEWED_AND_APPROVED = strtobool(_config['preferences']['omit_reviewed_and_approved'])
    NOTIFICATIONS_ENABLED = strtobool(_config['preferences']['notifications_enabled'])
