import json
from distutils.util import strtobool

from ..common import AppConfigReader


class GitlabConfig(object):
    _config = AppConfigReader.read("gitlab")

    CHECK_MEMBERSHIP = strtobool(_config['preferences']['check_membership'])
    CHECK_STARRED_ONLY = strtobool(_config['preferences']['check_starred_only'])
    SORT_ON = _config['preferences']['sort_on']

    API_PROJECTS = '/api/v4/projects'
    API_PIPELINES = '/pipelines'

    GITLAB_HOSTS = list()

    for instance in json.loads(_config['preferences']['gitlab_hosts']):
        GITLAB_HOSTS.append(
            dict(name=instance, host=_config[instance]['host'], private_token=_config[instance]['private_token']))
