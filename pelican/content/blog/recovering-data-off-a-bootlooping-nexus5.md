---
title: Recovering data off a bootlooping Nexus 5
date: 2018-09-18 18:30
modified: 2020-03-17 22:38
author: Carey Metcalfe
tags:
 - android
 - data recovery
 - electronics
 - hardware
---

The situation
-------------
The [Nexus 5][] that I've had for almost 5 years started bootlooping repeatedly.

I've replaced/repaired multiple parts of it over the years but lately it had been more flaky than
usual. For example:

 - Sometimes when booting it would show a "Firmware update in progress, don't disconnect your
   computer" message, even though there was nothing connected to the USB port.
 - It would randomly freeze and soft reboot when using it about once a week.
 - When propping it up on a book or something to angle the screen towards me, the screen would
   sometimes turn off and on (as it turns out, this was a warning sign)

I've been ready to replace it for a while, but couldn't justify it while this one was perfectly (ok,
mostly) functional. That changed today when I tried to turn it on and it started bootlooping.

So buy a new phone and move on, right? Right, except I committed the cardinal sin of living in the
digital age - not having complete backups. Yeah, yeah, I know.

I got most of it. I'd been using [Syncthing][] to automatically back up photos, videos, and other
files to my home server every night so they were all good. The problem was that I had been using
[FreeOTP-export][] to back up my [2FA][] secrets manually and the latest backup was missing a bunch
of logins.

So I needed to somehow get into my non-booting phone and pull the data off it. At least because I
was replacing it, all destructive options were on the table.

Diagnosis
---------

The first step was seeing if other people had this problem. Some searching revealed that it was most
likely the power button gone bad and being stuck in the pressed position.

To confirm this, I rapidly hammered the power button on a hard surface while booting, hoping that
the jarring would un-stick it and let it boot. This sort of worked in that it would boot, but
stopping at any point would result it it powering off again. It was also extremely difficult to tap
it consistently enough to keep the phone on for long enough to pull any data off it.

The issue I mentioned earlier where propping the phone up made the screen turn on and off now made sense.
I'm guessing this was causing a slight flexing of the power button switch, causing it to close and
trigger. Over time this must've permanently bent something so it stayed closed, causing the
bootloop.

Now that I had pretty much confirmed that it was something physically wrong with the power button
circuitry, I messaged my friend [Mike][]. When it comes to electronics, he's definitely more
experienced than me. Plus, he lets me borrow his tools :)

The "fix"
---------

The next day Mike came over with his soldering iron and we started brainstorming.

The plan of attack was to just take the power button off the board entirely. It can't always be
pressed down if it's not on the board right?

In preparation for this, I wanted the phone to automatically boot when it was plugged into a charger
so I wouldn't have to manually short the pins on the board. Fortunately this can be done with a
fastboot command: `fastboot oem off-mode-charge 0` (basically: don't allow charging while off,
therefore turn on when charging).

After desoldering the power button from the main board, it was still bootlooping. Not good. I went
back and cleaned up the solder to make absolutely sure that the power button signal pins weren't
connected in any way. Still bootlooping when powered on. It would get to the bootloader and stay
there, meaning the power button wasn't being pressed anymore, but when launching to either recovery
or the main OS, it would immediately restart.

Looked into dumping data from the bootloader - impossible.

Reflashed the boot and recovery partitions - same thing.

Tried booting into recovery using `fastboot boot <recovery-image>` - bootloop.

> sounds like it's time to cry
>
>   -- Someone on [Freenode's #lineageos-dev channel][] after I explained the situation


Thankfully, it was not. Right after that, someone else asked if I had reconnected the battery. I had
not.

Turns out that a working battery is required to boot the phone, even when it's plugged in. I had
taken the battery out to desolder the power button and never put it back in since the phone seemed
to boot fine without it. Whoops.

After plugging the battery into the board and booting the phone, it launched the main OS without any
issues. Huge relief.

Recovering the data
-------------------
With the phone booted up normally I used `adb` (running as root) to pull the 2FA codes and
other important things that I knew I needed over to my laptop.

I really don't trust myself to remember everything so I booted the phone into recovery mode and
pulled a complete backup of `/data/data`, `/data/app`, and `/storage/sdcard` ([not actually an
sdcard][]) to my laptop as well.

To make **absolutely** sure I didn't miss anything, I also pulled a raw image of the entire flash
memory (disk-based encryption was not enabled) using `adb pull /dev/block/mmcblk0 mmcblk0.img`.
Everything I need should be in the normal backups, but if not, I can always go spelunking through
that image.

Lessons learned
---------------
 - If it's important, back it up *automatically*. If it's not automatic, at some point it will be
   missed.
 - Make sure you have the ability to get root access on every device you own before you need it - in
   this case I wouldn't've been able to pull the 2FA codes or do full backups without it.

Future plans
------------
For the Nexus 5, I'm planning on either buying a replacement power button or maybe just soldering
some wires to the exposed pads and snaking them out of the phone to an external button if I can't
find one. The phone can then continue to be used as an app development testbed, a [Chromecast][]
remote, or as a [basic emulation console][] until it dies for real. In theory I could keep using it
as a phone too, but at this point I just don't trust it enough.

For my next phone, I've decided on the [Xperia XZ1 Compact][]. It's a smaller phone that's mostly
waterproof ([IP68][]), has a fast SoC ([Snapdragon 835][]), a headphone jack, SD card support, and
great battery life. I have high hopes for it. Also, as evidenced by this post, having root access to
the OS is pretty critical at times so I'll be flashing [LineageOS][] on it ASAP.


[2FA]: https://en.wikipedia.org/wiki/Multi-factor_authentication
[Chromecast]: https://store.google.com/product/chromecast
[FreeOTP-export]: https://github.com/pR0Ps/freeotp-export
[Freenode's #lineageos-dev channel]: https://webchat.freenode.net/?channels=#lineageos-dev
[IP68]: https://en.wikipedia.org/wiki/IP_Code
[LineageOS]: https://lineageos.org/
[Mike]: https://mremallin.ca/
[Nexus 5]: https://en.wikipedia.org/wiki/Nexus_5
[Snapdragon 835]: https://en.wikipedia.org/wiki/List_of_Qualcomm_Snapdragon_systems-on-chip#Snapdragon_835_and_845_(2017/18)
[Syncthing]: https://github.com/pR0Ps/freeotp-export
[TOTP]: https://en.wikipedia.org/wiki/Time-based_One-time_Password_algorithm
[Xperia XZ1 Compact]: https://en.wikipedia.org/wiki/Sony_Xperia_XZ1_Compact
[basic emulation console]: {filename}/blog/adding-xbox360-controller-support-to-a-nexus5.md
[not actually an sdcard]: https://developer.android.com/guide/topics/data/data-storage.html#filesExternal
