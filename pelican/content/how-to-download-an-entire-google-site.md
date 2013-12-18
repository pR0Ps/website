Title: How to download an entire Google Site
Date: 2012-08-16 12:13
Author: Carey Metcalfe
Tags: website, shell script, backup

When using Google Sites, there is currently no way to make a backup of your
site, or download the site so you can host it on another server.  

This command uses a tool called `wget` to spider through a website
and download all the public files to the local computer. Unix users will
most likely have the wget tool already installed (if not, you can
install it via your preferred package manager), while Windows users can
get it from [here][].  

Once wget is installed, run it with the following parameters:  

```bash
#Downloads all public pages on a Google Site

wget -e robots=off -m -k -K -E -rH -Dsites.google.com --no-check-certificate http://sites.google.com/a/domain/site/
```

This tells wget to spider through all the links on your site and download
the html files and linked content (such as images). Note that pages that
aren't linked from anywhere on the site won't be downloaded.

This technique will also work for websites other than the ones hosted on Google Sites.

  [here]: http://gnuwin32.sourceforge.net/packages/wget.htm
