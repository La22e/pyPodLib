# Reading and writing the library

## Opening the library

```python
lib = ipod.library()
```

The result is cached. Pass `reload=True` to force a fresh parse from disk:

```python
lib = ipod.library(reload=True)
```

## Track metadata

The `Track` object exposes typed properties for every field in the iTunesDB:

```python
track = lib.tracks[0]

# Read
print(track.title, track.artist, track.album, track.genre)
print(track.track_number, track.total_tracks)
print(track.disc_number, track.total_discs)
print(track.year, track.bpm, track.rating, track.volume)
print(track.play_count, track.skip_count)
print(track.duration, track.size, track.bitrate, track.sample_rate)
print(track.location, track.filetype)
print(track.composer, track.comment, track.grouping, track.lyrics)

# Write
track.title = "New Title"
track.rating = 80   # 4 stars (0-100)
track.play_count = 42
ipod.save()
```

## Playlists

```python
# All playlists
for pl in lib.playlists:
    print(pl.name, "→", [t.title for t in pl.tracks])

# Master playlist (all tracks)
master = lib.master_playlist

# Smart playlists (auto-evaluated on save)
for spl in lib.smart_playlists:
    print(spl.name, "-", pl.smart_criteria)
```

## Saving

```python
ok = ipod.save()                  # raises on error (default)
ok = ipod.save(raise_on_error=False)  # returns True/False
```

`save()` performs:

1. **Build & evaluate playlists** — smart playlists re-evaluated, duplicate checks
2. **Serialise iTunesDB** — binary format with all track/playlist data
3. **Sign** — per-device checksum (HASH58 / HASH72 / HASHAB / NONE)
4. **Write SQLite databases** — for Nano 6G/7G (Library.itdb, Extras.itdb, etc.)
5. **Write iTunesPrefs** — plist-based preference sync
6. **Verify** — re-reads the written DB and validates referenced media files exist

If a referenced media file is missing, `save(raise_on_error=False)` returns `False`.
