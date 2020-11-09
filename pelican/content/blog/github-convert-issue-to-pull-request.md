---
Title: "GitHub: Convert an issue to a pull request"
Date: 2013-11-26 01:46
Modified: 2015-01-22 00:54
Author: Carey Metcalfe
Tags:
  - code
  - git
  - shell script
---

[GitHub][] currently doesn't provide a way to convert an issue to a pull request in their interface.
However, the capability exists in their [Pull Request API][].

!!! Update
    I've built a self-hostable webapp called [gh-i2p][] that makes this process easier.

To call the API using a simple `curl` command, run the command:

```bash
curl --user "[github username]" \
     --request POST \
     --data '{"issue": "[issue num]", "head": "[branch to merge from]", "base": "[branch to merge into]"}' \
     https://api.github.com/repos/[user]/[repo]/pulls
```

For example, to make `user1` change issue 13 into a pull request to merge branch `test_branch` into
`master` in the `testing_repo` repository belonging to `user2`, the command would be:

```bash
curl --user 'user1' \
     --request POST \
     --data '{"issue": "13", "head": "test_branch", "base": "master"}' \
     https://api.github.com/repos/user2/testing_repo/pulls
```

To specify a fork of a repository to merge from, put the username followed by a semicolon in front
of the branch name like so: `"username:branch_name"`

After running the command, you will be prompted for your GitHub password. Enter it and curl should
output the JSON response from the API. Make sure to check this response for errors!

  [GitHub]: http://github.com
  [gh-i2p]: https://github.com/pR0Ps/gh-i2p
  [Pull Request API]: http://developer.github.com/v3/pulls/#alternative-input
