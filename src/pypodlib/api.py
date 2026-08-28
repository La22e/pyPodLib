"""High-level public API for pypodlib.

This is the friendly entry point.  The lower-level package modules
(``pypodlib.device``, ``pypodlib.itunesdb_parser``, ``pypodlib.sync``, ...)
remain importable for power users.

Typical usage::

    import pypodlib

    ipod = pypodlib.connect("/media/user/IPOD")
    lib = ipod.library()

    lib.tracks[0].title = "New title"
    ipod.save()
"""

from __future__ import annotations

import logging
import os
import shutil
from collections.abc import Callable
from pathlib import Path
from typing import Any

from .device import (
    DeviceInfo,
    identify_ipod_at_path,
    scan_for_ipods,
    set_current_device,
)
from .device.checksum import ChecksumType

logger = logging.getLogger(__name__)

__all__ = [
    "IPod",
    "Library",
    "Playlist",
    "Track",
    "connect",
    "library_from_path",
    "scan_ipods",
]


# ────────────────────────────────────────────────────────────────────────────
# Typed track / playlist wrappers
# ────────────────────────────────────────────────────────────────────────────


class Track:
    """A typed view over one parsed track dictionary.

    Reading/writing :class:`~pypodlib.Track` attributes mutates the
    underlying parsed data, so edits appear in the next
    :meth:`IPod.save`.  The full parsed row stays available via
    :attr:`Track.data`, and ``track["Any Parsed Key"]`` also works.
    """

    __slots__ = ("_data",)

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    # ── Raw access ────────────────────────────────────────────────────

    @property
    def data(self) -> dict[str, Any]:
        """The complete parsed track dictionary."""
        return self._data

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __repr__(self) -> str:
        title = self._data.get("Title") or ""
        artist = self._data.get("Artist") or ""
        return f"<Track {title!r} by {artist!r} db_id={self.db_track_id}>"

    # ── Identity ──────────────────────────────────────────────────────

    @property
    def db_track_id(self) -> int:
        """Persistent track ID (stable across database rewrites)."""
        return int(self._data.get("db_track_id") or self._data.get("db_id") or 0)

    @db_track_id.setter
    def db_track_id(self, value: int) -> None:
        self._data["db_track_id"] = int(value or 0)
        self._data["db_id"] = int(value or 0)

    @property
    def track_id(self) -> int:
        """The parsed mhit ``track_id`` (may differ from ``db_track_id``)."""
        return int(self._data.get("track_id") or 0)

    @property
    def location(self) -> str:
        """The on-iPod colon path, e.g. ``:iPod_Control:Music:F00:AB12.mp3``."""
        return self._data.get("Location") or ""

    @location.setter
    def location(self, value: str) -> None:
        self._data["Location"] = value

    # ── Metadata strings ──────────────────────────────────────────────

    @property
    def title(self) -> str:
        return self._data.get("Title") or ""

    @title.setter
    def title(self, value: str) -> None:
        self._data["Title"] = value

    @property
    def artist(self) -> str:
        return self._data.get("Artist") or ""

    @artist.setter
    def artist(self, value: str) -> None:
        self._data["Artist"] = value

    @property
    def album(self) -> str:
        return self._data.get("Album") or ""

    @album.setter
    def album(self, value: str) -> None:
        self._data["Album"] = value

    @property
    def album_artist(self) -> str:
        return self._data.get("Album Artist") or ""

    @album_artist.setter
    def album_artist(self, value: str) -> None:
        self._data["Album Artist"] = value

    @property
    def genre(self) -> str:
        return self._data.get("Genre") or ""

    @genre.setter
    def genre(self, value: str) -> None:
        self._data["Genre"] = value

    @property
    def composer(self) -> str:
        return self._data.get("Composer") or ""

    @composer.setter
    def composer(self, value: str) -> None:
        self._data["Composer"] = value

    @property
    def comment(self) -> str:
        return self._data.get("Comment") or ""

    @comment.setter
    def comment(self, value: str) -> None:
        self._data["Comment"] = value

    @property
    def grouping(self) -> str:
        return self._data.get("Grouping") or ""

    @grouping.setter
    def grouping(self, value: str) -> None:
        self._data["Grouping"] = value

    @property
    def lyrics(self) -> str:
        return self._data.get("Lyrics") or ""

    @lyrics.setter
    def lyrics(self, value: str) -> None:
        self._data["Lyrics"] = value

    @property
    def filetype(self) -> str:
        """Parsed filetype string (e.g. ``"MPEG audio file"``)."""
        return self._data.get("filetype") or ""

    # ── Numeric metadata ──────────────────────────────────────────────

    @property
    def year(self) -> int:
        return int(self._data.get("year") or 0)

    @year.setter
    def year(self, value: int) -> None:
        self._data["year"] = int(value or 0)

    @property
    def track_number(self) -> int:
        return int(self._data.get("track_number") or 0)

    @track_number.setter
    def track_number(self, value: int) -> None:
        self._data["track_number"] = int(value or 0)

    @property
    def total_tracks(self) -> int:
        return int(self._data.get("total_tracks") or 0)

    @total_tracks.setter
    def total_tracks(self, value: int) -> None:
        self._data["total_tracks"] = int(value or 0)

    @property
    def disc_number(self) -> int:
        return int(self._data.get("disc_number") or 1)

    @disc_number.setter
    def disc_number(self, value: int) -> None:
        self._data["disc_number"] = int(value or 1)

    @property
    def total_discs(self) -> int:
        return int(self._data.get("total_discs") or 1)

    @total_discs.setter
    def total_discs(self, value: int) -> None:
        self._data["total_discs"] = int(value or 1)

    @property
    def bpm(self) -> int:
        return int(self._data.get("bpm") or 0)

    @bpm.setter
    def bpm(self, value: int) -> None:
        self._data["bpm"] = int(value or 0)

    @property
    def rating(self) -> int:
        """0-100 rating (stars × 20)."""
        return int(self._data.get("rating") or 0)

    @rating.setter
    def rating(self, value: int) -> None:
        self._data["rating"] = int(value or 0)

    @property
    def play_count(self) -> int:
        return int(self._data.get("play_count_1") or 0)

    @play_count.setter
    def play_count(self, value: int) -> None:
        self._data["play_count_1"] = int(value or 0)

    @property
    def skip_count(self) -> int:
        return int(self._data.get("skip_count") or 0)

    @skip_count.setter
    def skip_count(self, value: int) -> None:
        self._data["skip_count"] = int(value or 0)

    @property
    def volume(self) -> int:
        """Volume adjustment in the range -255..+255."""
        return int(self._data.get("volume") or 0)

    @volume.setter
    def volume(self, value: int) -> None:
        self._data["volume"] = int(value or 0)

    @property
    def length(self) -> int:
        """Duration in milliseconds."""
        return int(self._data.get("length") or 0)

    @length.setter
    def length(self, value: int) -> None:
        self._data["length"] = int(value or 0)

    @property
    def duration(self) -> float:
        """Duration in seconds."""
        return self.length / 1000.0

    @property
    def size(self) -> int:
        """File size in bytes."""
        return int(self._data.get("size") or 0)

    @size.setter
    def size(self, value: int) -> None:
        self._data["size"] = int(value or 0)

    @property
    def bitrate(self) -> int:
        return int(self._data.get("bitrate") or 0)

    @property
    def sample_rate(self) -> int:
        return int(self._data.get("sample_rate_1") or 0)


class Playlist:
    """A typed view over one parsed playlist row.

    ``track_ids`` references :attr:`Track.db_track_id` values.  Edits are
    staged on the underlying parsed row and are committed on the next
    :meth:`IPod.save`.
    """

    __slots__ = ("_data", "_library")

    def __init__(self, data: dict[str, Any], library: Library) -> None:
        self._data = data
        self._library = library

    # ── Raw access ────────────────────────────────────────────────────

    @property
    def data(self) -> dict[str, Any]:
        """The complete parsed playlist row."""
        return self._data

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def __repr__(self) -> str:
        return f"<Playlist {self.name!r} ({len(self.track_ids)} tracks)>"

    # ── Identity ──────────────────────────────────────────────────────

    @property
    def name(self) -> str:
        return self._data.get("Title") or "Untitled"

    @name.setter
    def name(self, value: str) -> None:
        self._data["Title"] = value

    @property
    def playlist_id(self) -> int | None:
        try:
            value = self._data.get("playlist_id")
            return int(value) if value else None
        except (TypeError, ValueError):
            return None

    @playlist_id.setter
    def playlist_id(self, value: int | None) -> None:
        self._data["playlist_id"] = value

    @property
    def master(self) -> bool:
        """True for the master playlist (the whole-library view)."""
        return bool(self._data.get("master_flag", 0))

    @property
    def is_podcast(self) -> bool:
        return bool(
            self._data.get("_source") == "podcast"
            or self._data.get("_mhsd_dataset_type") == 3
            or self._data.get("podcast_flag", 0)
        )

    @property
    def is_smart(self) -> bool:
        return bool(self._data.get("_mhsd_dataset_type") == 5 or self._data.get("smart_playlist_data"))

    # ── Membership ────────────────────────────────────────────────────

    @property
    def items(self) -> list[dict[str, Any]]:
        """The raw MHIP item rows (each has ``track_id``/``db_track_id``)."""
        return self._data.get("items") or []

    @property
    def track_ids(self) -> list[int]:
        """The playlist's member track IDs (:attr:`Track.db_track_id`)."""
        old_tid_to_db = self._library._track_id_to_db_id()
        ids: list[int] = []
        for item in self.items:
            tid = item.get("track_id", 0)
            db_track_id = old_tid_to_db.get(tid, 0)
            if not db_track_id:
                db_track_id = item.get("db_track_id", item.get("db_id", 0))
            if db_track_id:
                try:
                    ids.append(int(db_track_id))
                except (TypeError, ValueError):
                    continue
        return ids

    @track_ids.setter
    def track_ids(self, values: list[int]) -> None:
        self._data["items"] = [{"db_track_id": int(v)} for v in values]
        self._data["mhip_child_count"] = len(self._data["items"])

    def add(self, track: Track) -> None:
        """Append a track (referenced by ``db_track_id``) to this playlist."""
        if not isinstance(track, Track):
            track = Track(track) if isinstance(track, dict) else Track({"db_track_id": int(track)})
        db_id = track.db_track_id
        if db_id and db_id not in self.track_ids:
            self.track_ids = [*self.track_ids, db_id]

    def remove(self, track: Track) -> None:
        """Remove a track (referenced by ``db_track_id``) from this playlist."""
        if not isinstance(track, Track):
            track = Track({} if isinstance(track, dict) else {"db_track_id": int(track)})
        db_id = track.db_track_id
        if db_id:
            self.track_ids = [i for i in self.track_ids if i != db_id]


class Library:
    """The parsed library of one iPod.

    Holds the raw parsed tracks/playlists plus typed :class:`Track` and
    :class:`Playlist` views.  Mutating the views updates the same underlying
    data that :meth:`IPod.save` writes back.
    """

    def __init__(
        self,
        path: str | os.PathLike[str],
        *,
        tracks: list[dict[str, Any]],
        dataset2_standard_playlists: list[dict[str, Any]] | None = None,
        dataset3_podcast_playlists: list[dict[str, Any]] | None = None,
        dataset5_smart_playlists: list[dict[str, Any]] | None = None,
        device_time_context: Any = None,
        playcounts_timezone_changed: bool = False,
    ) -> None:
        self.path = os.fspath(path)
        self._tracks_data: list[dict[str, Any]] = tracks
        self._ds2 = dataset2_standard_playlists or []
        self._ds3 = dataset3_podcast_playlists or []
        self._ds5 = dataset5_smart_playlists or []
        self._device_time_context = device_time_context
        self.playcounts_timezone_changed = playcounts_timezone_changed

    # ── Typed views ───────────────────────────────────────────────────

    @property
    def tracks(self) -> list[Track]:
        """All library tracks."""
        return [Track(d) for d in self._tracks_data]

    def track(self, db_track_id: int) -> Track | None:
        """Find a track by its persistent ``db_track_id``."""
        for d in self._tracks_data:
            if int(d.get("db_track_id") or d.get("db_id") or 0) == int(db_track_id):
                return Track(d)
        return None

    @property
    def playlists(self) -> list[Playlist]:
        """User playlists (dataset 2), including the master playlist."""
        return [Playlist(d, self) for d in self._ds2]

    @property
    def podcast_playlists(self) -> list[Playlist]:
        """Podcast playlists (dataset 3)."""
        return [Playlist(d, self) for d in self._ds3]

    @property
    def smart_playlists(self) -> list[Playlist]:
        """Smart playlists and browsing categories (dataset 5)."""
        return [Playlist(d, self) for d in self._ds5]

    @property
    def all_playlists(self) -> list[Playlist]:
        return [
            *self.playlists,
            *self.podcast_playlists,
            *self.smart_playlists,
        ]

    @property
    def master_playlist(self) -> Playlist | None:
        for pl in self.all_playlists:
            if pl.master:
                return pl
        return None

    # ── Mutation helpers ──────────────────────────────────────────────

    def add_track(self, track: Track | dict[str, Any]) -> Track:
        """Append a track row to the library."""
        if isinstance(track, Track):
            data = track.data
        elif isinstance(track, dict):
            data = track
        else:
            raise TypeError("add_track expects a Track or a parsed track dict")
        self._tracks_data.append(data)
        return Track(data)

    def remove_track(self, track: Track) -> None:
        """Remove a track row from the library (not from the device's disk)."""
        if not isinstance(track, Track):
            track = Track(track) if isinstance(track, dict) else Track({"db_track_id": int(track)})
        db_id = track.db_track_id
        self._tracks_data[:] = [
            d for d in self._tracks_data
            if int(d.get("db_track_id") or d.get("db_id") or 0) != db_id
        ]
        for pl in self.all_playlists:
            if not pl.master:
                pl.track_ids = [i for i in pl.track_ids if i != db_id]

    def create_playlist(self, name: str) -> Playlist:
        """Create a new user playlist and append it to the library."""
        row: dict[str, Any] = {
            "Title": name,
            "playlist_id": None,
            "master_flag": 0,
            "sort_order": 1,
            "items": [],
            "_source": "regular",
            "_mhsd_dataset_type": 2,
            "_mhsd_result_key": "mhlp",
        }
        self._ds2.append(row)
        return Playlist(row, self)

    def get_playlist(self, name: str) -> Playlist | None:
        """Find a playlist by name (first match wins)."""
        for pl in self.all_playlists:
            if pl.name == name:
                return pl
        return None

    # ── Internal ──────────────────────────────────────────────────────

    def _track_id_to_db_id(self) -> dict[int, int]:
        mapping: dict[int, int] = {}
        for d in self._tracks_data:
            tid = int(d.get("track_id") or 0)
            db_id = int(d.get("db_track_id") or d.get("db_id") or 0)
            if tid and db_id:
                mapping[tid] = db_id
        return mapping

    def __repr__(self) -> str:
        return (
            f"<Library {len(self._tracks_data)} tracks, "
            f"{len(self._ds2)} playlists, {len(self._ds3)} podcast playlists, "
            f"{len(self._ds5)} smart playlists>"
        )


# ────────────────────────────────────────────────────────────────────────────
# Device wrapper
# ────────────────────────────────────────────────────────────────────────────


class IPod:
    """A detected or connected iPod.

    You normally obtain one via :func:`connect` or :func:`scan_ipods`.
    """

    def __init__(self, info: DeviceInfo) -> None:
        if not info.path:
            raise ValueError("Device has no mount path")
        self._info = info
        self._library: Library | None = None
        self._library_error: Exception | None = None
        set_current_device(info)

    # ── Identity / capability accessors ───────────────────────────────

    @property
    def info(self) -> DeviceInfo:
        return self._info

    @property
    def path(self) -> str:
        return self._info.path

    @property
    def model_number(self) -> str:
        return self._info.model_number

    @property
    def model_family(self) -> str:
        return self._info.model_family

    @property
    def generation(self) -> str:
        return self._info.generation

    @property
    def capacity(self) -> str:
        return self._info.capacity

    @property
    def color(self) -> str:
        return self._info.color

    @property
    def serial(self) -> str:
        return self._info.serial

    @property
    def firewire_guid(self) -> str:
        return self._info.firewire_guid

    @property
    def checksum_type(self) -> ChecksumType:
        return ChecksumType(self._info.checksum_type)

    @property
    def name(self) -> str:
        """The user-assigned iPod name (from the master playlist title)."""
        return self._info.ipod_name or (self._library.master_playlist.name if self._library else "") or self._info.mount_name

    @property
    def capabilities(self) -> Any:
        return self._info.capabilities

    @property
    def volume_identity_key(self) -> str:
        return self._info.volume_identity_key

    @property
    def connected_bus(self) -> str:
        return self._info.connected_bus

    @property
    def display_name(self) -> str:
        return self._info.display_name

    def __repr__(self) -> str:
        return f"<IPod {self.model_family} {self.generation} ({self.capacity}) at {self.path!r}>"

    # ── Reading ───────────────────────────────────────────────────────

    def library(self, *, include_playcounts: bool = True, reload: bool = False) -> Library:
        """Parse and return the iPod library.

        The result is cached; pass ``reload=True`` to force a fresh parse.
        """
        if self._is_library_available() and not reload:
            return self._library  # type: ignore[return-value]
        from .sync._db_io import read_existing_database

        try:
            data = read_existing_database(
                Path(self.path),
                include_playcounts=include_playcounts,
                raise_on_error=True,
            )
        except Exception as exc:  # pragma: no cover - surfaced to callers
            self._library = None
            self._library_error = exc
            raise
        self._library = Library(
            self.path,
            tracks=data.get("tracks") or [],
            dataset2_standard_playlists=data.get("dataset2_standard_playlists"),
            dataset3_podcast_playlists=data.get("dataset3_podcast_playlists"),
            dataset5_smart_playlists=data.get("dataset5_smart_playlists"),
            device_time_context=data.get("device_time_context"),
            playcounts_timezone_changed=bool(data.get("playcounts_timezone_changed")),
        )
        # The master playlist title is the canonical device name.
        master = self._library.master_playlist
        if master is not None:
            self._info.ipod_name = master.name
        return self._library

    def _is_library_available(self) -> bool:
        return self._library is not None

    # ── Writing ───────────────────────────────────────────────────────

    def save(self, *, raise_on_error: bool = True) -> bool:
        """Write the current library state back to the iPod.

        The database is fully re-serialized with the correct per-device
        checksum signature; SQLite databases (Nano 6G/7G) and iTunesPrefs
        are updated as well.  Returns ``True`` on success.
        """
        lib = self.library() if not self._is_library_available() else self._library
        assert lib is not None

        from .sync._playlist_builder import build_and_evaluate_playlists
        from .sync._track_conversion import track_dict_to_info
        from .sync.database_commit import DatabaseCommitPayload, write_database_commit

        all_tracks = [track_dict_to_info(t.data) for t in lib.tracks]
        (
            master_name,
            master_id,
            playlists,
            podcast_master_name,
            podcast_master_id,
            podcast_playlists,
            smart_playlists,
        ) = build_and_evaluate_playlists(
            lib._tracks_data,
            lib._ds2,
            lib._ds3,
            lib._ds5,
            all_tracks,
            time_context=lib._device_time_context,
        )

        payload = DatabaseCommitPayload(
            all_tracks=all_tracks,
            playlists=playlists,
            podcast_playlists=podcast_playlists,
            smart_playlists=smart_playlists,
            master_playlist_name=master_name,
            master_playlist_id=master_id,
            podcast_master_playlist_name=podcast_master_name,
            podcast_master_playlist_id=podcast_master_id,
        )
        ok = write_database_commit(
            self.path,
            payload,
            protect_itunes=True,
            raise_on_error=raise_on_error,
        )
        if ok:
            self._library = None  # force a fresh read next time
        return bool(ok)

# ── Sync ──────────────────────────────────────────────────────────

    def add_tracks(
        self,
        paths: list[str | os.PathLike[str]],
        *,
        progress_callback: Callable[[int, int, str], None] | None = None,
        raise_on_error: bool = False,
    ) -> int:
        """Copy local media files onto the iPod and commit a new library.

        Each file is placed in ``iPod_Control/Music`` (metadata read via
        mutagen when available), added to the library, and the iTunesDB is
        regenerated with the correct device signature.  Returns the number
        of files added.

        ``progress_callback(current, total, message)`` is invoked between
        copies; ``progress_callback(count, total, "Committing database...")``
        marks the final write.
        """
        from .sync._track_conversion import ipod_filetype_for_extension, pc_track_to_info
        from .sync.pc_library import PCLibrary

        lib = self.library()
        music_root = Path(self.path) / "iPod_Control" / "Music"
        music_root.mkdir(parents=True, exist_ok=True)

        seen_sources = {
            str(t.get("source_path") or t.get("Source Path") or "")
            for t in lib._tracks_data
        }

        resolved = [os.path.abspath(os.path.expanduser(os.fspath(p))) for p in paths]
        to_add = sorted(set(p for p in resolved if p not in seen_sources))

        # ── copy media ────────────────────────────────────────────────
        import secrets

        copies: list[tuple[str, Path, object, str]] = []
        total = len(to_add)
        for index, src in enumerate(to_add):
            if progress_callback is not None:
                progress_callback(index, total, f"Reading {os.path.basename(src)}")
            src_path = Path(src)
            if not src_path.is_file():
                if raise_on_error:
                    raise FileNotFoundError(src)
                continue
            try:
                library = PCLibrary([src_path.parent])
                pc_track = library._read_track(src_path)
            except Exception as exc:
                if raise_on_error:
                    raise
                logger.warning("Could not read metadata for %s: %s", src, exc)
                continue
            if pc_track is None:
                continue
            folder = _next_free_folder(music_root)
            on_device = folder / f"{secrets.token_hex(8).upper()}{src_path.suffix}"
            dst = shutil.copy2(src, on_device)
            copies.append((src, Path(dst), pc_track, ipod_filetype_for_extension(src_path.suffix)))

        # ── stage new library rows ────────────────────────────────────
        for src, dst_path, pc_track, filetype in copies:
            rel = dst_path.relative_to(Path(self.path))
            ipod_location = ":" + ":".join(rel.parts)
            info = pc_track_to_info(pc_track, ipod_location, was_transcoded=False, ipod_file_path=dst_path)
            from .sync._track_conversion import trackinfo_to_eval_dict

            row = trackinfo_to_eval_dict(info)
            row["Location"] = ipod_location
            row["source_path"] = src
            row["db_track_id"] = 0
            row["filetype"] = filetype
            lib.add_track(Track(row))

        if not copies:
            return 0
        if progress_callback is not None:
            progress_callback(len(copies), total, "Committing database...")
        if not self.save(raise_on_error=raise_on_error):
            raise RuntimeError("Database commit failed after staging new tracks")
        return len(copies)

    # ── Backup / restore ──────────────────────────────────────────────

    def backup(
        self,
        backup_dir: str | os.PathLike[str] = "",
        *,
        reason: str = "manual",
    ) -> Any:
        """Create a full snapshot backup of the iPod.

        Returns a :class:`pypodlib.sync.backup_manager.SnapshotInfo` on
        success, or ``None``.
        """
        from .sync.backup_manager import BackupManager

        manager = BackupManager(
            device_id=self.serial or self.path,
            backup_dir=os.fspath(backup_dir) if backup_dir else "",
            device_name=self.name or self.display_name,
            identity_is_stable=True,
        )
        return manager.create_backup(
            self.path,
            reported_volume_format=self._info.reported_volume_format,
            expected_volume_identity_key=self.volume_identity_key,
            reason=reason,
        )

    def restore(
        self,
        snapshot_id: str,
        *,
        backup_dir: str | os.PathLike[str] = "",
    ) -> bool:
        """Restore a prior snapshot backup to the iPod."""
        from .sync.backup_manager import BackupManager

        manager = BackupManager(
            device_id=self.serial or self.path,
            backup_dir=os.fspath(backup_dir) if backup_dir else "",
            device_name=self.name or self.display_name,
            identity_is_stable=True,
        )
        return manager.restore_backup(
            snapshot_id,
            self.path,
            reported_volume_format=self._info.reported_volume_format,
            expected_volume_identity_key=self.volume_identity_key,
        )


# ────────────────────────────────────────────────────────────────────────────
# Module-level helpers
# ────────────────────────────────────────────────────────────────────────────


def _next_free_folder(music_root: Path) -> Path:
    """Return the next iPod ``Music/Fxx`` folder with room for a file.

    Real devices lay media out in ``iPod_Control/Music/F00`` .. ``FFF``,
    each holding up to ~1000 files.
    """
    for index in range(256):
        folder = music_root / f"F{index:02X}"
        folder.mkdir(exist_ok=True)
        if sum(1 for _ in folder.iterdir()) < 1000:
            return folder
    raise RuntimeError("iPod media store is full (no F00-F255 folder with space)")


def scan_ipods() -> list[IPod]:
    """Scan for connected iPods and return them (empty list if none)."""
    found = scan_for_ipods()
    return [IPod(info) for info in found]


def connect(path: str | os.PathLike[str]) -> IPod:
    """Identify the iPod mounted at *path* and return an :class:`IPod`.

    Raises :class:`ValueError` when no iPod can be identified there.
    """
    resolved = os.path.abspath(os.path.expanduser(os.fspath(path)))
    info = identify_ipod_at_path(resolved)
    if info is None:
        raise ValueError(f"No iPod identified at {resolved!r}")
    return IPod(info)


def library_from_path(path: str | os.PathLike[str]) -> Library:
    """Parse just the library at *path* without touching any device store.

    Useful for inspecting a backup or an offline copy of an iPod.
    """
    resolved = os.path.abspath(os.path.expanduser(os.fspath(path)))
    from .sync._db_io import read_existing_database

    data = read_existing_database(Path(resolved), raise_on_error=True)
    return Library(
        resolved,
        tracks=data.get("tracks") or [],
        dataset2_standard_playlists=data.get("dataset2_standard_playlists"),
        dataset3_podcast_playlists=data.get("dataset3_podcast_playlists"),
        dataset5_smart_playlists=data.get("dataset5_smart_playlists"),
        device_time_context=data.get("device_time_context"),
        playcounts_timezone_changed=bool(data.get("playcounts_timezone_changed")),
    )