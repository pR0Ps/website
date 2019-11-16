---
Title: Git checkout - autocomplete local branches only
Date: 2014-09-24 23:05
Modified: 2018-03-24 19:00
Author: Carey Metcalfe
Tags:
  - git
  - shell script
---

Having Git autocomplete branch names when doing a checkout is super useful.  Having the autocomplete
hang for 30 seconds because it has to look up all 3000 of the remote branches in a massive repo is
not so useful. It's actually pretty frustrating.

My solution: changing the `git checkout` autocomplete to only look at local branches, while using a
`git checkoutr` alias to preserve the original behaviour (because sometimes it's actually needed).

How it's done:

Define an alias for checkout
----------------------------
We're going to use the same checkout command for the remote checkout, but need to have a different
command so the script can differentiate between them.  Making an alias does exactly this.

Create the alias by running `git config --global alias.checkoutr checkout`

Change the autocompletion function
----------------------------------
The checkout autocomplete behaviour is defined in a function called `_git_checkout` in the git
autocompletion file. We're going to override the function with our own version that has different
autocomplete logic in it.

The location of the file varies over different operating systems and configurations, but here are a
few spots to look:

 - `/etc/bash_completion.d/git`
 - `/usr/share/bash-completion/completions/git`

For a brew-installed git autocomplete on macOS, the file will probably be
`$(brew --prefix)/etc/bash_completion.d/git-completion.bash`

Once you've found the file, copy the entire `_git_checkout` function into your `.bashrc` (or
equivalent non-login shell startup script). Now look for the line

`__git_complete_refs $track_opt`

We're going to replace that line with:

```bash
if [ "$command" = "checkoutr" ]; then
    __git_complete_refs $track_opt
else
    __gitcomp_direct "$(__git_heads "" "$cur" " ")"
fi
```

After saving and re-sourcing your `.bashrc` file, git will autocomplete local branches and tags when
using `git checkout`, but will go back to the default behaviour of autocompleting all references
when using `git checkoutr`.

Credits to a combination of answers on [this](disable-auto-completion-of-remote-branches-in-git-bash) StackOverflow post.

EDIT 2017-10-02: Updated to work with [git v2.13.0][] thanks to [Alexander Ko's comment][].  
EDIT 2018-03-24: Updated to [speed up branch and tag completion][].


  [disable-auto-completion-of-remote-branches-in-git-bash]: https://stackoverflow.com/questions/6623649/disable-auto-completion-of-remote-branches-in-git-bash
  [git v2.13.0]: https://github.com/git/git/commit/15b4a163950c2e8660a7797ce3975ccea8705f80#diff-f37c4f4a898819f0ca4b5ff69e81d4d9
  [Alexander Ko's comment]: https://gist.github.com/mmrko/b3ec6da9bea172cdb6bd83bdf95ee817#gistcomment-2218059
  [speed up branch and tag completion]: https://github.com/git/git/commit/227307a639c96b3579b7fe60840fdae123d1ee88
