# Limitations

- **Requires a mounted iPod volume** — USB enumeration is used for identification only. You must mount the iPod's filesystem before using the library.
- **Photo sync needs `artwork` extra** — embedded-art extraction and encoding require `numpy`, `Pillow`, and `mutagen`. Install with `pip install 'pypodlib[artwork]'`.
- **Video / ffmpeg transcoding** — transcoding video requires an `ffmpeg`/`ffprobe` binary on the system PATH.
- **Smart playlists are re-evaluated on save** — this matches iTunes behaviour but may surprise users who expect manual playlist edits to survive.
- **If checking out from source** — the repo includes a binary `.wasm` file for HASHAB checksums; it is not reproducible. Ensure the file is present at `src/pypodlib/itunesdb_writer/wasm/calcHashAB.wasm` (included in the wheel and source distribution).
- **Nano 5G/6G/7G use SQLite** — the database files inside `iPod_Control/iTunes/iTunes Library.itlp` use the `.itdb` extension but are SQLite databases, not binary iTunesDB files.
