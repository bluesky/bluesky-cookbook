<!-- #region -->
# Data Storage and Management


The flyscanning plans developed for PandA rely on the streaming capabilities of Bluesky enabled in the recent versions of [EventModel](https://github.com/bluesky/event-model) and make use of `StreamResource` and `StreamDatum` documents. The legacy approach for managing collected Bluesky data with databroker does not support these types of documents. Hence, to improve the conveneince of data access, it is recommended that the flyscanning solution be deployed along with the [Tiled](https://blueskyproject.io/tiled/) data management service backed by an SQL catalog. See the official documentation of Tiled for details on how to deploy and configure it.

Once the Tiled service is set up, the writing of flyscanning data collected with Bluesky plans is achieved via a dedicated `TiledWriter` callback instantiated with a Tiled client and subscribed to the RunEngine. Please ensure that the client has appropriate writing permissions to the desired Tiled catalog. Assuming that the Tiled server is started locally with `tiled serve catalog --temp --api-key=secret` (or using a more detaild configuration as descibed [here](https://blueskyproject.io/tiled/how-to/configuration.html)), the `TiledWriter` can be initialized as shown below.
<!-- #endregion -->

```python
from bluesky import RunEngine
from bluesky.callbacks.tiled_writer import TiledWriter
from tiled.client import from_uri
```

```python
RE = RunEngine()
tiled_client = from_uri("http://localhost:8000", api_key="secret")
tw = TiledWriter(tiled_client)
RE.subscribe(tw)

tiled_client
```

Tiled allows the user to work with their data using the familiar array or dataframe API without the need to consider specifics of how the data is stored. Under the hood, however, Tiled distinguishes between two types of data based on their origin. First, the data that originates from the Bluesky Event documents and is transmitted in the stream itself (so called "slow" data: scalar measurements, motor positions, or device configurations) are saved by Tiled itself in its internal writable storage. Second, the "fast" data are typically produced by area detectors at much higher rates and saved directly to the file system; Tiled then uses references to the saved location from the StreamResource documents and registers the file in the catalog of external assets. Typoically, datasets produced by the PandA controller would also be saved externally as HDF5 files and registered similarly.

`TiledWriter` handles both types of data and places them in subcontainers according the stream name (configured in the Descriptor document). More detail about the layout of the resulting container can be found [here](https://blueskyproject.io/bluesky/main/tiled-writer.html).

In this tutorial, to demonstrate these capabilities, we mimic the Bluesky document stream using simulated ophyd devices that write internal and external data.

```python
from ophyd.sim import det
from ophyd.sim import hw
import bluesky.plans as bp
from pathlib import Path
```

```python
# Collect and write "internal" (Event) data
uid, = RE(bp.count([det], 10))

print(f"Finished collecting data for Bluesky run with uid = {uid}")
```

```python
tiled_client[uid]
```

```python
# Read the acquired data as an xarray dataset
tiled_client[uid]['streams/primary'].read()
```

```python
# Collect and write external data
Path('/tmp/tiled_data').mkdir(exist_ok=True)
uid, = RE(bp.count([hw(save_path='/tmp/tiled_data').img], 10))

print(f"Finished collecting data for Bluesky run with uid = {uid}")
```

Note: to be able to retrieve the registered external data from Tiled, please ensure that the server has read access to the storgae location, e.g. start it using
```
tiled serve catalog --temp --api-key=secret -r /tmp/tiled_data
```

```python
tiled_client[uid]['streams/primary'].read()
```

```python

```
