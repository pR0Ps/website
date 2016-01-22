Personal Website
================

This is the contents of my personal website, found at https://cmetcalfe.ca


Updating
-----
Note that this setup uses [Nginx](http://nginx.org/) on [Debian](http://www.debian.org/). The steps will be similar for other setups, but might not be exactly the same.

1. Initialize a git repo on the server with

    ```
    cd [path to site]
    git init
    git config --bool receive.denyCurrentBranch false
    git config --path core.worktree ../
    ```

2. Setup an Nginx site configuration file that includes all configuration files in the repositories `out/_config/nginx` directory. Ex:

    ```
    include [path to site]/out/_config/nginx/*.conf;
    ```

3. Modify `/etc/sudoers` (with `visudo`) to allow the user to restart the webserver without a password

    ```
    [user] ALL=(root) NOPASSWD: /etc/init.d/nginx restart
    ```

4. Link the Git post-receive hook (in `.git/hooks/post-receive`) to the `post-receive` script in the repo

    ```
    # Make something to link to intially - will be replaced on first push
    touch [path to site]/post-receive
    ln -s [path to site]/post-receive [path to site]/.git/hooks/post-receive
    ```

5. Locally add the remote repository to your local git remotes with

    ```
    git remote add deploy ssh://[user]@[server]:[port]/[path to site]
    ```

6. To update the website, commit changes then run `git push deploy`
