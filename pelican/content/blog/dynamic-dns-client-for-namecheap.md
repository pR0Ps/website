---
Title: Dynamic DNS client for Namecheap using bash & cron
Date: 2015-02-26 23:21
Modified: 2015-10-06 22:05
Author: Carey Metcalfe
Tags:
 - shell script
 - code
 - linux
 - website
---

In addition to running this website, I also run a home server. For convenience,
I point a subdomain of `cmetcalfe.ca` at it so even though it's connected using
a dynamic IP (and actually seems to change fairly frequently), I can get access
to it from anywhere.

As a bit of background, the domain for this website is registered and managed
through [Namecheap][]. While they do provide a [recommended DDNS client][] for
keeping a domain's DNS updated, it only runs on Windows.

Instead, after [enabling DDNS for the domain] and reading [Namecheap's article
on using the browser to update DDNS] I came up with the following `dns-update`
script.

```bash
#!/bin/sh

# Abort if anything goes wrong (negates the need for error-checking)
set -e

# Uses drill instead of dig
resolve() {
    #dig "$1" @resolver1.opendns.com +short 2> /dev/null
    line=$(drill "$1" @resolver1.opendns.com 2> /dev/null | sed '/;;.*$/d;/^\s*$/d' | grep "$1")
    echo "$line" | head -1 | cut -f5
}

dns=$(resolve <subdomain>.cmetcalfe.ca)
curr=$(resolve myip.opendns.com)
if [ "$dns" != "$curr" ]; then
    if curl -s "https://dynamicdns.park-your-domain.com/update?host=<subdomain>&domain=cmetcalfe.ca&password=<my passkey>" | grep -q "<ErrCount>0</ErrCount>"; then
        echo "Server DNS record updated ($dns -> $curr)"
    else
        echo "Server DNS record update FAILED (tried $dns -> $curr)"
    fi
fi
```

It basically checks if the IP returned by a DNS query for the subdomain matches
the current IP of the server (as reported by an [OpenDNS][] resolver) and if it
doesn't, sends a request to update the DNS. The `echo` commands are there just
to output some record of the IP changing. Maybe I'll do some analysis of it at
some point.

To run the script every 30 minutes and redirect any output from it to the
syslog, the following [crontab][] entry can be used:
```bash
*/30 * * * * /path/to/dns-update | /usr/bin/logger -t dns-update
```

With the script automatically running every 30 minutes I can now be confident
that my subdomain will always be pointing at my home server whenever I need
access to it.


!!! note
    A previous version of this article used `curl -sf http://curlmyip.com` to
    find the server's current IP address. However, after curlmyip went down for
    a few days, I decided to take the advice in [this StackExchange answer][]
    and use [OpenDNS][] instead.

  [Namecheap]: http://namecheap.com
  [recommended DDNS client]: https://www.namecheap.com/support/knowledgebase/article.aspx/28
  [enabling DDNS for the domain]: https://www.namecheap.com/support/knowledgebase/article.aspx/595
  [Namecheap's article on using the browser to update DDNS]: https://www.namecheap.com/support/knowledgebase/article.aspx/29
  [OpenDNS]: https://en.wikipedia.org/wiki/OpenDNS
  [crontab]: http://en.wikipedia.org/wiki/Cron
  [this StackExchange answer]: http://unix.stackexchange.com/a/81699
