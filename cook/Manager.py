#!/usr/bin/env python

import pycurl
import sys

try:
    # Python 3
    from io import BytesIO
except ImportError:
    # Python 2
    from StringIO import StringIO as BytesIO

url = 'http://zongbinghuang.com'
url = 'http://127.0.0.1'

c = pycurl.Curl()
c.setopt(c.URL, url)

buffer = BytesIO()
c.setopt(c.WRITEFUNCTION, buffer.write)
try:
    c.perform()
except:
    exctype, error = sys.exc_info()[:2]
    print(error)

string_body = buffer.getvalue().decode('utf-8')
buffer.close()
print(string_body)
