---
Title: Youtube subscriptions via RSS
Author: Carey Metcalfe
Date: 2015/03/04 20:00
Tags:
 - sites
---

The [subscription feature][] on [Youtube][] allows you to keep up to date with content
that people upload to the site.

Since I use an RSS reader for every other blog or site that I follow, why not do
the same for Youtube subscriptions?

The feed for anyone's subscribed videos is at the URL:

```
http://gdata.youtube.com/feeds/base/users/<userID>/newsubscriptionvideos
```

Where `<userID>` is either your Youtube account name or a long string of letters and
numbers that can be found on the [Youtube advanced settings page][].

Try it out, it makes watching episodic content a breeze!

!!! Warning
    You'll have to have "Keep all my subscriptions private" unchecked on the
    [Youtube privacy settings page][] for this to work.

    This will allow anyone to access the feed of your subscriptions at the url
    above.

  [Youtube]: https://www.youtube.com
  [subscription feature]: https://support.google.com/youtube/answer/4489286
  [Youtube privacy settings page]: https://www.youtube.com/account_privacy
  [Youtube advanced settings page]: https://www.youtube.com/account_advanced
