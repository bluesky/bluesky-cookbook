---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.6
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Saving Bluesky Data in Tiled

+++

In the standard Bluesky data model, it is assumed that each data point produced during an experiment is emitted in a separate Event document. During the acquisition, such high granularity enables fast feedback and supports low-latency downstream agents (e.g. live plotting), however the naive storage of individual documents as records in a database or lines in a file is not optimized for the retrieval of blocks of data spanning multiple rows. Instead, the recently developed solution presented here parses the Event data into a tabular format during ingestion.

This tutorial introduces TiledWriter -- a specialized callback in Bluesky designed to aggregate and store the incoming data in a way that would facilitate future random access. TiledWriter consumes Bluesky documents (all types of them) stores their contents at rest via API calls into a Tiled server. It transforms the data streams into a tabular form, suitable for the efficient retrieval of columns.

+++

### Initial Set-Up

```{code-cell} ipython3
import bluesky.plans as bp
from ophyd.sim import det, motor
from bluesky.run_engine import RunEngine
from bluesky.callbacks.tiled_writer import TiledWriter
from tiled.client import from_uri
from pprint import pprint
```

```{code-cell} ipython3
# Start a local Tiled server
# The following is equivalent to 'tiled server catalog --temp --api-key=secret'

from tiled_server import TempTiledServer

server = TempTiledServer(api_key='secret', dir_path='tiled_data')
tiled_uri = server.run()
```

```{code-cell} ipython3
# Initialize a Tiled client

client = from_uri(tiled_uri, api_key="secret")
client
```

```{code-cell} ipython3
# Initialize RunEngine and subscribe it to TiledWriter

RE = RunEngine({})
tw = TiledWriter(client)
RE.subscribe(tw)

# Keep the documents for monitoring/debug
docs = []
RE.subscribe(lambda name, doc : docs.append( (name, doc) ))
```

### Running the Acquisition

```{code-cell} ipython3
# Run the acquisition
docs.clear()
scan_id, = RE(bp.scan([det], motor, -5, 5, 10))
print(f"Finished aquisition: {scan_id=}")
```

Executing the above cell would have produced a stream of Bluesky documents, which have been saved and can be inspected in the `docs` list. Specifically, the Descriptor (`docs[1]`) contains specification of all available `data_keys` produced by the experinment (values of detector, `det`, `motor` and `motor_setpoint`).

```{code-cell} ipython3
# Data specification from the Descriptor document
stream_name = docs[1][1]['name']
print(f"Stream name: {stream_name}\n")
print("Specifications of recorded data:")
pprint(docs[1][1]['data_keys'])
```

The actual data values, along with their corresponding timestamps, are emmitted via Event documents (`docs[2:-1]`)

```{code-cell} ipython3
# Example of Event documents
pprint(docs[2:4])
```

### Accessing Data in Tiled

+++

The data produced during the experiment has been ingested into Tiled and stored in a container under the correpoding scan uuid.

NOTE: The internal structure of the Bluesky container is not finzalized yet and will change in the future releases.

```{code-cell} ipython3
bs_run = client[scan_id]
bs_stream = bs_run[stream_name]
event_data = bs_stream['internal/events']
event_data
```

It can now be accessed as a usual `pandas.DataFrame`:

```{code-cell} ipython3
event_data.read()
```

### Reading Data Directly from File

```{code-cell} ipython3
import pandas as pd

data_fpath = f'./tiled_data/data/{scan_id}/{stream_name}/internal/events/partition-0.csv'
df = pd.read_csv(data_fpath)
df
```

### Exploring the Tiled Catalog

```{code-cell} ipython3
import sqlite3

db_fpath = f'./tiled_data/catalog.db'
con = sqlite3.connect(db_fpath)
cur = con.cursor()
```

```{code-cell} ipython3
res = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
res.fetchall()
```

```{code-cell} ipython3
res = cur.execute("PRAGMA table_info('assets');")
res.fetchall()
```

```{code-cell} ipython3
res = cur.execute("SELECT * FROM assets;")
res.fetchall()
```

```{code-cell} ipython3

```

```{code-cell} ipython3

```
