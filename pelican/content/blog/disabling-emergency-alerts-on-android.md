---
Title: Disabling emergency alerts on Android
Date: 2020-08-15
Modified: 2023-06-18
Author: Carey Metcalfe
Tags:
  - android
  - canada
---

!!! WARNING
    You probably shouldn't do this. If you already know this and don't care, read on.

## Background
In Canada, the [CRTC][] mandates that telecommunications companies and other organizations broadcast
warning messages over various mediums, one of which is via cell phones.

Overall, this is a good idea that saves lives. However, the implementation is incredibly bad. All
alerts, no matter the severity, are broadcast at the very highest level (called "Presidential" by
Android phones), meaning that they can't be silenced or disabled by the user. In fact, the CRTC
actually [tested this][Testing the Response of Mobile Telephones to Wireless Public Alerts] and
found that the only reliable way to silence the alerts was to put the phone on airplane mode.

After I received three alerts all about an hour apart starting at 2am telling me about a missing
child over 1,300km away, I'd had enough.

This is a "boy who cried wolf" situation here. If these alerts ever:

1. Implement a basic distance filter so I'm not woken up by things happening nowhere near me
2. Start using an appropriate alert level instead of using the highest level for everything

I'll re-enable them. For now though, I don't want to be repeatedly woken up in the middle of the
night because someone a full day's drive from me went missing. Maybe that's cold-hearted, but
realistically what was I even going to do about it?

On Android at least, the lower-level emergency alerts can be configured to not make noise when the
device is silenced, but not disabled entirely. This seems a lot better as it won't wake people up,
but will show them the information the next time they look at the phone. Let's do that instead.

For now though, I'm turning everything off. Hopefully I don't get killed by a tornado or something.

## How to disable ALL alerts
This is surprisingly simple - the application responsible for handling the broadcasts can be
uninstalled.

!!! WARNING
    This will disable ALL emergency broadcasts. If you live in an area that regularly has severe
    weather or don't have a backup method for receiving these alerts, this is definitely not a good
    idea. It also probably violates some sort of policy or something (not a lawyer). You are
    responsible for your own decisions.

To uninstall it, enable developer options and debugging on the phone, connect it to a computer with
[ADB][] installed and run:
```bash
adb -d shell "pm uninstall -k com.android.cellbroadcastreceiver"
```

Thanks to [this reddit post][/r/ontario: How To Disable AMBER Alerts] for the method of disabling
the alerts.

## Why is it like this?
Which organization is responsible? Can this be changed?

Below is a rough dump of some details I found while trying to dig up which organization is
responsible for this with the hopes of actually affecting some change.

On 2017-04-06 the [CRTC][] issued [Telecom Regulatory Policy CRTC 2017-91][] which "directs wireless
service providers to implement wireless public alerting capability on their long-term evolution
networks by 6 April 2018". Relevant information pulled from that page:
>34\. SOREM has established a definitive list of emergency alert message types for immediate
>     broadcast by alert distributors. These messages are defined as “Broadcast Immediately” (BI).

In a footnote on the page it defines SOREM as:
> SOREM is a federal/provincial/territorial body that works to harmonize and improve emergency
> practices across the country. It includes representatives from provincial and territorial
> emergency management organizations as well as Public Safety Canada.

There was some disagreement on making the alerts mandatory:
>35\. Individual interveners’ views were divided among mandatory receipt, an opt-in mechanism, and
>     the choice to opt out. Technology solutions providers indicated mixed support between
>     mandatory reception and the choice to opt out. EMOs strongly supported mandatory receipt.

>36\. The OPC submitted that many people consider their mobile devices to be private and personal,
>     and that some individuals could consider emergency alerts to be intrusive. It recommended
>     that the Commission review how opt-out mechanisms have been implemented in the United States
>     and other jurisdictions, and whether the ability to opt out has had a significant negative
>     effect on alerting individuals in an emergency situation. It submitted that individuals should
>     be allowed to opt out if the effect is found to be minimal.

>39\. Some WSPs provided insight on past experiences regarding the distribution of AMBER Alerts over
>     their parent BDUs. For example, in March 2016, the Ontario Provincial Police issued an AMBER
>     Alert, which was distributed by BDUs. Many television viewers were upset by the interruption
>     of their television viewing and contacted their BDU customer service centres and, in some
>     cases, 9-1-1 to complain.

And finally, in a section titled "Commission’s analysis and determinations", a decision was made:
>41\. Although some interveners suggested modifying the BI list, there was no consensus on which
>     specific categories should be added or removed.

>42\. However, the question in this proceeding is not whether the BI list used in the broadcasting
>     context should be changed, but whether the same or a different approach should be taken with
>     respect to emergency alert messages sent to mobile devices compared to those sent via
>     broadcasting emergency alerting. The current BI list is designed to protect against threats to
>     life and property. It is therefore important to promote consistency between broadcasting and
>     wireless emergency alerts so that Canadians can receive the same alerts regardless of
>     transmission medium.

>43\. In light of the above, the Commission mandates the reception of emergency alert messages on
>     mobile devices, based on the BI list developed by SOREM, as amended from time to time.

This seems to say that the list of what alerts exist and their priority is managed by SOREM.

To back this up, the CRTC's [Emergency Alerts and the National Public Alerting System][Emergency
Alerts and the NPAS] page has a section titled "Consistent appearance and sound of alerts" with the
quote:
> The visual appearance, sound, content, and other aspects of emergency alerts are guided by the
> Senior Officials Responsible for Emergency Management. This federal, provincial and territorial
> body works to harmonize and improve emergency practices across the country.

That section also includes a link to the [National Public Alerting System's Common Look and Feel
Guidance][NPAS: CLF] which has some more information in it:

From the [7.3 SOREM Public Alerting Layer][NPAS: CLF - 7.3] section:
> The SOREM Public Alerting Layer establishes parameters that are referred to by the CLF. The
> current version of the specification can be found in Appendix B.

From the [APPENDIX B – SOREM Public Alerting Layer][NPAS: CLF - APPENDIX B] section:
> The SOREM Public Alerting Layer establishes a number of CAP <parameter>s which are used to support
> the public alerting community in Canada. In a separate document, SOREM maintains the “Broadcast
> Immediate Events List”, which works in conjunction with this layer. The current version of this
> list is available at <https://alerts.pelmorex.com/highpriorityalerts/>

That link goes to a page that doesn't exist, but by visiting <https://alerts.pelmorex.com> directly
and looking around, it looks like it should point to: [List of Event Codes for Broadcast
Immediate Alerts (version 2.1)][] (last updated 2022-05-25).

This document contains a table titled "EVENT CODE DESCRIPTIONS FOR EMERGENCY PUBLIC ALERT BROADCAST
IMMEDIATE EVENTS" that defines what codes map to what alert severity. For example, the reason why an
AMBER alert is sent at the highest level is because of this entry:

> **Event Code**: amber <br>
> **CAP Code for Urgency**: Immediate <br>
> **CAP Code for Severity**: Severe or Extreme <br>
> **CAP Code for Certainty**: Observed <br>
> **Description**: Amber Alert:
>     Issued by police services when a child has been abducted and it is believed that his/her life
>     is in grave danger. An Amber Alert provides the public with immediate and up-to-date
>     information about a child abduction and solicits the public's help in the safe and swift
>     return of the child.

Where the following definitions for the CAP codes are used:

 - "Immediate" - Responsive action SHOULD be taken immediately
 - "Extreme" - Extraordinary threat to life
 - "Severe" - Significant threat to life
 - "Observed" - Determined to have occurred or to be ongoing

This is where the "everything at the highest alert level" issue comes from. Aside from
`testMessage`, literally every other event code on this list has the same Immediate + Severe/Extreme
classification. This includes everything from `silver` (*"a missing, wandering older adult who may
be suffering from a documented cognitive disability or degenerative memory disorder"*) to `meteor`
(*"A natural object of extraterrestrial origin [...] hits the ground with the potential for
catastrophic damage."*) 

### Summary

The CRTC requires that Wireless Service Providers (WSPs) implement the alerts as defined by SOREM.
SOREM's list of alerts defines an AMBER alert as requiring the same amount of urgency and disruption
as a planet-killing meteor dropping from the sky.

This seems to be by design, but if not, SOREM is the organization that would need to fix it. As an
aside, it seems like the CRTC wouldn't even have to get involved as the policy just defers to the
*"BI list developed by SOREM, as amended from time to time"* which seems pretty loose. Maybe I'm
missing something though.

I didn't find anything that specified any details about how wide the affected range for these alerts
should or should not be. It seems like that's left up to the organization issuing the alert.


  [CRTC]: https://crtc.gc.ca/
  [Testing the Response of Mobile Telephones to Wireless Public Alerts]: https://crtc.gc.ca/eng/publications/reports/alertmobil/alertmobil.htm#a13
  [ADB]: http://developer.android.com/tools/help/adb.html
  [Telecom Regulatory Policy CRTC 2017-91]: https://crtc.gc.ca/eng/archive/2017/2017-91.htm
  [Emergency Alerts and the NPAS]: https://crtc.gc.ca/eng/television/services/alert.htm
  [NPAS: CLF]: https://www.publicsafety.gc.ca/cnt/mrgnc-mngmnt/mrgnc-prprdnss/npas/clf-lng-20-en.aspx
  [NPAS: CLF - 7.3]: https://www.publicsafety.gc.ca/cnt/mrgnc-mngmnt/mrgnc-prprdnss/npas/clf-lng-20-en.aspx#s73
  [NPAS: CLF - APPENDIX B]: https://www.publicsafety.gc.ca/cnt/mrgnc-mngmnt/mrgnc-prprdnss/npas/clf-lng-20-en.aspx#sb
  [List of Event Codes for Broadcast Immediate Alerts (version 2.1)]: https://alerts.pelmorex.com/wp-content/uploads/2022/07/List-of-Event-Codes-for-Broadcast-Immediate-Alerts_version-2.1.pdf
  [/r/ontario: How To Disable AMBER Alerts]: https://web.archive.org/web/20230420065952/https://www.reddit.com/r/ontario/comments/boxx11/how_to_disable_amber_alerts/
