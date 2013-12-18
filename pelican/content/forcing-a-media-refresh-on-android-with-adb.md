Title: Forcing a media refresh on Android with adb
Date: 2013-09-09 18:52
Author: Carey Metcalfe
Tags: android, shell script

Android will automatically perform a media refresh when an SD card is
mounted.

Using [adb][], we can fake that event by manually sending a `MEDIA_MOUNTED`
intent.

For example, if you wanted to run a media refresh of the entire SD
card:

```bash
adb -d shell "am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard"
```
To refresh different directory, just change "/sdcard" to the absolute
path of the directory you want to refresh.

For more fine-grained control, use the `MEDIA_SCANNER_SCAN_FILE`
intent, which triggers a rescan of a single file.

  [adb]: http://developer.android.com/tools/help/adb.html
