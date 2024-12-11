---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Registering Bluesky Data in Tiled

+++

In the standard Bluesky data model, it is assumed that each data point produced during an experiment is emitted in a separate Event document. During the acquisition, such high granularity enables fast feedback and supports low-latency downstream agents (e.g. live plotting), however the naive storage of individual documents as records in a noSQL database is not optimized for the retrieval of blocks of data spanning multiple rows. Instead, the recently developed solution presented here parses the Event data into a tabular format during ingestion.

This tutorial introduces TiledWriter -- a specialized callback in Bluesky designed to aggregate and store the incoming data in a way that would facilitate future random access. While initially conceived as a mechanism for registering array data asynchronously written by area detectors (see Flyscanning tutorial), TiledWriter supports the ingestion of all existing synchronous data modalities (e.g. the usual Event/Datum documents) and transforms their contents into a tabular form, suitable for the efficient retrieval of columns.

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
!pip install canonicaljson
```

Start a local Tiled server, for example:
```bash
tiled serve catalog --temp --api-key=secret
```

```{code-cell} ipython3
# Initialize Tiled client
client = from_uri("http://localhost:8000", api_key="secret")
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
