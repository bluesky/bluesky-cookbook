import asyncio
import threading
from bluesky.utils import DefaultDuringTask
from ophyd_async.sim.demo import PatternDetector, SimMotor
from typing import Optional

class SampleSimulator(DefaultDuringTask):

    """A helper class that connects simulated PatternDetector to SimMotors to mimick an actual physical sample.

    Changes the signal produced by the pattern detector depending on the motors' positions.

    """

    def __init__(self, det : PatternDetector, motx : Optional[SimMotor] = None, moty : Optional[SimMotor] = None):
        self._loop = asyncio.new_event_loop()
        self.det = det
        self.motx = motx
        self.moty = moty
        super().__init__()

    @property
    def motx_pos(self):
        if self.motx is not None:
            return self._loop.run_until_complete(self.motx.user_readback.get_value())
        else: return 0.0

    @property
    def moty_pos(self):
        if self.moty is not None:
            return self._loop.run_until_complete(self.moty.user_readback.get_value())
        else: return 0.0

    def block(self, blocking_event):
        def target(event):
            while not event.wait(0.1):
                self.det.writer.pattern_generator.x = self.motx_pos
                self.det.writer.pattern_generator.y = self.moty_pos

        ev = threading.Event()
        th = threading.Thread(target = target, args=(ev, ), daemon=True)
        th.start()
        super().block(blocking_event)

        ev.set()