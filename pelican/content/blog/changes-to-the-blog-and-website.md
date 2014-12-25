---
Title: Changes to the blog and website
Date: 2013-12-11 06:30
Author: Carey Metcalfe
Tags: website
---

I used to run this site on two different platforms.
There was a static landing page hosted on my server, and a blog hosted on [Blogger][].

While the landing page was reasonably nice-looking (screenshot [here][screenshot]), the blog looked terrible.
Free Blogger templates are generally not the nicest-looking things to look at and the one I used was no exception.

More importantly though, the Blogger composer made really hard to generate nice-looking articles.
For just writing text posts, it wasn't bad (aside from the crazy HTML it generated), but for inserting code
snippits or doing any kind of advanced formatting it was incredibly frustrating.

A few weeks ago I finally decided to deal with the situation. My general plan was to find a static site generator
that allowed for writing posts in [Markdown syntax][] and use it to create a website that would
host some static content as well as the blog.

Static sites are exactly what they sound like. Just some static HTML files for a webserver to serve to clients.
No fancy frameworks, databases, or server-side processing involved. This is advantageous primarily because it
makes site blazing fast and very light on server resources.

After looking at a few static site generators, I decided to go with [Pelican][].
Pelican is a Python-based static site generator that uses the awesome [Jinja2][] templating library
and understands content written in a number of formats, including Markdown.
It's extremely easy to set up and requires only a single command to regenerate the entire site.

Transferring content from the old blog into the *.md files that Pelican reads was also really simple.
Pelican includes a tool called `pelican-import` that allows for reading in data from a variety of sources.
I used this tool to pull all my previous posts down from the RSS feed of the old blog.

After fixing up the imported data (the import tool is good, but not perfect), I started looking into templates.

Like with Blogger themes, I was having a hard time finding anything I liked, until I came across a template called [svbhack][].
It had a nice page layout and the general aesthetic was good, but needed a fair bit of tweaking.
I forked the repository (+1 for open-source) and over the next few weeks used my limited HTML and CSS knowledge to transform it into the one you see today.

There are still a bunch of things I want to change/fix/add, but at this point I feel that the site is ready to be released.
The code for the [template] and the [site] is all freely availible on GitHub.

If you have any comments or suggestions I'd love to hear them!

  [Blogger]: http://blogger.com
  [screenshot]: {filename}/images/old_website_screenshot.png
  [Markdown syntax]: http://daringfireball.net/projects/markdown
  [Pelican]: http://blog.getpelican.com
  [Jinja2]: http://jinja.pocoo.org/docs
  [svbhack]: https://github.com/giulivo/pelican-svbhack
  [template]: https://github.com/pR0Ps/pelican-svbhack
  [site]: https://github.com/pR0Ps/website
