#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import unicode_literals

AUTHOR = 'Carey Metcalfe'
SITENAME = 'Carey Metcalfe'

TIMEZONE = 'America/Toronto'

DEFAULT_LANG = u'en'

FEED_ALL_ATOM = None
FEED_ALL_RSS = "feeds/rss.xml"
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

PLUGIN_PATH = "plugins"
PLUGINS = ["sitemap",]

THEME = "theme"

#Theme specific
GOOGLE_ANALYTICS = "UA-28306875-1"
GOOGLE_PLUS_URL = "https://plus.google.com/+CareyMetcalfe"
TAGLINE = "B.CMP.H. Undergraduate"
USER_LOGO_URL = "https://s.gravatar.com/avatar/0b81e10e795095db6e3cb9b68a6d031d?s=150" # Gravatar
SCROLL_TO_CONTENT = True
FORCE_PIXELS = False
MANGLE_EMAILS = True
GLOBAL_KEYWORDS = ("cmetcalfe", "carey", "metcalfe", "pr0ps", "pr0pscm", "blog")

STATIC_PATHS = ['images', "files"]
EXTRA_PATH_METADATA = {
    'files/favicon.ico': {'path': 'favicon.ico'},
    'files/robots.txt': {'path': 'robots.txt'},
}

# Sitemap plugin
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

# Hacky name->icon logic (lowercase, \255 -> '-', '+' -> 'plus')
SOCIAL = (
    ("GitHub", "https://github.com/pR0Ps"),
    ("Google+", "https://plus.google.com/+CareyMetcalfe"),
    ("Twitter", "https://twitter.com/CareyMetcalfe"),
    #("Stackoverflow", "https://stackoverflow.com/users/369977/pr0ps"),
    ("LinkedIn", "https://linkedin.com/pub/carey-metcalfe/21/b6b/bba"),
    ("Résumé (PDF)", "/files/cv.pdf"),
    ("Email", "mailto:carey@cmetcalfe.ca"),
    ("Donate (BTC)", "bitcoin:1EuToNinKcR8mF2sTcgM9LLLN7aVi4zDSs"),
)

DEFAULT_PAGINATION = 3

RELATIVE_URLS = True

DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False
DEFAULT_CATEGORY = "content"
SUMMARY_MAX_LENGTH = None

INDEX_SAVE_AS = "blog/index.html"
ARCHIVES_URL = "blog/archives.html"
ARCHIVES_SAVE_AS = 'blog/archives.html'
ARTICLE_URL = 'blog/{slug}.html'
ARTICLE_SAVE_AS = 'blog/{slug}.html'
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'

TAGS_URL = 'blog/tags/'
TAGS_SAVE_AS = 'blog/tags/index.html'
TAG_URL = 'blog/tags/{slug}.html'
TAG_SAVE_AS = 'blog/tags/{slug}.html'

CATEGORIES_URL = ''#'blog/categories/'
CATEGORIES_SAVE_AS = ''#'blog/categories/index.html'
CATEGORY_URL = ''#'blog/categories/{slug}.html'
CATEGORY_SAVE_AS = ''#'blog/categories/{slug}.html'

AUTHORS_URL = ''#'blog/authors/'
AUTHORS_SAVE_AS = ''#'blog/authors/index.html'
AUTHOR_URL = ''#'blog/authors/{slug}.html'
AUTHOR_SAVE_AS = ''#'blog/authors/{slug}.html'
