# Virtual iPods (test without hardware)

You can create a "virtual iPod" — a regular directory with a seeded database — for testing and development without physical hardware.

## Creating a virtual iPod

```python
from pypodlib.device import create_virtual_ipod, available_virtual_ipod_models

import tempfile
root = tempfile.mkdtemp()

info = create_virtual_ipod(root, "MC297")
# Now use it like a real iPod:
ipod = pypodlib.connect(root)
lib = ipod.library()
ipod.save()  # round-trips through the real writer
```

## Available models

The `create_virtual_ipod` function accepts any model number from the lookup table:

```python
for m in available_virtual_ipod_models():
    print(m["model"], m["generation"], m["checksum"])
```

Key models for testing each checksum family:

| Model | Generation | Checksum | Notes |
|---|---|---|---|
| `MC297` | Classic 7G 160GB | HASH58 | FireWire GUID |
| `MB029` | Classic 5.5G 30GB | HASH58 | |
| `MB562` | Classic 5.5G 80GB | HASH58 | |
| `MC027` | Nano 5G 8GB | HASH72 | AES via pycryptodome |
| `MC060` | Nano 5G 4GB | HASH72 | |
| `MC525` | Nano 6G 8GB | HASHAB | WebAssembly via wasmtime |
| `MKMX2` | Nano 7G 16GB | HASHAB | |
| `MA005` | Mini 2G 4GB | NONE | Pre-2007, no signature |

## Limitations

- Virtual iPods use a seeded empty database. You must add tracks via `add_tracks()` or populate the database manually before you can exercise write paths that verify media file existence.
- `scan_for_ipods()` and `identify_ipod_at_path()` will **not** detect virtual iPods (they expect actual USB-connected devices). Use `create_virtual_ipod()` + `connect()` directly.
