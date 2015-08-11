---
Title: Installing Fehlstart - A simple, quick application launcher
Date: 2013-09-09 18:51
Author: Carey Metcalfe
Tags:
  - application
  - code
---

[Fehlstart][] is an application launcher, much like [Launchy][],
[Quicksilver][], or [GNOME Do][]. However, where other launchers focus
on adding features, Fehlstart is as basic as they come. If you want to
search for files or control your media player, look elsewhere. Felhstart
launches applications. Period.

Fehlstart isn't in any major repositories so it has to be compiled from
source.

1. Install dependencies
    - `git`, `gcc`, `make`, `libgtk2.0-dev`, `libkeybinder-dev`
    - On most systems these packages will be available through your package manager
2. Get the code
    - `git clone https://gitlab.com/fehlstart/fehlstart.git`
3. Compile and install
    - Navigate into the folder containing the code
    - Run `make`
    - Run `make install` (with the needed permissions)
4. Add `fehlstart` to your window manager's autostart list
5. Log out and back in to launch Fehlstart.
6. Press the key combination `<Super>` + `<Space>` to bring up the
   launcher
7. Type to search through the installed applications, then press
   `<Enter>` to launch.

  [Fehlstart]: https://gitlab.com/fehlstart/fehlstart
  [Launchy]: http://www.launchy.net/
  [Quicksilver]: http://qsapp.com/
  [GNOME Do]: http://do.cooperteam.net/
