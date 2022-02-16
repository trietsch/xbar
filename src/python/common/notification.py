from subprocess import Popen
from sys import platform

from .util import get_absolute_path_to_repo_file


def send_notification(title, message, path_to_image: str = None, url: str = None):

    if platform == "linux" or platform == "linux2":
        # linux
        Popen(["notify-send", "-t", "2000", "-i", path_to_image, title, message])
    elif platform == "darwin":
        # OS X
        notifier = get_absolute_path_to_repo_file('notifications/terminal-notifier.app/Contents/MacOS/terminal-notifier')
        arguments = f'-title "{title}" -message "{message}"'

        if path_to_image:
            arguments = f'{arguments} -appIcon "{get_absolute_path_to_repo_file(path_to_image)}"'

        if url:
            arguments = f'{arguments} -open "{url}"'

        Popen(["/bin/bash", "-c", f"{notifier} {arguments}"])
