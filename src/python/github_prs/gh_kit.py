import asyncio

from githubkit import GitHub

g = GitHub("")


gql_login_query = """
query {
  viewer {
    login
  }
}
"""



gql_query = """
query($githubQuery: String!){
  search(query: $githubQuery, type: ISSUE, first: 100) {
    issueCount
    edges {
      node {
        ... on PullRequest {
          number
          title
          labels(first: 10) {
            nodes {
              name
            }
          }
          author {
            login
          }
          repository {
            nameWithOwner
          }
          reviews(first: 100) {
            nodes {
              author {
                login
              }
              state
              comments(first: 10) {
                totalCount
              }
            }
          }
          updatedAt
          url
        }
      }
    }
  }
}
"""

organizations = " ".join(list(map(lambda o: f"org:{o}", ["getstrm"])))
me = "trietsch"
labels_to_exclude = " ".join(list(map(lambda l: f"-label:{l}", ["renovate"])))
github_search_query = f"is:pr is:open {organizations} {labels_to_exclude} -author:{me}"

print(g.graphql(query=gql_query, variables={"githubQuery": github_search_query}))


async def queries():
    login = g.async_graphql(query=gql_login_query)


    await asyncio.gather(
        login,
    )
