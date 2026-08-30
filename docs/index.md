# pyPodLib

Read, write, and sync iPod Classic/Nano/Mini libraries from Python — no iTunes required.

pyPodLib is a pure-Python library extracted from [iOpenPod](https://github.com/TheRealSavi/iOpenPod) (MIT, © John Gibbons). It keeps the battle-tested iTunesDB / iTunesCDB parsing and writing engine, device detection, and sync logic, and exposes it as a headless library.

## Features

- **Device detection** — scan for connected iPods and identify model, generation, capacity, colour, serial, and checksum type
- **Read** — parse the full library: tracks, user playlists, podcast playlists, smart playlists, play counts, artwork refs
- **Write** — save edits back with the correct per-device signature (HASH58, HASH72, HASHAB, or NONE), plus SQLite databases and iTunesPrefs protection
- **Sync** — plan and execute media sync, with optional artwork and transcode support
- **Testable without hardware** — create "virtual iPods" (a folder identity + seeded database) for round-trip tests

## Quick example

```python
import pypodlib

ipod = pypodlib.connect("/media/user/IPOD")
print(ipod.model_number, ipod.generation, ipod.capacity)

lib = ipod.library()
track = lib.tracks[0]
track.title = "New Title"
track.rating = 80   # 4 stars
ipod.save()
```

Full documentation: [la22e.github.io/pyPodLib](https://la22e.github.io/pyPodLib/) — or browse the [GitHub repo](https://github.com/La22e/pyPodLib).
