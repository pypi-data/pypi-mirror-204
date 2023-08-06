# TODOs

## GitHub REST API rate limit

Find a way to securely use a user's GitHub auth token.

`curl -H "Accept: application/vnd.github.v3+json" https://api.github.com/rate_limit`

60 calls
vs

```sh
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>"\
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/rate_limit
```

Authenticated users have a much higher rate than non-users.
Those have just 60 connections / hour.
One pytest run makes 6 calls.

See [rate limit info on GitHub](https://docs.github.com/en/rest/overview/resources-in-the-rest-api?apiVersion=2022-11-28#rate-limiting).
