Title: Git Checkout - Autocomplete Local Branches Only
Date: 2014-09-24 23:05
Author: Carey Metcalfe
Tags: git, shell script

Having Git autocomplete branch names when doing a checkout is super useful.
Having the autocomplete hang for 30 seconds because it has to look up all 3000
of the remote branches in a repo on a slow server is not so useful.
It's actually pretty frustrating.

My solution: changing the `git checkout` autocomplete to only look at local
branches, while using a `git checkoutr` alias to preserve the original
behaviour (because sometimes it's actually needed).

How it's done:

Define an alias for checkout
--------------------------------------------
We're going to use the same checkout command for the remote checkout, but need
to have a different command so the script can differentiate between them.
Making an alias does exactly this.

Create the alias by running `git config --global alias.checkoutr checkout`

Change the autocompletion function
----------------------------------
The checkout autocomplete behaviour is defined in a function called
`_git_checkout` in the git autocompletion file. We're going to override the
function with our own version that has different autocomplete logic in it.

The location of the file varies over different operating systems and
configurations, but on most distros it's `/etc/bash_completion.d/git`.

For a brew-installed git autocomplete on OSX, the file will probably be
`$(brew --prefix)/etc/bash_completion.d/git`

Once you've found the file, copy the entire `_git_checkout` function into your
`.bashrc` (or equivalent non-login shell startup script). Now look for the line

`__gitcomp_nl "$(__git_refs '' $track)"`

We're just going to change this line to:

```bash
if [ "$command" = "checkoutr" ]; then
    __gitcomp_nl "$(__git_refs '' $track)"
else
	__gitcomp_nl "$(__git_heads '' $track)"
fi
```

After saving and re-sourcing your `.bashrc` file, git will autocomplete local
branches when using `git checkout`, but will go back to the default behaviour
of autocompleting all references when using `git checkoutr`.

Credits to a combination of answers on [this](https://stackoverflow.com/questions/6623649/disable-auto-completion-of-remote-branches-in-git-bash) StackOverflow post.
