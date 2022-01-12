from collections import defaultdict

import dateutil.parser
from requests import Timeout

from . import GitlabConfig, PipelineStatus, get_projects, get_most_recent_project_pipeline_status, GitlabIcons
from ..common.util import time_ago

overall_status = PipelineStatus.INACTIVE
bitbar_gitlab_projects = []

# Overall status counters
statuses = defaultdict(int)

for instance in GitlabConfig.GITLAB_HOSTS:
    host = instance['host']
    private_token = instance['private_token']

    gitlab_instance_projects = []

    try:
        projects = get_projects(private_token, host, GitlabConfig.ONLY_PROJECTS_LAST_WEEKS)

        for project in projects:
            project_id = project['id']
            project_name_and_path = project['path_with_namespace']
            project_activity = dateutil.parser.parse(project['last_activity_at'])

            pipeline_status, web_url = get_most_recent_project_pipeline_status(
                private_token,
                host,
                project_id
            )

            if GitlabConfig.ONLY_PROJECTS_WITH_PIPELINES and pipeline_status == PipelineStatus.INACTIVE:
                continue
            statuses[pipeline_status] += 1

            gitlab_instance_projects.append(dict(
                id=project_id,
                name=project_name_and_path,
                activity=project_activity,
                time_ago=time_ago(project_activity),
                href=web_url,
                status=pipeline_status,
                image=GitlabIcons.STATUS[pipeline_status]
            ))

        bitbar_gitlab_projects.append(dict(gitlab_name=instance['name'], projects=gitlab_instance_projects))
    except Timeout as e:
        bitbar_gitlab_projects.append(dict(gitlab_name=instance['name'], projects=gitlab_instance_projects,
                                           exception="timeout"))
        continue
    except ConnectionError as e:
        bitbar_gitlab_projects.append(dict(gitlab_name=instance['name'], projects=gitlab_instance_projects,
                                           exception="connection error"))
        continue
    except Exception as e:
        bitbar_gitlab_projects.append(dict(gitlab_name=instance['name'], projects=gitlab_instance_projects,
                                           exception="unknown error"))
        continue

# Now construct the bitbar menu
if GitlabConfig.ALTERNATE_HEADER:
    for k, v in statuses.items():
        print(str(v) + "|image=" + GitlabIcons.STATUS[k].base64_image)
else:
    # Print the current active overall status
    if statuses.get(PipelineStatus.FAILURE_BUILDING, 0) > 0:
        print(str(statuses.get(PipelineStatus.FAILURE_BUILDING, 0)) + "|image=" +
              GitlabIcons.STATUS[PipelineStatus.FAILURE_BUILDING].base64_image)
    elif statuses.get(PipelineStatus.SUCCESS_BUILDING, 0) > 0:
        print(str(statuses.get(PipelineStatus.SUCCESS_BUILDING, 0)) + "|image=" +
              GitlabIcons.STATUS[PipelineStatus.SUCCESS_BUILDING].base64_image)
    elif statuses.get(PipelineStatus.FAILURE, 0) > 0:
        print(str(statuses.get(PipelineStatus.FAILURE, 0)) + "|image=" +
              GitlabIcons.STATUS[PipelineStatus.FAILURE].base64_image)
    elif statuses.get(PipelineStatus.SUCCESS, 0) > 0:
        print("|image=" + GitlabIcons.STATUS[PipelineStatus.SUCCESS].base64_image)

for instance in bitbar_gitlab_projects:
    # Start menu items
    gitlab_name = instance['gitlab_name']
    exception = instance.get('exception')
    print("---")

    if exception is not None:
        print(f"{gitlab_name} - Error: {exception} |templateImage={GitlabIcons.GITLAB_LOGO.base64_image}")
    else:
        print(f"{gitlab_name} |templateImage={GitlabIcons.GITLAB_LOGO.base64_image}")

        sorted_projects = sorted(instance['projects'],
                                 key=lambda p: tuple([str(p[sort_prop]) for sort_prop in GitlabConfig.SORT_ON]),
                                 reverse=GitlabConfig.SORT_REVERSE)

        for project in sorted_projects:
            print(
                f"{project['name']}  -  {project['time_ago']} |href={project['href']} image={project['image'].base64_image}")
