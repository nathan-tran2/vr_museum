# vr_museum

Proactive gaze-aware AI companion for an immersive Pompeii museum exhibit in VR.
Built on Meta Quest 3 + Pupil Labs Neon XR, with Unity for the environment and
a Python real-time pipeline for gaze interpretation.

## Status

- [x] Python environment set up (venv, pupil-labs-realtime-api)
- [x] Project structure and git repo initialized
- [ ] Phone / Neon hardware tested end-to-end
- [ ] First gaze stream running
- [ ] Unity project created
- [ ] MRTK3 template running on Quest 3
- [ ] First Pompeii asset imported with AOI colliders
- [ ] Dwell → LLM → audio pipeline (GazeGPT-style)

## Setup

Requires Python 3.12+, Meta Quest 3, Pupil Labs Neon with Companion phone,
and PC + phone on the same Wi-Fi.

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Scripts

- `scripts/test_gaze.py` — one-shot discovery test
- `scripts/stream_gaze.py` — live gaze + pupil stream to console
- `scripts/log_session.py` — logs session data to CSV in `data/`
- `scripts/connect_by_ip.py` — fallback when network discovery fails

## Hardware

- Meta Quest 3
- Pupil Labs Neon module + Companion phone
- PC on the same Wi-Fi as the phone

## Project Layout

- `scripts/` — Python real-time API code
- `unity/` — Unity project (to be created)
- `notes/` — planning docs, meeting notes, system design
- `data/` — session logs (git-ignored)
