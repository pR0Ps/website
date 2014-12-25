---
Title: Backing up data to an external server via SSH
Date: 2012-08-16 12:12
Author: Carey Metcalfe
Tags:
  - linux
  - shell script
  - backup
---

I recently needed to back up the contents of a website, but found that a
disk quota was preventing me from doing so. What I really needed to do
was find a way to compress all the files and, instead of storing the
archive locally, pipe the output to another server.  

After much Googling and messing about, I ended up with the following
command:  

```bash
#Uses the tar utility to backup files to an external server

tar zcvf - /path/to/backup | ssh user@server:port dd of="filename.tgz" obs=1024
```

Of course, this is only practical for a one-off data dump. If regular
backups were needed, using [rsync][] would be the best option, as it
only transfers incremental changes. An excellent tutorial can be found
[here][].

  [rsync]: http://rsync.samba.org/
  [here]: http://troy.jdmz.net/rsync/index.html
