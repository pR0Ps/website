Title: How keyboard media keys work
Date: 2012-02-11 22:05
Author: Carey Metcalfe
Tags: application, registry, windows

A recent project of mine involved tearing apart an old keyboard (a [Dell
Y-UK-DEL1][]) and using the media keys to make a simple media controller box.  

Everything went smoothly with the build, but when I plugged it in, the
music media key launched [VLC][] instead of my preferred player, [foobar2000][].
After spending a while in the control panel looking for how to change this behavour
and finding nothing, I used [Process Explorer][] to trace the registry key
it was using to determine which application to launch.  

Turns out, the registry keys in
`HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\AppKey`
store the information regarding what program gets launched when a media key is pressed.

In this location there are a bunch of keys that map button IDs to file associations.
This is done by looking up the button ID when the button is pressed, then looking at
the contents of the string called "Association" in the button ID's key.

With my keyboard, the music media key maps to button 16. On my system, within the
key called "16", there is a string value called "Association". This was set to the
".cda" extension, which is associated with VLC. After changing the ".cda" association
to open using foobar2000, whenever I press the music key on my media controller, foobar2000 opens.

  [Dell Y-UK-DEL1]: http://i.imgur.com/dWBnR.jpg
  [VLC]: http://www.videolan.org/vlc/
  [foobar2000]: http://www.foobar2000.org/
  [Process Explorer]: http://technet.microsoft.com/en-us/sysinternals/bb896653
