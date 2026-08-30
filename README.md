# pyPodLib

Read, write, and sync iPod Classic/Nano/Mini libraries from Python — no
iTunes required.

pyPodLib is a pure-Python library extracted from
[iOpenPod](https://github.com/TheRealSavi/iOpenPod) (MIT, © John Gibbons).
It keeps the battle-tested iTunesDB / iTunesCDB parsing and writing engine,
device detection, and sync logic, and exposes it as a headless library.

## Features

- **Device detection** — scan for connected iPods and identify model,
  generation, capacity, colour, serial, and checksum type (`scan_ipods`,
  `identify_ipod_at_path`).
- **Read** — parse the full library: tracks, user playlists, podcast
  playlists, smart playlists (dataset 2/3/5), play counts, artwork refs.
- **Write** — save edits back with the correct per-device signature
  (HASH58 via FireWire GUID, HASH72 via AES, HASHAB via WebAssembly,
  NONE for pre-2007 devices), plus SQLite DBs for Nano 6G/7G and
  iTunesPrefs protection.
- **Sync** — plan and execute media sync, with optional artwork and
  transcode support.
- **Testable without hardware** — create "virtual iPods" (a folder
  identity + seeded database) for round-trip tests
  (`pypodlib.device.create_virtual_ipod`).

## Install

```console
pip install pypodlib                          # core (device + library read/write)
pip install 'pypodlib[artwork]'               # + embedded-art extraction/encoding
```

Runtime dependencies: `pyusb` / `libusb-package` (USB identification),
`pycryptodome` (HASH72 signing), `wasmtime` (HASHAB signing).

## Documentation

Full documentation: [la22e.github.io/pyPodLib](https://la22e.github.io/pyPodLib/)

## Quick start

```python
import pypodlib

ipod = pypodlib.connect("/media/user/IPOD")        # or pypodlib.scan_ipods()[0]
print(ipod.model_number, ipod.generation, ipod.capacity)

lib = ipod.library()
print(len(lib.tracks), "tracks")

track = lib.tracks[0]
track.title = "New Title"
track.rating = 80                                 # 4 stars
ipod.save()                                       # writes iTunesDB + signature
```

### Low-level access

Every layer stays importable:

```python
from pypodlib.device import scan_for_ipods, identify_ipod_at_path
from pypodlib.itunesdb_parser import parse_itunesdb, load_ipod_library
from pypodlib.itunesdb_writer import write_itunesdb, detect_checksum_type
from pypodlib.sync._db_io import read_existing_database, write_database
```

### Virtual iPods (no hardware)

```python
from pypodlib.device import create_virtual_ipod, available_virtual_ipod_models

import tempfile
root = tempfile.mkdtemp()
info = create_virtual_ipod(root, "MC297")   # iPod Classic 7th Gen (HASH58)
ipod = pypodlib.connect(root)
ipod.library()
ipod.save()                                  # round-trips through real writer
```

## Limitations

- Requires a mounted iPod volume (or a virtual iPod root) — USB enumeration
  is used for identification only.
- Photo sync and embedded-art encoding need the `artwork` extra
  (`numpy`, `Pillow`, `mutagen`).
- Video/ffmpeg transcoding requires an `ffmpeg`/`ffprobe` binary.
- Smart playlists are re-evaluated on save (matching iTunes behaviour).

## License

MIT. pyPodLib is derived from iOpenPod (MIT, © John Gibbons).