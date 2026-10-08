<p align="center">
  <img src="media/readme/banner.png" width="100%" alt="LiDAR Touch Tracking — turning 360° distance measurements into real-time touch input. On the right, the scan plane: a sensor on the LED wall's left edge and three tracked touches, each with an ID.">
</p>

# LiDAR Touch Tracking

Real-time multi-touch detection and tracking from a single 360° LiDAR sensor, built to drive an interactive LED wall game.

One sensor on the edge of the wall reads the whole surface about 20 times a second. Its raw distance points are filtered, clustered and tracked into stable touches — each with a persistent ID — and sent over OSC to a game built in TouchDesigner.

<p>
  <img src="https://img.shields.io/badge/sensor-LDROBOT%20D800-0e0e0e" alt="Sensor: LDROBOT D800">
  <img src="https://img.shields.io/badge/tracking-Python-0e0e0e" alt="Tracking: Python">
  <img src="https://img.shields.io/badge/output-OSC-0e0e0e" alt="Output: OSC">
  <img src="https://img.shields.io/badge/game-TouchDesigner-f2281d" alt="Game: TouchDesigner">
  <img src="https://img.shields.io/badge/license-MIT-6b7280" alt="License: MIT">
</p>

## Watch

<p align="center">
  <a href="media/films/lidar-touch-tracking-technical.mp4">
    <img src="media/readme/film-technical.gif" width="420" alt="Animated explainer: a LiDAR ray sweeps a wall and deposits points; the static background is removed; the remaining points cluster into three blobs, become touches, and keep their IDs as they move.">
  </a>
</p>
<p align="center">
  <sub><b>How it works, in 30 seconds.</b> Silent preview — <a href="media/films/lidar-touch-tracking-technical.mp4">open the film with sound</a>.</sub>
</p>

<table>
<tr>
<td width="50%" align="center">
  <a href="media/films/wenodes-case-study.mp4"><img src="media/readme/film-case-study.gif" width="340" alt="A visitor touches the LED wall and it lights up under her hand; the sensor on the wall's edge is ringed and its scan fans out across the surface."></a>
</td>
<td width="50%" align="center">
  <a href="media/films/wenodes-teaser.mp4"><img src="media/readme/film-teaser.gif" width="340" alt="A fingertip meets the wall, colour blooms under it, then the wide shot with the sensor marked, then the game."></a>
</td>
</tr>
<tr>
<td align="center"><sub><b>The installation</b> — Sense, Track, Play (22 s)<br><a href="media/films/wenodes-case-study.mp4">open with sound</a></sub></td>
<td align="center"><sub><b>Teaser</b> — one touch, the wall answers (16 s)<br><a href="media/films/wenodes-teaser.mp4">open with sound</a></sub></td>
</tr>
</table>

## At a Glance

- **One sensor** — an LDROBOT D800 360° LiDAR on the wall's left edge, scanning a plane just in front of the LED surface.
- **About 20 scans a second**, roughly 600–860 distance points per scan (figures from the live tracker).
- **True multi-touch** — every touch is tracked independently, with an ID that survives movement and brief dropouts.
- **OSC out** — touches go to TouchDesigner, which runs the game and drives the wall in real time.
- **Deployed** — an interactive LED wall activation for **Dima**, the mobile app of **Bank Mellat** (Iran), at the Mellat Multiverse booth.

<table>
<tr>
<td><img src="media/wall-touch-glow.jpg" width="340" alt="A visitor's touch driving the LED wall glow effect"></td>
<td><img src="media/dima-game-ui.jpg" width="340" alt="The Dima game screen — SCORE and PLAY counters, touch-controlled"></td>
</tr>
<tr>
<td align="center"><sub>The wall answering a touch</sub></td>
<td align="center"><sub>The Dima game — SCORE and PLAY, touch-controlled</sub></td>
</tr>
</table>

<img src="media/dima-logo.png" width="120" alt="Dima app mark">

## Where the Sensor Sits

<img src="media/readme/sensor-location.jpg" width="760" alt="The real installation: the LiDAR is ringed on the dark left edge of the LED wall. Arcs fan out from it across the wall, and a red line runs from the sensor to a visitor's hand where it touches the surface, labelled TOUCH ID 01.">

<sub>The real installation, with the sensor ringed. The arcs, the ray and the labels are drawn on; the photo is not.</sub>

The D800 is mounted on the left edge of the wall, at about chest height. Its scan plane lies just in front of the LED surface, so anything that reaches the wall — a hand, a fingertip — breaks the plane and shows up as a small cluster of points at that position.

Everything else the plane cuts through is static: the stage floor, the frame, the seams where it grazes the wall itself. That is learned once and subtracted, which is what leaves only touches.

## System

```mermaid
flowchart LR
    L["360° LiDAR<br/>LDROBOT D800"] --> E["ESP32 / MCU<br/>serial read"]
    E --> F
    subgraph PC["Host PC · Python"]
        direction LR
        F["Filtering"] --> C["Clustering"] --> T["Touch detection"] --> I["Persistent IDs"]
    end
    I -- "OSC /touch" --> TD["TouchDesigner<br/>game logic + visuals"]
    TD --> W["LED wall"]
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

## Touch Detection & Tracking

The core problem: a LiDAR gives a noisy, unordered ring of distance points every frame — not touches. Getting from "points" to "stable multi-touch input" means solving a few distinct problems.

<table>
<tr>
<td><img src="media/readme/step-01.png" width="270" alt="Step 1, 360° distance data: one rotation of the sensor leaves a ring of range points outlining the wall's frame and floor."></td>
<td><img src="media/readme/step-02.png" width="270" alt="Step 2, raw scan: the same ring with three small arcs of points where hands touch the wall, among stray returns."></td>
<td><img src="media/readme/step-03.png" width="270" alt="Step 3, filtering: a red dashed range gate appears and the background points fade, leaving the hands and a few strays."></td>
</tr>
<tr>
<td><img src="media/readme/step-04.png" width="270" alt="Step 4, clustering: zoomed in on the wall, three groups of red points are circled and labelled with their point counts."></td>
<td><img src="media/readme/step-05.png" width="270" alt="Step 5, touch detection: each group has become a ringed touch labelled ID 01, ID 02 and ID 03, with its x and y position."></td>
<td><img src="media/readme/step-06.png" width="270" alt="Step 6, persistent tracking: the touches leave trails as they move; ID 02 has lost its points and is shown dashed, labelled held 2/3."></td>
</tr>
</table>

<sub>Frames from the film above. The wall in them is simulated; the filtering, clustering and ID matching that draw it are a port of the project's real tracking logic. Real captures of the tracker are further down.</sub>

1. **Scan** — every rotation returns one ring of range points: the frame, the floor, reflections, and somewhere in there, hands.
2. **Filtering** — points beyond a 3 m range gate are ignored. A background model, captured in a short calibration pass on the empty wall, is then subtracted, so only new objects (hands) remain.
3. **Clustering** — neighbouring points (within 50 mm of each other) merge into candidate touch blobs. A blob needs at least 4 points, which drops lone stray returns.
4. **Touch detection** — each blob's centroid becomes a touch coordinate.
5. **Persistent IDs** — each blob is matched frame-to-frame against existing tracked touches by proximity, so the same hand keeps the same ID as it moves. New blobs get a new ID; touches that leave the surface are retired.
6. **Occlusion handling** — if a touch's points vanish for a split second (a dropped frame, a momentary sensor gap, another hand in the way), its ID is kept alive for a short grace period — 3 frames — and re-matched when it reappears, instead of being dropped and re-created. This keeps IDs clean and stable rather than flickering.
7. **Gesture output** — tracked per-ID motion over time is used to recognize gestures such as swipes.

This is what makes **multi-touch** possible on a sensor that has no concept of "touch" on its own — every object on the surface is tracked independently and concurrently, each with its own stable ID.

### OSC output

Every tracked touch is sent to TouchDesigner as one message per frame:

```
/touch  x  y  id  state
```

| Field   | Meaning                                         |
| ------- | ----------------------------------------------- |
| `x`, `y` | Touch position on the wall, relative to the sensor |
| `id`    | The touch's persistent ID                       |
| `state` | `1` touch down · `0` moving · `-1` released    |

### The real tracker

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

<img src="media/live-scan-ui.png" width="600" alt="Live tracking UI showing two touches with persistent IDs">

<sub>The actual tracking script running live — each tracked touch gets its own ID (here, <code>228</code> and <code>230</code>), alongside live FPS/point/touch counters.</sub>

<sub>Note: steps 1 and 2 above are real captures of the tracking script itself; step 3 is a phone photo of the resulting on-surface output.</sub>

See [`demo/touch_tracking_concept.py`](demo/touch_tracking_concept.py) for a short, simplified illustration of the ID-matching and occlusion logic (not the production code — see [Note on code](#note-on-code) below).

## Interactive LED Wall

Tracked touch points are sent over OSC into **TouchDesigner**, which runs the interactive game logic and drives the LED wall visuals in real time.

<table>
<tr>
<td><img src="media/close-up-test.gif" width="340" alt="Close-up of a finger triggering the touch response"></td>
<td><img src="docs/led-wall-game.jpg" width="300" alt="Mellat Multiverse booth — LED floor installation"></td>
</tr>
<tr>
<td align="center"><sub>Touch response on the surface</sub></td>
<td align="center"><sub>The installation at the <b>Mellat Multiverse</b> booth (Dima, Bank Mellat)</sub></td>
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

## Posters

<table>
<tr>
<td align="center"><a href="media/posters/poster-technical.png"><img src="media/posters/poster-technical.png" width="270" alt="Engineering poster: the scan plane, the ten-stage pipeline from LiDAR to interactive game, and four tiles showing one scan as raw, filtered, clustered and tracked."></a></td>
<td align="center"><a href="media/posters/poster-wenodes-case-study.jpg"><img src="media/posters/poster-wenodes-case-study.jpg" width="270" alt="Wenodes poster: Turning an LED wall into a game. A player touches a target on the red game wall under SCORE and PLAY counters; below, Sense, Track, Play, Experience."></a></td>
<td align="center"><a href="media/posters/poster-wenodes-teaser.jpg"><img src="media/posters/poster-wenodes-teaser.jpg" width="270" alt="Wenodes poster: LiDAR × LED wall × Interactive game. A visitor touches the glowing wall; the sensor on the wall's edge is ringed, with a line to her hand."></a></td>
</tr>
<tr>
<td align="center"><sub>The system on one sheet</sub></td>
<td align="center"><sub>Turning an LED wall into a game</sub></td>
<td align="center"><sub>LiDAR × LED wall × Interactive game</sub></td>
</tr>
</table>

## Repository Structure

```
LiDAR-Touch-Tracking/
├── README.md
├── LICENSE
├── demo/
│   ├── touch_tracking_concept.py   # simplified, illustrative tracking logic
│   └── D800Touch.py                # LDROBOT D800 serial reader (packet framing, CRC, points)
├── docs/                           # real photos pulled from the test footage
└── media/
    ├── films/                      # the three edited films, with sound
    ├── posters/                    # the three posters, full resolution
    ├── readme/                     # banner, previews and figures used on this page
    └── …                           # hardware photos, raw test clips, tracker captures
```

## Note on Code

This repository is a portfolio writeup of the project rather than the full production codebase. The scripts in [`demo/`](demo/) demonstrate the core tracking concept and the sensor reader only.

The diagrams in the films and posters are plotted from a simulated scan; all installation photos and footage are real. The films' music and sound design were synthesised for this project, with no third-party audio.

## Credits

| **Role**                    | **Name**                                                |
| --------------------------- | ------------------------------------------------------- |
| Development & LiDAR R&D     | [MML](https://github.com/MML0/)                         |
| LiDAR Processing & Tracking | [Arman H. R.](https://github.com/Arman-H-R)             |
| LED Wall Visuals            | [Toomaj](https://www.instagram.com/2maj.k)              |
| Design                      | [Parsa Dibazar](https://www.instagram.com/parsadibazar) |

**WENODES** — Interactive Technology & Experience

Built for an interactive LED wall activation for **Dima (Bank Mellat, Iran)**.

*This repo documents the LiDAR touch system specifically — the credits above are for the full game/installation team.*

## License

[MIT](LICENSE)
