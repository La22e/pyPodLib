"""
pypodlib — communicate with iPod Classic/Nano/Mini devices from Python.

pyPodLib is a pure-Python library that reads and writes the iPod's on-disk
library (iTunesDB / iTunesCDB) without iTunes.  It can:

- detect and identify a connected iPod (model, generation, capacity, colour)
- read tracks, playlists, podcasts, smart playlists and play counts
- write the database back with the correct per-device checksum signature
- copy media files onto the device and regenerate the database

Typical usage::

    import pypodlib

    ipod = pypodlib.connect("/media/user/IPOD")           # or scan_ipods()[0]
    print(ipod.model.family, ipod.model.generation)

    lib = ipod.library()
    for track in lib.tracks:
        print(track.title, track.artist)

    lib.tracks[0].rating = 5
    ipod.save()

The low-level modules remain importable directly (``pypodlib.device``,
``pypodlib.itunesdb_parser``, ``pypodlib.itunesdb_writer``, ...).
"""

from __future__ import annotations

from .api import IPod, Library, Playlist, Track, connect, library_from_path, scan_ipods

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "connect",
    "scan_ipods",
    "library_from_path",
    "IPod",
    "Library",
    "Track",
    "Playlist",
]