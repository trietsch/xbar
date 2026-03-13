import os
from subprocess import Popen
from sys import platform
from urllib.parse import urlencode


def send_notification(title, message, url: str = None):
    if platform in ("linux", "linux2"):
        Popen(["notify-send", "-t", "2000", title, message])
    elif platform == "darwin":
        plugin = os.path.basename(os.environ.get("SWIFTBAR_PLUGIN_PATH", ""))
        params = {"plugin": plugin, "title": title, "body": message}
        if url:
            params["href"] = url
        Popen(["/usr/bin/open", "-g", f"swiftbar://notify?{urlencode(params)}"])