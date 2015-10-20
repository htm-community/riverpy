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
import requests
import json
import time



DEFAULT_RV_URL = "http://data.numenta.org/"



def fetchJsonData(url, params=None, debug=False):
  if debug:
    print "params: %s" % params
    print "url: %s" % url
  dataResp = requests.get(url, params=params)
  if debug:
    print "full url: %s" % dataResp.request.url
  dataObj = json.loads(dataResp.text)
  return dataObj



class DataCursor():
  
  def __init__(self, stream, config, debug=False):
    self._debug = debug
    self._stream = stream
    self._config = config
    if "errors" in self._config:
      raise Exception(self._config["errors"][0])


  def _fetch(self, direction):
    if "urls" not in self._config:
      return None
    if direction not in self._config["urls"]:
      return None
    url = self._config["urls"][direction]
    dataObj = fetchJsonData(url, debug=self._debug)
    return DataCursor(self._stream, dataObj, debug=self._debug)


  def get(self, key):
    return self._config[key]
  
  
  def data(self):
    return self.get("data")


  def headers(self):
    return self.get("headers")


  def next(self):
    return self._fetch("next")

  
  def prev(self):
    return self._fetch("prev")


  def isEmpty(self):
    return len(self.data()) == 0


  def __str__(self):
    meta = self.get("meta")
    dataCount = len(self.data())
    dataDescription = "(%i data points / %s)" % (dataCount, meta["duration"])
    since = meta["since"]["timestring"] 
    until = meta["until"]["timestring"]
    
    return "%s [%s ==> %s] %s" % (self._stream, since, until, dataDescription)



class Stream():

  
  def __init__(self, river, config, debug=False):
    self._debug = debug
    self._river = river
    self._config = config


  def meta(self):
    return self._config["meta"]


  def get(self, key):
    return self._config[key]

  
  def data(self, since=None, until=None, limit=None, aggregate=None):
    url = self._config["urls"]["data"]

    # Convert all date queries into timestamps    
    if since is not None:
      since = int(time.mktime(since.timetuple()))
    if until is not None:
      until = int(time.mktime(until.timetuple()))

    params = {
      "since": since,
      "until": until
    }
    
    if limit is not None:
      params["limit"] = limit
    if aggregate is not None:
      params["aggregate"] = aggregate

    dataObj = fetchJsonData(url, params=params, debug=self._debug)
    return DataCursor(self, dataObj, self._debug)

  def __str__(self):
    return self._river.get("name") + " " + self.get("name")



class River():

  
  def __init__(self, config, debug=False):
    self._debug = debug
    self._config = config
    self._streams = []


  def get(self, key):
    return self._config[key]


  def _populateStreams(self):
    url = self._config["urls"]["keys"]
    params = {"includeDetails": True}
    streamsObject = fetchJsonData(url, params=params, debug=self._debug)
    streams = []
    meta = streamsObject["keys"]
    urls = streamsObject["urls"]["streams"]
    for streamName in meta.keys():
      metadata = meta[streamName]
      streams.append(Stream(self, dict({
        "name": streamName,
        "urls": urls[streamName],
        "meta": metadata
      }), debug=self._debug))
    self._streams = streams


  def streams(self):
    if len(self._streams) is 0:
      self._populateStreams()
    return self._streams


  def stream(self, name):
    streams = self.streams()
    for stream in streams:
      if stream.get("name") == name:
        return stream
    return None


  def __str__(self):
    return "%s (contains %i streams)" % (self.get("name"), len(self.streams()))



class RiverViewClient():


  def __init__(self, url=None, debug=False):
    self._debug = debug
    if url is None:
      url = DEFAULT_RV_URL
    self.url = url
    self._rivers = []
  

  def _populateRivers(self):
    url = self.url + "index.json"
    riversResp = fetchJsonData(url, debug=self._debug)
    rivers = []
    for riverObj in riversResp["rivers"]:
      rivers.append(River(riverObj, debug=self._debug))
    self._rivers = rivers


  def rivers(self):
    if len(self._rivers) is 0:
      self._populateRivers()
    return self._rivers


  def river(self, name):
    if len(self._rivers) is 0:
      self._populateRivers()
    for river in self._rivers:
      if river.get("name") == name:
        return river

