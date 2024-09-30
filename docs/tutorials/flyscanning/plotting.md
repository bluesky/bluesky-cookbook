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

```{code-cell} ipython3

```

# Live Plotting of Streamed Data

A distictive characteristic of fly scanning plans is their reliance on continuous data streams rather than acquisition of data points invidually. In Bluesky, data streaming is realized via StreamResource and StreamDatum documents (as aooposed to Resource and Datum in step scanning). The eventual number of data points in the stream (e.g. image frames acquired during a flyscanning experiment) is typically unknown at the begininng of the aquisition; furtehrmore, the frames may arrive at non-uniformly spaced time intervals. Eventually, the frames become parts of the same resource and are often appended to the same file (in case of hdf5) by the detector.


We introduce the notion of Consolidators to facilitate random access by data access services, e.g. Tiled. Consolidators are analogous to Handlers that have existed in Bluesky for a long time, but they enable working with streamed data. A Consolidator is defined for a particular stream of data and is tied to the underlying resource; it knows how to read the data from disk in the most efficient manner.


In this notebook, we will explore the use of Consolidators as an option for live plotting of streamed data.

```{code-cell} ipython3
%load_ext autoreload
%autoreload 2

import os
import asyncio
import ophyd_async
import bluesky
from ophyd_async.sim.demo import PatternDetector, SimMotor
import bluesky.plans as bp
import bluesky.plan_stubs as bps
import bluesky.preprocessors as bpp
from bluesky.callbacks.core import CollectLiveStream
from bluesky.callbacks.mpl_plotting import LiveStreamPlot
from bluesky.run_engine import RunEngine
from pathlib import Path
from sample_simulator import SampleSimulator
from json_writer import JSONWriter


print(f"{ophyd_async.__version__=}\n{bluesky.__version__    =}")
```

```{code-cell} ipython3
import matplotlib
import matplotlib.pyplot as plt

%matplotlib widget
plt.ion()
```

```{code-cell} ipython3
fig, ax = plt.subplots(1, 2, figsize=(13, 4))
```

```{code-cell} ipython3
det = PatternDetector(name="PATTERN1", path=Path('.'))
motx = SimMotor(name="Motor_X", instant=False)
moty = SimMotor(name="Motor_Y", instant=False)
await motx.velocity.set(2.0)
await moty.velocity.set(1.0)

RE = RunEngine({}, during_task = SampleSimulator(det, motx, moty))

cl = CollectLiveStream()
pl_1d = LiveStreamPlot(cl, data_key="PATTERN1-sum", ax=ax[0])
pl_2d = LiveStreamPlot(cl, data_key="PATTERN1", ax=ax[1], clim=(0, 16))
wr = JSONWriter('./documents_test.json')

RE.subscribe(cl)
RE.subscribe(pl_1d)
RE.subscribe(pl_2d)
RE.subscribe(wr)
```

```{code-cell} ipython3
### Simple count plan without moving motors
RE(bp.count([det], num=5, delay=0.2))
```

```{code-cell} ipython3
### One-dimensional scan
plan = bp.scan([det], motx, 0, 2.5, 50)
RE(plan)
```

```{code-cell} ipython3
### Spiral trajectory
spiral_plan = bp.spiral([det], motx, moty, x_start=0.0, y_start=0.0,
                 x_range=3.0, y_range=3.0, dr=0.3, nth=10)
RE(spiral_plan)

# from bluesky.simulators import plot_raster_path
# plot_raster_path(spiral_plan, 'motor1', 'motor2', probe_size=.01)
```

```{code-cell} ipython3

```

```{code-cell} ipython3

```

```{code-cell} ipython3

```

```{code-cell} ipython3
### A custom plan
def plan():
    yield from scan([det], motx, 0, 2.5, 50)

    yield from bps.unstage_all(det, motx)

RE(plan())
```

```{code-cell} ipython3
RE.stop()
```

```{code-cell} ipython3
await det.prepare(0)
await det.unstage()
```

```{code-cell} ipython3

```

```{code-cell} ipython3
---
jupyter:
  outputs_hidden: true
---
gen = bp.fly([det])
for msg in gen:
    print(msg)
```

```{code-cell} ipython3
---
jupyter:
  outputs_hidden: true
---
gen = bp.count([det], num=5, delay=0.5)
for msg in gen:
    print(msg)
```

```{code-cell} ipython3

```

```{code-cell} ipython3

```

```{code-cell} ipython3

```

```{code-cell} ipython3

```

```{code-cell} ipython3

```

```{code-cell} ipython3

```

```{code-cell} ipython3
from ophyd_async.sim.demo._pattern_detector._pattern_generator import generate_gaussian_blob, generate_interesting_pattern
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(7, 7))

x_arr = np.linspace(0, 6, 100)
y_arr = np.linspace(-3.14, 3.14, 100)
xx, yy = np.meshgrid(x_arr, y_arr)

im1 = generate_gaussian_blob(width=350, height=200)
im2 = generate_interesting_pattern(xx, yy)
```

```{code-cell} ipython3
im = ax.imshow(im2)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)
```

```{code-cell} ipython3

```

```{code-cell} ipython3

```
