Nginx Config Files
------------------

Files in this folder ending in '.conf' will be used by Nginx as config files.

The `post-update` script will open these files and perform the following replacements:
- `{{root}}` will be replaced with the root directory of the repository.
- `{{output}}` will be replaced with the root output directory of the website.
