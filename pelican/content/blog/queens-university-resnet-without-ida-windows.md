---
Title: Queen's University Resnet without IDA (Windows)
Date: 2013-05-07 13:21
Author: Carey Metcalfe
Tags:
  - queen's university
  - windows
---

Storytime
---------

So you're in your first year at Queen's University residence and you
want to access the internet. Sounds reasonable. You plug in your Windows
laptop, open your browser, and...nothing. Well, mostly nothing. A page
that tells you that you've been quarantined and to please click here,
download IDA, install it, and let it work it's magic.

Sounds easy right? What they don't tell you is that IDA holds ResNet
access hostage until you've installed some garbage antivirus, downloaded
all the new windows updates (IDA actually does this itself, it doesn't
step back and let Windows Update do it's job), and a few other things.
After all that, you enter your NetID and password, and it registers you.
In theory.

What I ran into every single time I ran it with my laptop (running Windows
XP at the time) was it failing to download something, throwing an error
message and refusing to register me. I gave up after a few times and
plugged in my other computer (Running the relatively obscure Windows XP
x64). What I noticed is that I didn't get the typical quarantine page, I
got a simple page that asked for a NetID and password. I entered my
information and got a message stating I was good to go. I checked a few
pages and they all seemed to work.

I plugged my laptop back in and tried to load a page. The same
quarantine screen. Since the main way a webpage tells the difference
between two operating systems is the user agent, I fired up [Tamper
Data][] and submitted a request with a blank one. I got the same page
that asked for my NetID and password.

I assume this works because if the registration server decides (based on
your user agent) that IDA won't run on your computer, instead of leaving
you screwed, it'll give you an alternate way out. Since when you take
away the user agent the server can't tell what kind of operating system
you're running, they assume that IDA won't work on it and give you the
simple "Enter your account details" prompt.  

Register a computer without IDA
-------------------------------

1.  Acquire unblocked internet (the queensu wireless is a good bet).
2.  Download and install [Firefox][] and the [Tamper Data][] addon.
4.  Disconnect from the internet and plug in to ResNet.
5.  In Firefox, click Tools,  Tamper Data.
6.  In the window that pops up, click "Start Tamper".
7.  Try to load a website.
8.  A window will pop up asking you if you want to tamper with the
    request. Click the "Tamper" option.
9.  In the windows that pops up, delete everything in the "User-Agent"
    field and hit OK.
10. Repeat steps 8 and 9 until the popups stop and the page loads.
11. Click "Stop Tamper" and close the Tamper Data window.
12. You should be on a page that tells you to enter your NetID and
    password, do so and hit OK.

Your computer should now be able to use ResNet normally.

Registering other devices
-------------------------

Your computer is registered via it's MAC address. This means that if you
want to use ResNet with a device that can't run IDA, doesn't have a web
browser, and is against IT policy \*cough\* wireless router \*cough\*,
you can't. In theory.

The easy way of course, it to call up ITS and tell them your Xbox can't
connect. They'll ask you for your Xbox's MAC address, you'll give them
the router's MAC address, and they'll register it. Aside from lying to
ITS being morally wrong, this works. However, I've heard complaints that
devices registered via calling ITS have had their speed throttled.
Throttling non-school-related devices on a school network makes sense,
but I haven't seen any actual proof of this.

The better way of registering your other devices though, is to trick the
registration server into thinking that your device is just a normal
computer. Since computers are registered by their MAC addresses, you
just need to register the MAC address of your device with the system.

The following steps will show you how to spoof your device's MAC address
and register it from your computer.

1.  Find the MAC address of your device. It will probably be somewhere
    in the Advanced Options.
2.  Unplug your device from ResNet and plug in your computer.
3.  Open Control Panel, Network and Internet, Network Connections
    and note the name of your connection. Usually it's "Local Area
    Connection"
4.  Download and extract [Macshift][] into a folder somewhere.
5.  Open a command prompt window in the Macshift folder.
6.  In the command prompt window type

        macshift.exe -i "[connection name]" [device MAC address, no dashes]

    For example, if my device's MAC address was "00-11-22-33-44-55" and my
    connection name was "Local Area Connection", I would run

        macshift.exe -i "Local Area Connection" 001122334455

7.  Wait until you have network access again and try to load a page. If
    everything went as planned, you should be seeing the ResNet
    quarantine page.
8.  Use the steps in the section above to register your computer again.
9.  Once you have ResNet access, go back to the command prompt and run

        macshift.exe -i "[connection name]" -d

    This restores your MAC address back to it's original value.

Your device should now be able to use ResNet normally.

Disclaimer
----------

All information above is provided for informational purposes only. I
take no responsibility for the outcome of your actions. Furthermore, all
information on IDA is based on experiences in 2009, It may have
improved over time (ha).

  [Tamper Data]: https://addons.mozilla.org/en-us/firefox/addon/tamper-data/
  [Firefox]: http://www.mozilla.org/firefox/
  [Macshift]: http://devices.natetrue.com/macshift/
