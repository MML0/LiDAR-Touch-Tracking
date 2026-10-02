"""
Conceptual illustration of the LiDAR touch-tracking pipeline.

This is a simplified, documentation-only version of the approach used in the
real project. It is NOT the production code that ran on the installation —
it exists to show the shape of the algorithm:

  raw points -> filtering -> clustering -> persistent IDs -> gesture output

Real-world concerns the production code handled that are left out here:
sensor-specific parsing, serial/USB I/O, angular offset calibration per boot,
wall/background subtraction, OSC output, and performance tuning.
"""

from dataclasses import dataclass, field
import math
import time


@dataclass
class TouchPoint:
    id: int
    x: float
    y: float
    last_seen: float
    history: list = field(default_factory=list)


class TouchTracker:
    """Turns noisy per-frame point clusters into stable, identified touches."""

    def __init__(self, match_radius=40.0, grace_period=0.25):
        self.match_radius = match_radius   # max distance (mm) to treat a new
                                            # cluster as the same touch
        self.grace_period = grace_period   # seconds a touch may vanish for
                                            # (e.g. a dropped frame) before
                                            # its ID is retired
        self._touches: dict[int, TouchPoint] = {}
        self._next_id = 0

    def update(self, clusters: list[tuple[float, float]], now: float | None = None):
        """clusters: list of (x, y) cluster centroids detected this frame."""
        now = now if now is not None else time.time()
        unmatched = set(self._touches)

        for (x, y) in clusters:
            touch_id = self._match_existing(x, y, unmatched)
            if touch_id is None:
                touch_id = self._next_id
                self._next_id += 1
                self._touches[touch_id] = TouchPoint(touch_id, x, y, now)
            else:
                touch = self._touches[touch_id]
                touch.history.append((touch.x, touch.y))
                touch.x, touch.y, touch.last_seen = x, y, now
                unmatched.discard(touch_id)

        self._retire_stale(unmatched, now)
        return list(self._touches.values())

    def _match_existing(self, x, y, candidate_ids):
        best_id, best_dist = None, self.match_radius
        for tid in candidate_ids:
            t = self._touches[tid]
            dist = math.hypot(t.x - x, t.y - y)
            if dist < best_dist:
                best_id, best_dist = tid, dist
        return best_id

    def _retire_stale(self, unmatched_ids, now):
        # A touch that briefly disappears (occlusion, a dropped frame) keeps
        # its ID for `grace_period` seconds instead of being dropped and
        # re-created — this is what keeps IDs stable across short gaps.
        for tid in list(unmatched_ids):
            if now - self._touches[tid].last_seen > self.grace_period:
                del self._touches[tid]

    @staticmethod
    def detect_swipe(touch: TouchPoint, min_distance=60.0) -> str | None:
        if len(touch.history) < 2:
            return None
        x0, y0 = touch.history[0]
        dx, dy = touch.x - x0, touch.y - y0
        if math.hypot(dx, dy) < min_distance:
            return None
        return "horizontal" if abs(dx) > abs(dy) else "vertical"
