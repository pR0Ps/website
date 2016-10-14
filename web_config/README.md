Config Files
------------

Files under this folder will be moved (preserving their folder structure) to the `out/_config`
directory.

The `post-update` script will perform the following replacements:
- `{{root}}` will be replaced with the root directory of the repository.
- `{{output}}` will be replaced with the root output directory of the website.
- `{{https}}` will be replaced with the https config directory of the website.
- `{{nginx}}` will be replaced with the nginx config directory of the website.

The `http` and `https` folders in the `nginx` directory store different versions of config files.
If HTTPS is enabled, nginx will attempt to use the config files in the `https` folder, otherwise the
config files in `http` will be used instead.

To accomplish this, when the update script is run, a symlink (named `include`) will be generated
pointing to the `https` folder. If Nginx reports an error, it will fall back to the `http` folder.
After the certificate generation/renewal is complete, the `https` configs will be tried again.
