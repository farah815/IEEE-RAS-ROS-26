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

**Terminal 3 — View the RQT graph :**
```bash
source /opt/ros/jazzy/setup.bash
rqt_graph
```
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

## Screenshots

### RQT Graph — Nodes & Topic Connections
Shows the `traffic_manager` node subscribed to a robot's two independent
topics (`/robot_N/pose` and `/robot_N/priority`), confirming the two data
streams are wired as separate connections rather than a single combined topic.

![RQT Graph](home/farah/ros2_ws/src/Task12/Task12/rosgraph1)

### Terminal Output — SAFE / CLEAR case
Two robots farther apart than the 2.0 m safety radius — no yield required.

![Safe / Clear log](home/farah/ros2_ws/src/Task12/Task12/clear_log_screenshot1)

### Terminal Output — TOO CLOSE / DANGER case
Two robots within the 2.0 m safety radius — the lower-priority robot is
told to yield.

![Too close / Danger log](home/farah/ros2_ws/src/Task12/Task12/anger_log1)

> Place the three screenshot files above in a `screenshots/` folder next to
> this README, named to match the paths used here (or update the paths to
> match your filenames).

---

## Synchronization Notes

Position and priority arrive on **two separate topics per robot**
(`/robot_N/pose` and `/robot_N/priority`), published independently and not
guaranteed to arrive at the same time or in the same order.

To handle this without locking or blocking:

- Each robot gets one dictionary entry (`self.robots[rid]`) holding `x`, `y`,
  and `priority`, all initialized to `None`.
- A separate, lightweight callback is registered per topic per robot. Each
  callback's only job is to overwrite its one field in the dictionary the
  instant a message arrives — it does no comparison or decision logic itself.
- The decision logic lives entirely in a single 10 Hz timer (`decision_loop`),
  which reads whatever is currently cached in the dictionary at that instant.
  This decouples "receiving data" from "acting on data": the timer always
  works off the latest known snapshot, not a value that might still be in
  transit.
- Before comparing any robot, the code checks that **both** `x`/`y` and
  `priority` are non-`None`. This guards against a startup race where pose
  arrives before priority (or vice versa) — that robot is simply skipped
  from comparisons until both streams have reported at least once.
- Since the node runs in ROS2's default single-threaded executor, all
  callbacks and the timer execute one at a time on the same thread — they
  can never run concurrently or interrupt each other mid-update, so no
  mutex/lock is needed to protect the shared dictionary.

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
