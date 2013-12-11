Title: Making Steam for Linux close to the system tray
Date: 2013-12-11 06:00
Author: Carey Metcalfe
Tags: application

Steam for Linux is a little odd in how it handles a user clicking the close button.
Instead of exiting the program or mimimizing the application to the system tray, it just minimizes it to the taskbar.
The developers have said that this is temporary and that it will be changed in the future, but for now, there is a workaround.

To make Steam always minimize to the system tray, just add `STEAM_FRAME_FORCE_CLOSE=1` to your environment.

For more information see the [original GitHub issue][].

  [original GitHub issue]: https://github.com/ValveSoftware/steam-for-linux/issues/1025
