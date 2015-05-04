---
Title: YouTube subscriptions via RSS
Author: Carey Metcalfe
Date: 2015/03/04 20:00
Modified: 2015/05/04 19:26
Tags:
 - sites
---

The [subscription feature][] on [Youtube][] allows you to keep up to date with content
that people upload to the site.

Since I use an RSS reader for every other blog or site that I follow, why not do
the same for YouTube subscriptions?

!!! Update
    This method no longer works. The YouTube v2 API (which is [what this method
    was using]) was [retired on April 20th, 2015][].

    To work around this, each channel must be subscribed to separately. See the
    RSS reader section on [this support page][].

The feed for anyone's subscribed videos is at the URL:

```
http://gdata.youtube.com/feeds/base/users/<userID>/newsubscriptionvideos
```

Where `<userID>` is either your YouTube account name or the long string of
letters and numbers that can be found on the [YouTube advanced settings page][].

Try it out, it makes watching episodic content a breeze!

!!! Warning
    You'll have to have "Keep all my subscriptions private" unchecked on the
    [YouTube privacy settings page][] for this to work.

    This will allow anyone to access the RSS feed of your subscriptions at the
    url above.

  [YouTube]: https://www.youtube.com
  [what this method was using]: https://developers.google.com/youtube/2.0/reference#Subscriptions_Feed
  [retired on April 20th, 2015]: http://youtube-eng.blogspot.ca/2014/03/committing-to-youtube-data-api-v3_4.html
  [this support page]: https://support.google.com/youtube/answer/6098135
  [subscription feature]: https://support.google.com/youtube/answer/4489286
  [YouTube privacy settings page]: https://www.youtube.com/account_privacy
  [YouTube advanced settings page]: https://www.youtube.com/account_advanced
