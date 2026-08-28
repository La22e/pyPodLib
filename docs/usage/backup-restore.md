# Backup and restore

pyPodLib can back up the full contents of an iPod (database + media files) to a directory on your computer and restore from a backup.

## Creating a backup

```python
snapshot = ipod.backup(
    backup_dir="/path/to/backups",
    reason="monthly backup",
)
print(snapshot.id)                   # e.g. "20260828_151400"
print(snapshot.file_count)           # number of files backed up
print(snapshot.total_size)           # bytes
```

## Restoring from a backup

```python
ok = ipod.restore(
    snapshot.id,
    backup_dir="/path/to/backups",
)
print("Restore succeeded" if ok else "Restore failed")
```

## Safety

- The backup location **must not** be inside the iPod's mount path (to prevent data loss if the iPod is disconnected mid-backup).
- The restore process copies files back to the device and regenerates the database.
- Metadata (timestamps, permissions) is preserved where possible.

## Listing snapshots

```python
snapshots = ipod.list_backups("/path/to/backups")
for s in snapshots:
    print(s.id, s.display_date, s.reason, s.file_count, s.total_size)
```
