import dateutil.parser
from requests import Timeout

from . import GitlabConfig, PipelineStatus, get_projects, get_most_recent_project_pipeline_status, GitlabIcons
from ..common.util import time_ago

overall_status = PipelineStatus.INACTIVE
bitbar_gitlab_projects = []

# Overall status counters
status_failure_building = 0
status_success_building = 0
status_failure = 0
status_success = 0

for instance in GitlabConfig.GITLAB_HOSTS:
    host = instance['host']
    private_token = instance['private_token']

    gitlab_instance_projects = []

    try:
        projects = get_projects(private_token, host)

        for project in projects:
            project_id = project['id']
            project_name_and_path = project['path_with_namespace']
            project_href = project['web_url'] + "/pipelines"
            project_activity = dateutil.parser.parse(project['last_activity_at'])

            pipeline_status = get_most_recent_project_pipeline_status(
                private_token,
                host,
                project_id
            )

            if pipeline_status == PipelineStatus.FAILURE_BUILDING:
                status_failure_building += 1
            elif pipeline_status == PipelineStatus.SUCCESS_BUILDING:
                status_success_building += 1
            elif pipeline_status == PipelineStatus.FAILURE:
                status_failure += 1
            elif pipeline_status == PipelineStatus.SUCCESS:
                status_success += 1

            gitlab_instance_projects.append(dict(
                id=project_id,
                name=project_name_and_path,
                activity=project_activity,
                time_ago=time_ago(project_activity),
                href=project_href,
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
if status_failure_building > 0:
    overall_status = PipelineStatus.FAILURE_BUILDING
elif status_success_building > 0:
    overall_status = PipelineStatus.SUCCESS_BUILDING
elif status_failure > 0:
    overall_status = PipelineStatus.FAILURE
elif status_success > 0:
    overall_status = PipelineStatus.SUCCESS

# Set menubar icon
if overall_status == PipelineStatus.FAILURE:
    print(str(status_failure) + "|image=" + GitlabIcons.STATUS[overall_status].base64_image)
else:
    print("|image=" + GitlabIcons.STATUS[overall_status].base64_image)

for instance in bitbar_gitlab_projects:
    # Start menu items
    gitlab_name = instance['gitlab_name']
    exception = instance.get('exception')
    print("---")

    if exception is not None:
        print(f"{gitlab_name} - Error: {exception} |templateImage={GitlabIcons.GITLAB_LOGO.base64_image}")
    else:
        print(f"{gitlab_name} |templateImage={GitlabIcons.GITLAB_LOGO.base64_image}")

        sorted_projects = sorted(instance['projects'], key=lambda p: p['activity'],
                                 reverse=True) if GitlabConfig.SORT_ON == 'activity' else sorted(
            instance['projects'],
            key=lambda p: p['name'])

        for project in sorted_projects:
            print(f"{project['name']}  -  {project['time_ago']} |href={project['href']} image={project['image'].base64_image}")
