`riverpy` is a python API client for [River View](https://github.com/nupic-community/river-view) instances.
 
## Installation
 
    pip install riverpy
 
## Usage
 
```python
from datetime import datetime
from riverpy import RiverViewClient

# create client that connects by default to http://data.numenta.org
client = RiverViewClient() 

# get River for http://data.numenta.org/portland-911/meta.html
river = client.river("portland-911")

# get Stream for http://data.numenta.org/portland-911/portland-911/data.html
stream = river.stream("portland-911")

# get first 500 data points, starting at 2015/05/01
cursor = stream.data(limit=500, since=datetime(2015, 4, 1))
# display some details about the data cursor
print cursor

# get data headers
headers = cursor.headers()
# get actual data
data = cursor.data()

# page through the data into the future until there's no more
while (cursor):
    cursor = cursor.next()
    print cursor
```

## Other Examples

See [`harness.py`](harness.py) for further examples of usage.