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

# Live Plotting of Streamed Data

A distictive characteristic of fly scanning plans is their reliance on continuous data streams rather than acquisition of data points invidually. In Bluesky, data streaming is realized via StreamResource and StreamDatum documents, which extend their discrete counterparts (Resource and Datum) used in step scanning. The eventual number of data points in the stream (e.g. image frames acquired during a flyscanning experiment) is typically unknown at the begininng of aquisition; furtehrmore, the frames may arrive .... become the part of the same resource and are often appended to the same file (in case of hdf5) by the detector.
we introduce the notion of Consolidators to facilitate random access by data access services, like Tiled. Consolidator are analogous to Handlers that have existed in Bluesky for a long time, but they enable working with streamed data. A Consolidator is defined for a particular stream of data and is tied to the underlying resource; it knows how to read the data from disk in the most efficient manner 
In this notebook, we will explore the use of Consolidatorsan option for live plotting of streamed data

```{code-cell} ipython3
import ophyd_async
```

```{code-cell} ipython3
ophyd_async.__version__
```

```{code-cell} ipython3
import os

import matplotlib
import matplotlib.pyplot as plt
from ophyd_async.sim.demo import PatternDetector

import bluesky.plans as bp
from bluesky.callbacks.core import CollectLiveStream
from bluesky.callbacks.mpl_plotting import LiveStreamPlot

# if not os.getenv("GITHUB_ACTIONS"):
#     matplotlib.use("QtAgg")
#     plt.ion()
```

```{code-cell} ipython3

    cl = CollectLiveStream()
    pl = LiveStreamPlot(cl, data_key="PATTERN1-sum")
    RE.subscribe(pl)
    det = PatternDetector(name="PATTERN1-sum", path=tmp_path)
    RE(bp.count([det], num=15), cl)


def test_hdf5_plotting_2d(RE, tmp_path):
    cl = CollectLiveStream()
    pl = LiveStreamPlot(cl, data_key="PATTERN1")
    RE.subscribe(pl)
    det = PatternDetector(name="PATTERN1", path=tmp_path)
    RE(bp.count([det], num=15), cl)
```
