---
title: Reducing Chromecast Idle Bandwidth
date: 2018-12-10 22:50
author: Carey Metcalfe
tags:
 - chromecast
 - png
---

Google's [Chromecast][] is a pretty useful device. It plugs into the HDMI port of a TV and allows
users to "cast" content to it via a smartphone, [Chrome browser][], etc. This content is mostly
assumed to be streaming services like [Youtube][], [Spotify][], or [Netflix][], but for someone who
doesn't really buy into the whole cloud revolution like myself, it's still perfectly capable of
playing local content as well.

The one downside of the Chromecast is that when it's not being used, instead of going into a
low-power state and/or turning off the TV, it instead enters [Ambient Mode][]. This shows some
useful information overlaid on a changing backdrop of featured photos downloaded from [Google
Photos][]. The issue with this is that the images are high-resolution, not cached, and are
continually being downloaded 24/7 even when the TV is turned off. Although I haven't personally
measured it, the general consensus seems to be that it uses around 15GB of data per month from just
being plugged in.

What I'll be going over here is reducing the data the Chromecast uses by configuring it to only
download some tiny black 1x1 px images to use as a backdrop.

The short version
-----------------
- Make a tiny black PNG ([pixel.png][])
- Make a slightly different tiny PNG to avoid deduplication ([pixel_alt1.png][])
- Upload both to an album in Google Photos
- Mark both images as favorites
- Configure the Chromecast to only pull images from your specific album every 10 minutes

If you like details, keep reading...

Making a small image
--------------------
I ended up creating a 1x1 solid black image in GIMP, saving it as a PNG, hacking out as much data as
possible using a hex editor, then using [`pngcrush`][pngcrush] to attempt to optimize the data
that was left.

As I was working on the PNG file, I used a small script based on the Python [construct][] library to
visualize the chunks and structure of it so I could figure out what to cut.

To install `construct` and download the example PNG specification:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install construct
wget "https://raw.githubusercontent.com/construct/construct/abd48c4892ceddc60c11d25f4a955573e2c61111/deprecated_gallery/png.py"
```

Create `pngview.py`:
```python
import png  # the png spec downloaded above
import sys

with open(sys.argv[1], 'rb') as f:
    data = f.read()
    print("Size:", len(data), "bytes")
    print(png.png_file.parse(data))
```

Running it on the PNG exported from GIMP using the default settings gives:
```bash
$ ./pngview.py pixel.png
Size: 146 bytes
Container: 
    signature = b'\x89PNG\r\n\x1a\n' (total 8)
    image_header = Container: 
        length = 13
        signature = b'IHDR' (total 4)
        width = 1
        height = 1
        bit_depth = 8
        color_type = (enum) truecolor 2
        compression_method = (enum) deflate 0
        filter_method = (enum) adaptive5 0
        interlace_method = (enum) none 0
        crc = 2423739358
    chunks = ListContainer: 
        Container: 
            length = 9
            type = b'pHYs' (total 4)
            data = Container: 
                pixels_per_unit_x = 11811
                pixels_per_unit_y = 11811
                unit = (enum) meter 1
            crc = 2024095606
        Container: 
            length = 7
            type = b'tIME' (total 4)
            data = Container: 
                year = 2018
                month = 12
                day = 11
                hour = 5
                minute = 2
                second = 19
            crc = 904567710
        Container: 
            length = 25
            type = b'tEXt' (total 4)
            data = Container: 
                keyword = u'Comment' (total 7)
                text = b'Created with GIM'... (truncated, total 17)
            crc = 1468075543
        Container: 
            length = 12
            type = b'IDAT' (total 4)
            data = b'\x08\xd7c```\x00\x00\x00\x04\x00\x01' (total 12)
            crc = 657729290
        Container: 
            length = 0
            type = b'IEND' (total 4)
            data = None
            crc = 2923585666
```

After removing the unneeded `pHYs`, `tIME`, and `tEXt` chunks using a hex editor, it looks like this:
```bash
$ ./pngview.py pixel.png 
Size: 69 bytes
Container: 
    signature = b'\x89PNG\r\n\x1a\n' (total 8)
    image_header = Container: 
        length = 13
        signature = b'IHDR' (total 4)
        width = 1
        height = 1
        bit_depth = 8
        color_type = (enum) truecolor 2
        compression_method = (enum) deflate 0
        filter_method = (enum) adaptive5 0
        interlace_method = (enum) none 0
        crc = 2423739358
    chunks = ListContainer: 
        Container: 
            length = 12
            type = b'IDAT' (total 4)
            data = b'\x08\xd7c```\x00\x00\x00\x04\x00\x01' (total 12)
            crc = 657729290
        Container: 
            length = 0
            type = b'IEND' (total 4)
            data = None
            crc = 2923585666
```

At this point, all that's left to optimize is the image data itself. This is where `pngcrush`
shines. After running `pngcrush -brute -ow pixel.png` we see:
```bash
$ ./pngview.py pixel.png
Size: 67 bytes
Container: 
    signature = b'\x89PNG\r\n\x1a\n' (total 8)
    image_header = Container: 
        length = 13
        signature = b'IHDR' (total 4)
        width = 1
        height = 1
        bit_depth = 8
        color_type = (enum) greyscale 0
        compression_method = (enum) deflate 0
        filter_method = (enum) adaptive5 0
        interlace_method = (enum) none 0
        crc = 981375829
    chunks = ListContainer: 
        Container: 
            length = 10
            type = b'IDAT' (total 4)
            data = b'\x08\x1dc`\x00\x00\x00\x02\x00\x01' (total 10)
            crc = 3486004709
        Container: 
            length = 0
            type = b'IEND' (total 4)
            data = None
            crc = 2923585666
```

The 2 byte savings in the data seem to have come from setting the `color_type` to `greyscale`
instead of `truecolor`. To view what actually changed in the data, we can un-`deflate` it using Python:

```python
>>> import zlib
>>> # before pngcrush (12 bytes)
>>> zlib.decompress(b'\x08\xd7c```\x00\x00\x00\x04\x00\x01')
b'\x00\x00\x00\x00'
>>> # after pngcrush (10 bytes)
>>> zlib.decompress(b'\x08\x1dc`\x00\x00\x00\x02\x00\x01')
b'\x00\x00'
>>>
```

This makes sense since, according to the [PNG spec][], when using `truecolor`, each pixel is an RGB
triple, requiring 3 bytes. For `greyscale`, only a single byte representing luminance is needed. The
first byte is the filtering method, which isn't relevant here since we only have a single pixel.

Interestingly enough, in both cases we would actually be much better off if we could opt to **not** use
compression, but alas, the spec does not allow for anything except `deflate`.

But I digress, we now have a black 1x1 px PNG image that's just 67 bytes ([pixel.png][pixel.png]).

Generating multiple unique small images
---------------------------------------
So now we have the small PNG we want to display. Since the Chromecast's ambient mode requires at
least 2 different images in an album to cycle through, all we need to to do is upload 2 copies
of this PNG and we're done right? Almost.

Since Google Photos will automatically deduplicate uploaded images, we need to find a way to make
the second image slightly different. Normally this would involve tweaking a comment or something,
but in this case, the image has already been stripped down to its bare essentials.

My strategy was attempt to abuse the data compression to see if I could generate an image that
compressed the same data into the same number of bytes, but differently. Fortunately, `pngcrush` can
be told to use specific compression strategies (there are currently 177 of them). My hope is that at
least one of these will achieve the same results, but in a different way. For starters we'll try the
first 9:
```bash
for x in $(seq 9); do
    pngcrush -m "$x" pixel.png pixel_alt${x}.png;
done
```

A quick `ls -l` reveals that all of the `pixel_alt*.png` files are still 67 bytes. Now we just need
to find one that has different data. `sha1sum` is the perfect utility for this:
```bash
$ sha1sum pixel.png pixel_alt*.png
d99a9d63b1cd9e4b3f823d4d03144ccd95328f48  pixel.png
7487dcce2b2bb81a442faf139b0a547bf070d5e2  pixel_alt1.png
7487dcce2b2bb81a442faf139b0a547bf070d5e2  pixel_alt2.png
7487dcce2b2bb81a442faf139b0a547bf070d5e2  pixel_alt3.png
c3ea09bfcfcb36ce22d3f19eacada359f3984ed1  pixel_alt4.png
c3ea09bfcfcb36ce22d3f19eacada359f3984ed1  pixel_alt5.png
c3ea09bfcfcb36ce22d3f19eacada359f3984ed1  pixel_alt6.png
c3ea09bfcfcb36ce22d3f19eacada359f3984ed1  pixel_alt7.png
c3ea09bfcfcb36ce22d3f19eacada359f3984ed1  pixel_alt8.png
d99a9d63b1cd9e4b3f823d4d03144ccd95328f48  pixel_alt9.png
```

`pixel_alt1.png` looks like a good candidate, let's see what changed:
```
$ diff <(./pngview.py pixel.png) <(./pngview.py pixel_alt1.png)
20,21c20,21
<             data = b'\x08\x1dc`\x00\x00\x00\x02\x00\x01' (total 10)
<             crc = 3486004709
---
>             data = b'\x08[c`\x00\x00\x00\x02\x00\x01' (total 10)
>             crc = 1648381800
```

There's the same amount of data, but it's different. Let's check if it decompresses to the same
image data:
```python
>>> import zlib
>>> zlib.decompress(b'\x08\x1dc`\x00\x00\x00\x02\x00\x01')
b'\x00\x00'
>>> zlib.decompress(b'\x08[c`\x00\x00\x00\x02\x00\x01')
b'\x00\x00'
>>>
```

Yep, this means that [pixel_alt1.png][] is the exact same image with the exact same size, but won't
be deduplicated when uploading it to Google Photos since the compressed data is different.

Final touches
-------------
Now that we have 2 different tiny images, we can upload them to Google Photos and put them in an
album so they can be pulled down by the Chromecast. Something to note is that you may have to mark
the images as favorites to get them to be displayed. There seems to be some sort of AI-fueled "we
know better than you" algorithm that initially refused to display my images until I starred them.

Now just set your ambient mode to display the album with your images in it (or your favorites
album), set the slideshow speed to its maximum value (change image every 10 mins), and you're done.

[Chromecast]: https://store.google.com/product/chromecast
[Google Photos]: https://photos.google.com/
[Chrome browser]: https://www.google.com/chrome/
[Youtube]: https://www.youtube.com/
[Spotify]: https://www.spotify.com/
[Netflix]: https://www.netflix.com/
[Ambient Mode]: https://support.google.com/chromecast/answer/6080931
[PNG spec]: https://www.w3.org/TR/PNG/
[pixel.png]: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAAAAAA6fptVAAAACklEQVQIHWNgAAAAAgABz8g15QAAAABJRU5ErkJggg==
[pixel_alt1.png]: data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAAAAAA6fptVAAAACklEQVQIW2NgAAAAAgABYkBPaAAAAABJRU5ErkJggg==
[pngcrush]: https://pmt.sourceforge.io/pngcrush/
[construct]: https://construct.readthedocs.io/en/latest/
