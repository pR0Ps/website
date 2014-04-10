Title: Limit download speed by IP or MAC address
Date: 2014-03-4 20:02
Author: Carey Metcalfe
Tags: router, shell script

Preamble
--------
This article will focus on setting strict speed limits on misbehaving devices on your network. This can be a housemate incessantly torrenting, your kid downloading movies on iTunes, or anyone else clogging up your network with their overzealous bandwidth gobbling.

If you're looking for help with the QOS (quality of service) settings that come baked into most router firmwares, this article is not for you.

This article assumes you have a router running OpenWRT, DD-WRT, Tomato, or any other firmware that uses [`tc`](http://linux.die.net/man/8/tc) to manipulate traffic control settings.

Procedure
---------
First, you'll need to get shell access to the router. With most custom router firmwares, this is as easy as selecting a radio button. Other firmwares might give you the ability to enter commands via a web interface. Whatever works.

Once you have shell access, follow the steps below. Note that bits of the commands you might want to change are included in brackets.

1.  Using `ifconfig`, find the interface to apply the limits to. You'll want to use either the internal or external default gateway (the interfaces all the packets go though). Keep in mind which interface you use as the filtering rules will be reversed. 
    - Internal gateway: to src = uploading, to dst = downloading
    - External gateway: to src = downloading, to dst = uploading

2.  Remove all existing rules on the interface (interface = `br0`)

        tc qdisc del dev br0 root

3.  Set up the connection (Ex: connection speed = 20mbit)

        tc qdisc add dev br0 root handle 1: cbq avpkt 1000 bandwidth 20mbit

4.  Add the limiting rule (Ex: speed limit = 10mbit)

        tc class add dev br0 parent 1: classid 1:1 cbq rate 10mbit allot 1500 prio 5 bounded isolated

5.  Filtering - Add the users to apply to rule to
    - By src IP (Ex: IP = `192.168.1.100`)
    
            tc filter add dev br0 parent 1: protocol ip prio 16 u32 match ip src 192.168.1.100 flowid 1:1

    - By dst IP (Ex: IP = `192.168.1.100`)
        
            tc filter add dev br0 parent 1: protocol ip prio 16 u32 match ip dst 192.168.1.100 flowid 1:1

    - By src MAC (Ex: MAC = `M0-M1-M2-M3-M4-M5`)
        
            tc filter add dev br0 parent 1: protocol ip prio 5 u32 match u16 0x0800 0xFFFF at -2 match u16 0xM4M5 0xFFFF at -4 match u32 0xM0M1M2M3 0xFFFFFFFF at -8 flowid 1:1
    
    - By dst MAC (Ex: MAC = `M0-M1-M2-M3-M4-M5`)
        
            tc filter add dev br0 parent 1: protocol ip prio 5 u32 match u16 0x0800 0xFFFF at -2 match u32 0xM2M3M4M5 0xFFFFFFFF at -12 match u16 0xM0M1 0xFFFF at -14 flowid 1:1

Disclaimer
----------
These settings worked for me, if there's a better way of doing this, let me know!
