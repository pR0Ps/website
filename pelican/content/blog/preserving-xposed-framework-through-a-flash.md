Title: Preserving the Xposed Framework through a ROM flash
Date: 2014-03-22 22:04
Author: Carey Metcalfe
Tags: android, shell script

The [Xposed Framework](http://repo.xposed.info/) is a neat Android program that
enables [user-made modules](http://repo.xposed.info/module-overview) to change
the behaviour of the lower-level Android OS. It does this by modifying
`/system/bin/app_process` to add some hooks into it.

The issue is that when flashing a new ROM, the modified `app_process` is
reverted back to the original version, disabling the Xposed Framework
until it's restored.

**UPDATE:** The Xposed Framework installer now includes the option to flash
a zip file to install the framework instead of patching `app_process` directly.
The method detailed in this post will still work, but the new way to make sure
the framework is installed after flashing a new ROM is to simply flash the
Xposed installer zip right after flashing the ROM.

The solution to this is a script that will automatically back up the existing
`app_process` before a flash, then restore it after the flash completes.

[This script](http://forum.xda-developers.com/showpost.php?p=43617268&postcount=2087)
does exactly that. To enable it, download it to the Android device, move it to
`/system/addon.d/90-xposed.sh`, and give it executable permissions.

This can be done on the device with a few different programs, but it's much
easier to do from a computer with [adb](https://developer.android.com/tools/help/adb.html).

Download the script and push it to the SD card of the Android device with
```bash
adb push 90-xposed.sh /sdcard/
```

Once the file is on the device, log into it (using `adb shell`) and run the
following commands:
```bash
su #Get root permissions
cp /sdcard/90-xposed.sh /system/addon.d/ #Copy the file to the correct folder
chmod 755 /system/addon.d/90-xposed.sh #Make the file executable
```

After logging out of the device, the Xposed framework will stay installed and
active even after flashing a new ROM. Note that this should only really be
used in situations where the ROM isn't changing too much (like flashing a new
nightly ROM).

In situations where `app_process` would actually be changed by the flash, this
script could cause issues as it would restore an incorrect version of the file.
If this happens, delete `app_process` and `app_process.orig` in the
`/system/bin/` directory, then reflash. The script won't interefere, allowing
the flash to update `app_process` to the correct version. After rebooting,
install the Xposed Framework again.
