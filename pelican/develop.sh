#!/bin/sh

function finish {
    if kill -0 $pid >/dev/null 2>&1; then
        kill $pid
    fi
}
trap finish EXIT

mkdir output 2> /dev/null
cd output
if python --version 2>&1 >/dev/null | grep -q "Python 2"; then
    python -m SimpleHTTPServer 8000 2> /dev/null &
else
    python -m http.server 8000 2> /dev/null &
fi
pid=$!
cd - > /dev/null
pelican --autoreload -s pelicanconf.py -o output/ --delete-output content/
