from . import get_pr_status, BitbucketIcons, PullRequestStatus, PullRequestsOverview, \
    PullRequestConfig, print_prs, send_notification_new_pr

pr_status = get_pr_status()

if pr_status.exception is not None:
    print("? | templateImage=" + BitbucketIcons.PULL_REQUEST)
    print("---")
    print("Error: " + pr_status.exception + "|templateImage=" + BitbucketIcons.BITBUCKET)
else:
    # Set menubar icon
    total_prs_to_review = len(pr_status.prs_to_review)
    total_prs_authored_with_work = len(pr_status.prs_authored_with_work)
    total_prs = str(total_prs_to_review + total_prs_authored_with_work)
    print(total_prs + " | templateImage=" + BitbucketIcons.PULL_REQUEST)

    # Start menu items
    if total_prs == 0:
        print("---")
        print("Nothing to review! | image = " + BitbucketIcons.STATUS[PullRequestStatus.APPROVED])

    if total_prs_to_review > 0:
        print("---")
        print_prs("Reviewing", pr_status.prs_to_review)

    if total_prs_authored_with_work > 0:
        print("---")
        print_prs("Authored", pr_status.prs_authored_with_work)

    previous_pr_status = PullRequestsOverview.load_cached()
    new_prs = pr_status.determine_new_pull_requests_to_review(previous_pr_status)

    if PullRequestConfig.NOTIFICATIONS_ENABLED:
        for pr in new_prs:
            send_notification_new_pr(pr.slug, pr.from_ref, pr.to_ref, pr.title)

    pr_status.store()
