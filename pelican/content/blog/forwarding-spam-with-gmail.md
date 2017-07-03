---
Title: Forwarding spam with Gmail
Date: 2017-07-03 15:15
Author: Carey Metcalfe
Tags:
  - email
---

With multiple Gmail accounts, it's often easier to forward all emails to a single main account that
you actually check. This can be accomplished by setting up a forwarding account in Gmail's settings.

However, something that isn't immediately obvious is that messages that are considered spam are
never forwarded. While Gmail's spam detection is extremely good, it's not perfect. There have been
times where emails that I actually wanted have ended up in the spam folder and weren't forwarded to
my main account.

To fix this, we want to tell Gmail to not flag anything as spam so it will be forwarded along.

!!! NOTE
    This will **not** cause spam to appear in your inbox. It bypasses the spam filters so the email
    is forwarded properly, but the account it's forwarded to will *also* flag the email as spam. The
    end result is that that the email will end up in the spam folder of your main account (where you
    can actually look at it) instead of not being forwarded from the original account at all.

We can do this with a filter that matches `is:spam` and applies the option "Never send it to Spam".
Unfortunately, Gmail's interface makes this task much harder than it needs to be.

1. Open Gmail and do a search for `is:spam`. Notice that Gmail autocorrects it to `in:spam`.
2. Click the dropdown arrow on the right side of the search box to bring down the advanced options
   and click "Create filter with this search". Hit "OK" on the warning box that pops up. Notice that
   the filter has been autocorrected *again* to `label:spam`.
3. In the URL you should see something like `#create-filter/has=label%3Aspam`. Change `label` to
   `is` in the URL and hit enter. It should modify the text in the box without changing anything
   else.
4. Check the "Never send it to Spam" checkbox and hit "Create filter". You'll see the text get
   autocorrected to `in:spam` again, but if you check in Settings -> Filters and Blocked Addresses
   you should see the correct `is:spam` filter.
