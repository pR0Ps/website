Config Files
------------

Files under this folder will be moved (preserving their folder structure) to the `out/_config`
directory.

The `post-update` script will perform the following replacements:
- `{{root}}` will be replaced with the root directory of the repository.
- `{{output}}` will be replaced with the root output directory of the website.
- `{{https}}` will be replaced with the https config directory of the website.
