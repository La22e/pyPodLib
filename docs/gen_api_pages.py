"""Generate API reference pages for mkdocstrings."""

from pathlib import Path

import mkdocs_gen_files

pages = [
    ("pypodlib/index.md", "pypodlib", "pypodlib"),
    ("pypodlib/api.md", "pypodlib.api", "pypodlib.api"),
    ("pypodlib/device.md", "pypodlib.device", "pypodlib.device"),
    ("pypodlib/itunesdb_parser.md", "iTunesDB parser", "pypodlib.itunesdb_parser"),
    ("pypodlib/itunesdb_writer.md", "iTunesDB writer", "pypodlib.itunesdb_writer"),
    ("pypodlib/itunesdb_shared.md", "iTunesDB shared", "pypodlib.itunesdb_shared"),
    ("pypodlib/artworkdb_parser.md", "ArtworkDB parser", "pypodlib.artworkdb_parser"),
    ("pypodlib/artworkdb_writer.md", "ArtworkDB writer", "pypodlib.artworkdb_writer"),
    ("pypodlib/artworkdb_shared.md", "ArtworkDB shared", "pypodlib.artworkdb_shared"),
    ("pypodlib/sqlitedb_writer.md", "SQLite writer", "pypodlib.sqlitedb_writer"),
    ("pypodlib/sync.md", "Sync", "pypodlib.sync"),
]

for path, title, identifier in pages:
    full_path = Path("reference") / path
    with mkdocs_gen_files.open(full_path, "w") as fd:
        fd.write(f"# {title}\n\n")
        fd.write(f"::: {identifier}\n")
