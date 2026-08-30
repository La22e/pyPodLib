# Changelog

## 0.1.0 (2026-08-30)

- Initial release extracted from [iOpenPod](https://github.com/TheRealSavi/iOpenPod) (MIT, © John Gibbons).
- Device detection and identification (USB + filesystem)
- iTunesDB / iTunesCDB parser and writer with per-device checksums
  - HASH58 (FireWire GUID), HASH72 (AES), HASHAB (WASM), NONE
- SQLite database writer (Nano 5G/6G/7G)
- Media sync (`add_tracks`, metadata extraction via mutagen)
- Backup and restore (`BackupManager`)
- Virtual iPods for testing without hardware
- Public API: `connect`, `scan_ipods`, `IPod`, `Library`, `Track`, `Playlist`, `add_tracks`, `backup`, `restore`
