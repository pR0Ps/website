---
Title: Adding Xbox 360 controller support to a Nexus 5
Date: 2015-01-14 20:26
Modified: 2018-09-11 14:30
Author: Carey Metcalfe
Tags:
  - android
---

!!! Update
    CyanogenMod has effectively been replaced by [LineageOS][]. The links in this article originally
    all pointed to CyanogenMod but since it no longer exists, I've updated them to use the LineageOS
    equivilents where possible. The instructions will also need to be slightly modified for use with
    LineageOS builds.

Introduction
------------
I finally just bought a new phone (a [Nexus 5][]), and after flashing [CyanogenMod][] onto it, I've
been messing around with its [OTG][] support. My old phone (a [Nexus 4][]) [didn't have the
capability][] so being able to plug in keyboards, mice, external hard drives, and various other
peripherals was (embarrassingly enough) a thrill.

Keyboards worked, mice worked, but when an Xbox 360 controller was plugged in, nothing happened.
Turns out that while the kernel didn't have support for it enabled out of the box, getting it
enabled and pushing the change upstream into the CyanogenMod project was easier than I thought.

Beware that this post is going to be more of a record of what I did so that I can do it again and
less of a coherent tutorial.

Building CyanogenMod
--------------------
First step was to download and compile CyanogenMod for my phone. I'm not going to go into this in
any detail on this because there's already a [good overview][] on the CyanogenMod wiki that covers
the entire process, as well as a [customized guide for the Nexus 5][]. If those articles are
followed correctly, you should be able to build a fresh CyanogenMod image with:

```bash
brunch hammerhead
```

Enabling the kernel module
--------------------------
Once the image was flashed to the phone and verified to be working, the next step was to enable the
[xpad kernel module][].

Copy current kernel config to the kernel directory for editing:
```bash
cd <build dir>/kernel/lge/hammerhead/
cp arch/arm/configs/cyanogenmod_hammerhead_defconfig .config
```

Edit the config:
```bash
make menuconfig ARCH=arm
```

At this point, a menu will come up. Search for `xpad` (type `/xpad`), and take note of the paths.
`ESC` out of the search, navigate the tree and enable the modules found with the search. Save and
exit.

Copy the config back and clean up any stray `*.o` files:
```bash
cp .config arch/arm/configs/cyanogenmod_hammerhead_defconfig
make mrproper
```

After enabling the module, rebuild CyanogenMod using the normal `brunch hammerhead` and flash it to
the phone.

Submitting the change upstream
------------------------------
Since Xbox controller support had already been requested in <del>[a JIRA ticket][]</del>(dead link), I went
through the process to submit [the change][] on the CyanogenMod Gerrit instance for inclusion in the
next release. There's a guide for this [here][]. As well as the guide, I found the people in
[#cyanogenmod-dev on Freenode][irc] to be very helpful.

A short while after submitting [the change][] to Gerrit, it was merged into the `cm-11.0` branch as
commit [`i7ef4f6a`][7ef4f6a] and pushed out in the next nightly build ([changelog screenshot][]).

Wrap-up
-------

It feels great to be able to contribute to an amazing open source project that had [at least a
million people][] using it at one point or another. I recognize that the change by itself was just
changing a config file to enable functionality that already existed, but it's helped me get through
some of the non-coding hurdles of contributing to an Android fork like CyanogenMod (adb, fastboot,
unlocking and rooting phones, compiling AOSP, flashing images, the contribution process, etc). This
time the actual contribution itself was minor, but it's gotten me more familier with the process,
hopefully making it easier to contribute something more substantial in the future.

In the end, I learned a lot about Android development and how all the different pieces that I had
read about at one point or another actually fit together. During the whole process I also lost a lot
of the fear I had about messing with phones and other more expensive locked down devices. Going
forward, I'm going to attempt to compile and flash open source operating systems like CyanogenMod
onto more devices that I own. I like being able to tweak things and feel like I really own them,
hardware and software.


  [CyanogenMod]: https://en.wikipedia.org/wiki/CyanogenMod
  [LineageOS]: https://lineageos.org/
  [Nexus 4]: http://en.wikipedia.org/wiki/Nexus_4
  [Nexus 5]: http://en.wikipedia.org/wiki/Nexus_5
  [didn't have the capability]: http://blog.gsmarena.com/nexus-4-does-not-support-usb-otg-despite-google-saying-otherwise/
  [OTG]: http://en.wikipedia.org/wiki/USB_On-The-Go
  [good overview]: https://web.archive.org/web/20161224200646/https://wiki.cyanogenmod.org/w/Development
  [customized guide for the Nexus 5]: https://wiki.lineageos.org/devices/hammerhead/build
  [a JIRA ticket]: https://jira.cyanogenmod.org/browse/CYAN-4469
  [the change]: https://review.lineageos.org/#/c/LineageOS/android_kernel_lge_hammerhead/+/87409/
  [7ef4f6a]: https://github.com/LineageOS/android_kernel_lge_hammerhead/commit/7ef4f6a87cc114b5010b623d72840b1d38ea01ed
  [xpad kernel module]: https://www.kernel.org/doc/html/v4.16/input/devices/xpad.html
  [here]: https://wiki.lineageos.org/submitting-patch-howto.html
  [irc]: https://webchat.freenode.net/?channels=#cyanogenmod-dev
  [changelog screenshot]: {static}/images/cyanogenmod-changelog-xbox-support.png
  [at least a million people]: https://twitter.com/CyanogenMod/status/157378138802888704
