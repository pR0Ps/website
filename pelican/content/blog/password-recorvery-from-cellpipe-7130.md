---
Title: Password recovery from an Alcatel-Lucent Cellpipe 7130
Date: 2018-09-11 22:30
Author: Carey Metcalfe
Tags: security
---

Background
----------
In my current rental situation, the landlord provides internet included with the rental. Since it's
fast enough and has enough bandwidth this isn't an issue at all. The only problem is that the modem
provided by the telco is an ancient `Alcatel-Lucent Cellpipe 7130 5VzA2001` modem/router combo. It's
running firmware version `1.0.4.4R8-wh`, released on 2012-05-08 16:30 (there are no updates, I
checked).

Since the Cellpipe only has 4 x 10/100 LAN ports and terrible WiFi performance, I would much prefer
to use my own equipment to perform the routing and just use the Cellpipe 7130 as a WAN gateway.
Unfortunately, for some reason, there is no way to turn off the routing aspect of the Cellpipe and
just use it as a modem (aka bridge mode). There is also no way to turn off [DHCP][] functionality on
it.

My current hacky solution to these problems is to let my router get an IP from the modem/router via
DHCP, then set that IP as the DMZ host on the Cellpipe. This effectively forwards all TCP and UDP
ports to the router, making it seem like it's the boundary device for the network. Luckily, my
router always seems to request the same IP no matter what so this continues to work even if both
devices are power cycled.

Since this is not an ideal situation, I'd like to replace the Cellpipe with a more performant modem
without any of the routing overhead. To do this, I just need to port the configuration details from
the Cellpipe (like the username and password for the upstream [PPPoE][] connection) over to a new
modem. Unfortunately, there's nothing in the web interface that will allow me to see the password
and there's no option to do a configuration backup. I also can't just call up the telco since it's
the landlord's account.

This means we're stuck, right?

Digging into the Cellpipe
-------------------------
Doing a quick [CVE][] search for the Cellpipe only turns up [CVE-2015-4586][] (a [CSRF][]
vulnerability) and [CVE-2015-4587][] (an [XSS][] vulnerability), both of which aren't useful in this
case. Oh well.

Seeing as the [Cellpipe 7130 manual][](PDF) mentions various functionality that my device
doesn't seem have, my hypothesis is that there might be a configuration backup/restore function
somewhere, just not exposed in the UI. With that in mind, I went trawling through the HTML and
JavaScript files the web UI served up. I found:

The color 'red' is commented out and redefined as white. This suggests that they could be hiding
error messages by just making them the same color as the background:
```javascript
//var red    ='#FF0000';
var red    ='#FFFFFF';
```

Debugging in production builds with commented out `alert` statements:
```javascript
//alert(isRouter);
//alert(isAPmode);
```

Various comments indicating lack of source control:
```javascript
//Jamie hide 20111109
/*if(menuItem=='HPNA')
{
    printMenuItem('hpna.html', 'HPNA', white, darkBlue);
}else{
    printMenuItem('hpna.html', 'HPNA', black, blue);
}
*/
```
```javascript
//fanny add 2011/02/22
printMenuItem('wifi_statistics.html', 'WLAN Statistics ', black, white);
```
```html
<!-- jonathan 2004.04.07    Begin  -->
<form name="logoutForm" method="post">
    <input type="hidden" name="logoutMsg">
</form>
<!-- jonathan 2004.04.07    End  -->
```

These all seem to allude to shoddy release processes, meaning that it's highly likely that
per-model customizations were rushed UI-level hack jobs on top of the current release and not
maintained branches where actual functionality was changed.

Since a configuration backup will include the PPPoE username and password, let's do a search for
"config". Sure enough:
```javascript hl_lines="6 7"
printMenuSection('util_main.html', 'Utilities', white);
printMenuItem('lang_set.html', 'Language Setting', black,white);
printMenuItem('util_reboot.html', 'Reboot Gateway', black,white);
//printMenuItem('util_reservice.html', 'Restart Service', black,white);
printMenuItem('util_factory.html', 'Restore Factory Defaults',black, white);
//printMenuItem('util_cfgstore.html', 'Configuration Store', black,white);
//printMenuItem('util_cfgrestore.html', 'Configuration Restore', black,white);
printMenuItem('util_webfirmware.html', 'Web Firmware Upload', black,white);//Jamie add back 20111109
```

Visiting `http://<router_ip>/util_cfgstore.html` shows a nice "Store" button that downloads a text
file containing 771(!) key/value pairs, including the username and password for the router. Success!

Future plans
------------
There are a ton of other options in the downloaded config file, some of which look like they enable
bridge mode. However, flipping those settings on and applying the new config using
`http://<router_ip>/util_cfgrestore.html` didn't seem to change anything. I'm going to keep messing
with it while I look into sourcing a better modem to use my newfound credentials with.

Longer-term, the plan is to transition to a dedicated modem that provides WAN access to a low-power
computer running [pfSense][] for firewall and routing duties. From there, an unmanaged switch
(possibly injecting [PoE][]) can provide access for enough dumb wireless APs to bathe the house in WiFi,
as well as wired hookups for the devices that don't move around too much or need the throughput. For
now though, I'll settle for replacing the modem.

[DHCP]: https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol
[PPPoE]: https://en.wikipedia.org/wiki/Point-to-Point_Protocol_over_Ethernet
[CVE]: https://en.wikipedia.org/wiki/Common_Vulnerabilities_and_Exposures
[CSRF]: https://en.wikipedia.org/wiki/Cross-site_request_forgery
[XSS]: https://en.wikipedia.org/wiki/Cross-site_scripting
[CVE-2015-4586]: https://www.cvedetails.com/cve/CVE-2015-4586
[CVE-2015-4587]: https://www.cvedetails.com/cve/CVE-2015-4587
[Cellpipe 7130 manual]: https://infoproducts.alcatel-lucent.com/cgi-bin/dbaccessfilename.cgi/401389004_V1_CellPipe
[pfSense]: https://www.pfsense.org/
[PoE]: https://en.wikipedia.org/wiki/Power_over_Ethernet
