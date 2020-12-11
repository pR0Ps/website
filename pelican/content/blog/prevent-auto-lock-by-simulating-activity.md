---
Title: Preventing auto-locking and sleeping by simulating user activity
Date: 2020-12-10 23:12
Author: Carey Metcalfe
Tags:
  - windows
  - macOS
  - linux
  - shell script
---

This post will detail how to simulate activity on your computer in order to prevent it from
auto-locking or going into sleep mode. Note that this will usually also prevent the "auto-away"
functionality of various chat programs from ever marking you as "away".

Generally you should change your operating system's settings to disable sleeping and auto-locking if
possible instead. These methods are for when you don't have the access or permission to change those
settings (ie. locked-down devices).

Windows
-------
This method runs a [Powershell][] script on login that toggles [scroll lock][] on/off every minute.
Since scroll lock mostly doesn't do anything on modern systems and the script will press it twice to
immediately unlock/relock it, this is basically unnoticeable to the user. However, if you have
issues simply swap the two `{SCROLLLOCK}`s in the below command to something else. A full list of
special keys can be found [here][VBScript SendKeys].

1. Open Explorer (shortcut: `Win+E`)
2. Paste `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup` into the location bar and hit
   enter to navigate there.
3. Right click in the folder and click `New > Shortcut` to open the shortcut creation wizard.
4. Paste the following as the shortcut's location:

        powershell.exe -windowstyle hidden -command "$myshell=New-Object -com \"Wscript.Shell\";while(1){$myshell.SendKeys(\"{SCROLLLOCK}{SCROLLLOCK}\");Start-Sleep -Seconds 60}"

5. Give it any name you like and hit `Finish`


macOS
-----
This method runs a shell script on login that uses a tool called [`cliclick`][cliclick] to move the
mouse one pixel left and right every minute. This is such a small and fast movement that it's
usually not noticeable unless you're really looking for it.

1. Install `cliclick` from [the project website][cliclick] or via [brew][] (`brew install cliclick`)
2. Create a script called `jiggle` with the following contents:
```
#!/bin/sh
while true; do
    cliclick 'm:-1,+0' 'm:+1,+0'
    sleep 60
done
```
3. Make the script executable (`chmod +x jiggle`)
4. Open System Preferences, search for "login items" and hit enter.
5. Click the `+` button, select the `jiggle` script and hit "Add". You should see it appear in the
   list of programs as a "Unix executable". Check the "Hide" checkbox beside it and exit.


Xorg-based Linux
----------------
Much like the macOS version above, this moves the mouse one pixel left and right every minute. If
you would prefer to instead use a keyboard-based method like the above Windows version, use `xdotool
key Scroll_Lock` twice instead of the `xdotool mousemove_relative *` commands in the following
script. More special key names for `xdotool` can be found [here][xdotool key names].

1. Install [`xdotool`][xdotool] (usually available via your package manager)
2. Create a script called `jiggle` with the following contents:
```
#!/bin/sh
while true; do
    xdotool mousemove_relative --sync -- -1 0
    xdotool mousemove_relative 1 0
    sleep 60
done
```
3. Make the script executable (`chmod +x jiggle`)
4. Configure your OS to run the script at login. Usually this would be done through the desktop
   environment's settings or via something like [`systemd`][systemd].


Wayland-based Linux
-------------------
Some preliminary research suggests that this is possible on Wayland using [`ydotool`][ydotool] as a
replacement for `xdotool`. I don't currently run a Wayland-based setup so I can't test it. If you
manage to find a solution for Wayland feel free to send it to me and I'll update the post.


 [brew]: https://brew.sh/
 [cliclick]: https://www.bluem.net/en/projects/cliclick/
 [Powershell]: https://en.wikipedia.org/wiki/Powershell
 [scroll lock]: https://en.wikipedia.org/wiki/Scroll_lock
 [systemd]: https://www.freedesktop.org/wiki/Software/systemd/
 [VBScript SendKeys]: https://social.technet.microsoft.com/wiki/contents/articles/5169.vbscript-sendkeys-method.aspx
 [xdotool key names]: https://gitlab.com/cunidev/gestures/-/wikis/xdotool-list-of-key-codes
 [xdotool]: https://www.semicomplete.com/projects/xdotool/
 [ydotool]: https://github.com/ReimuNotMoe/ydotool
