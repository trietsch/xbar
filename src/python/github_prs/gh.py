from itertools import groupby

from github import Github

g = Github("")

user = g.get_user()

print(user.login)

repos = g.get_organization("strmprivacy").get_repos()

for rep in repos:
    prs = rep.get_pulls()

    if prs.totalCount > 0:
        print(prs[0])

        reviews = prs[0].get_reviews()

        if reviews.totalCount > 0:
            print(reviews[0])
            reviews_grouped_by_login = groupby(reviews, key=(lambda r: r.user.login))
            last_review_state_per_user = {user_login: sorted(reviews, key=lambda r: r.submitted_at)[0].state for user_login, reviews in reviews_grouped_by_login}

            print({k: sorted(g, key=lambda r: r.submitted_at)[0].state for k, g in reviews_grouped_by_login})

# rep = g.get_repo("strmprivacy/cli")
#
# print()
#
# prs = rep.get_pulls()
#
# print(prs.totalCount)
