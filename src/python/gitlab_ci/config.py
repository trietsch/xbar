import json
from distutils.util import strtobool

from ..common.config import AppConfigReader


class GitlabConstants(object):
    MODULE = "gitlab_ci"


class GitlabConfig(object):
    _config = AppConfigReader.read(GitlabConstants.MODULE)

    CHECK_MEMBERSHIP = strtobool(_config['preferences'].get('check_membership', 'True'))
    CHECK_STARRED_ONLY = strtobool(_config['preferences'].get('check_starred_only', 'False'))
    ONLY_PROJECTS_WITH_PIPELINES = strtobool(_config['preferences'].get('only_projects_with_pipelines', 'True'))
    ONLY_PROJECTS_LAST_WEEKS = _config['preferences'].get('only_projects_last_weeks', None)

    SORT_ON = _config['preferences'].get('sort_on', 'activity')
    SORT_REVERSE = strtobool(_config['preferences'].get('sort_reverse', "False"))
    ALTERNATE_HEADER = strtobool(_config['preferences'].get('alternate_header', "False"))

    API_PROJECTS = '/api/v4/projects'
    API_PIPELINES = '/pipelines'

    GITLAB_HOSTS = list()
    _gitlab_hosts = json.loads(_config['preferences'].get('gitlab_hosts', '[]'))

    if len(_gitlab_hosts) == 0:
        print("No GitLab hosts defined, please check your config file")
    else:
        for instance in _gitlab_hosts:
            GITLAB_HOSTS.append(
                dict(name=instance, host=_config[instance]['host'], private_token=_config[instance]['private_token']))
