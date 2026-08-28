# Quickstart

## Connect to an iPod

```python
import pypodlib

# By known mount point
ipod = pypodlib.connect("/media/user/IPOD")

# Or scan for connected devices
all_ipods = pypodlib.scan_ipods()
if all_ipods:
    ipod = all_ipods[0]

print(ipod.model_number)   # e.g. "MA297"
print(ipod.generation)     # e.g. "7th Gen"
print(ipod.capacity)       # e.g. "160 GB"
print(ipod.checksum_type)  # pypodlib.device.ChecksumType.HASH58
```

## Read the library

```python
lib = ipod.library()

print(f"{len(lib.tracks)} tracks, {len(lib.playlists)} playlists")

for track in lib.tracks[:5]:
    print(track.title, track.artist, track.album)
```

## Edit a track

```python
track = lib.tracks[0]
track.title = "Renamed Track"
track.artist = "New Artist"
track.rating = 100  # 5 stars
```

## Save changes

```python
ipod.save()  # writes iTunesDB + signature + SQLite + iTunesPrefs
```

## Low-level access

All internal modules are importable:

```python
from pypodlib.device import scan_for_ipods, identify_ipod_at_path
from pypodlib.itunesdb_parser import parse_itunesdb, load_ipod_library
from pypodlib.itunesdb_writer import write_itunesdb, detect_checksum_type
from pypodlib.sync._db_io import read_existing_database, write_database
```
