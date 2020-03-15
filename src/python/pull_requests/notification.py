from ..common.notification import send_notification


def send_notification_pr(change_text, repo_slug, from_ref, to_ref, title, url=None):
    path_to_image = 'assets/pr-logo.png'
    send_notification(f"{change_text} pull request for {repo_slug}",
                      f"{title}\n{from_ref} -> {to_ref}", path_to_image, url)
