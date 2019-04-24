One day at standup, one of my colleagues complained that our repos were
cluttered up by branches from old PRs that hadn't been removed when the
PR was merged. This script aims to retroactively identify these branches
and delete them. By default, it just print the branches it intends to delete.

For deletion to happen, you must pass the -f (or --force) option.

It expects there to be a shell variable `GIT_AUTH_TOKEN` containing
a Github auth token with the appropriate privileges.
You can create a token at: https://github.com/settings/tokens
It just needs the `repo` scope.

It also expects:
  - an organization option (`-o <value>` or `--org=<value>`)
  - a repo option (`-r <value>` or `--repo=<value>`)

So a complete command line looks like:

`GIT_AUTH_TOKEN=<TOKEN> python cull_closed_pr_branches.py -o <org> -r <repo> -f`
