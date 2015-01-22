---
Title: Fixing save file corruption in Ridiculous Fishing
Date: 2014-12-11 12:44
Modified: 2015-01-21 23:01
Author: Carey Metcalfe
Tags:
  - android
  - games
---

[Ridiculous Fishing][] is a game by [Vlambeer][] about fishing. That's if you
can call chainsawing fish and blowing them out of the sky with a bazooka "fishing".

I've been playing this game on and off for a while now, but just recently I had
a problem where my save file somehow got corrupted, making the app refuse to open.

The problem first manifested as the game freezing for up to 5 seconds when
navigating around the UI or buying items in the in-game store. Since I was
running the game on a [Nexus 5][] (not the latest and greatest, but pretty
close), it seemed weird. The delay got longer and longer until the game
eventually crashed and refused to reopen.

Since I was pretty far into the game (I only needed to catch one more species
of fish!), I opted to try to fix it instead of just wiping the app's data and
starting again. I initially tried clearing the app's cache and
[reinstalling the app][], but the problem persisted.

The next step was to dump the games's data to my computer so I could do some
analysis on it. Some exploration on the device revealed that the settings and
data were stored in the folder `/data/data/com.vlambeer.RidiculousFishing.humble`
(I have the [Humble Bundle][] version of the app).

To pull that folder to my current directory, I used [ADB][]:

```bash
adb root #Restart adbd on the device with root permissions
adb pull /data/data/com.vlambeer.RidiculousFishing.humble/
```

A quick `du -h` revealed that something was very wrong in the
`files/Library/Preferences/com.vlambeer.RidiculousFishing.humble.plist` file.
It should've been just a text document, but was well over 200MB.

After trying out of habit to open the file in [Vim][] and having it hang (oops),
I paged through the document with [less][]. About halfway through the file,
there was a line containing `&amp;lt;message&amp;gt;@eggbirdTBA Take it to the
Smartypants Bar` (no, that's not a formatting error, in the plist there's XML
data stored in a `<string>` element, requiring the `<` and `>` characters to be
escaped) followed by about 200MB of garbage.

Apparently there are [ways to load huge files in Vim][], as well as other text
editors that handle them nicely, but since I already knew what line was causing
the issue, a simple [sed][] command would do the trick.

```bash
sed '/Take it to the Smartypants Bar/d' com.vlambeer.RidiculousFishing.humble.plist > temp.plist
```

Total size of `temp.plist`: 107.11KB. Much better.

After going though and deleting some lines around the one that was removed (to
make the XML valid again), I pushed the file back to the device:

```bash
adb push temp.plist /data/data/com.vlambeer.RidiculousFishing.humble/files/Library/Preferences/com.vlambeer.RidiculousFishing.humble.plist
```

Success! The game opened properly, all the freezing issues were gone, and my
save data was still there.

Now to find that stupid [Mimic Fish][]...

  [Ridiculous Fishing]: https://play.google.com/store/apps/details?id=com.vlambeer.RidiculousFishing
  [Vlambeer]: http://www.vlambeer.com/
  [Nexus 5]: http://en.wikipedia.org/wiki/Nexus_5
  [reinstalling the app]: {filename}/blog/reinstall-android-app-without-losing-data.md
  [Humble Bundle]: https://www.humblebundle.com/
  [ADB]: http://developer.android.com/tools/help/adb.html
  [Vim]: http://www.vim.org/
  [less]: http://en.wikipedia.org/wiki/Less_%28Unix%29
  [ways to load huge files in Vim]: http://stackoverflow.com/questions/908575/how-to-edit-multi-gigabyte-text-files-vim-doesnt-work
  [sed]: http://en.wikipedia.org/wiki/Sed
  [Mimic Fish]: http://gaming.stackexchange.com/questions/159564/how-to-catch-the-mimic-fish
