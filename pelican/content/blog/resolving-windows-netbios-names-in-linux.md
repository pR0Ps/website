---
Title: Resolving Windows NetBIOS names in Linux
Date: 2013-03-17 01:49
Author: Carey Metcalfe
Tags:
 - linux
 - windows
---

When accessing computers on a LAN, it's often useful to access them by
name instead of IP. This is especially true when dealing with dynamic IP
addresses.

In Windows, other Windows computer names are automatically resolved to
an IP address. In most Linux distros however, this is not the case (by default).

To resolve Windows NetBIOS names in Linux, you'll need the [winbind][]
component of the [Samba suite][]. Winbind allows a UNIX box to become a
full member of an NT domain, giving the ability to resolve names from
it.

Install winbind via your preferred package manager. For Debian and
derivatives, the following should work.   

    apt-get install winbind

Now that winbind is installed, the OS must be configured to use it when
looking up hostnames. Open the file `/etc/nsswitch.conf` and add "wins"
to the end of the line starting with "hosts:".

For example, the line in my file now looks like

    hosts: files dns wins

Save the file and reboot to start the winbindd deamon.

To test if if worked, try pinging a computer on your LAN by name. For
example:

```bash
$ ping windows-server
PING windows-server (192.168.0.107) 56(84) bytes of data.
64 bytes from 192.168.0.107: icmp_req=1 ttl=128 time=0.268 ms
64 bytes from 192.168.0.107: icmp_req=2 ttl=128 time=0.604 ms
64 bytes from 192.168.0.107: icmp_req=3 ttl=128 time=0.607 ms
```

  [winbind]: http://www.samba.org/samba/docs/man/manpages-3/winbindd.8.html
  [Samba suite]: http://www.samba.org/
