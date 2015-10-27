#!/usr/bin/env python
# The MIT License (MIT)
#
# Copyright (c) 2015 Numenta, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from datetime import datetime, date, timedelta

from riverpy import RiverViewClient


def kwargsToString(**kwargs):
  out = []
  for key, value in kwargs.iteritems():
    out.append("%s:%s" % (key, value))
  return "[%s]" % (", ".join(out))


# url = "http://localhost:8085/"
url = None
client = RiverViewClient(url=url, debug=True)



r = client.river("mn-traffic-sensors")
for stream in r.streams():
  print stream.meta()





class RiverViewHarness(object):
  
  def __init__(self, client):
    self._client = client

  def run(self, river, stream, fn, **kwargs):
    print "Running harness (%s %s): %s %s" \
          % (river, stream, fn.__name__, kwargsToString(**kwargs))
    fn(client.river(river).stream(stream), **kwargs)


harness = RiverViewHarness(client)


def chronological_paging(stream, since=None, **kwargs):
  if since is None:
    since = datetime(1980, 1, 1)
  kwargs.update({"since":since}) 
  data = stream.data(**kwargs)
  print data
  # Go forward indefinitely
  while data:
    data = data.next()
    print data


def reverse_chronological_paging(stream, **kwargs):
  data = stream.data(**kwargs)
  print data
  # Go backwards indefinitely
  emptyCount = 0
  while data and emptyCount < 10:
    data = data.prev()
    if data.isEmpty(): 
      emptyCount += 1
    else:
      emptyCount = 0
    print data




oneDayAgo = date.today() - timedelta(days=1)
oneWeekAgo = date.today() - timedelta(days=7)
oneMonthAgo = date.today() - timedelta(days=28)
oneYearAgo = date.today() - timedelta(days=365)

# harness.run("mn-traffic-sensors", "T4024", chronological_paging, limit=500)
# harness.run("mn-traffic-sensors", "T4024", reverse_chronological_paging, limit=500)

# harness.run("portland-911", "portland-911", chronological_paging, since=oneWeekAgo, limit=50)
# harness.run("portland-911", "portland-911", reverse_chronological_paging)

# harness.run("portland-911", "portland-911", chronological_paging, since=oneYearAgo, aggregate="15 minutes")

