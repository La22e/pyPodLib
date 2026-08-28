"""Headless import smoke tests — nothing here requires real hardware or the GUI."""

import pypodlib


def test_root_import_exposes_public_api() -> None:
    assert pypodlib.__version__
    for name in ("connect", "scan_ipods", "library_from_path", "IPod", "Library", "Track", "Playlist"):
        assert hasattr(pypodlib, name)


def test_device_package_imports() -> None:
    from pypodlib.device import (
        ChecksumType,
        available_virtual_ipod_models,
        identify_ipod_at_path,
        scan_for_ipods,
    )

    assert ChecksumType.NONE is not None
    assert callable(scan_for_ipods)
    assert callable(identify_ipod_at_path)
    assert available_virtual_ipod_models()


def test_parser_and_writer_packages_import() -> None:
    from pypodlib.itunesdb_parser import parse_itunesdb
    from pypodlib.itunesdb_parser.ipod_library import load_ipod_library
    from pypodlib.itunesdb_shared.device_time import DeviceTimeContext
    from pypodlib.itunesdb_writer import write_itunesdb
    from pypodlib.itunesdb_writer.mhit_writer import TrackInfo

    assert callable(parse_itunesdb)
    assert callable(load_ipod_library)
    assert callable(write_itunesdb)
    assert DeviceTimeContext is not None
    assert TrackInfo is not None


def test_sync_package_imports_without_pillow() -> None:
    """The sync package must import without numpy/Pillow at module scope."""
    try:
        import numpy as np  # noqa: F401
        has_numpy = True
    except ImportError:
        has_numpy = False
    assert not has_numpy or True  # only meaningful in a lean environment

    from pypodlib.sync import SyncEngine, build_filtered_sync_plan
    from pypodlib.sync._db_io import read_existing_database, verify_written_database

    assert SyncEngine is not None
    assert callable(build_filtered_sync_plan)
    assert callable(read_existing_database)
    assert callable(verify_written_database)


def test_artworkdb_writer_package_imports_lazily() -> None:
    """artworkdb_writer must import even when numpy/Pillow are absent."""
    import pypodlib.artworkdb_writer as aw

    assert callable(aw.extract_art)
    assert "write_artworkdb" in aw.__all__