---
Title: Proxied access to the Namecheap DNS API
Date: 2019-01-20 06:15
Author: Carey Metcalfe
Tags:
  - code
  - shell script
  - website
  - automation
  - let's encrypt
---

## Background

Both this site and my home server use HTTPS certificates provided by [Let's Encrypt][].
[Previously][adding https support] I was using the `http-01` challenge method, but once [wildcard
certificates became available][], I decided to switch to the `dns-01` method for simplicity.

My domains are currently registered through [Namecheap][] which provides an API for modifying DNS
records. The only catch is that it can only be accessed via manually-whitelisted IP addresses.
Because the server I'm trying to access the API from is assigned a dynamic IP, this restriction was
a bit of an issue.

Back in November when I initially made the switch to the DNS-based challenge, I set it up the easy
way: I manually added my current IP to the whitelist, added a TODO entry to fix it somehow, and set
a reminder scheduled for the week before the cert would expire telling me to update the IP
whitelist. Fast-forward to today when I was reminded to update my IP whitelist. Instead of
continuing to kick the can down the road, I decided to actually fix the issue.

## Setting up a temporary proxy

My home server is connected to the internet though a normal residential connection which is assigned
a dynamic IP address. However, the server that I run this website on is configured with a static IP
since it's a hosted [VPS][]. By proxying all traffic to the Namecheap API through my VPS, I could
add my VPS's static IP to the whitelist and not have to worry about my home IP changing all the
time.

SSH is perfect tool for this. The [OpenSSH client][] supports port forwarding using the `-D` flag.
By then setting the `HTTP[S]_PROXY` environment variables to point to the forwarded port, programs
that support those environment variables will transparently forward all their requests through the
proxy.

After a bunch of research and testing, I came up with the following script to easily set up the
temporary proxy:
```bash
#!/bin/sh
# Source this file to automatically setup and teardown an HTTP* proxy through cmetcalfe.ca
# Use the PROXY_PORT and PROXY_DEST environment variables to customize the proxy

PROXY_PORT="${PROXY_PORT:-11111}"
PROXY_DEST="${PROXY_DEST:-<username>@cmetcalfe.ca}"
PID="$$"

# Teardown the SSH connection when the script exits
trap 'ssh -q -S ".ctrl-socket-$PID" -O exit "$PROXY_DEST"' EXIT

# Set up an SSH tunnel and wait for the port to be forwarded before continuing
if ! ssh -o ExitOnForwardFailure=yes -M -S ".ctrl-socket-$PID" -f -N -D "$PROXY_PORT" "$PROXY_DEST"; then
    echo "Failed to open SSH tunnel, exiting"
    exit 1
fi

# Set environment variables to redirect HTTP* traffic through the proxy
export HTTP_PROXY="socks5://127.0.0.1:$PROXY_PORT"
export HTTPS_PROXY="$HTTP_PROXY"
```

This script is saved as `~/.config/tempproxy.rc` and can be sourced to automatically set up a proxy
session and have it be torn down when the script exits.

You'll want to use key-based authentication with an unencrypted private key so that you don't need
to type anything to initiate the SSH session. For this reason you'll probably want to create a
limited user on the target system that can only really do port forwarding. There's a good post on
this [here][ssh-limited-port-forward].

## Talking to the API through the proxy

To allow programs that use the `tempproxy.rc` script to talk to the Namecheap API, the IP address of
the VPS was added to the whitelist. Now that the proxying issue was taken care of, I just needed
to wire up the actual certificate renewal process to use it.

The tool I'm using to talk to the Namecheap DNS API is [lexicon][]. It can handle manipulating the
DNS records of a ton of providers and integrates really nicely with my [ACME][] client of choice,
[dehydrated][]. Also, because it's using the [PyNamecheap][] Python library, which in turn uses
[requests][] under the hood, it will [automatically use the `HTTP*_PROXY` environment
variables][requests proxy support] when making requests.

The only tricky bit is that the base install of `lexicon` won't automatically pull in the packages
required for accessing the Namecheap API. Likewise, `requests` won't install packages to support
SOCKS proxies. To install all the required packages you'll need to run a command like:
```bash
pip install 'requests[socks]' 'dns-lexicon[namecheap]'
```

Since lexicon can use environment variables as configuration, I created another small source-able
file at `~/.config/lexicon.rc`:
```bash
#!/bin/sh
# Sets environment variables for accessing the Namecheap API

# Turn on API access and get an API token here:
# https://ap.www.namecheap.com/settings/tools/apiaccess/
export PROVIDER=namecheap
export LEXICON_NAMECHEAP_USERNAME=<username>
export LEXICON_NAMECHEAP_TOKEN=<api token>
```

With that in place, the existing automation script that I had previously set up when I switched to
using the `dns-01` challenge just needed some minor tweaks to source the two new files. I've
provided the script below, along with some other useful ones that use the DNS API.

## Scripts

### `do-letsencrypt.sh`
This is the main script that handles all the domain renewals. It's called via `cron` on the first
of every month.

Fun fact: The previous `http-01` version of this script was a mess - it involved juggling `nginx`
configurations with symlinks, manually opening up the `.well-known/acme-challenge` endpoint, and
some other terrible hacks. This version is *much* nicer.

```
#!/bin/sh
# Generate/renew Let's Encrypt certificates using dehydrated and lexicon

set -e

# Set configuration variables and setup the proxy
source ~/.config/lexicon.rc
source ~/.config/tempproxy.rc

cd /etc/nginx/ssl

# Update the certs.
# Hook script copied verbatim from
# https://github.com/AnalogJ/lexicon/blob/master/examples/dehydrated.default.sh
if ! dehydrated --accept-terms --cron --challenge dns-01 --hook dehydrated.default.sh; then
    echo "Failed to renew certificates"
    exit 1
fi

# Restart nginx if it's currently running
if systemctl is-active nginx.service >/dev/null && ! systemctl restart nginx.service; then
    systemctl status nginx.service
    echo "Failed to restart nginx, check the error log"
    exit 1
fi
```

### `dns.sh`
This one is really simple - it just augments the normal lexicon CLI interface with the proxy and
configuration variables.

```bash
#!/bin/sh
# A simple wrapper around lexicon.
# Sets up the proxy and configuration, then passes all the arguments to the configured provider

source ~/.config/lexicon.rc
source ~/.config/tempproxy.rc
lexicon "$PROVIDER" "$@"
```
```bash
$ ./dns.sh list cmetcalfe.ca A
ID       TYPE NAME             CONTENT         TTL
-------- ---- ---------------- --------------- ----
xxxxxxxx A    @.cmetcalfe.ca   xxx.xxx.xxx.xxx 1800
xxxxxxxx A    www.cmetcalfe.ca xxx.xxx.xxx.xxx 1800
```

### `dns-update.sh`
An updated version of my [previous script][old dns-update] that uses the API instead of the
[DynamicDNS service Namecheap provides][Namecheap dyndns]. Called via `cron` every 30 minutes.

```
#!/bin/sh
# Check the server's current IP against the IP listed in its DNS entry.
# Set the current IP if they differ.

set -e

resolve() {
    line=$(drill "$1" @resolver1.opendns.com 2> /dev/null | sed '/;;.*$/d;/^\s*$/d' | grep "$1")
    echo "$line" | head -1 | cut -f5
}

dns=$(resolve <subdomain>.cmetcalfe.ca)
curr=$(resolve myip.opendns.com)
if [ "$dns" != "$curr" ]; then
    source ~/.config/lexicon.rc
    source ~/.config/tempproxy.rc
    if lexicon "$PROVIDER" update cmetcalfe.ca A --name "<subdomain>.cmetcalfe.ca" --content "$curr" --ttl=900; then
        echo "Server DNS record updated ($dns -> $curr)"
    else
        echo "Server DNS record update FAILED (tried $dns -> $curr)"
    fi
fi
```

[ACME]: https://en.wikipedia.org/wiki/Automated_Certificate_Management_Environment
[Let's Encrypt]: https://letsencrypt.org
[Namecheap dyndns]: https://www.namecheap.com/support/knowledgebase/article.aspx/29/11/how-do-i-use-a-browser-to-dynamically-update-the-hosts-ip
[Namecheap]: https://www.namecheap.com/
[OpenSSH client]: https://www.openssh.com/
[PyNamecheap]: https://github.com/Bemmu/PyNamecheap
[VPS]: https://en.wikipedia.org/wiki/Virtual_private_server
[adding https support]: {filename}/blog/adding-https-support.md
[dehydrated]: https://github.com/lukas2511/dehydrated
[lexicon]: https://github.com/AnalogJ/lexicon
[old dns-update]: {filename}/blog/dynamic-dns-client-for-namecheap.md
[requests proxy support]: http://docs.python-requests.org/en/master/user/advanced/#proxies
[requests]: http://python-requests.org
[ssh-limited-port-forward]: https://askubuntu.com/questions/48129/how-to-create-a-restricted-ssh-user-for-port-forwarding/50000#50000
[wildcard certificates became available]: https://community.letsencrypt.org/t/acme-v2-and-wildcard-certificate-support-is-live/55579
