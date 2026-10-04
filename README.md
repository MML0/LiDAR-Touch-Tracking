# LiDAR Touch Tracking

Real-time multi-touch detection and tracking from a 360° LiDAR sensor, built to drive an interactive LED wall game.

<img src="media/output-on-wall.gif" width="700" alt="LiDAR-tracked touch driving the LED wall in real time">

## Overview

This project turns a 360° LiDAR scanner into a large-scale, multi-touch interactive surface. A LiDAR unit mounted at the edge of an LED wall continuously scans the surface; raw distance points are filtered, clustered, and tracked over time to produce stable touch coordinates — each with a persistent ID — which drive an interactive game built in TouchDesigner.

The system was built for an interactive LED wall activation for **Dima**, the mobile app of **Bank Mellat** (Iran).

<img src="media/dima-logo.png" width="120" alt="Dima app mark">

## System

```
LiDAR (360°)
    │
    ▼
ESP32 / MCU  — serial read
    │
    ▼
Host PC — point cloud processing
    │
    ▼
Filtering → Clustering → Touch Detection
    │
    ▼
Multi-Touch Tracking (persistent IDs)
    │
    ▼
OSC
    │
    ▼
TouchDesigner  →  LED Wall / Game
```

<table>
<tr>
<td><img src="docs/system-in-situ.jpg" width="340" alt="The deployed system at the Mellat Multiverse booth"></td>
<td><img src="media/live-scan-dev-setup.jpg" width="340" alt="Live-testing the tracking script on a laptop, code next to the output"></td>
</tr>
<tr>
<td align="center"><sub>Deployed at the Mellat Multiverse booth</sub></td>
<td align="center"><sub>Live-testing the tracking script, code next to output</sub></td>
</tr>
</table>

## Hardware

<table>
<tr>
<td><img src="media/hardware-unboxing.jpg" width="380" alt="LDROBOT D800 LiDAR kit"></td>
<td><img src="media/hardware-assembly.jpg" width="380" alt="Sensor mount and electronics"></td>
</tr>
<tr>
<td align="center"><sub>LDROBOT D800 360° LiDAR</sub></td>
<td align="center"><sub>Sensor mount + ESP32 / driver electronics</sub></td>
</tr>
</table>

- **Sensor:** LDROBOT D800 360° LiDAR
- **Compute:** ESP32-based microcontroller(s) for sensor I/O, read over serial/USB by a host PC
- **Output:** OSC → TouchDesigner → LED wall

## Touch Detection & Tracking

The core problem: a LiDAR gives a noisy, unordered ring of distance points every frame — not touches. Getting from "points" to "stable multi-touch input" means solving a few distinct problems:

**Pipeline**

```
Raw Points → Filtering → Clustering → Touch Candidate → Persistent ID → Gesture
```

<table>
<tr>
<td><img src="media/live-scan-room-scan.png" width="220" alt="Full room scan, zoomed out, no touch"></td>
<td><img src="media/live-scan-demo.gif" width="220" alt="Live tracking output with persistent touch IDs"></td>
<td><img src="docs/led-wall-game.jpg" width="260" alt="Output on the LED wall"></td>
</tr>
<tr>
<td align="center"><sub>1. Raw scan</sub></td>
<td align="center"><sub>2. Touch detected (live)</sub></td>
<td align="center"><sub>3. Output on the wall</sub></td>
</tr>
</table>

1. **Filtering** — raw points are cleaned of sensor noise and the known static background (the wall itself) is subtracted, so only new objects (hands) remain.
2. **Clustering** — remaining points are grouped into candidate touch blobs.
3. **Persistent IDs** — each cluster is matched frame-to-frame against existing tracked touches by proximity, so the same hand keeps the same ID as it moves. New clusters get a new ID; touches that leave the surface are retired.
4. **Occlusion handling** — if a touch's points vanish for a split second (a dropped frame, a momentary sensor gap), its ID is kept alive for a short grace period and re-matched when it reappears, instead of being dropped and re-created. This keeps IDs clean and stable rather than flickering.
5. **Gesture output** — tracked per-ID motion over time is used to recognize gestures such as swipes.

This is what makes **multi-touch** possible on a sensor that has no concept of "touch" on its own — every object on the surface is tracked independently and concurrently, each with its own stable ID.

<img src="media/live-scan-ui.png" width="600" alt="Live tracking UI showing two touches with persistent IDs">

<sub>The actual tracking script running live — each tracked touch gets its own ID (here, <code>228</code> and <code>230</code>), alongside live FPS/point/touch counters.</sub>

See [`demo/touch_tracking_concept.py`](demo/touch_tracking_concept.py) for a short, simplified illustration of the ID-matching and occlusion logic (not the production code — see [Note on code](#note-on-code) below).

<sub>Note: steps 1 and 2 above are real captures of the tracking script itself; step 3 is a phone photo of the resulting on-surface output.</sub>

## Interactive LED Wall

Tracked touch points are sent over OSC into **TouchDesigner**, which runs the interactive game logic and drives the LED wall visuals in real time.

<img src="docs/led-wall-game.jpg" width="700" alt="Mellat Multiverse booth — LED floor installation">

<sub>The installation at the **Mellat Multiverse** booth (Dima, Bank Mellat).</sub>

## Demo

<table>
<tr>
<td><img src="media/close-up-test.gif" width="340" alt="Close-up of a finger triggering the touch response"></td>
<td><img src="media/live-scan-demo.gif" width="340" alt="Live tracking script output with persistent touch IDs"></td>
</tr>
<tr>
<td align="center"><sub>Touch response on the surface</sub></td>
<td align="center"><sub>The tracking script running live, side by side with the code</sub></td>
</tr>
</table>

## Repository Structure

```
LiDAR-Touch-Tracking/
├── README.md
├── LICENSE
├── media/              # hardware photos, test/demo videos
├── docs/               # real photos pulled from the test footage (see media/)
└── demo/
    └── touch_tracking_concept.py   # simplified, illustrative tracking logic
```

## Note on Code

This repository is a portfolio writeup of the project rather than the full production codebase. The script in [`demo/`](demo/) demonstrates the core tracking concept only.

## Credits

The LiDAR touch system itself — hardware, firmware, and tracking algorithm — was built by **Mohamad Mahdi Latifi ("MML")** and **[Arman-H-R](https://github.com/Arman-H-R)**. The interactive game running on top of it, in TouchDesigner, was also built by MML.

The wider installation had more people on it:

| Role | Name |
|---|---|
| Development | [Wenodes](https://www.instagram.com/wenodes) |
| LiDAR processing & tracking | [Arman-H-R](https://github.com/Arman-H-R) |
| LED wall visuals | [Toomaj](https://www.instagram.com/2maj.k) |
| Design | [Parsa Dirbas](https://www.instagram.com/parsadibazar) |

Built for an interactive LED wall activation for **Dima** (Bank Mellat, Iran).

*This repo documents the LiDAR touch system specifically — the credits above are for the full game/installation team.*

## License

[MIT](LICENSE)
