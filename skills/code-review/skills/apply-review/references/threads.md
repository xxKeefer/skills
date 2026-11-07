# GitHub review threads

A reply uses the REST API. A resolve uses GraphQL only. Put `OWNER`, `REPO`, and `PR` (the
number) in each call.

## 1. List the threads

The query gets the thread node id (`PRRT_…`, for the resolve), the `databaseId` of the first
comment (for the reply), the URL of the first comment (for the `thread` cell), and the text of
each comment, in one call. `/code-review:apply-review` and `/code-review:resolve-feedback` use it:

```bash
gh api graphql --paginate \
  --jq '.data.repository.pullRequest.reviewThreads.nodes[]
        | {id, isResolved, path, line,
           comment: .comments.nodes[0].databaseId, url: .comments.nodes[0].url,
           comments: [.comments.nodes[]
             | {author: .author.login, bot: (.author.__typename == "Bot"), body}]}' \
  -f query='
query($endCursor: String) {
  repository(owner: "OWNER", name: "REPO") {
    pullRequest(number: PR) {
      reviewThreads(first: 100, after: $endCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id isResolved path line
          comments(first: 100) { nodes { databaseId url author { __typename login } body } }
        }
      }
    }
  }
}'
```

`--paginate` needs the `$endCursor` variable and the `pageInfo` fields. Without them, a PR with
more than 100 threads loses the rest and gives no error.

`url` has the form `https://github.com/<owner>/<repo>/pull/<n>#discussion_r<id>`. The `<id>` is
the `databaseId` of the first comment. Match each row on it.

`bot` is `true` when GitHub types the author as a bot. Copilot is a bot, although its login has no
`[bot]` suffix. A deleted account has no author, so `bot` is `false`.

## 2. Reply

Write the reply to a file with a quoted heredoc (`<<'EOF'`), so that backticks and `$` stay as
written. `in_reply_to` is the `databaseId` of the first comment:

```bash
gh api repos/OWNER/REPO/pulls/PR/comments -F in_reply_to=<databaseId> -F body=@"$DIR/reply.md" \
  --jq .html_url
```

## 3. Resolve

`threadId` is the `PRRT_…` node id. No REST endpoint resolves a thread.

```bash
gh api graphql -f query='
mutation { resolveReviewThread(input: {threadId: "PRRT_…"}) { thread { isResolved } } }'
```

The result must show `isResolved: true`.
