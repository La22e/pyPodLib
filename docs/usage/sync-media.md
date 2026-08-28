# Syncing media (`add_tracks`)

`add_tracks` copies audio files from your computer onto the iPod, extracts metadata via [mutagen](https://mutagen.readthedocs.io/), rebuilds the database, and signs it.

## Usage

```python
added = ipod.add_tracks([
    "/home/user/Music/Song A.mp3",
    "/home/user/Music/Song B.flac",
])
print(f"Added {added} tracks")
```

## How it works

1. Each source path is resolved to an absolute path.
2. Files are deduplicated within a single call (duplicate paths are skipped).
3. For each new file:
   - Metadata is extracted via mutagen (ID3 tags, Vorbis comments, etc.).
   - The file is copied to `iPod_Control/Music/FXX/<random>.mp3`.
   - A unique `db_track_id` is assigned.
4. The library database is rebuilt and signed (via `save()`).
5. Returns the count of newly added tracks.

!!! note "Session dedup"
    The dedup set is **per-call** — it does not persist across reloads or runs. If you call `add_tracks` twice with the same file, it will be added twice. (The iTunesDB binary format does not store the original source path.)

## Metadata source

The library falls back on metadata read by mutagen. For best results, ensure your files have proper ID3v2 (MP3), Vorbis comments (FLAC/OGG), or MP4 tags (AAC/M4A).

Filename stem is used as the fallback title.

## Artwork

Artwork extraction is **not** included in the base `add_tracks` flow. To also extract and embed album artwork:

```python
pip install 'pypodlib[artwork]'
```

Then use the `pypodlib.artworkdb_writer` module directly for custom artwork workflows after `add_tracks`.
