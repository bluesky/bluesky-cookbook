# Integration of PandA with Motion and Sensors

In this section we will outline how to interface motion and sensors with the PandA, and how to setup the PandA for use with `ophyd-async`.

## Encoder I/O

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

## Onboard ADC

The PandA optionally provides ADC and DAC capabilities. If the ADC card has been installed, the readings from the ADCs can be accessed via the `FMC_IN` block (and similarly `FMC_OUT` for DAC).

Please consult the PandA manual for referencing ADC specifications. Note that just like with any other signal, the PandA can be configured to capture the value, mean, max, min, etc. of each ADC channel.

## TTL I/O

The PandA offers ten TTL output ports and six input ports as standard. These operate with the typical 0V low, 5V high. In order to trigger devices externally, see the device manuals for wiring. You may need BNC cable splitouts or adapters.

As a rule of thumb, use a single TTL output for each acquisition triggering frequency you need. For example, if you have two detectors being triggered at 10 Hz, use a single TTL output with a splitter if possible.

The TTL inputs can be used by other devices in order to initiate DAQ, or to keep track of when a detector was exposing. This can be useful in indentifying dropped frames; storing whether a detector ready signal is high/low when a trigger is sent can easily indicate a drop, or potentially be used as a condition to wait until the detector is ready.

It is even possible to use the TTL Input ready signal to trigger the detector directly, immediately after it is back to being ready, hence minimizing deadtime between exposures.

## Ophyd-Async

In order to utilize all of the above in DAQ plans, you will need to instantiate an `ophyd-async` PandA device, as well as devices for each of your triggered detectors.

To create a PandA `ophyd_async` device, you may use the following snippet:

```Python
from pathlib import Path
from ophyd_async.fastcs.panda import HDFPanda
from ophyd_async.core import init_devices, StaticPathProvider, UUIDFilenameProvider
from bluesky.run_engine import RunEngine

path_provider = StaticPathProvider(
    UUIDFilenameProvider(),         # Generates UUID filenames
    Path("/tmp/panda_data"),        # Base directory path
    create_dir_depth = -1           # Determines how many levels of directories to create
)

RE = RunEngine({})

with init_devices():
    panda = HDFPanda("MY:PV:PREFIX", path_provider, name="panda")
```

Note that the instantiation of the run engine in the namespace is required prior to calling the `init_devices` context manager, since the asynchronous connection operation will be executed in the run engine's event loop.

Once created, you can see the available blocks with:

```Python
list(panda.children())
```

Specific blocks are either attributes (if there is one instance of the block), or elements in a list that is an attribute. For example, to access the `INENC1` block, we use:

```Python
panda.inenc[1]
```

We can then see the signals that are provided by this block with the same `children` generator:

```Python
list(panda.inenc[1].children())
```

In order for the PandA's `ophyd_async` device to generate resource and datum documents for any specific dataset, it must first be configured to be captured, and then a scientifically relevant name must be given to the dataset.

For example, for a tomography experiment where we are interested in recording the angle at which the rotatry motion was at for each trigger pulse, we have the PandA record the value of `INENC1.VAL` at each trigger (scaling it by a constant to convert encoder positions to angles), and then give the resulting dataset a name of `Angles`.

To do this via the ophyd device, we can do the following:

```Python
from ophyd_async.core import Settings
from ophyd_async.plan_stubs import apply_panda_settings

tomo_capture_settings = Settings(
    panda,
    {
        panda.inenc[1].val_capture: "Value",
        panda.inenc[1].val_dataset: "Angles"
    }
)

RE(apply_panda_settings(tomo_capture_settings))

```

The `apply_panda_settings` stub is a special version of `apply_settings_if_different` that ensures that the settings applied to the PandA are done in the correct order. For example, units are set before values etc.

## Example Configurations

Below you will find guides for confiugring a full stack flyscanning solution using the described hardware and methodologies above for certain techniques.

### Tomography

A tomography flyscan can more-or-less be generalized to a single motion axis flyscan (the rotation axis), and can be setup to be performed via equidistant in position triggers, or equidistant in time.

In both cases, connect your movement axis encoder signal to an encoder input on the PandA, and confirm that it is being read correctly. Consult the instructions above for this.

Next, connect the appropriate encoder block's output to the input of the `PCOMP` block. This is the block responsible for comparing values.

In the case of equidistant in position triggers, the output of this block is fed directly to the trigger input of `PCAP`, and the `TTLOUT` blocks connected to external detectors.

Alternatively, in the case of equidistant in time, the output is redirected to `PULSE` block.

In either case, construct a settings object to setup the requisit parameters for the `PCOMP` block:

```Python
```
