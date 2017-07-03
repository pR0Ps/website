---
Title: Bank of Canada currency conversion rates in the terminal
Date: 2017-07-02 21:43
Author: Carey Metcalfe
Tags:
  - website
  - shell script
---

Preface
=======
In this entry I'll use two command line tools ([`curl`][curl] and [`jq`][jq]) to request currency conversion rates
from the [Bank of Canada]. Now obviously getting the same data through the [normal web interface] is
possible as well. However, doing it this way returns the data in a machine-readable form, allowing
it to be customized or used as input into other programs.

The basic flow will be request the data using `curl`, then pipe it to `jq` for processing.

!!! NOTE
    This article will request the USD/CAD exchange rate from 2017-01-01 to 2017-01-10. It should be
    fairly obvious how to switch this for any other currencies or date ranges. See the
    [Appendix](#appendix) for more information and caveats with the dates and the conversion codes.

We'll go from seeing the raw data the server returns to something that we can more easily use. **To
skip to the final result, click [here](#tldr)**.

Lets go!
========

Hitting the server without any processing will give the following result:
```bash
curl -s "http://www.bankofcanada.ca/valet/observations/FXUSDCAD/json?start_date=2017-01-01&end_date=2017-01-10"
```
```json
{
"terms":{
    "url": "http://www.bankofcanada.ca/terms/"
},
"seriesDetail":{
"FXUSDCAD":{"label":"USD/CAD","description":"US dollar to Canadian dollar daily exchange rate"}
},
"observations":[
{"d":"2017-01-02","FXUSDCAD":{"e":-64}},
{"d":"2017-01-03","FXUSDCAD":{"v":1.3435}},
{"d":"2017-01-04","FXUSDCAD":{"v":1.3315}},
{"d":"2017-01-05","FXUSDCAD":{"v":1.3244}},
{"d":"2017-01-06","FXUSDCAD":{"v":1.3214}},
{"d":"2017-01-09","FXUSDCAD":{"v":1.3240}},
{"d":"2017-01-10","FXUSDCAD":{"v":1.3213}}
]
}
```

To get the information we want, we need to iterate over the elements in the `observations` list and
map the date (`d`) to the conversion rate (`FXUSDCAD.v`). Since this will create a list of
single-element dictionaries, we'll also need to "add" (merge) them together.

To do this with `jq`, it looks like this:
```bash
curl -s "http://www.bankofcanada.ca/valet/observations/FXUSDCAD/json?start_date=2017-01-01&end_date=2017-01-10" |\
jq '
    [.observations[] | {(.d) : .FXUSDCAD.v}] | add
'
```
```json
{
  "2017-01-02": null,
  "2017-01-03": 1.3435,
  "2017-01-04": 1.3315,
  "2017-01-05": 1.3244,
  "2017-01-06": 1.3214,
  "2017-01-09": 1.324,
  "2017-01-10": 1.3213
}
```

That first `null` entry where there was no data is going to cause problems later, so let's just
delete it using the `del` function:
```bash
curl -s "http://www.bankofcanada.ca/valet/observations/FXUSDCAD/json?start_date=2017-01-01&end_date=2017-01-10" |\
jq '
    [.observations[] | {(.d) : .FXUSDCAD.v}] | add | del(.[] | nulls)
'
```
```json
{
  "2017-01-03": 1.3435,
  "2017-01-04": 1.3315,
  "2017-01-05": 1.3244,
  "2017-01-06": 1.3214,
  "2017-01-09": 1.324,
  "2017-01-10": 1.3213
}
```

Now this may be good enough for most purposes, but it would be useful to compute some other
statistics from this data. For example, we want to know the average exchange rate for the date
range. Now that we have the data in an easy to use format, computing an average with `jq` is just a
matter of passing the values to an `add / length` filter. For example:
```bash
curl -s "http://www.bankofcanada.ca/valet/observations/FXUSDCAD/json?start_date=2017-01-01&end_date=2017-01-10" |\
jq '
    [.observations[] | {(.d) : .FXUSDCAD.v}] | add | del(.[] | nulls) | add / length
'
```
```json
1.327683333333333
```

<a name="tldr"></a>We can now construct an object that has both the average, as well as all the
data. Putting it all together we get:

```bash
curl -s "http://www.bankofcanada.ca/valet/observations/FXUSDCAD/json?start_date=2017-01-01&end_date=2017-01-10" |\
jq '
[.observations[] | {(.d) : .FXUSDCAD.v}] | add | del(.[] | nulls) |
    {
        "average": (add / length),
        "values": .
    }
'
```
```json
{
  "average": 1.327683333333333,
  "values": {
    "2017-01-03": 1.3435,
    "2017-01-04": 1.3315,
    "2017-01-05": 1.3244,
    "2017-01-06": 1.3214,
    "2017-01-09": 1.324,
    "2017-01-10": 1.3213
  }
}
```

And that's it! Hopefully you found this useful, if not for it's stated purpose of retrieving
exchange rates, then at least for getting more familiar with `jq`. It's pretty much the best tool
out there when it comes to manipulating JSON on the command line.

Appendix<a name="appendix"></a>
===============================

### Date ranges
- The server will only ever return data from `2017-01-03` and onwards. If the start range is before
  that, it doesn't return an error, it just doesn't return any data for those dates.
- If the end date isn't specified, the server assumes the current date.
- There doesn't seem to be any limit on the amount of data retrieved

### Currency codes
A list of codes can be easily scraped from the lookup page. The command and its result are below for
reference.
```bash
curl -s "http://www.bankofcanada.ca/rates/exchange/daily-exchange-rates-lookup/" | grep -Eo '"FX......".*<'
```
```
"FXAUDCAD">Australian dollar<
"FXBRLCAD">Brazilian real<
"FXCNYCAD">Chinese renminbi<
"FXEURCAD">European euro<
"FXHKDCAD">Hong Kong dollar<
"FXINRCAD">Indian rupee<
"FXIDRCAD">Indonesian rupiah<
"FXJPYCAD">Japanese yen<
"FXMYRCAD">Malaysian ringgit<
"FXMXNCAD">Mexican peso<
"FXNZDCAD">New Zealand dollar<
"FXNOKCAD">Norwegian krone<
"FXPENCAD">Peruvian new sol<
"FXRUBCAD">Russian ruble<
"FXSARCAD">Saudi riyal<
"FXSGDCAD">Singapore dollar<
"FXZARCAD">South African rand<
"FXKRWCAD">South Korean won<
"FXSEKCAD">Swedish krona<
"FXCHFCAD">Swiss franc<
"FXTWDCAD">Taiwanese dollar<
"FXTHBCAD">Thai baht<
"FXTRYCAD">Turkish lira<
"FXGBPCAD">UK pound sterling<
"FXUSDCAD">US dollar<
"FXVNDCAD">Vietnamese dong<
```

 [curl]: https://curl.haxx.se/
 [jq]: https://stedolan.github.io/jq/
 [Bank of Canada]: http://www.bankofcanada.ca
 [normal web interface]: http://www.bankofcanada.ca/rates/exchange/daily-exchange-rates-lookup/
