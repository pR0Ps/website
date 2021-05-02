---
Title: Removing the Proxmox VE subscription notice
Date: 2021-04-28 10:03
Author: Carey Metcalfe
Tags:
  - proxmox
  - linux
  - shell script
---

[Proxmox VE][] is an open-source ([AGPL v3][]) virtualization platform for running containers and
VMs. It's comparable to a proprietary solution like [VMware ESXi][].

It can be downloaded and installed completely free of charge, lacking only access to support and
other things that more enterprise-focused users care about. For a homelab install, the free version
is perfect.

...except for one thing. Each time you log in, you have to click through this dialog:

!["You do not have a valid subscription for this server. Please visit www.proxmox.com to get a list of available options."]({static}/images/proxmox_subscription_notice.png)

The goal of this post is to walk through developing a solution to automatically remove that
notification in any installed version of Proxmox VE, as well as have that removal survive future
updates.

**To skip to the solution, click [here](#the-solution).**


# Developing a patch

Searching the internet reveals that a few other people ([1][], [2][], [3][]) have already attacked
this problem. All articles point to some code in
`/usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js` being responsible for the notification
so this is where we'll start.

Scanning though that file reveals a function called [`checked_command(orig_cmd)`][checked_command].
This function just executes `orig_cmd` after showing the subscription notification if it determines
that you don't have a valid subscription.

Based on this, the goal of this patch will be to make `checked_command` always execute `orig_cmd`
without bothering to check if there is a subscription at all. As a bonus, this will also speed up
the login process since it removes a blocking call to the server[^1].

Since we want this patch to work for as many versions as possible, it's a good idea to take a look
into how this function has changed over time. By looking at the [proxmox-widget-toolkit][] history,
we can see that `checked_command` was originally added in commit [`5f93e010`][5f93e010]. However, it
was actually moved from the [pve-manager][] project where it was written for the [initial
implementation of the subscription notice][]. By looking at the entire history of this function we can see that
while the function implementation has changed slightly over time, the name, arguments, and goal of
it has stayed exactly the same.

Given this, as long as we only use the function definition to do the patch, it should work for every
version of Proxmox VE to date (and hopefully into the future). Using `sed` to prepend `orig_cmd();
return;` to the function should work nicely:
```bash
sed --in-place 's/checked_command: function(orig_cmd) {$/& orig_cmd(); return;/' /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js
```

This results in the following change:
```diff
-checked_command: function(orig_cmd) {
+checked_command: function(orig_cmd) { orig_cmd(); return;
```

Notice that the `sed` script is looking for the function definition followed by a line ending (`$`).
Because the patch is added to the same line, if the command is run again it won't match and won't
make any changes, making it safe to blindly run multiple times. This becomes important for
automating it later.

Now that we know it works, we should harden it up against whitespace changes by replacing the spaces
in the regex with `\s*` (0 or more whitespace characters):
```bash
sed --in-place 's/checked_command:\s*function(orig_cmd)\s*{\s*$/& orig_cmd(); return;/' /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js
```

The only thing left to solve is which file `checked_command` is defined in. Since it used to be a
part of the `pve-manager` project, it's safe to say that it wasn't always stored in
`/usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js`. It could also move around in the
future.

To deal with this, we use `grep` to find the file that it's defined in, then run the previous
command over that file:
```bash
grep --files-with-matches --include '*.js' --recursive --null 'checked_command:\s*function(orig_cmd)' /usr/share/ \
  | xargs --null --no-run-if-empty sed --in-place 's/checked_command:\s*function(orig_cmd)\s*{\s*$/& orig_cmd(); return;/'
```

Simply run this command on your Proxmox VE server[^2], refresh the web UI, and the notice should be
gone!


# Automating it

At this point we have a working command that will remove the subscription notice from any version of
Proxmox VE to date. However, after updating the system, there's a chance that a newer version of the
file will have overwritten our patched version.

While we could just save the command in a script and manually run it after every update, that's
annoying and will definitely be forgotten. Instead, we want to automatically run the command every
time the web server starts. This will ensure that it will always be serving a patched version of the
file.

Proxmox VE uses [`systemd`][systemd] to manage the startup of its services. This means that once we
find the service that manages the web server, we should be able to make `systemd` launch a service
that applies our patch just before the web server.

The first step is to find the service that manages the web server. Since we know it's running on
port 8006, we can use `netstat` to enumerate all listening TCP ports and `grep` to filter it down to
just the port we're interested in:
```bash
$ netstat --listening --tcp --numeric-ports --program | grep 8006
tcp  0  0  0.0.0.0:8006  0.0.0.0:*  LISTEN  15771/pveproxy
```

Once we know the PID of the program, running `systemctl status <PID>` will show the status
(including the service name) of the service that's managing it[^3]. In this case it shows that the
service is `pveproxy.service`.

We can now define a service that runs our code, is wanted by `pveproxy.service`, and
must be run before it. Then, whenever `systemd` starts (or restarts) `pveproxy.service`, it will
make sure to also run our service that applies the patch.

# The solution
<a name="the-solution"></a>
Putting it all together:

1\. Create `/etc/systemd/system/no-subscription-notice.service`:
```ini
[Unit]
Description=Remove Proxmox VE subscription notice
Before=pveproxy.service

[Service]
Type=oneshot
ExecStart=/bin/sh -c "grep --files-with-matches --include '*.js' --recursive --null 'checked_command:\s*function(orig_cmd)' /usr/share/ | xargs --null --no-run-if-empty sed --in-place 's/checked_command:\s*function(orig_cmd)\s*{\s*$/& orig_cmd(); return;/'"

[Install]
WantedBy=pveproxy.service
```
2\. `systemctl enable --now no-subscription-notice.service`

And that's it! The subscription notice should now be gone for good. I'll update this post if it
breaks, but that hopefully won't be for a while.


  [^1]: Interestingly, the existing solutions I found all patch the code that checks the returned
        subscription status instead of just not asking about the status at all. Compared to the
        solution here, this is both more fragile, as well as slower.
  [^2]: Commands can be run from the web UI (Datacenter -> node -> Shell), via SSH, or just by
        using a keyboard and monitor hooked up to the server.
  [^3]: Another way to go from PID or command to service name is to use `ps` like so:
        `ps --format=unit= <PID>` or `ps --format=unit= -C <cmd>`. Note that this requires your
        version of `ps` to be compiled with `systemd` support (which it is in most `systemd`-based
        distros).


  [AGPL v3]: https://www.gnu.org/licenses/agpl-3.0.en.html
  [Proxmox VE]: https://www.proxmox.com/proxmox-ve
  [VMWare ESXi]: https://www.vmware.com/products/esxi-and-esx.html
  [proxmox-widget-toolkit]: https://git.proxmox.com/?p=proxmox-widget-toolkit.git
  [pve-manager]: https://git.proxmox.com/?p=pve-manager.git;
  [checked_command]: https://git.proxmox.com/?p=proxmox-widget-toolkit.git;a=blob;f=src/Utils.js;h=85387946165e592e89a65e6973dc7f1836edc984;hb=HEAD#l460
  [initial implementation of the subscription notice]: https://git.proxmox.com/?p=pve-manager.git;a=commitdiff;h=1556735e9c4dfdd13d1b0823942adf8feb003891
  [5f93e010]: https://git.proxmox.com/?p=proxmox-widget-toolkit.git;a=commitdiff;h=5f93e010854dadb38fa1e7d10c00f42df38cedd4
  [systemd]: https://systemd.io/
  [1]: https://johnscs.com/remove-proxmox51-subscription-notice/
  [2]: https://dannyda.com/2020/05/17/how-to-remove-you-do-not-have-a-valid-subscription-for-this-server-from-proxmox-virtual-environment-6-1-2-proxmox-ve-6-1-2-pve-6-1-2/
  [3]: https://www.jamescoyle.net/how-to/614-remove-the-proxmox-no-subscription-message

