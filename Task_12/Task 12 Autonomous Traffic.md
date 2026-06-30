# Task 12 — Centralized Traffic Manager

## Overview
A **centralized** ROS2 system where multiple warehouse robots broadcast their
position and priority, and a single Traffic Manager node compares **every
unique pair of robots** and applies a Yielding Protocol to avoid collisions.

Unlike a decentralized design (where each robot decides for itself), all
decision-making here happens in one place: the `traffic_manager` node. The
robots themselves do nothing but report their state.

---

## File Structure
```
Task_12/
 fleet_emulator.py   : Simulates 4 robots broadcasting pose and priority
 traffic_manager.py  : Centralized controller — compares every robot pair
 README.md
```

---

## How to Run

**Terminal 1 — Start the fleet:**
```bash
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run task_12 fleet_emulator
```

**Terminal 2 — Start the traffic manager:**
```bash
cd ~/ros2_ws
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run task_12 traffic_manager
```

**Terminal 3 — View the RQT graph (optional):**
```bash
source /opt/ros/jazzy/setup.bash
rqt_graph
```

> If running as loose scripts instead of an installed package, replace the
> `ros2 run` commands above with `python3 fleet_emulator.py` and
> `python3 traffic_manager.py` (after sourcing ROS2 in each terminal).

---

## Robots & Priorities

| Robot ID | Priority |
|----------|----------|
| 1        | 3        |
| 2        | 5        |
| 3        | 1        |
| 4        | 4        |

Higher number = higher priority = right of way.

---

## Terminal Output

Each 0.1s cycle prints a full comparison table, e.g.:

```
======================================================================
               CENTRAL TRAFFIC MANAGER
======================================================================
Robot 1 vs Robot 2 | distance=8.46 m | SAFE -> both CLEAR
Robot 1 vs Robot 3 | distance=1.63 m | TOO CLOSE -> Robot 3 (priority=1) YIELDS to Robot 1 (priority=3)
Robot 1 vs Robot 4 | distance=2.04 m | SAFE -> both CLEAR
Robot 2 vs Robot 3 | distance=8.53 m | SAFE -> both CLEAR
Robot 2 vs Robot 4 | distance=7.65 m | SAFE -> both CLEAR
Robot 3 vs Robot 4 | distance=0.94 m | TOO CLOSE -> Robot 3 (priority=1) YIELDS to Robot 4 (priority=4)
======================================================================
```

---

## Yielding Protocol — Math

### Distance Calculation (Euclidean)
```
distance = √( (x_other − x_self)² + (y_other − y_self)² )
```

### Decision Rule (applied to every unique pair)
```
IF distance < 2.0 m
THEN -> the robot with the LOWER priority YIELDS to the one with HIGHER priority
       (if priorities are equal, the lower robot ID yields, to break the tie)
ELSE -> SAFE, both CLEAR
```

Each pair is evaluated independently and symmetrically — there is no fixed
"self" robot. Any robot can be told to yield to any other robot, depending on
who is closest and who has the lower priority at that moment.

---

## Centralization & Nested-Loop Comparison

All decision logic lives in **one node**: `TrafficManager`. It subscribes to
the pose and priority topics of **all 4 robots**, caches the latest values,
and every 0.1s runs a nested loop that compares each robot against every
other robot **exactly once**:

```python
for i, id1 in enumerate(ALL_ROBOT_IDS):
    for id2 in ALL_ROBOT_IDS[i + 1:]:
        # compare robot id1 and robot id2
```

Starting the inner loop at `i + 1` guarantees each pair (e.g. Robot 1 vs
Robot 3) is checked only once, not twice in both directions — for 4 robots
this gives 6 comparisons per cycle instead of 12.

---

## Synchronization Between Position and Priority Streams

Each robot publishes on two independent topics — one for `Pose2D` and one for
`Int32`. The `traffic_manager` subscribes to both streams for every robot and
caches the latest value in a shared dictionary:

```python
self.robots = {
    1: {"x": None, "y": None, "priority": None},
    2: {"x": None, "y": None, "priority": None},
    3: {"x": None, "y": None, "priority": None},
    4: {"x": None, "y": None, "priority": None},
}
```

- The **pose callback** updates `x` and `y` whenever a `/robot_N/pose`
  message arrives.
- The **priority callback** updates `priority` whenever a `/robot_N/priority`
  message arrives.
- The **10 Hz decision timer** (`decision_loop`) reads the latest snapshot of
  this dictionary every tick and runs the full pairwise comparison.

Since all callbacks and the timer run inside a single-threaded ROS2 executor,
they never interleave — no locking is needed. A robot is only included in a
comparison once both its `x`/`y` and `priority` are non-`None`, which
prevents partial or stale reads at startup.

The entire cycle's report is built as one string and printed with a single
`print()` call, so output is never garbled or interleaved between cycles.

---

## Demo Video
[https://youtu.be/PaUAHdrA5yc
]
