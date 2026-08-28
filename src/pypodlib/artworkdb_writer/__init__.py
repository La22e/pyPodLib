"""
ArtworkDB Writer for iPod Classic/Nano.

Writes ArtworkDB binary files and .ithmb image files from PC music
file embedded album art.

The image-encoding helpers (``convert_art_for_ipod``, ``image_from_bytes``,
``rgb888_to_rgb565``, ``get_artwork_formats`` and the format tables) require
the optional ``artwork`` extra (``numpy`` + ``Pillow``).  They are resolved
lazily so importing this package never fails when the extra is not installed.

Usage:
    from pypodlib.artworkdb_writer import write_artworkdb

    # pc_file_paths maps track db_track_id → PC source file path
    db_track_id_to_art = write_artworkdb(
        ipod_path="/media/ipod",
        tracks=track_list,
        pc_file_paths={12345: "/home/user/Music/song.mp3", ...},
    )
"""

# Re-export canonical format lookups from ipod_device
from pypodlib.device import ITHMB_FORMAT_MAP, ITHMB_SIZE_MAP, ithmb_formats_for_device

from .art_extractor import art_hash, extract_art, extract_art_with_folder, extract_art_with_source  # noqa: F401

__all__ = [
    'write_artworkdb',
    'ArtworkEntry',
    'extract_art',
    'extract_art_with_source',
    'extract_art_with_folder',
    'art_hash',
    'convert_art_for_ipod',
    'image_from_bytes',
    'rgb888_to_rgb565',
    'get_artwork_formats',
    'IPOD_CLASSIC_FORMATS',
    'IPOD_NANO_1G2G_FORMATS',
    'IPOD_4G_PHOTO_FORMATS',
    'IPOD_5G_FORMATS',
    'IPOD_NANO_4G_FORMATS',
    'IPOD_NANO_5G_FORMATS',
    'ALL_KNOWN_FORMATS',
    'ITHMB_FORMAT_MAP',
    'ITHMB_SIZE_MAP',
    'ithmb_formats_for_device',
]

_LAZY_IMPORTS = {
    "write_artworkdb": ("pypodlib.artworkdb_writer.artwork_writer", "write_artworkdb"),
    "ArtworkEntry": ("pypodlib.artworkdb_writer.artwork_writer", "ArtworkEntry"),
    "convert_art_for_ipod": ("pypodlib.artworkdb_writer.rgb565", "convert_art_for_ipod"),
    "image_from_bytes": ("pypodlib.artworkdb_writer.rgb565", "image_from_bytes"),
    "rgb888_to_rgb565": ("pypodlib.artworkdb_writer.rgb565", "rgb888_to_rgb565"),
    "get_artwork_formats": ("pypodlib.artworkdb_writer.rgb565", "get_artwork_formats"),
    "IPOD_CLASSIC_FORMATS": ("pypodlib.artworkdb_writer.rgb565", "IPOD_CLASSIC_FORMATS"),
    "IPOD_NANO_1G2G_FORMATS": ("pypodlib.artworkdb_writer.rgb565", "IPOD_NANO_1G2G_FORMATS"),
    "IPOD_4G_PHOTO_FORMATS": ("pypodlib.artworkdb_writer.rgb565", "IPOD_4G_PHOTO_FORMATS"),
    "IPOD_5G_FORMATS": ("pypodlib.artworkdb_writer.rgb565", "IPOD_5G_FORMATS"),
    "IPOD_NANO_4G_FORMATS": ("pypodlib.artworkdb_writer.rgb565", "IPOD_NANO_4G_FORMATS"),
    "IPOD_NANO_5G_FORMATS": ("pypodlib.artworkdb_writer.rgb565", "IPOD_NANO_5G_FORMATS"),
    "ALL_KNOWN_FORMATS": ("pypodlib.artworkdb_writer.rgb565", "ALL_KNOWN_FORMATS"),
}


def __getattr__(name: str):
    if name in _LAZY_IMPORTS:
        module_name, attr = _LAZY_IMPORTS[name]
        import importlib

        module = importlib.import_module(module_name)
        value = getattr(module, attr)
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")