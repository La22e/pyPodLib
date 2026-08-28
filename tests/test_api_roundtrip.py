"""End-to-end read → edit → write → re-read round-trips on virtual iPods.

Covers every checksum family the writer must sign:
- HASH58  — iPod Classic 5.5G/6G/7G (FireWire GUID)
- HASH72  — iPod Nano 5G (AES via pycryptodome) + SQLite DBs
- HASHAB  — iPod Nano 6G/7G (WebAssembly via wasmtime) + SQLite DBs
- NONE    — pre-2007 iPods (no signature)
"""

from pathlib import Path

import pytest

import pypodlib
from pypodlib.device import ChecksumType, create_virtual_ipod


def _write_media(root: Path, name: str, data: bytes = b"id3\x03dummy-audio") -> Path:
    path = root / "iPod_Control" / "Music" / "F00" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def _make_track(folder: str, name: str, db_id: int, title: str, artist: str, **overrides) -> pypodlib.Track:
    media_path = _write_media(root=Path(folder), name=name)
    row = {
        "Title": title,
        "Artist": artist,
        "Album": "Album X",
        "Genre": "Rock",
        "year": 2005,
        "track_number": 1,
        "rating": 60,
        "length": 200_000,
        "size": media_path.stat().st_size,
        "db_track_id": db_id,
        "Location": f":iPod_Control:Music:F00:{name}",
    }
    row.update(overrides)
    return pypodlib.Track(row)


CASES = [
    ("MC297", ChecksumType.HASH58, False),
    ("MC060", ChecksumType.HASH72, True),   # Nano 5G
    ("MC027", ChecksumType.HASH72, True),
    ("MC525", ChecksumType.HASHAB, True),   # Nano 6G
    ("MKMX2", ChecksumType.HASHAB, True),   # Nano 7G
    ("MA005", ChecksumType.NONE, False),    # 4G
]


@pytest.mark.parametrize("model,checksum,uses_sqlite", CASES)
def test_library_roundtrip(tmp_path, model, checksum, uses_sqlite) -> None:
    info = create_virtual_ipod(tmp_path, model)
    assert ChecksumType(info.checksum_type) == checksum

    ipod = pypodlib.connect(str(tmp_path))
    lib = ipod.library()
    assert lib.tracks == []
    assert ipod.name == "iPod"
    assert ipod.model_number == model

    lib.add_track(_make_track(str(tmp_path), "SONG1.mp3", 101, "Song One", "Artist A"))
    lib.add_track(_make_track(str(tmp_path), "SONG2.mp3", 102, "Song Two", "Artist A", year=2006))
    pl = lib.create_playlist("Favorites")
    pl.track_ids = [101, 102]

    assert ipod.save(raise_on_error=True) is True

    lib2 = ipod.library(reload=True)
    assert len(lib2.tracks) == 2
    by_id = {t.db_track_id: t for t in lib2.tracks}
    assert set(by_id) == {101, 102}
    assert by_id[101].title == "Song One"
    assert by_id[101].artist == "Artist A"
    assert by_id[101].rating == 60
    assert by_id[101].track_number == 1
    assert by_id[102].year == 2006

    fav = lib2.get_playlist("Favorites")
    assert fav is not None
    assert fav.track_ids == [101, 102]

    if uses_sqlite:
        itlp = tmp_path / "iPod_Control" / "iTunes" / "iTunes Library.itlp"
        assert itlp.is_dir()
        assert (itlp / "Library.itdb").exists()
        assert (itlp / "Extras.itdb").exists()


@pytest.mark.parametrize("model,checksum,_uses_sqlite", CASES)
def test_edit_after_write_preserves_track_identity(tmp_path, model, checksum, _uses_sqlite) -> None:
    create_virtual_ipod(tmp_path, model)
    ipod = pypodlib.connect(str(tmp_path))
    lib = ipod.library()
    lib.add_track(_make_track(str(tmp_path), "A_1.mp3", 500, "First", "The Artist", rating=20))
    assert ipod.save(raise_on_error=True) is True

    lib = ipod.library()
    (tr := lib.tracks[0]).title = "Renamed"
    tr.rating = 100
    assert ipod.save(raise_on_error=True) is True

    lib = ipod.library(reload=True)
    (tr2 := lib.tracks[0])
    assert tr2.title == "Renamed"
    assert tr2.rating == 100
    assert tr2.db_track_id == 500  # identity preserved across rewrites


def test_media_verification_rejects_missing_files(tmp_path) -> None:
    create_virtual_ipod(tmp_path, "MC297")
    ipod = pypodlib.connect(str(tmp_path))
    lib = ipod.library()
    lib.add_track(
        pypodlib.Track(
            {
                "Title": "Orphan",
                "db_track_id": 7,
                "Location": ":iPod_Control:Music:F00:MISSING.mp3",
            }
        )
    )
    assert ipod.save(raise_on_error=False) is False  # verification catches the dangling reference


def test_add_tracks_transfers_media_and_builds_library(tmp_path) -> None:
    """add_tracks copies real media files and commits a valid DB."""
    from pathlib import Path

    create_virtual_ipod(tmp_path, "MC297")
    ipod = pypodlib.connect(str(tmp_path))

    # Build two valid MP3s with ID3 tags (header + minimal MPEG frame)
    from mutagen.id3 import ID3, TIT2, TPE1

    def _mini_mp3(path: Path, title: str, artist: str) -> None:
        tag = ID3()
        tag.add(TIT2(encoding=3, text=title))
        tag.add(TPE1(encoding=3, text=artist))
        tag.save(str(path))
        hdr = bytes.fromhex("FF FB 90 00")
        path.write_bytes(path.read_bytes() + b"".join(hdr + b"\x00" * (417 - 4) for _ in range(4)))

    src_dir = tmp_path / "sources"
    src_dir.mkdir()
    _mini_mp3(src_dir / "A.mp3", "Alpha", "Artist X")
    _mini_mp3(src_dir / "B.mp3", "Beta", "Artist Y")

    added = ipod.add_tracks([str(src_dir / "A.mp3"), str(src_dir / "B.mp3")])
    assert added == 2

    lib = ipod.library(reload=True)
    assert len(lib.tracks) == 2
    titles = {t.title for t in lib.tracks}
    assert titles == {"Alpha", "Beta"}
    assert all(t.db_track_id for t in lib.tracks)
    assert all(t.location.startswith(":iPod_Control:Music:F") for t in lib.tracks)

    media_files = list((tmp_path / "iPod_Control" / "Music").rglob("*.mp3"))
    assert len(media_files) == 2

    # Dedup within a single call (duplicate paths in one list are skipped)
    dedup_test = ipod.add_tracks([
        str(src_dir / "A.mp3"), str(src_dir / "A.mp3"),  # duplicate
    ])
    # After reload the session dedup state is reset (source_path not in iTunesDB).
    # Within the call, duplicate paths are collapsed, so at most 1 is added.
    assert dedup_test <= 1, f"expected <=1 new, got {dedup_test}"


def test_backup_and_restore_on_virtual_ipod(tmp_path) -> None:
    """backup/restore round-trip on a virtual iPod."""
    create_virtual_ipod(tmp_path, "MC297")
    ipod = pypodlib.connect(str(tmp_path))
    lib = ipod.library()

    # Add one track with a real file so the backup picks it up
    music_f00 = tmp_path / "iPod_Control" / "Music" / "F00"
    music_f00.mkdir(parents=True, exist_ok=True)
    song = music_f00 / "TRACK.mp3"
    song.write_bytes(b"fake-audio-data")
    lib.add_track(pypodlib.Track({
        "Title": "Saved",
        "db_track_id": 42,
        "Location": ":iPod_Control:Music:F00:TRACK.mp3",
        "size": song.stat().st_size,
    }))
    ipod.save(raise_on_error=True)

    backup_dir = tmp_path.parent / "backups"
    backup_dir.mkdir(exist_ok=True)
    snapshot = ipod.backup(backup_dir=str(backup_dir), reason="test")
    assert snapshot is not None
    assert snapshot.id is not None

    # Restore to the same device
    ok = ipod.restore(snapshot.id, backup_dir=str(backup_dir))
    assert ok is True

    # Re-read library — tracks should be preserved
    lib2 = ipod.library(reload=True)
    assert len(lib2.tracks) == 1
    assert lib2.tracks[0].title == "Saved"