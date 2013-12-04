Personal Website
================

This is the content of my personal website, found at http://cmetcalfe.ca


Updating
-----
Note that this setup uses [Nginx](http://nginx.org/) on [Debian](http://www.debian.org/). The steps will be similar for other setups, but might not be exactly the same.

1. Initialize a bare git repo somewhere on the server with

    `git init --bare`

2. Setup a site configuration file that includes all configuration files in the repositories `.config` directory. Ex:

    ```
    include [path to website]/.config/*.conf;
    ```

3. Modify `/etc/sudoers` (with `visudo`) to allow the user to restart the webserver

    ```
    [user] ALL=(root) NOPASSWD: /etc/init.d/nginx restart
    ```

4. Add the Git post-receive hook to update the data and restart the webserver

    ```
    #!/bin/sh

    # Set up the location to update
    OUTPUT_DIR=[path to website]

    # Check out the new version of the website
    GIT_WORK_TREE=$OUTPUT_DIR git checkout -f
    unset GIT_DIR

    # Call the website's restart script
    $OUTPUT_DIR/.config/restart
    ```

5. Locally add the remote repository to the git remotes with

    `git remote add deploy ssh://[user]@[server]:[port]/[path to repo]`

6. To update the website, commit changes then run `git push deploy`
