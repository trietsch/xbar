from common.config import AppConfigReader


class GitlabConstants(object):
    MODULE = "gitlab_ci"


class GitlabConfig(object):
    _config = AppConfigReader.read(GitlabConstants.MODULE)

    CHECK_MEMBERSHIP = _config['preferences'].get('check_membership', True)
    CHECK_STARRED_ONLY = _config['preferences'].get('check_starred_only', False)
    ONLY_PROJECTS_WITH_PIPELINES = _config['preferences'].get('only_projects_with_pipelines', True)
    ONLY_PROJECTS_LAST_WEEKS = _config['preferences'].get('only_projects_last_weeks', None)

    SORT_ON = _config['preferences'].get('sort_on', ['activity'])
    SORT_REVERSE = _config['preferences'].get('sort_reverse', False)
    IGNORE_STATUSES = _config['preferences'].get('ignore_statuses', [])
    ALTERNATE_HEADER = _config['preferences'].get('alternate_header', False)

    API_PROJECTS = '/api/v4/projects'
    API_PIPELINES = '/pipelines'

    GITLAB_HOSTS = list()
    _gitlab_hosts = _config['preferences'].get('gitlab_hosts', [])

    if len(_gitlab_hosts) == 0:
        print("No GitLab hosts defined, please check your config file")
    else:
        for instance in _gitlab_hosts:
            GITLAB_HOSTS.append(
                dict(name=instance, host=_config[instance]['host'], private_token=_config[instance]['private_token']))