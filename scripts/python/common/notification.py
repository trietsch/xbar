from subprocess import Popen

from .util import get_absolute_path_to_repo_file


def send_notification(title, message, path_to_image):
    notifier = get_absolute_path_to_repo_file('notifications/terminal-notifier.app/Contents/MacOS/terminal-notifier')
    arguments = f"-title '{title}' -message '{message}' -appIcon '{get_absolute_path_to_repo_file(path_to_image)}'"

    Popen(["/bin/bash", "-c", f"{notifier} {arguments}"])
