Title: Gotcha with basic HTTP authentication in Python
Date: 2013-06-12 19:53
Author: Carey Metcalfe
Tags: code, python

When doing basic HTTP authentication in Python, make sure your
authentication realm is surrounded by double, _NOT_ single quotes.

Bad:
```python
self.send_response(401)
self.send_header("WWW-Authenticate", "Basic realm='/'")
self.end_headers()
```

Good:
```python
self.send_response(401)
self.send_header("WWW-Authenticate", "Basic realm=\"/\"")
self.end_headers()
```

The single quotes work with most browsers, curl, wget, and tons of other
tools. However, when using Python to access the page (using
[urllib2.HTTPPasswordMgrWithDefaultRealm][] to manage authentication)
single quotes don't trigger the "automatic retry with authentication"
response, and instead just raise a 401 `HTTPError`.

  [urllib2.HTTPPasswordMgrWithDefaultRealm]: http://docs.python.org/2/library/urllib2.html#urllib2.HTTPPasswordMgrWithDefaultRealm
