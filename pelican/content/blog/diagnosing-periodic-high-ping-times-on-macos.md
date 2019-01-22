---
title: Diagnosing periodic high ping times on macOS
date: 2019-01-22 04:00
author: Carey Metcalfe
tags:
 - macOS
 - networking
---

Background
----------
Up until a few months ago, my home network setup was pretty terrible. The entire house ran off the
WiFi provided by an [OpenWRT][]-powered [TP-Link WDR3600][] from 2013 in the far corner of the
house. So when I fired up a game on my laptop via [Steam in-home streaming][] and got unplayable lag
and stuttering, I just figured that the issue was the network and left it at that. After all, the
gaming PC was connected via WiFI from the opposite corner of the house with no shortage of walls in
between.

In November 2018, I finally got serious about the network upgrade I had been planning. I'll probably
do a more in-depth post about this at some point, but to make a long story short: Most things are
wired and what isn't is connected via a modern, centrally-located access point. Performance is
noticeably better in general and *amazingly* better for high-bandwidth tasks like transferring
files.

So when I excitedly fired up the same game on my laptop, I was pretty surprised that it was still
unplayable. At this point I should clarify that the game was not something that requires a CRT and
wired controller for super-low response times. So when I say unplayable, I mean legitimately
unplayable. I'm talking periodic lag spikes that caused the video to drop a few seconds or more
behind the inputs. Even turn-based games would have issues with the amount of lag.

Narrowing the scope
-------------------
To make sure it wasn't an issue with the streaming software, the gaming PC, or the network, I used
`ping` to test the latency to the gateway from a few hosts. All the computers *except* my laptop had
normal ping times. Running it on my laptop looked like this:
```bash
$ ping pfsense.lan | tee >(grep -oP 'time=\K\S*' | spark)
PING pfsense.lan (192.168.1.1): 56 data bytes
64 bytes from 192.168.1.1: icmp_seq=0 ttl=64 time=1.574 ms
64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=0.996 ms
64 bytes from 192.168.1.1: icmp_seq=2 ttl=64 time=1.568 ms
64 bytes from 192.168.1.1: icmp_seq=3 ttl=64 time=92.153 ms
64 bytes from 192.168.1.1: icmp_seq=4 ttl=64 time=39.079 ms
64 bytes from 192.168.1.1: icmp_seq=5 ttl=64 time=14.307 ms
64 bytes from 192.168.1.1: icmp_seq=6 ttl=64 time=1.570 ms
64 bytes from 192.168.1.1: icmp_seq=7 ttl=64 time=1.636 ms
64 bytes from 192.168.1.1: icmp_seq=8 ttl=64 time=1.698 ms
64 bytes from 192.168.1.1: icmp_seq=9 ttl=64 time=1.568 ms
64 bytes from 192.168.1.1: icmp_seq=10 ttl=64 time=1.550 ms
64 bytes from 192.168.1.1: icmp_seq=11 ttl=64 time=1.106 ms
64 bytes from 192.168.1.1: icmp_seq=12 ttl=64 time=1.832 ms
64 bytes from 192.168.1.1: icmp_seq=13 ttl=64 time=1.816 ms
64 bytes from 192.168.1.1: icmp_seq=14 ttl=64 time=36.598 ms
64 bytes from 192.168.1.1: icmp_seq=15 ttl=64 time=42.863 ms
64 bytes from 192.168.1.1: icmp_seq=16 ttl=64 time=20.747 ms
64 bytes from 192.168.1.1: icmp_seq=17 ttl=64 time=3.112 ms
64 bytes from 192.168.1.1: icmp_seq=18 ttl=64 time=1.695 ms
64 bytes from 192.168.1.1: icmp_seq=19 ttl=64 time=1.795 ms
64 bytes from 192.168.1.1: icmp_seq=20 ttl=64 time=1.504 ms
64 bytes from 192.168.1.1: icmp_seq=21 ttl=64 time=1.644 ms
64 bytes from 192.168.1.1: icmp_seq=22 ttl=64 time=1.732 ms
64 bytes from 192.168.1.1: icmp_seq=23 ttl=64 time=1.581 ms
64 bytes from 192.168.1.1: icmp_seq=24 ttl=64 time=1.794 ms
64 bytes from 192.168.1.1: icmp_seq=25 ttl=64 time=33.367 ms
64 bytes from 192.168.1.1: icmp_seq=26 ttl=64 time=124.282 ms
64 bytes from 192.168.1.1: icmp_seq=27 ttl=64 time=97.719 ms
64 bytes from 192.168.1.1: icmp_seq=28 ttl=64 time=76.501 ms
64 bytes from 192.168.1.1: icmp_seq=29 ttl=64 time=1.734 ms
64 bytes from 192.168.1.1: icmp_seq=30 ttl=64 time=1.622 ms
64 bytes from 192.168.1.1: icmp_seq=31 ttl=64 time=1.758 ms
64 bytes from 192.168.1.1: icmp_seq=32 ttl=64 time=1.578 ms
64 bytes from 192.168.1.1: icmp_seq=33 ttl=64 time=1.527 ms
64 bytes from 192.168.1.1: icmp_seq=34 ttl=64 time=1.017 ms
^C
 ▁▁▁▆▃▁▁▁▁▁▁▁▁▁▃▃▂▁▁▁▁▁▁▁▁▂█▆▅▁▁▁▁▁▁
```
(sweet graph at the end courtesy of [spark][])

Notice the periodic spikes. Clearly there's something going on with the network connection on my
laptop. Connecting via a wired connection and running it again confirmed that it was only happening
on WiFi.

WiFi debugging
--------------
Now that I had narrowed the issue down to an issue with the WiFi, I could start trying to debug it.

After coming across [this very helpful post][] explaining how, I enabled WiFi debug logging by running:
```bash
sudo /System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport en0 debug +AllUserland
```
(remember to turn this off after, `airport` is pretty chatty with debug logs enabled)

I then watched the wifi log (`sudo tail -f /var/log/wifi.log`) as I ran the same `ping` command.
Whenever I saw ping times spike, I also saw the following entries in the WiFi log:
```bash
Tue Nov 27 02:01:33.764 IPC: <airportd[68]> ADDED XPC CLIENT CONNECTION [QSyncthingTray (pid=14397, euid=501, egid=20)]
Tue Nov 27 02:01:33.765 Info: <airportd[68]> SCAN request received from pid 14397 (QSyncthingTray) with priority 0
Tue Nov 27 02:01:33.766 Scan: <airportd[68]> Cache-assisted scan request for QSyncthingTray on channel 1 does not require a live scan
Tue Nov 27 02:01:33.766 Scan: <airportd[68]> Cache-assisted scan request for QSyncthingTray on channel 2 does not require a live scan
Tue Nov 27 02:01:33.766 Scan: <airportd[68]> Cache-assisted scan request for QSyncthingTray on channel 3 does not require a live scan
Tue Nov 27 02:01:33.766 Scan: <airportd[68]> Cache-assisted scan request for QSyncthingTray on channel 4 does not require a live scan
Tue Nov 27 02:01:33.766 Scan: <airportd[68]> Cache-assisted scan request for QSyncthingTray on channel 5 does not require a live scan
Tue Nov 27 02:01:33.766 Scan: <airportd[68]> Cache-assisted scan request for QSyncthingTray on channel 6 does not require a live scan
Tue Nov 27 02:01:33.766 Scan: <airportd[68]> Cache-assisted scan request for QSyncthingTray does not require a live scan
Tue Nov 27 02:01:33.766 AutoJoin: <airportd[68]> Successful cache-assisted scan request for QSyncthingTray with channels {(
Tue Nov 27 02:01:33.766     <CWChannel: 0x7f9073514e70> [channelNumber=1(2GHz), channelWidth={20MHz}, active],
Tue Nov 27 02:01:33.766     <CWChannel: 0x7f90735507b0> [channelNumber=2(2GHz), channelWidth={20MHz}, active],
Tue Nov 27 02:01:33.766     <CWChannel: 0x7f9073526370> [channelNumber=3(2GHz), channelWidth={20MHz}, active],
Tue Nov 27 02:01:33.766     <CWChannel: 0x7f9073526420> [channelNumber=4(2GHz), channelWidth={20MHz}, active],
Tue Nov 27 02:01:33.766     <CWChannel: 0x7f907354ddb0> [channelNumber=5(2GHz), channelWidth={20MHz}, active],
Tue Nov 27 02:01:33.766     <CWChannel: 0x7f907354c6c0> [channelNumber=6(2GHz), channelWidth={20MHz}, active]
Tue Nov 27 02:01:33.766 )} took 0.0007 seconds, returned 5 results
< insert logs like above for all channels all the way up to 144 in batches of 6 >
Tue Nov 27 02:01:33.779 IPC: <airportd[68]> INVALIDATED XPC CLIENT CONNECTION [QSyncthingTray (pid=14397, euid=501, egid=20)]
< 10 seconds pass>
Tue Nov 27 02:01:43.847 IPC: <airportd[68]> ADDED XPC CLIENT CONNECTION [QSyncthingTray (pid=14397, euid=501, egid=20)]
< same scanning logs as above >
Tue Nov 27 02:01:46.741 IPC: <airportd[68]> INVALIDATED XPC CLIENT CONNECTION [QSyncthingTray (pid=14397, euid=501, egid=20)]
< ... and repeat >
```

This pretty clearly indicates that the [QSyncthingTray][] application (a tray icon to monitor
[Syncthing][]) was periodically requesting WiFi scans which, in turn, caused the bursts of latency.
After quitting the application and running `ping` again, the times were all <2ms, even after running
for a few minutes. Also, when I started up the game again to test it, the lag was completely gone!

Digging deeper
--------------
Since QSyncthingTray is open source, I filed a [bug report][] on the project and dug into the code
to see if I could pinpoint the issue. After finding nothing out of the ordinary and doing a bunch of
searching the internet, it turns out that it's not an issue with QSyncthingTray at all, but with
[Qt][], a cross-platform SDK that QSyncthingTray and many other programs use. Some classmates and I
actually used it to make a game called [ParticleStorm][] back in university.

There are open bug reports against this issue from [2013][], [2014][], and [2015][]. Additionally,
there are loads of [blog][] [posts][] and [per][]-[program][] [workarounds][]. It's a little
disappointing that just running a network-enabled Qt application can seriously disrupt real-time
applications on the same system. Granted, I have no knowledge of the complexities of this issue, but
at the very least it seems [the documentation][] could be clearer on the issue so developers stop
[getting surprised by it][].

Anyway, the "fix" is to set `QT_BEARER_POLL_TIMEOUT=-1` as an environment variable on your system.
Honestly, I've just stopped using QSyncthingTray instead. Not that it's not useful, I just realized
that I didn't really need it. Syncthing works well enough that I don't find myself ever worrying
about it. If a Qt application ever becomes an essential part of my setup I guess I'll have to
revisit this.

Takeaways
---------
1. When macOS scans for networks (as it does when requested by an application, when you click the WiFi
   icon, or when you request your location) it causes high ping times and dropped packets. According to
   bug reports, scanning for WiFi networks on other OS's causes the same issues. This is something I
   didn't really expect, but good to know going forward.

2. Qt has a bug where instantiating a `QNetworkConfigurationManager` causes it to scan for WiFi
   networks every 10 seconds by default. Some applications set the `QT_BEARER_POLL_TIMEOUT` environment
   variable themselves to disable this behaviour, but the majority probably have no idea that it's even
   an issue until a user reports it.

So if you're seeing regular latency spikes, audit what programs you have running. Specifically look
for programs built with Qt. Setting the `QT_BEARER_POLL_TIMEOUT` environment variable to `-1` can
help with these. Applications that use your location [could also be the culprit][]. Who knew keeping
your ping down to an acceptable level was such a minefield...


[2013]: https://bugreports.qt.io/browse/QTBUG-34641
[2014]: https://bugreports.qt.io/browse/QTBUG-40332
[2015]: https://bugreports.qt.io/browse/QTBUG-46015
[OpenWRT]: https://openwrt.org/
[ParticleStorm]: https://github.com/pR0Ps/ParticleStorm
[QSyncthingTray]: https://github.com/sieren/QSyncthingTray
[Qt]: https://www.qt.io
[Steam in-home streaming]: https://store.steampowered.com/streaming/
[Syncthing]: https://syncthing.net/
[TP-Link WDR3600]: https://www.tp-link.com/us/products/details/TL-WDR3600.html
[blog]: https://lostdomain.org/2017/06/17/qt-qnetworkaccessmanager-causing-latency-spikes-on-wifi/
[bug report]: https://github.com/sieren/QSyncthingTray/issues/237
[could also be the culprit]: https://apple.stackexchange.com/questions/263638/macbook-pro-experiencing-ping-spikes-to-local-router/317431#317431
[getting surprised by it]: https://www.reddit.com/r/krita/comments/9xea9b/this_is_gonna_sound_crazy_but_is_krita/e9tfify/
[per]: https://github.com/qbittorrent/qBittorrent/commit/c2b6e1ce1aa402b143d0154748c518a87bc6424a
[posts]: https://justus.berlin/2016/04/reducing-cpu-load-and-energy-consumption-of-texstudio-on-the-mac/
[program]: https://github.com/sqlitebrowser/sqlitebrowser/commit/73946400c32d1f7cfcd4672ab0ab3f563eb84f4e
[spark]: https://github.com/holman/spark/wiki/Wicked-Cool-Usage#visualize-ping-times-jnovinger
[the documentation]: https://doc.qt.io/qt-5/qnetworkconfigurationmanager.html
[this very helpful post]: https://superuser.com/questions/585473/debugging-osx-airport-wifi-connection/735572#735572
[workarounds]: https://github.com/KDE/krita/commit/19ba224692a52b1d5799fda308bed4b02ff38f7a
