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

# Flyscanning Basics

Collecting synchrotron data "on the fly" rather than point-by-point makes use of specialized equipment to dramatically improve throughput. Instead of waiting for conditions to stabilize at each point along a scan, data can be collected by taking snapshots as changes occur continuously over a wide range of interest. In order to support this capability at facility scale, DSSI has identified standard hardware and software approaches which meet the needs of multiple techniques. Broadly speaking, these flyscanning approaches include:

* Measurements and position data are collected synchronously. (time-based)
* Measurements are collected at specific pre-defined positions. (position-based)
* Measurement and position data are collected independently, using time stamps and interpolation to co-bin streams. (asynchronous)

Implementing flyscanning in a supportable manner requires standards in hardware and software. A controls and data acquisition stack which satisfies this need is summarized as follows:

* PandABox position and signal acquisition system with FMC ACQ427ELF 8 channels ADC at 16 bit / 2 MSPS​ and 4 monitor cards
* PandABox firmware​ PandABlocks-FPGA 3.0-4​ or greater
* PandABox EPICS driver PandaBlocks-ioc 0.11.5​ or greater
* Bluesky data acquisition interface layer ophyd-async 0.10.0a2​ or greater

This implementation is described in the remaining sections of this tutorial.

## Integration of PandA with Motion and Sensors

In this section we will outline how to interface motion and sensors with the PandA, and how to setup the PandA for use with `ophyd-async`.

### Encoder I/O

In order to leverage motor positions in your flyscanning setup, you will require a compatible encoder. The encoder should be RS422, and be one of:

* Incremental (A Quad B)
* SSI
* BISS-C
* enDat

In all cases, adapt the encoder cable pinout to that of the PandA - pinout documentation is readily available in the manual and online. Connect the encoder cable to one of the four encoder ports on the PandA.

Next, in the Web UI, drag-and-drop the corresponding `INENC` block onto the GUI, and click on it to open the configuration menu on the right hand side of the page.

Here, find the option for setting encoder signal type, and match it to the one configured for your motor. Once this is done, move the motor and confirm that the value reported by the encoder block moves by an expected number of counts. You can also double check this by looking at the raw encoder count value from the  motor controller, and confirming that the delta from position A to B is the same for the controller and the PandA.

In the event that the encoder direction is reversed on the PandA and the controller, it can be re-inverted by feeding it's signal to a `CALC` block.

One additional feature of the `INENC` block is the toggle to `Reset on Z`. This will reset the PandA's encoder block reading to zero when a z-pulse is encountered. This feature is especially useful for rotatry motions that we want represented as an angle; the reset on Z option ensures that we can retrieve a degree value without needing to perform a modulo division first.

### Onboard ADC

The 

### TTL I/O

The PandA offers ten TTL output ports and six input ports as standard. These operate with the typical 0V low, 5V high. In order to trigger devices externally, see the device manuals for wiring. You may need BNC cable splitouts or adapters.

As a rule of thumb, use a single TTL output for each acquisition triggering frequency you need. For example, if you have two detectors being triggered at 10 Hz, use a single TTL output with a splitter if possible.

The TTL inputs can be used by other devices in order to initiate DAQ, or to keep track of when a detector was exposing. This can be useful in indentifying dropped frames; storing whether a detector ready signal is high/low when a trigger is sent can easily indicate a drop, or potentially be used as a condition to wait until the detector is ready.

It is even possible to use the TTL Input ready signal to trigger the detector directly, immediately after it is back to being ready, hence minimizing deadtime between exposures.

### Ophyd-Async

In order to utilize all of the above in DAQ plans, you will need to instantiate an `ophyd-async` PandA device, as well as devices for each of your triggered detectors.

To create a PandA ophyd_async device, you may use the following snippet:

```Python
from ophyd_async.fastcs.panda import HDFPanda
from ophyd_async.core import init_devices
from bluesky.run_engine import RunEngine

RE = RunEngine({})

with init_devices():
    my_panda = HDFPanda("MY:PV:PREFIX", name="my_panda")
```

Note that the instantiation of the run engine in the namespace is required prior to calling the `init_devices` context manager, since the asynchronous connection operation will be executed in the run engine's event loop

## Example Configurations

Below you will find guides for confiugring a full stack flyscanning solution using the described hardware and methodologies above for certain techniques.

### Tomography

A tomography flyscan can more-or-less be generalized to a single motion axis flyscan (the rotation axis), and can be setup to be performed vie equidistant in position triggers, or equidistant in time.

In both cases, 