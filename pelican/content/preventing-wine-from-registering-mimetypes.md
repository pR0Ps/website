Title: Preventing Wine from registering mimetypes
Date: 2013-12-29 14:37
Author: Carey Metcalfe
Tags: linux, wine

When installing [Wine for Linux][], the install script insists on associating all text files with its built-in notepad.exe

As someone who uses [Vim][] almost exculsively, this is definitely not the desired behaviour.

To stop this from happening, run the following command _before_ installing Wine.

```bash
export WINEDLLOVERRIDES='winemenubuilder.exe=a'
```

This sets the path of the winemenubuilder library (the library that creates mimetype associations) to something invalid,
preventing the associations from being made when Wine installs.

Once Wine is installed, it won't try to associate notepad.exe again. However, if needed,
the library can be properly disabled via the libraries tab of wineconf.


  [Wine for Linux]: http://winehq.org/
  [vim]: http://www.vim.org/
