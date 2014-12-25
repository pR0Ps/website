---
Title: "Vim: Search and replace in multiple files"
Date: 2012-08-27 14:11
Author: Carey Metcalfe
Tags:
  - code
  - vim
---

As is the way with [Vim][], there are a ton of features, but stumbling
on the combination of commands that does what you want can be a bit
difficult sometimes. In this case, the objective is to perform a search
and replace over some files.

This is done in two steps: loading up the files to process, then issuing
a command to run on each of the files.

Load up the files to search using the `args` command. This command
supports multiple arguments and can use bash-style path completion.

    :args src/*.cpp src/*.hpp README.txt

Perform a replace using sed-style syntax using the `argdo` command. This
command iterates over all the files loaded by the `args` command and
performs a command on them. In this case, it's performing the replace
operation.

    :argdo %s/FindMe/ReplaceWithMe/gec | update

The flags used in this case are:

- g: global search (find more than a single occurance per line)
- e: suppress "string not found" error messages
- c: confirm each replace

Running `update` after the replace operation saves any changes to the
file before moving to the next one.

  [Vim]: http://www.vim.org/
