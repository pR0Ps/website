---
title: Remove an application from the cmd-tab switcher on macOS
date: 2015-01-22 23:30
author: Carey Metcalfe
tags:
  - application
  - macOS
---

At work, I use [iTerm2][] as my main terminal emulator. For quick access, I have
it configured to drop down from the top of the screen when `F12` is pressed.

Unfortunately, it also shows up in the application switcher, bumping up into
the 'last used' position whenever it's activated and getting in the way. Since
I already have access to the terminal via `F12`, there's no need for it to be
shown in the application switcher as well.

Changing how an application behaves can be done by editing its `Info.plist`
file. The key `LSUIElement` ([according to the Apple documentation][])
"Specifies whether the app is an agent app, that is, an app that should not
appear in the Dock or Force Quit window."

To set this key, open the application's `Info.plist` at
`/Applications/[application name].app/Contents/Info.plist` and add
`<key>LSUIElement</key><true/>` after the first `<dict>` tag. The result should
look something like this:

```xml hl_lines="5"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>LSUIElement</key><true/>
    <!-- The rest of the plist data -->
</dict>
</plist>
```

Once the `LSUIElement` key is set to `true`, relaunch the application to see the
changes.

Be warned that not only does this remove the application from the
application switcher, it also removes it from the dock and stops it from showing
the menu bar on the top of the screen.

  [iTerm2]: http://iterm2.com
  [according to the Apple documentation]: https://developer.apple.com/library/mac/documentation/General/Reference/InfoPlistKeyReference/Articles/LaunchServicesKeys.html#//apple_ref/doc/uid/20001431-108256
