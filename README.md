Personal Website
================

This is the contents of my personal website, found at http://cmetcalfe.ca


Updating
-----
Note that this setup uses [Nginx](http://nginx.org/) on [Debian](http://www.debian.org/). The steps will be similar for other setups, but might not be exactly the same.

1. Initialize a git repo on the server with

    ```
    cd [path to website]
    git init
    git config --bool receive.denyCurrentBranch false
    git config --path core.worktree ../
    ```

2. Setup an Nginx site configuration file that includes all configuration files in the repositories `out/_conf` directory. Ex:

    ```
    include [path to website]/out/_conf/*.conf;
    ```

3. Modify `/etc/sudoers` (with `visudo`) to allow the user to restart the webserver (and any other commands in `post-update` that need root)

    ```
    [user] ALL=(root) NOPASSWD: /etc/init.d/nginx restart
    ```

4. Add the Git post-receive hook (in `.git/hooks/post-receive`) to update the data and call the `post-update` script

    ```
    #!/bin/sh

    unset GIT_DIR

    echo "Moving to output directory"
    cd `git config --get core.worktree` || exit

    echo "Checking out the repo"
    git checkout -f

    echo "Calling the website's update script"
    ./post-update
    ```

5. Locally add the remote repository to the git remotes with

    ```
    git remote add deploy ssh://[user]@[server]:[port]/[path to website]
    ```

6. To update the website, commit changes then run `git push deploy`
